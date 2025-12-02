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