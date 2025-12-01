# ERP Construction

Application web de gestion d'entreprise (ERP) pour le secteur du bâtiment et de la construction.

## Fonctionnalités

- **Tableau de bord** : Vue d'ensemble de l'activité avec statistiques clés
- **Gestion des Projets** : Suivi des chantiers, budget et avancement
- **Gestion des Clients** : Base de données clients avec historique
- **Facturation** : Création et suivi des factures
- **Gestion des Équipements** : Inventaire du matériel et outillage

## Technologies

- React 19 avec TypeScript
- Vite (build tool)
- React Router (navigation)

## Installation

```bash
cd app
npm install
npm run dev
```

## Développement

L'application sera accessible sur `http://localhost:5173`

## Structure du projet

```
app/
├── src/
│   ├── components/    # Composants réutilisables
│   ├── pages/         # Pages de l'application
│   ├── types/         # Définitions TypeScript
│   ├── utils/         # Utilitaires et données
│   ├── App.tsx        # Composant principal
│   └── main.tsx       # Point d'entrée
└── package.json
```
