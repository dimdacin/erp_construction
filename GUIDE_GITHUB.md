# 📦 Guide de Sauvegarde et Publication sur GitHub

## 🎯 Ce qui est prêt à être sauvegardé

Votre projet ERP Construction est maintenant prêt avec :
- ✅ 4 modules principaux fonctionnels
- ✅ Application web complète
- ✅ API REST CRUD
- ✅ Base de données avec données réelles
- ✅ Documentation complète
- ✅ Fichiers de configuration

## 📋 Étapes pour GitHub

### 1. Initialiser le dépôt Git local

```bash
# Se positionner dans le projet
cd C:\Users\user\Desktop\erp_construction

# Initialiser Git (si pas déjà fait)
git init

# Configurer votre identité
git config user.name "Votre Nom"
git config user.email "votre.email@example.com"
```

### 2. Ajouter tous les fichiers au dépôt

```bash
# Ajouter tous les fichiers
git add .

# Vérifier les fichiers ajoutés
git status

# Créer le premier commit
git commit -m "🚀 Initial commit - ERP Construction v1.0

- 4 modules fonctionnels : Dashboard, Sites, Equipements, Personnel
- Application web complète avec authentification
- API REST CRUD complète
- Base de données PostgreSQL
- 16 sites, 133 équipements, 165 salariés
- Documentation complète"
```

### 3. Créer un dépôt sur GitHub

**Option A : Via l'interface web GitHub**
1. Allez sur https://github.com
2. Connectez-vous à votre compte
3. Cliquez sur le bouton "+" en haut à droite
4. Sélectionnez "New repository"
5. Nom du dépôt : `erp-construction`
6. Description : "Application web de gestion de chantiers, équipements et personnel"
7. **Ne cochez PAS** "Initialize with README" (vous avez déjà un README)
8. Cliquez sur "Create repository"

**Option B : Via GitHub CLI** (si installé)
```bash
gh repo create erp-construction --public --source=. --remote=origin
```

### 4. Lier votre dépôt local à GitHub

```bash
# Remplacez USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/USERNAME/erp-construction.git

# Vérifier la connexion
git remote -v
```

### 5. Pousser le code vers GitHub

```bash
# Pousser la branche main
git branch -M main
git push -u origin main
```

### 6. (Optionnel) Créer des branches pour les fonctionnalités futures

```bash
# Créer une branche de développement
git checkout -b develop

# Pousser la branche develop
git push -u origin develop

# Revenir à main
git checkout main
```

## 🔒 Fichiers Sensibles à NE PAS Publier

Le fichier `.gitignore` est déjà configuré pour exclure :
- ❌ `venv/` - Environnement virtuel
- ❌ `.env` - Variables d'environnement (mots de passe, etc.)
- ❌ `__pycache__/` - Fichiers Python compilés
- ❌ `*.pyc`, `*.pyo` - Bytecode Python
- ❌ `.vscode/`, `.idea/` - Configuration IDE

**⚠️ IMPORTANT** : Vérifiez que votre fichier `.env` contient bien les informations sensibles et n'est PAS dans Git :

```bash
# Vérifier que .env est bien ignoré
git check-ignore .env
# Doit retourner : .env
```

## 💾 Sauvegarde Locale

### Créer une archive complète du projet

**Windows PowerShell :**
```powershell
# Créer une archive ZIP
$date = Get-Date -Format "yyyy-MM-dd"
Compress-Archive -Path C:\Users\user\Desktop\erp_construction -DestinationPath "C:\Users\user\Desktop\erp_construction_backup_$date.zip" -Force
```

**Ou manuellement :**
1. Clic droit sur le dossier `erp_construction`
2. "Envoyer vers" → "Dossier compressé"
3. Nommer : `erp_construction_backup_2025-12-03.zip`
4. Sauvegarder sur un disque externe ou cloud

### Sauvegarder la base de données

