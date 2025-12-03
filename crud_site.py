# crud_site.py
from sqlalchemy.orm import Session
import pandas as pd
from typing import List, Optional
from datetime import datetime

from models import Site, Client, Personne, CentreAnalytique

# ============================================================
# FONCTIONS CRUD DE BASE POUR LES SITES
# ============================================================

def get_site(db: Session, site_id: int) -> Optional[Site]:
    """Récupère un site par son ID."""
    return db.query(Site).filter(Site.id == site_id).first()

def get_site_by_code(db: Session, code: str) -> Optional[Site]:
    """Récupère un site par son code."""
    return db.query(Site).filter(Site.code == code).first()

def get_sites(db: Session, skip: int = 0, limit: int = 100, actif: Optional[bool] = True) -> List[Site]:
    """Récupère une liste de sites avec pagination."""
    query = db.query(Site)
    if actif is not None:
        query = query.filter(Site.actif == actif)
    return query.offset(skip).limit(limit).all()

def create_site(db: Session, site_data: dict) -> Site:
    """Crée un nouveau site."""
    db_site = Site(**site_data)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

def update_site(db: Session, site_id: int, site_data: dict) -> Optional[Site]:
    """Met à jour un site existant."""
    db_site = db.query(Site).filter(Site.id == site_id).first()
    if not db_site:
        return None
    
    for key, value in site_data.items():
        if value is not None:
            setattr(db_site, key, value)
    
    db.commit()
    db.refresh(db_site)
    return db_site

# ============================================================
# FONCTIONS POUR LES CLIENTS
# ============================================================

def get_or_create_client(db: Session, nom: str) -> Client:
    """Récupère un client ou le crée s'il n'existe pas."""
    client = db.query(Client).filter(Client.nom == nom).first()
    if not client:
        client = Client(nom=nom, actif=True)
        db.add(client)
        db.commit()
        db.refresh(client)
    return client

# ============================================================
# FONCTION D'IMPORTATION DEPUIS EXCEL
# ============================================================

def import_sites_from_excel(db: Session, file_path: str):
    """
    Lit le fichier Excel des sites/chantiers/usines et les importe dans la base de données.
    Colonnes attendues : ChantierID, Intitule, TypeSite, Client, Localisation, 
    DateDebut, DateFin, ChefChantier, Statut
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
            chantier_id = str(row.get('ChantierID', '')).strip() if row.get('ChantierID') else None
            intitule = str(row.get('Intitule', '')).strip() if row.get('Intitule') else None
            type_site = str(row.get('TypeSite', 'CHANTIER')).strip().upper() if row.get('TypeSite') else 'CHANTIER'
            
            # Vérification des champs obligatoires
            if not chantier_id or not intitule:
                print(f"Ligne {index + 2} ignorée : ChantierID ou Intitulé manquant")
                compteur_erreurs += 1
                continue
            
            # --- GESTION DU CLIENT ---
            client_id = None
            if row.get('Client'):
                client_nom = str(row['Client']).strip()
                client = get_or_create_client(db, client_nom)
                client_id = client.id
            
            # --- GESTION DU CHEF DE CHANTIER ---
            chef_chantier_id = None
            if row.get('ChefChantier'):
                chef_nom = str(row['ChefChantier']).strip()
                # Recherche par nom (on pourrait améliorer avec une recherche plus précise)
                chef = db.query(Personne).filter(Personne.nom_prenom.ilike(f"%{chef_nom}%")).first()
                if chef:
                    chef_chantier_id = chef.id
                else:
                    print(f"Ligne {index + 2} : Chef de chantier '{chef_nom}' non trouvé dans le personnel")
            
            # --- GESTION DES DATES ---
            date_debut = None
            date_fin = None
            
            if row.get('DateDebut'):
                try:
                    if isinstance(row['DateDebut'], pd.Timestamp):
                        date_debut = row['DateDebut'].date()
                    elif isinstance(row['DateDebut'], str):
                        date_debut = pd.to_datetime(row['DateDebut']).date()
                except:
                    print(f"Ligne {index + 2} : Erreur conversion DateDebut")
            
            if row.get('DateFin'):
                try:
                    if isinstance(row['DateFin'], pd.Timestamp):
                        date_fin = row['DateFin'].date()
                    elif isinstance(row['DateFin'], str):
                        date_fin = pd.to_datetime(row['DateFin']).date()
                except:
                    print(f"Ligne {index + 2} : Erreur conversion DateFin")
            
            # --- DÉTERMINATION DU CENTRE ANALYTIQUE ---
            # Mapping par défaut basé sur le type de site
            centre_mapping = {
                'USINE': CentreAnalytique.PROD,
                'CHANTIER': CentreAnalytique.CHANTIER,
                'DEPOT': CentreAnalytique.ADMIN,
                'BUREAU': CentreAnalytique.ADMIN
            }
            centre_analytique = centre_mapping.get(type_site, CentreAnalytique.CHANTIER)
            
            # --- GESTION DU STATUT ---
            statut = str(row.get('Statut', 'EN_COURS')).strip().upper() if row.get('Statut') else 'EN_COURS'
            
            # --- LOCALISATION ---
            localisation = str(row.get('Localisation', '')).strip() if row.get('Localisation') else None
            
            # --- CRÉATION OU MISE À JOUR DU SITE ---
            site = db.query(Site).filter(Site.code == chantier_id).first()
            
            if not site:
                # Création d'un nouveau site
                site = Site(
                    code=chantier_id,
                    nom=intitule,
                    type_site=type_site,
                    centre_analytique=centre_analytique,
                    client_id=client_id,
                    localisation=localisation,
                    date_debut=date_debut,
                    date_fin=date_fin,
                    chef_chantier_id=chef_chantier_id,
                    statut=statut,
                    actif=(statut != 'TERMINE')
                )
                db.add(site)
                compteur_creations += 1
            else:
                # Mise à jour d'un site existant
                site.nom = intitule
                site.type_site = type_site
                site.centre_analytique = centre_analytique
                site.client_id = client_id
                site.localisation = localisation
                site.date_debut = date_debut
                site.date_fin = date_fin
                site.chef_chantier_id = chef_chantier_id
                site.statut = statut
                site.actif = (statut != 'TERMINE')
                compteur_mises_a_jour += 1
                
        except Exception as e:
            print(f"Erreur ligne {index + 2} : {e}")
            compteur_erreurs += 1
            continue
    
    db.commit()
    return f"Importation des sites terminée. {compteur_creations} créations, {compteur_mises_a_jour} mises à jour, {compteur_erreurs} erreurs."

