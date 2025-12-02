# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from decimal import Decimal

# --- 1. Imports de la Couche Base de Données et Schémas ---
from database import get_db, engine
from models import (
    Equipement, Personne, AffectationEquipement, DepenseEquipement, EquipementCategorie
)
from schemas import (
    AffectationCreate, DepenseEquipementCreate, 
    EquipementCreate, EquipementUpdate, EquipementResponse
) # Les schémas Pydantic

# --- 2. Imports de la Couche Logique Métier (CRUD) ---
from crud_equipement import (
    import_equipements_from_excel,
    get_equipement, get_equipements, create_equipement, 
    update_equipement, delete_equipement
) # Importe les fonctions CRUD pour équipements
from crud_depenses import import_depenses_from_excel # Importe l'import des dépenses


# --- Initialisation de l'Application ---
app = FastAPI(title="ERP Maintenance & Chantiers API")

# ----------------------------------------------------------------------
# FONCTIONS UTILITAIRES (Logique Métier)
# ----------------------------------------------------------------------

def get_cost_data(db: Session, equip_id: int, operateur_id: Optional[int]):
    """Récupère les données de coût nécessaires au calcul d'affectation."""
    
    equip = db.query(Equipement).filter(Equipement.id == equip_id).first()
    if not equip:
        raise HTTPException(status_code=404, detail=f"Équipement ID {equip_id} non trouvé.")

    taux_horaire_operateur = Decimal(0.0)
    if operateur_id:
        operateur = db.query(Personne).filter(Personne.id == operateur_id).first()
        if not operateur:
             raise HTTPException(status_code=404, detail=f"Opérateur ID {operateur_id} non trouvé.")
        
        taux_horaire_operateur = operateur.taux_horaire_cout if operateur.taux_horaire_cout is not None else Decimal(0.0)

    return equip, taux_horaire_operateur

# ----------------------------------------------------------------------
# ROUTES API (Endpoints)
# ----------------------------------------------------------------------

@app.get("/")
def read_root():
    """Route de base pour vérifier que l'API est en ligne."""
    return {"message": "API ERP opérationnelle. Visitez /docs pour la documentation interactive."}

# Route 1 : Saisie de l'Affectation (Matin/APM)
@app.post("/affectations/create")
def create_affectation(affectation: AffectationCreate, db: Session = Depends(get_db)):
    
    existing = db.query(AffectationEquipement).filter(
        AffectationEquipement.date_jour == affectation.date_jour,
        AffectationEquipement.equipement_id == affectation.equipement_id,
        AffectationEquipement.bloc_jour == affectation.bloc_jour
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Une affectation existe déjà pour cet engin, cette date et ce bloc journalier.")

    equip, taux_operateur = get_cost_data(db, affectation.equipement_id, affectation.operateur_id)
    
    cout_operateur = affectation.heure_jour * taux_operateur
    cout_usage = (affectation.heure_jour * equip.cout_usage_1h_lei) + \
                 (affectation.km_effectue * equip.cout_usage_100km_lei / Decimal(100))

    db_affectation = AffectationEquipement(
        **affectation.model_dump(exclude_none=True), 
        cout_usage_calc=cout_usage, 
        cout_operateur_calc=cout_operateur
    )

    db.add(db_affectation)
    db.commit()
    db.refresh(db_affectation)
    
    return {"message": "Affectation Matin/APM créée avec succès.", "id": db_affectation.id}


# Route 2 : Saisie des Dépenses d'Équipement (Maintenance, Assurance, etc.)
@app.post("/depenses/create")
def create_depense_equipement(depense: DepenseEquipementCreate, db: Session = Depends(get_db)):
    
    equip = db.query(Equipement).filter(Equipement.id == depense.equipement_id).first()
    if not equip:
        raise HTTPException(status_code=404, detail="Équipement non trouvé. Impossible d'enregistrer la dépense.")
        
    db_depense = DepenseEquipement(**depense.model_dump(exclude_none=True))
    
    db.add(db_depense)
    db.commit()
    db.refresh(db_depense)
    
    return {"message": "Dépense enregistrée avec succès.", "id": db_depense.id}

# Route 3 : Affichage des Équipements (FILTRE PAR CATÉGORIE)
@app.get("/equipements", response_model=List[dict]) 
def list_equipements(
    db: Session = Depends(get_db),
    categorie_code: Optional[str] = None
):
    """Affiche tous les équipements ou filtre par catégorie (pour le menu Équipement)."""
    
    # Assurez-vous d'avoir un Pydantic Model de Réponse EquipementResponse dans schemas.py !
    
    query = db.query(Equipement, EquipementCategorie.libelle.label('categorie_libelle'))\
              .join(EquipementCategorie, Equipement.categorie_id == EquipementCategorie.id)

    if categorie_code:
        query = query.filter(EquipementCategorie.code == categorie_code)

    results = query.all()
    
    equipements_list = []
    for equipement, libelle in results:
        equipements_list.append({
            "id": equipement.id,
            "code": equipement.code,
            "immatriculation": equipement.immatriculation,
            "categorie": libelle,
            "cout_horaire_theorique": equipement.cout_usage_1h_lei,
            "site_rattachement_id": equipement.site_rattachement_id
        })
        
    return equipements_list

# Route 4 : Importation de Masse des Équipements (TEMPORAIRE)
@app.post("/import/equipements")
def run_import_equipements(db: Session = Depends(get_db)):
    """
    Lance l'importation de la liste des équipements à partir du fichier Excel.
    Colonnes attendues : EquipID, Categorie, Modele, Immatriculation, Annee, Statut, 
    UsageSource, UniteCompteur, TypeCarburant, Conso_100km_L, Conso_h_L, etc.
    """
    file_path = r"C:\Users\user\Desktop\QUOTIDIEN\Tableau_Equipements.xlsx" 
    
    result = import_equipements_from_excel(db, file_path)
    
    return {"status": "success", "message": result}

# Route 5 : Importation de Masse des Dépenses/Interventions (TEMPORAIRE)
@app.post("/import/depenses")
def run_import_depenses(db: Session = Depends(get_db)):
    """
    Lance l'importation de l'historique des interventions et dépenses d'équipement.
    Colonnes attendues : Immatriculation, Categorie, Modele, Date, Fournisseur_Nom, 
    Categ_intervention, description_intervention, montant
    """
    file_path = r"C:\Users\user\Desktop\QUOTIDIEN\interventionEquipement.xlsx" 
    
    result = import_depenses_from_excel(db, file_path)
    
    return {"status": "success", "message": result}