# schemas.py

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal

# --- Schémas de Saisie des Données ---

class AffectationCreate(BaseModel):
    """Schéma de validation pour la création d'une affectation Matin/APM."""
    
    # Clés étrangères (ID des référentiels)
    equipement_id: int = Field(..., description="ID de l'équipement (PL1, R4...).")
    site_id: int = Field(..., description="ID du site/chantier d'affectation.")
    operateur_id: Optional[int] = Field(None, description="ID de l'opérateur affecté.")
    activite_id: Optional[int] = Field(None, description="ID de l'activité.")
    motif_jour_code: Optional[str] = Field(None, description="Code motif (TRAVAIL, PANNE...).")
    
    # Données d'Affectation
    date_jour: date = Field(..., description="Date de l'affectation.")
    bloc_jour: int = Field(..., ge=1, le=2, description="Bloc journalier (1 ou 2).") # Le 1 ou 2
    
    # Mesures de Saisie
    heure_jour: Decimal = Field(Decimal(0.0), description="Heures moteur/travail réelles.")
    km_effectue: Decimal = Field(Decimal(0.0), description="Distance parcourue réelle.")
    carburant_litres: Decimal = Field(Decimal(0.0), description="Litres de carburant consommés/saisis.")

    class Config:
        from_attributes = True

class DepenseEquipementCreate(BaseModel):
    """Schéma de validation pour l'enregistrement d'une dépense d'équipement."""
    
    equipement_id: int = Field(..., description="ID de l'équipement concerné.")
    # Le fournisseur_id est omis ici pour la simplicité de la saisie initiale
    
    date_depense: date
    type_depense: str = Field(..., description="Ex: Assurance, Pneumatiques, Réparation.")
    montant_ht: Decimal = Field(..., ge=0.01, description="Montant hors taxe de la dépense.")

    class Config:
        from_attributes = True
        # schemas.py (Ajouter ce code)

class EquipementResponse(BaseModel):
    """Schéma de réponse pour la liste des équipements."""
    id: int
    code: str
    immatriculation: Optional[str] = None
    categorie: Optional[str] = None
    cout_horaire_theorique: Optional[Decimal] = None
    site_rattachement_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class EquipementCreate(BaseModel):
    """Schéma de validation pour la création d'un équipement."""
    code: str = Field(..., description="Code unique de l'équipement (ex: PL1, R4).")
    immatriculation: Optional[str] = Field(None, description="Immatriculation de l'équipement.")
    categorie_id: Optional[int] = Field(None, description="ID de la catégorie d'équipement.")
    unite_compteur: Optional[str] = Field('H', description="Unité de compteur (H pour heures, KM pour kilomètres).")
    usage_source: Optional[str] = Field('MANUEL', description="Source d'usage (MANUEL, OMNICOMM).")
    conso_h_l: Optional[Decimal] = Field(None, description="Consommation horaire en litres.")
    cout_usage_1h_lei: Optional[Decimal] = Field(None, description="Coût d'usage pour 1 heure en LEI.")
    cout_usage_100km_lei: Optional[Decimal] = Field(None, description="Coût d'usage pour 100 km en LEI.")
    site_rattachement_id: Optional[int] = Field(None, description="ID du site de rattachement.")
    actif: Optional[bool] = Field(True, description="Statut actif de l'équipement.")
    
    class Config:
        from_attributes = True

class EquipementUpdate(BaseModel):
    """Schéma de validation pour la mise à jour d'un équipement."""
    code: Optional[str] = Field(None, description="Code unique de l'équipement.")
    immatriculation: Optional[str] = Field(None, description="Immatriculation de l'équipement.")
    categorie_id: Optional[int] = Field(None, description="ID de la catégorie d'équipement.")
    unite_compteur: Optional[str] = Field(None, description="Unité de compteur.")
    usage_source: Optional[str] = Field(None, description="Source d'usage.")
    conso_h_l: Optional[Decimal] = Field(None, description="Consommation horaire en litres.")
    cout_usage_1h_lei: Optional[Decimal] = Field(None, description="Coût d'usage pour 1 heure en LEI.")
    cout_usage_100km_lei: Optional[Decimal] = Field(None, description="Coût d'usage pour 100 km en LEI.")
    site_rattachement_id: Optional[int] = Field(None, description="ID du site de rattachement.")
    actif: Optional[bool] = Field(None, description="Statut actif de l'équipement.")
    
    class Config:
        from_attributes = True

# --- Schémas pour les Sites/Chantiers ---

