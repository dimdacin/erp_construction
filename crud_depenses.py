# crud_depenses.py
from sqlalchemy.orm import Session
from decimal import Decimal
import pandas as pd
from typing import List, Dict, Any

# Modèles BDD nécessaires
from models import Equipement, DepenseEquipement, Fournisseur 
# Fonctions de référence (doivent exister dans crud_refs.py)
from crud_refs import get_or_create_fournisseur 


def import_depenses_from_excel(db: Session, file_path: str, equip_code_col: str):
    """
    Lit le fichier Excel des dépenses historiques et les importe dans DepenseEquipement.
    
    Arguments:
        file_path: Chemin d'accès au fichier Excel.
        equip_code_col: Nom de la colonne dans Excel contenant le Code Engin (ex: 'EquipID' ou 'Code Engin').
    """
    try:
        # Lire le fichier Excel, en convertissant la colonne Date en type Date si possible
        df = pd.read_excel(file_path, na_values=[' -  ', '?', 'nan'])
    except Exception as e:
        return f"Erreur de lecture du fichier Excel : {e}"

    compteur_creations = 0
    df = df.where(pd.notna(df), None)
    
    # --- Renommage des colonnes pour un accès facile ---
   df.rename(columns={
        'Номерной знак': 'immatriculation', # <-- Clé de Jointure
        'Поставшик': 'fournisseur_nom',
        'Дата': 'date_depense',
        'Категория': 'type_depense',
        'Сумма': 'montant_ht',
        'Ремонт': 'description_reparation',
    }, inplace=True)
    
    # --- Boucle d'Importation ---
    for index, row in df.iterrows():
        # 1. Vérification des données critiques
        if row['equip_code'] is None or row['montant_ht'] is None or row['date_depense'] is None:
            continue
# --- 1. Recherche de l'Equipement ID par Immatriculation ---
        # ATTENTION: Nous cherchons l'équipement par Immatriculation (le Nomeroï znak)
        equipement = db.query(Equipement).filter(
            Equipement.immatriculation == row['immatriculation']
        ).first()

        if not equipement:
            print(f"Skipping: Équipement avec Immat. ({row['immatriculation']}) non trouvé. Assurez-vous d'avoir importé les équipements en premier.")
            continue
        # 2. Trouver l'Equipement ID par son CODE
        equipement = db.query(Equipement).filter(
            Equipement.code == row['equip_code']
        ).first()

        if not equipement:
            print(f"Skipping: Équipement Code ({row['equip_code']}) non trouvé dans la base de référentiel.")
            continue
        
        # 3. Obtenir/Créer le Fournisseur
        fournisseur_id = None
        if row['fournisseur_nom']:
            fournisseur = get_or_create_fournisseur(db, str(row['fournisseur_nom']))
            fournisseur_id = fournisseur.id
        
        # 4. Nettoyage et Création de la Dépense
        try:
            montant_ht = Decimal(str(row['montant_ht']))
            
            # Gestion de la date (s'assurer qu'elle est bien de type date)
            if isinstance(row['date_depense'], pd.Timestamp):
                date_depense = row['date_depense'].date()
            else:
                date_depense = row['date_depense'] 
                
        except Exception:
            print(f"Skipping: Erreur de conversion du montant ou de la date pour l'engin {row['equip_code']}.")
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