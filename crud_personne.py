# crud_personne.py
from sqlalchemy.orm import Session
from decimal import Decimal
import pandas as pd
from typing import List, Optional

from models import Personne, Division, Service, Fonction
from crud_refs import get_or_create_division, get_or_create_service, get_or_create_fonction

# ============================================================
# FONCTIONS CRUD DE BASE POUR LES PERSONNES
# ============================================================

def get_personne(db: Session, personne_id: int) -> Optional[Personne]:
    """Récupère une personne par son ID."""
    return db.query(Personne).filter(Personne.id == personne_id).first()

def get_personne_by_matricule(db: Session, matricule: str) -> Optional[Personne]:
    """Récupère une personne par son matricule."""
    return db.query(Personne).filter(Personne.matricule == matricule).first()

def get_personnes(db: Session, skip: int = 0, limit: int = 100, actif: Optional[bool] = True) -> List[Personne]:
    """Récupère une liste de personnes avec pagination."""
    query = db.query(Personne)
    if actif is not None:
        query = query.filter(Personne.actif == actif)
    return query.offset(skip).limit(limit).all()

def create_personne(db: Session, personne_data: dict) -> Personne:
    """Crée une nouvelle personne."""
    db_personne = Personne(**personne_data)
    db.add(db_personne)
    db.commit()
    db.refresh(db_personne)
    return db_personne

def update_personne(db: Session, personne_id: int, personne_data: dict) -> Optional[Personne]:
    """Met à jour une personne existante."""
    db_personne = db.query(Personne).filter(Personne.id == personne_id).first()
    if not db_personne:
        return None
    
    for key, value in personne_data.items():
        if value is not None:
            setattr(db_personne, key, value)
    
    db.commit()
    db.refresh(db_personne)
    return db_personne

def delete_personne(db: Session, personne_id: int) -> bool:
    """Supprime (désactive) une personne."""
    db_personne = db.query(Personne).filter(Personne.id == personne_id).first()
    if not db_personne:
        return False
    
    # Soft delete : on désactive plutôt que de supprimer
    db_personne.actif = False
    db.commit()
    return True

# ============================================================
# FONCTION D'IMPORTATION DEPUIS EXCEL
# ============================================================

def import_personnes_from_excel(db: Session, file_path: str):
    """
    Lit le fichier Excel du personnel RH et importe les personnes dans la base de données.
    Colonnes attendues : Sector, Diviziune, Serviciu, Fuctia, Codul functiei, 
    Nr. de tabel, Numele, prenumele, Salariu tarifar schema, Acord sup, Selection, Commentaire
    """
    try:
        df = pd.read_excel(file_path, na_values=[' -  ', '?', 'nan', ''])
    except Exception as e:
        return f"Erreur de lecture du fichier Excel : {e}"

    compteur_creations = 0
    compteur_mises_a_jour = 0
    compteur_erreurs = 0
    df = df.where(pd.notna(df), None)
    
    # Afficher les colonnes disponibles pour débogage
    print(f"Colonnes disponibles dans le fichier Excel : {list(df.columns)}")
    
    for index, row in df.iterrows():
        try:
            # --- RÉCUPÉRATION DES DONNÉES DE BASE ---
            matricule = str(row.get('Nr. de tabel', '')).strip() if row.get('Nr. de tabel') else None
            nom_prenom = str(row.get('Numele, prenumele', '')).strip() if row.get('Numele, prenumele') else None
            secteur = str(row.get('Sector', '')).strip() if row.get('Sector') else None
            
            # Vérification des champs obligatoires
            if not nom_prenom:
                print(f"Ligne {index + 2} ignorée : nom/prénom manquant")
                compteur_erreurs += 1
                continue
            
            # Si pas de matricule, on génère un code temporaire
            if not matricule or matricule == 'nan':
                matricule = f"TEMP_{index + 1}"
            
            # --- GESTION DES RÉFÉRENTIELS RH ---
            division_id = None
            if row.get('Diviziune'):
                division = get_or_create_division(db, str(row['Diviziune']).strip())
                division_id = division.id
            
            service_id = None
            if row.get('Serviciu'):
                service = get_or_create_service(db, str(row['Serviciu']).strip(), division_id)
                service_id = service.id
            
            fonction_id = None
            if row.get('Fuctia'):  # Note: "Fuctia" semble être une faute de frappe dans votre fichier
                fonction_nom = str(row['Fuctia']).strip()
                fonction_code = str(row.get('Codul functiei', '')).strip() if row.get('Codul functiei') else None
                fonction = get_or_create_fonction(db, fonction_nom, fonction_code)
                fonction_id = fonction.id
            
            # --- GESTION DES DONNÉES SALARIALES ---
            def get_decimal(col_name):
                val = row.get(col_name)
                try:
                    return Decimal(str(val)) if val is not None and str(val).lower() not in ['nan', ''] else Decimal(0)
                except:
                    return Decimal(0)
            
            salaire_tarif = get_decimal('Salariu tarifar schema')
            accord_sup = get_decimal('Acord sup')
            
            # Calcul du taux horaire (si vous avez une formule spécifique, ajustez ici)
            # Exemple : on peut estimer le taux horaire en divisant le salaire mensuel par 168h (standard)
            taux_horaire_cout = (salaire_tarif + accord_sup) / Decimal(168) if (salaire_tarif + accord_sup) > 0 else Decimal(0)
            
            # --- CRÉATION OU MISE À JOUR DE LA PERSONNE ---
            personne = db.query(Personne).filter(Personne.matricule == matricule).first()
            
            if not personne:
                # Création d'une nouvelle personne
                personne = Personne(
                    matricule=matricule,
                    nom_prenom=nom_prenom,
                    secteur=secteur,
                    division_id=division_id,
                    service_id=service_id,
                    fonction_id=fonction_id,
                    salaire_tarif=salaire_tarif,
                    accord_supplementaire=accord_sup,
                    taux_horaire_cout=taux_horaire_cout,
                    actif=True
                )
                db.add(personne)
                compteur_creations += 1
            else:
                # Mise à jour d'une personne existante
                personne.nom_prenom = nom_prenom
                personne.secteur = secteur
                personne.division_id = division_id
                personne.service_id = service_id
                personne.fonction_id = fonction_id
                personne.salaire_tarif = salaire_tarif
                personne.accord_supplementaire = accord_sup
                personne.taux_horaire_cout = taux_horaire_cout
                compteur_mises_a_jour += 1
                
        except Exception as e:
            print(f"Erreur ligne {index + 2} : {e}")
            compteur_erreurs += 1
            continue
    
    db.commit()
    return f"Importation du personnel terminée. {compteur_creations} créations, {compteur_mises_a_jour} mises à jour, {compteur_erreurs} erreurs."