class SiteCreate(BaseModel):
    """Schéma de validation pour la création d'un site/chantier."""
    code: str = Field(..., description="Code unique du site.")
    nom: str = Field(..., description="Nom/intitulé du site.")
    type_site: str = Field(..., description="Type: USINE, CHANTIER, DEPOT, BUREAU.")
    client_nom: Optional[str] = Field(None, description="Nom du client.")
    localisation: Optional[str] = Field(None, description="Localisation du site.")
    date_debut: Optional[date] = Field(None, description="Date de début.")
    date_fin: Optional[date] = Field(None, description="Date de fin.")
    chef_chantier_id: Optional[int] = Field(None, description="ID du chef de chantier.")
    statut: Optional[str] = Field("EN_COURS", description="Statut: EN_COURS, TERMINE, PLANIFIE, SUSPENDU.")
    actif: Optional[bool] = Field(True, description="Statut actif du site.")
    
    class Config:
        from_attributes = True

class SiteUpdate(BaseModel):
    """Schéma de validation pour la mise à jour d'un site/chantier."""
    code: Optional[str] = Field(None, description="Code unique du site.")
    nom: Optional[str] = Field(None, description="Nom/intitulé du site.")
    type_site: Optional[str] = Field(None, description="Type du site.")
    client_nom: Optional[str] = Field(None, description="Nom du client.")
    localisation: Optional[str] = Field(None, description="Localisation du site.")
    date_debut: Optional[date] = Field(None, description="Date de début.")
    date_fin: Optional[date] = Field(None, description="Date de fin.")
    chef_chantier_id: Optional[int] = Field(None, description="ID du chef de chantier.")
    statut: Optional[str] = Field(None, description="Statut du site.")
    actif: Optional[bool] = Field(None, description="Statut actif du site.")
    
    class Config:
        from_attributes = True

class SiteResponse(BaseModel):
    """Schéma de réponse pour un site/chantier."""
    id: int
    code: str
    nom: str
    type_site: str
    client: Optional[str] = None
    localisation: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    chef_chantier: Optional[str] = None
    statut: Optional[str] = None
    actif: bool
    
    class Config:
        from_attributes = True

# --- Schémas pour les Personnes/Salariés ---

class PersonneCreate(BaseModel):
    """Schéma de validation pour la création d'un salarié."""
    matricule: str = Field(..., description="Matricule unique du salarié.")
    nom_prenom: str = Field(..., description="Nom et prénom du salarié.")
    secteur: Optional[str] = Field(None, description="Secteur d'activité.")
    division_nom: Optional[str] = Field(None, description="Nom de la division.")
    service_nom: Optional[str] = Field(None, description="Nom du service.")
    fonction_nom: Optional[str] = Field(None, description="Nom de la fonction.")
    fonction_code: Optional[str] = Field(None, description="Code de la fonction.")
    salaire_tarif: Optional[Decimal] = Field(None, description="Salaire tarifaire.")
    accord_supplementaire: Optional[Decimal] = Field(None, description="Accord supplémentaire.")
    taux_horaire_cout: Optional[Decimal] = Field(None, description="Taux horaire de coût.")
    actif: Optional[bool] = Field(True, description="Statut actif du salarié.")
    
    class Config:
        from_attributes = True

class PersonneUpdate(BaseModel):
    """Schéma de validation pour la mise à jour d'un salarié."""
    matricule: Optional[str] = Field(None, description="Matricule du salarié.")
    nom_prenom: Optional[str] = Field(None, description="Nom et prénom du salarié.")
    secteur: Optional[str] = Field(None, description="Secteur d'activité.")
    division_nom: Optional[str] = Field(None, description="Nom de la division.")
    service_nom: Optional[str] = Field(None, description="Nom du service.")
    fonction_nom: Optional[str] = Field(None, description="Nom de la fonction.")
    fonction_code: Optional[str] = Field(None, description="Code de la fonction.")
    salaire_tarif: Optional[Decimal] = Field(None, description="Salaire tarifaire.")
    accord_supplementaire: Optional[Decimal] = Field(None, description="Accord supplémentaire.")
    taux_horaire_cout: Optional[Decimal] = Field(None, description="Taux horaire de coût.")
    actif: Optional[bool] = Field(None, description="Statut actif du salarié.")
    
    class Config:
        from_attributes = True

class PersonneResponse(BaseModel):
    """Schéma de réponse pour un salarié."""
    id: int
    matricule: str
    nom_prenom: str
    secteur: Optional[str] = None
    division: Optional[str] = None
    service: Optional[str] = None
    fonction: Optional[str] = None
    salaire_tarif: Optional[Decimal] = None
    taux_horaire_cout: Optional[Decimal] = None
    actif: bool
    
    class Config:
        from_attributes = True