```bash
# Export de la base de données PostgreSQL
pg_dump -U postgres -d erp_construction > backup_db_2025-12-03.sql

# Ou avec toutes les options
pg_dump -U postgres -h localhost -p 5432 -d erp_construction -F c -b -v -f "C:\Users\user\Desktop\erp_backup.dump"
```

## 🔄 Commandes Git Utiles pour l'Avenir

### Sauvegarder les modifications
```bash
# Voir les fichiers modifiés
git status

# Ajouter des fichiers spécifiques
git add nom_fichier.py

# Ou ajouter tous les fichiers modifiés
git add .

# Créer un commit
git commit -m "Description des modifications"

# Pousser vers GitHub
git push
```

### Récupérer le projet sur un autre PC
```bash
# Cloner le dépôt
git clone https://github.com/USERNAME/erp-construction.git
cd erp-construction

# Créer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt

# Configurer .env avec vos informations
# Initialiser la base de données
python reset_db.py
```

## 📊 Structure à Publier

```
erp_construction/
├── .gitignore                    ✅ Inclus
├── README.md                     ✅ Inclus (nouveau)
├── requirements.txt              ✅ Inclus (nouveau)
├── GUIDE_GITHUB.md              ✅ Inclus (ce fichier)
├── COMMENT_DEMARRER.txt         ✅ Inclus
├── README_WEB.md                ✅ Inclus
├── README_API.md                ✅ Inclus
├── AMELIORATIONS_APPORTEES.md   ✅ Inclus
├── main_web.py                   ✅ Inclus
├── api_routes.py                 ✅ Inclus
├── models.py                     ✅ Inclus
├── schemas.py                    ✅ Inclus
├── database.py                   ✅ Inclus
├── crud_*.py                     ✅ Inclus
├── start_web.py                  ✅ Inclus
├── reset_db.py                   ✅ Inclus
├── init_db.py                    ✅ Inclus
├── templates/                    ✅ Inclus
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── sites.html
│   ├── equipements.html
│   └── personnel.html
├── static/                       ✅ Inclus
│   └── css/
│       └── style.css
├── venv/                         ❌ Exclu (.gitignore)
├── .env                          ❌ Exclu (.gitignore)
└── __pycache__/                  ❌ Exclu (.gitignore)
```

## ✅ Checklist avant de Pousser

- [ ] Fichier `.gitignore` créé
- [ ] Fichier `.env` dans `.gitignore`
- [ ] `README.md` à jour
- [ ] `requirements.txt` créé
- [ ] Code testé et fonctionnel
- [ ] Documentation complète
- [ ] Aucune donnée sensible (mots de passe, clés API)
- [ ] `git status` vérifié
- [ ] Premier commit créé
- [ ] Remote GitHub configuré

## 🎓 Résumé - Commandes Complètes

```bash
# 1. Initialisation
cd C:\Users\user\Desktop\erp_construction
git init
git config user.name "Votre Nom"
git config user.email "votre@email.com"

# 2. Premier commit
git add .
git commit -m "🚀 Initial commit - ERP Construction v1.0"

# 3. Créer et lier le dépôt GitHub (via web d'abord)
git remote add origin https://github.com/USERNAME/erp-construction.git

# 4. Pousser vers GitHub
git branch -M main
git push -u origin main
```

## 🆘 En cas de problème

### Erreur : "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/erp-construction.git
```

### Erreur : Authentification GitHub
```bash
# Utiliser un token d'accès personnel (PAT)
# 1. Allez sur GitHub.com → Settings → Developer settings → Personal access tokens
# 2. Générez un nouveau token
# 3. Utilisez-le comme mot de passe lors du push
```

### Fichier trop volumineux
```bash
# GitHub limite les fichiers à 100 MB
# Vérifier les gros fichiers
git ls-files --stage | awk '$2 > 100000000'

# Ajouter les gros fichiers à .gitignore
```

---

**Votre projet est maintenant prêt à être sauvegardé et partagé ! 🚀**

