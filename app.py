# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import engine, SessionLocal, Base, get_db
from models import * # Importe tous vos modèles (Personne, Equipement, etc.)
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Charger la clé secrète depuis .env
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")

# Fonction pour initialiser la BDD (créer les tables si elles n'existent pas)
def init_db():
    """Crée toutes les tables si elles n'existent pas"""
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès.")

@app.route('/')
def index():
    """Page d'accueil/Tableau de Bord"""
    return jsonify({
        "message": "Bienvenue dans l'ERP Construction",
        "version": "1.0.0",
        "endpoints": {
            "equipements": "/api/equipements",
            "personnes": "/api/personnes",
            "sites": "/api/sites",
            "planning": "/api/planning"
        }
    })

# ============================================================
# API ROUTES - ÉQUIPEMENTS
# ============================================================

@app.route('/api/equipements', methods=['GET'])
def get_equipements():
    """Récupère tous les équipements"""
    db: Session = next(get_db())
    try:
        equipements = db.query(Equipement).filter(Equipement.actif == True).all()
        return jsonify([{
            "id": e.id,
            "code": e.code,
            "immatriculation": e.immatriculation,
            "site_rattachement_id": e.site_rattachement_id,
            "actif": e.actif
        } for e in equipements])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/equipements', methods=['POST'])
