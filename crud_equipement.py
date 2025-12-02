# crud_equipement.py
from sqlalchemy.orm import Session
from decimal import Decimal
import pandas as pd
from typing import List, Dict, Any, Optional

# IMPORTS : Utilisation du module crud_refs et models
from models import Equipement, EquipementCategorie, Site
from crud_refs import get_or_create_categorie, get_or_create_site 
# Assurez-vous que get_or_create_categorie et get_or_create_site sont importés

# ============================================================
# FONCTIONS CRUD DE BASE POUR LES ÉQUIPEMENTS
# ============================================================

def get_equipement(db: Session, equipement_id: int) -> Optional[Equipement]:
    """Récupère un équipement par son ID."""
    return db.query(Equipement).filter(Equipement.id == equipement_id).first()

def get_equipement_by_code(db: Session, code: str) -> Optional[Equipement]:
    """Récupère un équipement par son code."""
    return db.query(Equipement).filter(Equipement.code == code).first()

def get_equipements(db: Session, skip: int = 0, limit: int = 100, actif: Optional[bool] = True) -> List[Equipement]:
    """Récupère une liste d'équipements avec pagination."""
    query = db.query(Equipement)
    if actif is not None:
        query = query.filter(Equipement.actif == actif)
    return query.offset(skip).limit(limit).all()

def create_equipement(db: Session, equipement_data: dict) -> Equipement:
    """Crée un nouvel équipement."""
    db_equipement = Equipement(**equipement_data)
    db.add(db_equipement)
    db.commit()
    db.refresh(db_equipement)
    return db_equipement

def update_equipement(db: Session, equipement_id: int, equipement_data: dict) -> Optional[Equipement]:
    """Met à jour un équipement existant."""
    db_equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not db_equipement:
        return None
    
    for key, value in equipement_data.items():
        if value is not None:
            setattr(db_equipement, key, value)
    
    db.commit()
    db.refresh(db_equipement)
    return db_equipement

def delete_equipement(db: Session, equipement_id: int) -> bool:
    """Supprime (désactive) un équipement."""
    db_equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not db_equipement:
        return False
    
    # Soft delete : on désactive plutôt que de supprimer
    db_equipement.actif = False
    db.commit()
    return True

# ============================================================
# FONCTION D'IMPORTATION DEPUIS EXCEL
# ============================================================

def import_equipements_from_excel(db: Session, file_path: str):
    """
    Lit le fichier Excel et insère/met à jour les équipements (référentiel d'actifs).
    Colonnes attendues : EquipID, Categorie, Modele, Immatriculation, Annee, Statut, 
    UsageSource, UniteCompteur, TypeCarburant, Conso_100km_L, Conso_h_L, CoutCarb_h_lei, 
    CoutCarb_100km_lei, Entretien_Annuel_lei, Km_Travail_Ann, Entretien_100km_lei, 
    Heures_Travail_Ann, Entretien_h_lei, Valeur_Comptable_lei, Duree_vie_ans, 
    Valeur_Residuelle_lei, Base_Amortissable_lei, Taux_Amort_Ann, Amort_Total_lei, 
    Amort_h_lei, Cout_Usage_1h_lei, Cout_Usage_100km_lei, TauxHoraireOperateur_lei
    """
    try:
        df = pd.read_excel(file_path, na_values=[' -  ', '?', 'nan', ''])
    except Exception as e:
        return f"Erreur de lecture du fichier Excel : {e}"

    compteur_creations = 0
    compteur_mises_a_jour = 0
    df = df.where(pd.notna(df), None)
    
    for index, row in df.iterrows():
        # --- LOGIQUE DE CRÉATION DE CATÉGORIE ET DE SITE DE RATTACHEMENT (RÉFÉRENTIELS) ---
        categorie_id = None
        if row.get('Categorie'):
            categorie = get_or_create_categorie(db, row['Categorie'], row['Categorie']) 
            categorie_id = categorie.id

        # Création du site de rattachement initial si non trouvé
        site_rattachement = get_or_create_site(db, 
                                               'DEPOT-CENTRAL', 
                                               'Dépôt Central Non Spécifié', 
                                               'DEPOT', 
                                               'ADMIN') 
        site_rattachement_id = site_rattachement.id

        # --- CRÉATION OU MISE À JOUR DE L'ÉQUIPEMENT ---
        equip_code = row.get('EquipID')
        immatriculation = row.get('Immatriculation')
        
        # Si pas d'EquipID, on utilise l'immatriculation comme clé
        if not equip_code and not immatriculation:
            continue
        
        # On cherche l'équipement soit par code, soit par immatriculation
        if equip_code:
            equipement = db.query(Equipement).filter(Equipement.code == equip_code).first()
        else:
            # Si pas d'EquipID, on cherche par immatriculation
            equipement = db.query(Equipement).filter(Equipement.immatriculation == immatriculation).first()
            # On génère un code basé sur l'immatriculation
            equip_code = immatriculation

        # Fonction utilitaire pour gérer les Decimal
        def get_decimal(col_name):
            val = row.get(col_name)
            try:
                # IMPORTANT : Convertir en string avant Decimal pour éviter les erreurs de type NaN
                return Decimal(str(val)) if val is not None and str(val).lower() != 'nan' else Decimal(0)
            except:
                return Decimal(0)
        
        # Extraction des valeurs depuis les nouvelles colonnes
        cout_usage_1h = get_decimal('Cout_Usage_1h_lei')
        cout_usage_100km = get_decimal('Cout_Usage_100km_lei')
        conso_h_l = get_decimal('Conso_h_L')
        
        if not equipement:
            equipement = Equipement(
                code=equip_code,
                immatriculation=immatriculation,
                categorie_id=categorie_id,
                site_rattachement_id=site_rattachement_id,
                unite_compteur=row.get('UniteCompteur') if row.get('UniteCompteur') else 'H',
                usage_source=row.get('UsageSource') if row.get('UsageSource') else 'MANUEL',
                conso_h_l=conso_h_l,
                cout_usage_1h_lei=cout_usage_1h,
                cout_usage_100km_lei=cout_usage_100km,
                actif=(row.get('Statut') != 'INACTIF') if row.get('Statut') else True
            )
            db.add(equipement)
            compteur_creations += 1
        else:
            # Mise à jour des valeurs
            if immatriculation:
                equipement.immatriculation = immatriculation
            if categorie_id:
                equipement.categorie_id = categorie_id
            if row.get('UniteCompteur'):
                equipement.unite_compteur = row.get('UniteCompteur')
            if row.get('UsageSource'):
                equipement.usage_source = row.get('UsageSource')
            
            equipement.conso_h_l = conso_h_l
            equipement.cout_usage_1h_lei = cout_usage_1h
            equipement.cout_usage_100km_lei = cout_usage_100km
            
            if row.get('Statut'):
                equipement.actif = (row.get('Statut') != 'INACTIF')
            
            compteur_mises_a_jour += 1
            
    db.commit()
    return f"Importation des équipements terminée. {compteur_creations} créations, {compteur_mises_a_jour} mises à jour."