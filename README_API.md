# Documentation API - ERP Construction

## 🔧 Réinitialisation de la Base de Données

### Méthode 1 : Script Python
```bash
python reset_db.py
```

Ce script va :
- ⚠️ **Supprimer toutes les tables existantes** (ATTENTION : perte de données)
- ✅ Recréer toutes les tables selon les modèles définis
- 📋 Afficher la liste des tables créées

### Méthode 2 : Via Python directement
```python
from reset_db import reset_database
reset_database(drop_all=True, create_all=True)
```

### Méthode 3 : Via app.py
Décommentez la ligne `init_db()` dans `app.py` et lancez l'application.

## 📋 Problèmes Corrigés

### ✅ Problèmes identifiés et corrigés :

1. **Import manquant** : `UniqueConstraint` n'était pas importé dans `models.py`
2. **Classe manquante** : La classe `Activite` était référencée mais non définie
3. **Fichiers .txt** : Les fichiers `database.py` et `models.py` étaient en `.txt` au lieu de `.py`
4. **Routes API manquantes** : Aucune route API n'était définie
5. **Fonction init_db incomplète** : Le corps de la fonction était vide

## 🚀 Endpoints API Disponibles

### Base
- `GET /` - Page d'accueil avec liste des endpoints
- `GET /api/health` - Vérification de l'état de l'API et de la base de données

### Équipements
- `GET /api/equipements` - Liste tous les équipements actifs
- `POST /api/equipements` - Crée un nouvel équipement
- `GET /api/equipements/<id>` - Récupère un équipement par ID

### Personnes
- `GET /api/personnes` - Liste toutes les personnes actives
- `POST /api/personnes` - Crée une nouvelle personne

### Sites
- `GET /api/sites` - Liste tous les sites actifs
- `POST /api/sites` - Crée un nouveau site

### Planning
- `GET /api/planning` - Liste le planning (avec filtres optionnels : `date_debut`, `date_fin`, `site_id`)
- `POST /api/planning` - Crée une nouvelle entrée de planning

### Affectations
- `GET /api/affectations` - Liste toutes les affectations d'équipements
- `POST /api/affectations` - Crée une nouvelle affectation

## 📝 Exemples d'utilisation

### Créer un équipement
```bash
curl -X POST http://localhost:5000/api/equipements \
  -H "Content-Type: application/json" \
  -d '{
    "code": "EQ001",
    "immatriculation": "ABC-123",
    "unite_compteur": "heures",
    "usage_source": "MANUEL",
    "site_rattachement_id": 1,
    "actif": true
  }'
```

### Créer une personne
```bash
curl -X POST http://localhost:5000/api/personnes \
  -H "Content-Type: application/json" \
  -d '{
    "matricule": "EMP001",
    "nom_prenom": "Dupont Jean",
    "division_id": 1,
    "service_id": 1,
    "fonction_id": 1,
    "actif": true
  }'
```

### Créer un site
```bash
curl -X POST http://localhost:5000/api/sites \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SITE001",
    "nom": "Chantier Principal",
    "type_site": "CHANTIER",
    "centre_analytique": "CHANTIER",
    "actif": true
  }'
```

## ⚙️ Configuration

1. Copiez `.env.example` vers `.env`
2. Modifiez `DATABASE_URL` avec vos informations de connexion
3. Générez une clé secrète pour `FLASK_SECRET_KEY` en production

## 🐛 Dépannage

### Erreur : "DATABASE_URL n'est pas configurée"
- Vérifiez que le fichier `.env` existe et contient `DATABASE_URL`
- Vérifiez que `python-dotenv` est installé

### Erreur : "Table already exists"
- Utilisez `reset_db.py` pour réinitialiser la base de données
- Ou supprimez manuellement les tables dans votre base de données

### Erreur : "Foreign key constraint failed"
- Assurez-vous que les entités référencées existent (ex: Site, Personne, etc.)
- Vérifiez les IDs dans vos requêtes POST

