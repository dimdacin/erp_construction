# crud_equipement.py
from sqlalchemy.orm import Session
from decimal import Decimal
import pandas as pd
from typing import List, Dict, Any

# IMPORTS : Utilisation du module crud_refs et models
from models import Equipement, EquipementCategorie, Site
from crud_refs import get_or_create_categorie, get_or_create_site 
# Assurez-vous que get_or_create_categorie et get_or_create_site sont importés

def import_equipements_from_excel(db: Session, file_path: str):
    """
    Lit le fichier Excel et insère/met à jour les équipements (référentiel d'actifs).
    """
    try:
        df = pd.read_excel(file_path, na_values=[' -  ', '?', 'nan'])
    except Exception as e:
        return f"Erreur de lecture du fichier Excel : {e}"

    compteur_creations = 0
    df = df.where(pd.notna(df), None)
    
    for index, row in df.iterrows():
        # --- LOGIQUE DE CRÉATION DE CATÉGORIE ET DE SITE DE RATTACHEMENT (RÉFÉRENTIELS) ---
        categorie_id = None
        if row['Categorie']:
            categorie = get_or_create_categorie(db, row['Categorie'], row['Categorie']) 
            categorie_id = categorie.id

        # Création du site de rattachement initial si non trouvé (Exemple)
        site_rattachement = get_or_create_site(db, 
                                               'DEPOT-CENTRAL', 
                                               'Dépôt Central Non Spécifié', 
                                               'DEPOT', 
                                               'ADMIN') 
        site_rattachement_id = site_rattachement.id

        # --- CRÉATION OU MISE À JOUR DE L'ÉQUIPEMENT ---
        equip_code = row['EquipID']
        if not equip_code:
            continue

        equipement = db.query(Equipement).filter(Equipement.code == equip_code).first()

        # Fonction utilitaire pour gérer les Decimal
        def get_decimal(col_name):
            val = row.get(col_name)
            try:
                # IMPORTANT : Convertir en string avant Decimal pour éviter les erreurs de type NaN
                return Decimal(str(val)) if val is not None and str(val).lower() != 'nan' else Decimal(0)
            except:
                return Decimal(0)
        
        cout_usage_1h = get_decimal('Cout_Usage_1h_lei')
        cout_usage_100km = get_decimal('Cout_Usage_100km_lei')
        conso_h_l = get_decimal('Conso_h_L')
        
        if not equipement:
            equipement = Equipement(
                code=equip_code,
                immatriculation=row['Immatriculation'],
                modele=row['Modele'],
                categorie_id=categorie_id,
                site_rattachement_id=site_rattachement_id,
                unite_compteur=row['UniteCompteur'] if row['UniteCompteur'] else 'H',
                usage_source=row['UsageSource'] if row['UsageSource'] else 'MANUEL',
                conso_h_l=conso_h_l,
                cout_usage_1h_lei=cout_usage_1h,
                cout_usage_100km_lei=cout_usage_100km,
                actif=True
            )
            db.add(equipement)
            compteur_creations += 1
        else:
            # Mise à jour des coûts
            equipement.cout_usage_1h_lei = cout_usage_1h
            equipement.cout_usage_100km_lei = cout_usage_100km
            
    db.commit()
    return f"Importation des équipements terminée. {compteur_creations} lignes créées/mises à jour."