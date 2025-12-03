# 🏗️ ERP Construction - Application de Gestion de Chantiers

Application web complète pour la gestion des chantiers, équipements et personnel dans le secteur de la construction.

## 📋 Fonctionnalités Principales

### ✅ 4 Modules Opérationnels

1. **🏠 Dashboard / Tableau de bord**
   - Vue d'ensemble des statistiques
   - Accès rapide aux modules principaux
   - Indicateurs clés : Sites, Équipements, Personnel

2. **🏗️ Sites & Chantiers** (CRUD Complet)
   - Liste complète des sites/chantiers/usines/centres administratifs
   - Ajout de nouveaux sites
   - Modification des sites existants
   - Désactivation de sites
   - Filtres : par type (CHANTIER, USINE, DEPOT, ADMIN) et statut
   - Recherche dynamique

3. **🚜 Équipements** (Liste + Gestion des Dépenses)
   - Liste complète des 133 équipements
   - Recherche par code équipement
   - Recherche par immatriculation
   - Filtre par catégorie (Autogredere, Compactoare, Excavatoare, etc.)
   - **Saisie des dépenses/interventions** (maintenance, réparations, etc.)
   - Bouton rapide de saisie par équipement

4. **👥 Personnel / Salariés**
   - Liste complète des 165 salariés
   - Recherche multi-critères
   - Filtre par division
   - Filtre par statut (actif/inactif)
   - Affichage des informations : secteur, division, service, fonction, salaire

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+
- PostgreSQL
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le dépôt**
```bash
git clone [URL_DU_REPO]
cd erp_construction
```

2. **Créer l'environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
- Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```
- Windows CMD:
```cmd
venv\Scripts\activate.bat
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configurer la base de données**
- Créer un fichier `.env` à la racine du projet
```env
DATABASE_URL=postgresql://user:password@localhost:5432/erp_construction
```

6. **Initialiser la base de données**
```bash
python reset_db.py
```

7. **Importer les données initiales**
```bash
curl -X POST http://localhost:8000/import/equipements
curl -X POST http://localhost:8000/import/depenses
curl -X POST http://localhost:8000/import/personnel
curl -X POST http://localhost:8000/import/sites
```

### Démarrage de l'application

**Méthode recommandée :**
```bash
python start_web.py
```

**Ou avec uvicorn directement :**
```bash
uvicorn main_web:app --reload --host 0.0.0.0 --port 8000
```

**Accès à l'application :**
- URL : http://localhost:8000
- Identifiants de test :
  - Admin : `admin` / `admin123`
  - User : `user` / `user123`

## 📊 Données Actuelles

- **16 Sites** (9 chantiers, 4 usines, 2 centres admin, 1 dépôt)
- **133 Équipements** (grues, pelleteuses, camions, compacteurs, etc.)
- **165 Salariés** répartis en 7 divisions
- **1200+ Dépenses/Interventions** historiques

## 🎯 Architecture Technique

### Backend
- **Framework** : FastAPI
- **ORM** : SQLAlchemy
- **Base de données** : PostgreSQL
- **Serveur ASGI** : Uvicorn

### Frontend
- **Templates** : Jinja2
- **CSS Framework** : Bootstrap 5
- **JavaScript** : jQuery + AJAX
- **Icons** : Font Awesome 6

### Structure du Projet
```
erp_construction/
├── main_web.py              # Application web principale
├── api_routes.py            # Routes API REST CRUD
├── models.py                # Modèles SQLAlchemy
├── schemas.py               # Schémas Pydantic
├── database.py              # Configuration BDD
├── crud_*.py                # Fonctions CRUD métier
├── templates/               # Templates HTML
│   ├── base.html           # Template de base
│   ├── login.html          # Page de connexion
│   ├── dashboard.html      # Tableau de bord
│   ├── sites.html          # Gestion sites/chantiers
│   ├── equipements.html    # Gestion équipements
│   └── personnel.html      # Gestion personnel
├── static/                 # Fichiers statiques
│   └── css/
│       └── style.css       # Styles personnalisés
└── requirements.txt        # Dépendances Python
```

## 🔌 API REST

Toutes les routes API sont accessibles via `/api/` :

### Sites
- `GET /api/sites` - Liste tous les sites
- `GET /api/sites/{id}` - Détails d'un site
- `POST /api/sites` - Créer un site
- `PUT /api/sites/{id}` - Modifier un site
- `DELETE /api/sites/{id}` - Désactiver un site

### Équipements
- `GET /api/equipements` - Liste tous les équipements
- `GET /api/equipements/{id}` - Détails d'un équipement
- `POST /api/equipements` - Créer un équipement
- `PUT /api/equipements/{id}` - Modifier un équipement
- `DELETE /api/equipements/{id}` - Désactiver un équipement

### Personnel
- `GET /api/personnel` - Liste tous les salariés
- `GET /api/personnel/{id}` - Détails d'un salarié
- `POST /api/personnel` - Créer un salarié
- `PUT /api/personnel/{id}` - Modifier un salarié
- `DELETE /api/personnel/{id}` - Désactiver un salarié

### Dépenses
- `GET /api/depenses` - Liste toutes les dépenses
- `POST /api/depenses` - Créer une dépense

## 📖 Documentation

- **Guide de démarrage** : `COMMENT_DEMARRER.txt`
- **Documentation web** : `README_WEB.md`
- **Documentation API** : `README_API.md`
- **Améliorations récentes** : `AMELIORATIONS_APPORTEES.md`

## 🛠️ Développement

### Arrêter le serveur
```powershell
Stop-Process -Name python -Force
```

### Réinitialiser la base de données
```bash
python reset_db.py
```

### Créer une migration
```bash
# À implémenter avec Alembic (voir setup_alembic.md)
```

## 🚧 Fonctionnalités à Venir

- [ ] Module d'affectations journalières (équipement + opérateur + chantier)
- [ ] Tableaux de bord avec graphiques
- [ ] Rapports et exports Excel/PDF
- [ ] Gestion avancée des utilisateurs et permissions
- [ ] Module de suivi des coûts par chantier
- [ ] Alertes de maintenance préventive

## 📝 Licence

Projet propriétaire - Tous droits réservés

## 👤 Auteur

Développé pour la gestion de chantiers et équipements de construction

## 📞 Support

Pour toute question ou assistance, référez-vous à la documentation dans le dossier du projet.

---

**Version** : 1.0.0  
**Date** : Décembre 2025  
**Statut** : ✅ Opérationnel - 4 modules principaux fonctionnels
