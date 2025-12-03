# api_routes.py - Routes API CRUD complètes pour l'application web

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from database import get_db
from models import Site, Equipement, Personne, Client, Division, Service, Fonction, EquipementCategorie, CentreAnalytique, DepenseEquipement, Fournisseur
from schemas import (
    SiteCreate, SiteUpdate, SiteResponse,
    EquipementCreate, EquipementUpdate, EquipementResponse,
    PersonneCreate, PersonneUpdate, PersonneResponse
)
from crud_site import get_or_create_client
from crud_refs import get_or_create_division, get_or_create_service, get_or_create_fonction
from crud_site import get_or_create_client

router = APIRouter()

# ============================================================================
# ROUTES CRUD POUR LES SITES/CHANTIERS
# ============================================================================

@router.get("/api/sites", response_model=List[SiteResponse])
def api_list_sites(
    db: Session = Depends(get_db),
    type_site: Optional[str] = None,
    statut: Optional[str] = None,
    actif: Optional[bool] = True
):
    """Liste tous les sites avec filtres optionnels."""
    query = db.query(Site)
    
    if actif is not None:
        query = query.filter(Site.actif == actif)
    if type_site:
        query = query.filter(Site.type_site == type_site.upper())
    if statut:
        query = query.filter(Site.statut == statut.upper())
    
    sites = query.all()
    
    result = []
    for s in sites:
        client_nom = None
        if s.client_id:
            client = db.query(Client).filter(Client.id == s.client_id).first()
            if client:
                client_nom = client.nom
        
        chef_nom = None
        if s.chef_chantier_id:
            chef = db.query(Personne).filter(Personne.id == s.chef_chantier_id).first()
            if chef:
                chef_nom = chef.nom_prenom
        
        result.append(SiteResponse(
            id=s.id,
            code=s.code,
            nom=s.nom,
            type_site=s.type_site,
            client=client_nom,
            localisation=s.localisation,
            date_debut=s.date_debut,
            date_fin=s.date_fin,
            chef_chantier=chef_nom,
            statut=s.statut,
            actif=s.actif
        ))
    
    return result

@router.get("/api/sites/{site_id}", response_model=SiteResponse)
def api_get_site(site_id: int, db: Session = Depends(get_db)):
    """Récupère un site par son ID."""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    
    client_nom = None
    if site.client_id:
        client = db.query(Client).filter(Client.id == site.client_id).first()
        if client:
            client_nom = client.nom
    
    chef_nom = None
    if site.chef_chantier_id:
        chef = db.query(Personne).filter(Personne.id == site.chef_chantier_id).first()
        if chef:
            chef_nom = chef.nom_prenom
    
    return SiteResponse(
        id=site.id,
        code=site.code,
        nom=site.nom,
        type_site=site.type_site,
        client=client_nom,
        localisation=site.localisation,
        date_debut=site.date_debut,
        date_fin=site.date_fin,
        chef_chantier=chef_nom,
        statut=site.statut,
        actif=site.actif
    )

