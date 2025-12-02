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
        df = pd.read_excel(file_path, na_values=[' -  ', '?', 'nan'])
    except Exception as e:
        return f"Erreur de lecture du fichier Excel : {e}"

    compteur_creations = 0
    df = df.where(pd.notna(df), None)
    
    # --- Renommage des colonnes pour le mapping (utiliser les noms Python) ---
    df.rename(columns={
        'Immatriculation': 'immatriculation_excel',
        'Categorie': 'categorie_excel',
        'Modele': 'modele_excel',
        'Date': 'date_depense',
        'Fournisseur_Nom': 'fournisseur_nom',
        'Categ_intervention': 'type_depense',
        'description_intervention': 'description_reparation',
        'montant': 'montant_ht'
    }, inplace=True)
    
    # --- Boucle d'Importation ---
    for index, row in df.iterrows():
        # 1. Vérifications et Conversion
        if row['immatriculation_excel'] is None or row['montant_ht'] is None:
            continue

        # 2. Trouver l'Equipement ID par Immatriculation
        equipement = db.query(Equipement).filter(
            Equipement.immatriculation == row['immatriculation_excel']
        ).first()

        if not equipement:
            print(f"Skipping: Engin (Immat={row['immatriculation_excel']}) non trouvé dans le référentiel.")
            continue
        
        # 3. Création du Fournisseur
        fournisseur_id = None
        if row['fournisseur_nom']:
            fournisseur = get_or_create_fournisseur(db, str(row['fournisseur_nom']))
            fournisseur_id = fournisseur.id
        
        # 4. Création de la Dépense
        try:
            montant_ht = Decimal(str(row['montant_ht']))
            date_depense = row['date_depense'].date() if isinstance(row['date_depense'], pd.Timestamp) else row['date_depense']
        except Exception:
            print(f"Skipping: Erreur de conversion du montant/date pour {row['immatriculation_excel']}.")
            continue

        db_depense = DepenseEquipement(
            equipement_id=equipement.id,
            fournisseur_id=fournisseur_id,
            date_depense=date_depense, 
            type_depense=str(row['type_depense']) if row['type_depense'] else "INCONNU",
            montant_ht=montant_ht,
            description=row['description_reparation']
        )
        
        db.add(db_depense)
        compteur_creations += 1
            
    db.commit()
    return f"Importation des dépenses terminée. {compteur_creations} enregistrements créés."