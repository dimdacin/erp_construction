# crud_depenses.py

from sqlalchemy.orm import Session
from decimal import Decimal
import pandas as pd
from models import Equipement, DepenseEquipement, Fournisseur 
from crud_refs import get_or_create_fournisseur

# --- Assurez-vous que les imports sont corrects ---

def import_depenses_from_excel(db: Session, file_path: str):
    """
    Lit le fichier Excel des dépenses/interventions équipements et les importe dans DepenseEquipement.
    Colonnes attendues : Immatriculation, Categorie, Modele, Date, Fournisseur_Nom, 
    Categ_intervention, description_intervention, montant
    """
    try:
        df = pd.read_excel(file_path, na_values=[' -  ', '?', 'nan', ''])
    except Exception as e:
        return f"Erreur de lecture du fichier Excel : {e}"

    compteur_creations = 0
    df = df.where(pd.notna(df), None)
    
    # Afficher les colonnes disponibles pour débogage
    print(f"Colonnes disponibles dans le fichier Excel : {list(df.columns)}")
    
    # --- Renommage des colonnes pour le mapping (utiliser les noms Python) ---
    df.rename(columns={
        'Immatriculation': 'immatriculation_excel',
        'Categorie': 'categorie_excel',
        'Modele': 'modele_excel',
        'Data': 'date_depense',  # Attention : 'Data' et pas 'Date'
        'Fournisseur_nom': 'fournisseur_nom',  # Déjà correct, pas de changement nécessaire
        'Categ_intervention': 'type_depense',
        'description_intervention': 'description_reparation',
        'montant': 'montant_ht'
    }, inplace=True)
    
    print(f"Colonnes après renommage : {list(df.columns)}")
    
    # --- Boucle d'Importation ---
    for index, row in df.iterrows():
        # 1. Vérifications et Conversion - utiliser .get() pour éviter les KeyError
        immat = row.get('immatriculation_excel')
        montant = row.get('montant_ht')
        
        if immat is None or montant is None:
            continue

        # 2. Trouver l'Equipement ID par Immatriculation
        equipement = db.query(Equipement).filter(
            Equipement.immatriculation == immat
        ).first()

        if not equipement:
            print(f"Skipping: Engin (Immat={immat}) non trouvé dans le référentiel.")
            continue
        
        # 3. Création du Fournisseur
        fournisseur_id = None
        fournisseur_nom = row.get('fournisseur_nom')
        if fournisseur_nom:
            fournisseur = get_or_create_fournisseur(db, str(fournisseur_nom))
            fournisseur_id = fournisseur.id
        
        # 4. Création de la Dépense
        try:
            montant_ht = Decimal(str(montant))
            date_dep = row.get('date_depense')
            date_depense = date_dep.date() if isinstance(date_dep, pd.Timestamp) else date_dep
        except Exception as e:
            print(f"Skipping: Erreur de conversion du montant/date pour {immat}: {e}")
            continue

        db_depense = DepenseEquipement(
            equipement_id=equipement.id,
            fournisseur_id=fournisseur_id,
            date_depense=date_depense, 
            type_depense=str(row.get('type_depense')) if row.get('type_depense') else "INCONNU",
            montant_ht=montant_ht,
            description=row.get('description_reparation')
        )
        
        db.add(db_depense)
        compteur_creations += 1
            
    db.commit()
    return f"Importation des dépenses terminée. {compteur_creations} enregistrements créés."