@router.post("/api/sites", response_model=SiteResponse)
def api_create_site(site_data: SiteCreate, db: Session = Depends(get_db)):
    """Crée un nouveau site."""
    # Vérifier si le code existe déjà
    existing = db.query(Site).filter(Site.code == site_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Un site avec ce code existe déjà")
    
    # Créer ou récupérer le client
    client_id = None
    if site_data.client_nom:
        client = get_or_create_client(db, site_data.client_nom)
        client_id = client.id
    
    # Déterminer le centre analytique
    centre_mapping = {
        'USINE': CentreAnalytique.PROD,
        'CHANTIER': CentreAnalytique.CHANTIER,
        'DEPOT': CentreAnalytique.ADMIN,
        'BUREAU': CentreAnalytique.ADMIN
    }
    centre_analytique = centre_mapping.get(site_data.type_site.upper(), CentreAnalytique.CHANTIER)
    
    # Créer le site
    new_site = Site(
        code=site_data.code,
        nom=site_data.nom,
        type_site=site_data.type_site.upper(),
        centre_analytique=centre_analytique,
        client_id=client_id,
        localisation=site_data.localisation,
        date_debut=site_data.date_debut,
        date_fin=site_data.date_fin,
        chef_chantier_id=site_data.chef_chantier_id,
        statut=site_data.statut.upper() if site_data.statut else "EN_COURS",
        actif=site_data.actif
    )
    
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    
    return api_get_site(new_site.id, db)

@router.put("/api/sites/{site_id}", response_model=SiteResponse)
def api_update_site(site_id: int, site_data: SiteUpdate, db: Session = Depends(get_db)):
    """Met à jour un site existant."""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    
    # Mettre à jour les champs fournis
    if site_data.code is not None:
        site.code = site_data.code
    if site_data.nom is not None:
        site.nom = site_data.nom
    if site_data.type_site is not None:
        site.type_site = site_data.type_site.upper()
    if site_data.client_nom is not None:
        client = get_or_create_client(db, site_data.client_nom)
        site.client_id = client.id
    if site_data.localisation is not None:
        site.localisation = site_data.localisation
    if site_data.date_debut is not None:
        site.date_debut = site_data.date_debut
    if site_data.date_fin is not None:
        site.date_fin = site_data.date_fin
    if site_data.chef_chantier_id is not None:
        site.chef_chantier_id = site_data.chef_chantier_id
    if site_data.statut is not None:
        site.statut = site_data.statut.upper()
    if site_data.actif is not None:
        site.actif = site_data.actif
    
    db.commit()
    db.refresh(site)
    
    return api_get_site(site.id, db)

@router.delete("/api/sites/{site_id}")
def api_delete_site(site_id: int, db: Session = Depends(get_db)):
    """Désactive un site (soft delete)."""
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site non trouvé")
    
    site.actif = False
    db.commit()
    
    return {"message": "Site désactivé avec succès", "id": site_id}

# ============================================================================
# ROUTES CRUD POUR LES ÉQUIPEMENTS
# ============================================================================

@router.get("/api/equipements", response_model=List[EquipementResponse])
def api_list_equipements(
    db: Session = Depends(get_db),
    categorie_code: Optional[str] = None,
    actif: Optional[bool] = True
):
    """Liste tous les équipements avec filtres optionnels."""
    query = db.query(Equipement, EquipementCategorie.libelle.label('categorie_libelle'))\
              .join(EquipementCategorie, Equipement.categorie_id == EquipementCategorie.id, isouter=True)
    
    if actif is not None:
        query = query.filter(Equipement.actif == actif)
    if categorie_code:
        query = query.filter(EquipementCategorie.code == categorie_code)
    
    results = query.all()
    
    equipements_list = []
    for equipement, libelle in results:
        equipements_list.append(EquipementResponse(
            id=equipement.id,
            code=equipement.code,
            immatriculation=equipement.immatriculation,
            categorie=libelle,
            cout_horaire_theorique=equipement.cout_usage_1h_lei,
            site_rattachement_id=equipement.site_rattachement_id
        ))
    
    return equipements_list

@router.get("/api/equipements/{equipement_id}", response_model=EquipementResponse)
def api_get_equipement(equipement_id: int, db: Session = Depends(get_db)):
    """Récupère un équipement par son ID."""
    equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not equipement:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    
    categorie_libelle = None
    if equipement.categorie_id:
        categorie = db.query(EquipementCategorie).filter(EquipementCategorie.id == equipement.categorie_id).first()
        if categorie:
            categorie_libelle = categorie.libelle
    
    return EquipementResponse(
        id=equipement.id,
        code=equipement.code,
        immatriculation=equipement.immatriculation,
        categorie=categorie_libelle,
        cout_horaire_theorique=equipement.cout_usage_1h_lei,
        site_rattachement_id=equipement.site_rattachement_id
    )

@router.post("/api/equipements", response_model=EquipementResponse)
def api_create_equipement(equipement_data: EquipementCreate, db: Session = Depends(get_db)):
    """Crée un nouvel équipement."""
    # Vérifier si le code existe déjà
    existing = db.query(Equipement).filter(Equipement.code == equipement_data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Un équipement avec ce code existe déjà")
    
    new_equipement = Equipement(**equipement_data.model_dump(exclude_none=True))
    
    db.add(new_equipement)
    db.commit()
    db.refresh(new_equipement)
    
    return api_get_equipement(new_equipement.id, db)

@router.put("/api/equipements/{equipement_id}", response_model=EquipementResponse)
def api_update_equipement(equipement_id: int, equipement_data: EquipementUpdate, db: Session = Depends(get_db)):
    """Met à jour un équipement existant."""
    equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not equipement:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    
    # Mettre à jour les champs fournis
    for key, value in equipement_data.model_dump(exclude_none=True).items():
        setattr(equipement, key, value)
    
    db.commit()
    db.refresh(equipement)
    
    return api_get_equipement(equipement.id, db)

@router.delete("/api/equipements/{equipement_id}")
def api_delete_equipement(equipement_id: int, db: Session = Depends(get_db)):
    """Désactive un équipement (soft delete)."""
    equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not equipement:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    
    equipement.actif = False
    db.commit()
    
    return {"message": "Équipement désactivé avec succès", "id": equipement_id}

# ============================================================================
# ROUTES CRUD POUR LES SALARIÉS/PERSONNEL
# ============================================================================

@router.get("/api/personnel", response_model=List[PersonneResponse])
def api_list_personnel(
    db: Session = Depends(get_db),
    division: Optional[str] = None,
    actif: Optional[bool] = True
):
    """Liste tous les salariés avec filtres optionnels."""
    query = db.query(Personne)
    
    if actif is not None:
        query = query.filter(Personne.actif == actif)
    if division:
        div = db.query(Division).filter(Division.nom == division).first()
        if div:
            query = query.filter(Personne.division_id == div.id)
    
    personnes = query.all()
    
    result = []
    for p in personnes:
        division_nom = None
        if p.division_id:
            div = db.query(Division).filter(Division.id == p.division_id).first()
            if div:
                division_nom = div.nom
        
        service_nom = None
        if p.service_id:
            serv = db.query(Service).filter(Service.id == p.service_id).first()
            if serv:
                service_nom = serv.nom
        
        fonction_nom = None
        if p.fonction_id:
            fonc = db.query(Fonction).filter(Fonction.id == p.fonction_id).first()
            if fonc:
                fonction_nom = fonc.nom
        
        result.append(PersonneResponse(
            id=p.id,
            matricule=p.matricule,
            nom_prenom=p.nom_prenom,
            secteur=p.secteur,
            division=division_nom,
            service=service_nom,
            fonction=fonction_nom,
            salaire_tarif=p.salaire_tarif,
            taux_horaire_cout=p.taux_horaire_cout,
            actif=p.actif
        ))
    
    return result

@router.get("/api/personnel/{personne_id}", response_model=PersonneResponse)
def api_get_personne(personne_id: int, db: Session = Depends(get_db)):
    """Récupère un salarié par son ID."""
    personne = db.query(Personne).filter(Personne.id == personne_id).first()
    if not personne:
        raise HTTPException(status_code=404, detail="Salarié non trouvé")
    
    division_nom = None
    if personne.division_id:
        div = db.query(Division).filter(Division.id == personne.division_id).first()
        if div:
            division_nom = div.nom
    
    service_nom = None
    if personne.service_id:
        serv = db.query(Service).filter(Service.id == personne.service_id).first()
        if serv:
            service_nom = serv.nom
    
    fonction_nom = None
    if personne.fonction_id:
        fonc = db.query(Fonction).filter(Fonction.id == personne.fonction_id).first()
        if fonc:
            fonction_nom = fonc.nom
    
    return PersonneResponse(
        id=personne.id,
        matricule=personne.matricule,
        nom_prenom=personne.nom_prenom,
        secteur=personne.secteur,
        division=division_nom,
        service=service_nom,
        fonction=fonction_nom,
        salaire_tarif=personne.salaire_tarif,
        taux_horaire_cout=personne.taux_horaire_cout,
        actif=personne.actif
    )

@router.post("/api/personnel", response_model=PersonneResponse)
def api_create_personne(personne_data: PersonneCreate, db: Session = Depends(get_db)):
    """Crée un nouveau salarié."""
    # Vérifier si le matricule existe déjà
    existing = db.query(Personne).filter(Personne.matricule == personne_data.matricule).first()
    if existing:
        raise HTTPException(status_code=400, detail="Un salarié avec ce matricule existe déjà")
    
    # Créer ou récupérer les référentiels
    division_id = None
    if personne_data.division_nom:
        division = get_or_create_division(db, personne_data.division_nom)
        division_id = division.id
    
    service_id = None
    if personne_data.service_nom:
        service = get_or_create_service(db, personne_data.service_nom, division_id)
        service_id = service.id
    
    fonction_id = None
    if personne_data.fonction_nom:
        fonction = get_or_create_fonction(db, personne_data.fonction_nom, personne_data.fonction_code)
        fonction_id = fonction.id
    
    # Calculer le taux horaire si non fourni
    taux_horaire = personne_data.taux_horaire_cout
    if not taux_horaire and personne_data.salaire_tarif:
        salaire = personne_data.salaire_tarif or Decimal(0)
        accord = personne_data.accord_supplementaire or Decimal(0)
        taux_horaire = (salaire + accord) / Decimal(168)
    
    new_personne = Personne(
        matricule=personne_data.matricule,
        nom_prenom=personne_data.nom_prenom,
        secteur=personne_data.secteur,
        division_id=division_id,
        service_id=service_id,
        fonction_id=fonction_id,
        salaire_tarif=personne_data.salaire_tarif,
        accord_supplementaire=personne_data.accord_supplementaire,
        taux_horaire_cout=taux_horaire,
        actif=personne_data.actif
    )
    
    db.add(new_personne)
    db.commit()
    db.refresh(new_personne)
    
    return api_get_personne(new_personne.id, db)

@router.put("/api/personnel/{personne_id}", response_model=PersonneResponse)
def api_update_personne(personne_id: int, personne_data: PersonneUpdate, db: Session = Depends(get_db)):
    """Met à jour un salarié existant."""
    personne = db.query(Personne).filter(Personne.id == personne_id).first()
    if not personne:
        raise HTTPException(status_code=404, detail="Salarié non trouvé")
    
    # Mettre à jour les champs fournis
    if personne_data.matricule is not None:
        personne.matricule = personne_data.matricule
    if personne_data.nom_prenom is not None:
        personne.nom_prenom = personne_data.nom_prenom
    if personne_data.secteur is not None:
        personne.secteur = personne_data.secteur
    if personne_data.division_nom is not None:
        division = get_or_create_division(db, personne_data.division_nom)
        personne.division_id = division.id
    if personne_data.service_nom is not None:
        service = get_or_create_service(db, personne_data.service_nom, personne.division_id)
        personne.service_id = service.id
    if personne_data.fonction_nom is not None:
        fonction = get_or_create_fonction(db, personne_data.fonction_nom, personne_data.fonction_code)
        personne.fonction_id = fonction.id
    if personne_data.salaire_tarif is not None:
        personne.salaire_tarif = personne_data.salaire_tarif
    if personne_data.accord_supplementaire is not None:
        personne.accord_supplementaire = personne_data.accord_supplementaire
    if personne_data.taux_horaire_cout is not None:
        personne.taux_horaire_cout = personne_data.taux_horaire_cout
    if personne_data.actif is not None:
        personne.actif = personne_data.actif
    
    db.commit()
    db.refresh(personne)
    
    return api_get_personne(personne.id, db)

@router.delete("/api/personnel/{personne_id}")
def api_delete_personne(personne_id: int, db: Session = Depends(get_db)):
    """Désactive un salarié (soft delete)."""
    personne = db.query(Personne).filter(Personne.id == personne_id).first()
    if not personne:
        raise HTTPException(status_code=404, detail="Salarié non trouvé")
    
    personne.actif = False
    db.commit()
    
    return {"message": "Salarié désactivé avec succès", "id": personne_id}

# ============================================================================
# ROUTES CRUD POUR LES DÉPENSES ÉQUIPEMENT
# ============================================================================

@router.get("/api/depenses")
def api_list_depenses(
    db: Session = Depends(get_db),
    equipement_id: Optional[int] = None,
    date_debut: Optional[str] = None,
    date_fin: Optional[str] = None
):
    """Liste toutes les dépenses avec filtres optionnels."""
    query = db.query(DepenseEquipement)
    
    if equipement_id:
        query = query.filter(DepenseEquipement.equipement_id == equipement_id)
    if date_debut:
        query = query.filter(DepenseEquipement.date_depense >= date_debut)
    if date_fin:
        query = query.filter(DepenseEquipement.date_depense <= date_fin)
    
    depenses = query.order_by(DepenseEquipement.date_depense.desc()).all()
    
    result = []
    for d in depenses:
        equipement = db.query(Equipement).filter(Equipement.id == d.equipement_id).first()
        fournisseur_nom = None
        if d.fournisseur_id:
            fournisseur = db.query(Fournisseur).filter(Fournisseur.id == d.fournisseur_id).first()
            if fournisseur:
                fournisseur_nom = fournisseur.nom_entreprise
        
        result.append({
            "id": d.id,
            "equipement_code": equipement.code if equipement else None,
            "equipement_immatriculation": equipement.immatriculation if equipement else None,
            "date_depense": d.date_depense.isoformat() if d.date_depense else None,
            "type_depense": d.type_depense,
            "fournisseur": fournisseur_nom,
            "montant_ht": float(d.montant_ht) if d.montant_ht else 0,
            "description": d.description
        })
    
    return result

@router.post("/api/depenses")
def api_create_depense(
    equipement_id: int = Form(...),
    date_depense: str = Form(...),
    type_depense: str = Form(...),
    montant_ht: Decimal = Form(...),
    fournisseur_nom: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Crée une nouvelle dépense équipement."""
    from datetime import datetime
    
    # Vérifier que l'équipement existe
    equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not equipement:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    
    # Créer ou récupérer le fournisseur
    fournisseur_id = None
    if fournisseur_nom:
        fournisseur = get_or_create_client(db, fournisseur_nom)  # Réutiliser la fonction
        # Ou créer une nouvelle fonction pour les fournisseurs
        fournisseur_obj = db.query(Fournisseur).filter(Fournisseur.nom_entreprise == fournisseur_nom).first()
        if not fournisseur_obj:
            fournisseur_obj = Fournisseur(nom_entreprise=fournisseur_nom)
            db.add(fournisseur_obj)
            db.commit()
            db.refresh(fournisseur_obj)
        fournisseur_id = fournisseur_obj.id
    
    # Convertir la date
    date_obj = datetime.strptime(date_depense, '%Y-%m-%d').date()
    
    # Créer la dépense
    new_depense = DepenseEquipement(
        equipement_id=equipement_id,
        fournisseur_id=fournisseur_id,
        date_depense=date_obj,
        type_depense=type_depense,
        montant_ht=montant_ht,
        description=description
    )
    
    db.add(new_depense)
    db.commit()
    db.refresh(new_depense)
    
    return {
        "message": "Dépense enregistrée avec succès",
        "id": new_depense.id,
        "equipement": equipement.code,
        "montant": float(new_depense.montant_ht)
    }

# Version JSON pour les appels AJAX
@router.post("/api/depenses/json")
def api_create_depense_json(
    depense_data: dict,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle dépense équipement (format JSON)."""
    from datetime import datetime
    
    equipement_id = depense_data.get('equipement_id')
    date_depense = depense_data.get('date_depense')
    type_depense = depense_data.get('type_depense')
    montant_ht = Decimal(str(depense_data.get('montant_ht', 0)))
    fournisseur_nom = depense_data.get('fournisseur_nom')
    description = depense_data.get('description')
    
    # Vérifier que l'équipement existe
    equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
    if not equipement:
        raise HTTPException(status_code=404, detail="Équipement non trouvé")
    
    # Créer ou récupérer le fournisseur
    fournisseur_id = None
    if fournisseur_nom:
        fournisseur_obj = db.query(Fournisseur).filter(Fournisseur.nom_entreprise == fournisseur_nom).first()
        if not fournisseur_obj:
            fournisseur_obj = Fournisseur(nom_entreprise=fournisseur_nom)
            db.add(fournisseur_obj)
            db.commit()
            db.refresh(fournisseur_obj)
        fournisseur_id = fournisseur_obj.id
    
    # Convertir la date
    date_obj = datetime.strptime(date_depense, '%Y-%m-%d').date()
    
    # Créer la dépense
    new_depense = DepenseEquipement(
        equipement_id=equipement_id,
        fournisseur_id=fournisseur_id,
        date_depense=date_obj,
        type_depense=type_depense,
        montant_ht=montant_ht,
        description=description
    )
    
    db.add(new_depense)
    db.commit()
    db.refresh(new_depense)
    
    return {
        "message": "Dépense enregistrée avec succès",
        "id": new_depense.id,
        "equipement": equipement.code,
        "montant": float(new_depense.montant_ht)
    }