def create_equipement():
    """Crée un nouvel équipement"""
    db: Session = next(get_db())
    try:
        data = request.get_json()
        equipement = Equipement(
            code=data.get('code'),
            immatriculation=data.get('immatriculation'),
            unite_compteur=data.get('unite_compteur'),
            usage_source=data.get('usage_source', 'MANUEL'),
            site_rattachement_id=data.get('site_rattachement_id'),
            actif=data.get('actif', True)
        )
        db.add(equipement)
        db.commit()
        db.refresh(equipement)
        return jsonify({"id": equipement.id, "message": "Équipement créé avec succès"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@app.route('/api/equipements/<int:equipement_id>', methods=['GET'])
def get_equipement(equipement_id):
    """Récupère un équipement par son ID"""
    db: Session = next(get_db())
    try:
        equipement = db.query(Equipement).filter(Equipement.id == equipement_id).first()
        if not equipement:
            return jsonify({"error": "Équipement non trouvé"}), 404
        return jsonify({
            "id": equipement.id,
            "code": equipement.code,
            "immatriculation": equipement.immatriculation,
            "site_rattachement_id": equipement.site_rattachement_id,
            "actif": equipement.actif
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# ============================================================
# API ROUTES - PERSONNES
# ============================================================

@app.route('/api/personnes', methods=['GET'])
def get_personnes():
    """Récupère toutes les personnes"""
    db: Session = next(get_db())
    try:
        personnes = db.query(Personne).filter(Personne.actif == True).all()
        return jsonify([{
            "id": p.id,
            "matricule": p.matricule,
            "nom_prenom": p.nom_prenom,
            "division_id": p.division_id,
            "service_id": p.service_id,
            "fonction_id": p.fonction_id,
            "actif": p.actif
        } for p in personnes])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/personnes', methods=['POST'])
def create_personne():
    """Crée une nouvelle personne"""
    db: Session = next(get_db())
    try:
        data = request.get_json()
        personne = Personne(
            matricule=data.get('matricule'),
            nom_prenom=data.get('nom_prenom'),
            division_id=data.get('division_id'),
            service_id=data.get('service_id'),
            fonction_id=data.get('fonction_id'),
            salaire_tarif=data.get('salaire_tarif'),
            taux_horaire_cout=data.get('taux_horaire_cout'),
            actif=data.get('actif', True)
        )
        db.add(personne)
        db.commit()
        db.refresh(personne)
        return jsonify({"id": personne.id, "message": "Personne créée avec succès"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

# ============================================================
# API ROUTES - SITES
# ============================================================

@app.route('/api/sites', methods=['GET'])
def get_sites():
    """Récupère tous les sites"""
    db: Session = next(get_db())
    try:
        sites = db.query(Site).filter(Site.actif == True).all()
        return jsonify([{
            "id": s.id,
            "code": s.code,
            "nom": s.nom,
            "type_site": s.type_site,
            "centre_analytique": s.centre_analytique.value if s.centre_analytique else None,
            "actif": s.actif
        } for s in sites])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/sites', methods=['POST'])
def create_site():
    """Crée un nouveau site"""
    db: Session = next(get_db())
    try:
        data = request.get_json()
        site = Site(
            code=data.get('code'),
            nom=data.get('nom'),
            type_site=data.get('type_site'),
            centre_analytique=CentreAnalytique(data.get('centre_analytique')),
            actif=data.get('actif', True)
        )
        db.add(site)
        db.commit()
        db.refresh(site)
        return jsonify({"id": site.id, "message": "Site créé avec succès"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

# ============================================================
# API ROUTES - PLANNING
# ============================================================

@app.route('/api/planning', methods=['GET'])
def get_planning():
    """Récupère le planning"""
    db: Session = next(get_db())
    try:
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')
        site_id = request.args.get('site_id', type=int)
        
        query = db.query(PlanningJour)
        if site_id:
            query = query.filter(PlanningJour.site_id == site_id)
        if date_debut:
            query = query.filter(PlanningJour.date_jour >= datetime.strptime(date_debut, '%Y-%m-%d').date())
        if date_fin:
            query = query.filter(PlanningJour.date_jour <= datetime.strptime(date_fin, '%Y-%m-%d').date())
        
        planning = query.all()
        return jsonify([{
            "id": p.id,
            "date_jour": p.date_jour.isoformat() if p.date_jour else None,
            "site_id": p.site_id,
            "statut": p.statut.value if p.statut else None
        } for p in planning])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/planning', methods=['POST'])
def create_planning():
    """Crée une nouvelle entrée de planning"""
    db: Session = next(get_db())
    try:
        data = request.get_json()
        planning = PlanningJour(
            date_jour=datetime.strptime(data.get('date_jour'), '%Y-%m-%d').date(),
            site_id=data.get('site_id'),
            statut=StatutPlanning(data.get('statut', 'BROUILLON'))
        )
        db.add(planning)
        db.commit()
        db.refresh(planning)
        return jsonify({"id": planning.id, "message": "Planning créé avec succès"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

# ============================================================
# API ROUTES - AFFECTATIONS ÉQUIPEMENTS
# ============================================================

@app.route('/api/affectations', methods=['GET'])
def get_affectations():
    """Récupère toutes les affectations d'équipements"""
    db: Session = next(get_db())
    try:
        affectations = db.query(AffectationEquipement).all()
        return jsonify([{
            "id": a.id,
            "date_jour": a.date_jour.isoformat() if a.date_jour else None,
            "equipement_id": a.equipement_id,
            "site_id": a.site_id,
            "bloc_jour": a.bloc_jour,
            "operateur_id": a.operateur_id,
            "heure_jour": float(a.heure_jour) if a.heure_jour else 0
        } for a in affectations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route('/api/affectations', methods=['POST'])
def create_affectation():
    """Crée une nouvelle affectation d'équipement"""
    db: Session = next(get_db())
    try:
        data = request.get_json()
        affectation = AffectationEquipement(
            date_jour=datetime.strptime(data.get('date_jour'), '%Y-%m-%d').date(),
            equipement_id=data.get('equipement_id'),
            site_id=data.get('site_id'),
            bloc_jour=data.get('bloc_jour', 1),
            operateur_id=data.get('operateur_id'),
            activite_id=data.get('activite_id'),
            motif_jour_code=data.get('motif_jour_code'),
            heure_jour=data.get('heure_jour', 0),
            km_effectue=data.get('km_effectue', 0),
            carburant_litres=data.get('carburant_litres', 0)
        )
        db.add(affectation)
        db.commit()
        db.refresh(affectation)
        return jsonify({"id": affectation.id, "message": "Affectation créée avec succès"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

# ============================================================
# ROUTE DE SANTÉ / HEALTH CHECK
# ============================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérifie l'état de l'API et de la base de données"""
    db: Session = next(get_db())
    try:
        # Test de connexion à la base de données
        db.execute("SELECT 1")
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 503
    finally:
        db.close()

if __name__ == '__main__':
    # Décommenter la ligne ci-dessous si vous voulez créer les tables au démarrage
    # init_db() 
    app.run(debug=True, host='0.0.0.0', port=5000)
