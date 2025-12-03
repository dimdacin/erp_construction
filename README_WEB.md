# 🎉 Application Web ERP Construction - Guide d'utilisation

## ✅ Ce qui a été créé

Vous disposez maintenant d'une **application web complète** pour gérer votre ERP Construction !

### 📦 Architecture créée

```
erp_construction/
├── main_web.py              # Application web principale avec authentification
├── api_routes.py            # Routes API REST CRUD complètes
├── schemas.py               # Schémas Pydantic mis à jour
├── start_web.py             # Script de démarrage
├── templates/               # Templates HTML
│   ├── base.html           # Template de base avec menu navigation
│   ├── login.html          # Page de connexion
│   ├── dashboard.html      # Tableau de bord
│   ├── sites.html          # Gestion des sites/chantiers (CRUD complet)
│   ├── equipements.html    # Liste des équipements
│   └── personnel.html      # Liste du personnel
└── static/                 # Fichiers statiques
    ├── css/
    │   └── style.css       # Styles personnalisés
    └── js/                 # (pour futurs scripts)
```

## 🚀 Démarrage de l'application

### Méthode 1 : Script de démarrage (recommandé)
```bash
python start_web.py
```

### Méthode 2 : Avec l'environnement virtuel
```bash
.\venv\Scripts\python.exe start_web.py
```

### Méthode 3 : Directement avec uvicorn
```bash
uvicorn main_web:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Accès à l'application

Une fois démarrée, ouvrez votre navigateur et accédez à :
```
http://localhost:8000
```

## 👤 Identifiants de connexion

**Administrateur :**
- Nom d'utilisateur : `admin`
- Mot de passe : `admin123`

**Utilisateur standard :**
- Nom d'utilisateur : `user`
- Mot de passe : `user123`

## 📋 Fonctionnalités disponibles

### 1. Tableau de bord (`/dashboard`)
- Vue d'ensemble avec statistiques
- Nombre total de sites, équipements et salariés
- Accès rapide aux différentes sections

### 2. Sites & Chantiers (`/sites`)
✅ **CRUD Complet implémenté :**
- ✅ **Voir** la liste complète des sites
- ✅ **Ajouter** un nouveau site/chantier
- ✅ **Modifier** un site existant
- ✅ **Désactiver** un site
- 🔍 **Recherche** et **filtres** par type et statut
- 📊 Affichage avec badges colorés par type/statut

#### Comment utiliser :
1. Cliquez sur "Nouveau Site" pour ajouter
2. Remplissez le formulaire (code et intitulé obligatoires)
3. Cliquez sur l'icône crayon pour modifier
4. Cliquez sur l'icône poubelle pour désactiver

### 3. Équipements (`/equipements`)
- ✅ Liste complète des 133 équipements
- ✅ Recherche dynamique
- ⏳ Ajout/Modification : interface prête, à compléter

### 4. Personnel (`/personnel`)
- ✅ Liste complète des 165 salariés
- ✅ Recherche dynamique
- ⏳ Ajout/Modification : interface prête, à compléter

## 🎯 API REST disponibles

Toutes les routes API sont accessibles via `/api/` :

### Sites
- `GET /api/sites` - Liste tous les sites
- `GET /api/sites/{id}` - Détails d'un site
- `POST /api/sites` - Créer un site
- `PUT /api/sites/{id}` - Mettre à jour un site
- `DELETE /api/sites/{id}` - Désactiver un site

### Équipements
- `GET /api/equipements` - Liste tous les équipements
- `GET /api/equipements/{id}` - Détails d'un équipement
- `POST /api/equipements` - Créer un équipement
- `PUT /api/equipements/{id}` - Mettre à jour un équipement
- `DELETE /api/equipements/{id}` - Désactiver un équipement

### Personnel
- `GET /api/personnel` - Liste tous les salariés
- `GET /api/personnel/{id}` - Détails d'un salarié
- `POST /api/personnel` - Créer un salarié
- `PUT /api/personnel/{id}` - Mettre à jour un salarié
- `DELETE /api/personnel/{id}` - Désactiver un salarié

## 📊 Données actuelles dans la base

- **16 Sites/Chantiers** (9 chantiers, 4 usines, 2 admin, 1 dépôt)
- **133 Équipements** (grues, pelleteuses, camions, etc.)
- **165 Salariés** répartis en 7 divisions
- **1202 Interventions/Dépenses** historiques
- **5 Clients** principaux

## 🔧 Personnalisation

### Modifier les identifiants de connexion
Éditez le fichier `main_web.py`, ligne 19-22 :
```python
USERS = {
    "admin": "admin123",
    "user": "user123",
    "votre_nom": "votre_mot_de_passe"
}
```

### Ajouter de nouvelles pages
1. Créez un template HTML dans `templates/`
2. Ajoutez une route dans `main_web.py`
3. Ajoutez l'entrée dans le menu de `templates/base.html`

### Personnaliser les styles
Modifiez `static/css/style.css`

## 🚧 Prochaines étapes suggérées

1. **Compléter les formulaires d'ajout/modification** pour Équipements et Personnel
   - Réutiliser la même structure que `sites.html`
   - Ajouter les modals et fonctions JavaScript

2. **Ajouter l'authentification réelle**
   - Implémenter une vraie gestion d'utilisateurs
   - Ajouter des rôles et permissions

3. **Module d'affectations journalières**
   - Créer l'interface de planning
   - Affecter équipements + opérateurs aux chantiers

4. **Rapports et tableaux de bord**
   - Graphiques de coûts par chantier
   - Suivi des maintenances
   - Indicateurs de performance

5. **Export de données**
   - Export Excel des listes
   - Génération de rapports PDF

## 💡 Conseils d'utilisation

- L'application utilise **Bootstrap 5** pour le design
- Les données sont chargées dynamiquement via **AJAX/jQuery**
- Toutes les actions (ajout, modification, suppression) sont **en temps réel**
- Les filtres et recherches fonctionnent **instantanément**

## 🐛 En cas de problème

### Le serveur ne démarre pas
```bash
# Vérifier que l'environnement virtuel est activé
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install fastapi uvicorn jinja2 python-multipart sqlalchemy psycopg2-binary pandas openpyxl
```

### Erreur de connexion à la base de données
```bash
# Vérifier que PostgreSQL est démarré
# Vérifier le fichier .env avec DATABASE_URL
```

### Page blanche ou erreur 500
```bash
# Consulter les logs du terminal
# Vérifier que tous les templates existent
```

## 📝 Notes importantes

- ⚠️ Les modifications sont **permanentes** (pas de mode test)
- 💾 Pensez à **sauvegarder** votre base régulièrement
- 🔒 En production, **changez** les mots de passe par défaut
- 📱 L'interface est **responsive** (fonctionne sur mobile)

## ✨ Félicitations !

Votre application ERP Construction est maintenant opérationnelle !
Vous pouvez voir et gérer vos sites, équipements et personnel via une interface web moderne et intuitive.

---

**Développé pour la gestion de chantiers et équipements de construction** 🏗️

