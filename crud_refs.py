# crud_refs.py
from sqlalchemy.orm import Session
from typing import List, Dict, Any

# --- Importation des modèles de BDD nécessaires ---
from models import (
    EquipementCategorie, 
    Site, 
    Fournisseur,        # <-- ESSENTIEL pour get_or_create_fournisseur
    Client,             # Pour les chantiers/projets
    CentreAnalytique,   # L'Enum pour le type de site
    Division,           # Référentiel RH
    Service,            # Référentiel RH
    Fonction,           # Référentiel RH
    Personne            # Pour le chef de chantier
) 

# -------------------------------------------------------------------------
# FONCTIONS CRUD DE BASE (Get or Create)
# Ces fonctions garantissent qu'un élément de référence n'est pas dupliqué
# -------------------------------------------------------------------------

def get_or_create_categorie(db: Session, code: str, libelle: str) -> EquipementCategorie:
    """Récupère une catégorie d'équipement ou la crée si elle n'existe pas."""
    categorie = db.query(EquipementCategorie).filter(EquipementCategorie.code == code).first()
    if not categorie:
        categorie = EquipementCategorie(code=code, libelle=libelle)
        db.add(categorie)
        db.commit()
        db.refresh(categorie)
    return categorie

def get_or_create_site(db: Session, code: str, nom: str, type_site: str, centre: CentreAnalytique) -> Site:
    """Récupère un site (chantier, usine, dépôt) ou le crée si un n'existe pas."""
    # Note : Le paramètre 'centre' doit être une instance de l'Enum CentreAnalytique
    site = db.query(Site).filter(Site.code == code).first()
    if not site:
        site = Site(code=code, nom=nom, type_site=type_site, centre_analytique=centre)
        db.add(site)
        db.commit()
        db.refresh(site)
    return site

def get_or_create_fournisseur(db: Session, nom_entreprise: str) -> Fournisseur:
    """Récupère un fournisseur ou le crée si l'entreprise n'existe pas encore."""
    fournisseur = db.query(Fournisseur).filter(Fournisseur.nom_entreprise == nom_entreprise).first()
    if not fournisseur:
        fournisseur = Fournisseur(nom_entreprise=nom_entreprise)
        db.add(fournisseur)
        db.commit()
        db.refresh(fournisseur)
    return fournisseur

# -------------------------------------------------------------------------
# FONCTIONS CRUD POUR LES RÉFÉRENTIELS RH
# -------------------------------------------------------------------------

def get_or_create_division(db: Session, nom: str) -> Division:
    """Récupère une division ou la crée si elle n'existe pas."""
    division = db.query(Division).filter(Division.nom == nom).first()
    if not division:
        division = Division(nom=nom)
        db.add(division)
        db.commit()
        db.refresh(division)
    return division

def get_or_create_service(db: Session, nom: str, division_id: int = None) -> Service:
    """Récupère un service ou le crée si il n'existe pas."""
    service = db.query(Service).filter(Service.nom == nom).first()
    if not service:
        service = Service(nom=nom, division_id=division_id)
        db.add(service)
        db.commit()
        db.refresh(service)
    return service

def get_or_create_fonction(db: Session, nom: str, code: str = None) -> Fonction:
    """Récupère une fonction ou la crée si elle n'existe pas."""
    # Recherche par code si fourni, sinon par nom
    if code:
        fonction = db.query(Fonction).filter(Fonction.code == code).first()
    else:
        fonction = db.query(Fonction).filter(Fonction.nom == nom).first()
    
    if not fonction:
        fonction = Fonction(nom=nom, code=code)
        db.add(fonction)
        db.commit()
        db.refresh(fonction)
    return fonction