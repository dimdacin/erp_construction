import type { Client, Projet, Facture, Equipement } from '../types';

// Données de démonstration pour l'ERP Construction

export const clientsData: Client[] = [
  {
    id: '1',
    nom: 'Martin',
    prenom: 'Jean',
    email: 'jean.martin@email.com',
    telephone: '06 12 34 56 78',
    adresse: '15 rue de la Paix',
    ville: 'Paris',
    codePostal: '75001',
    dateCreation: '2024-01-15',
  },
  {
    id: '2',
    nom: 'Dupont',
    prenom: 'Marie',
    email: 'marie.dupont@email.com',
    telephone: '06 98 76 54 32',
    adresse: '42 avenue Victor Hugo',
    ville: 'Lyon',
    codePostal: '69002',
    dateCreation: '2024-02-20',
  },
  {
    id: '3',
    nom: 'Bernard',
    prenom: 'Pierre',
    email: 'pierre.bernard@email.com',
    telephone: '06 45 67 89 01',
    adresse: '8 boulevard Gambetta',
    ville: 'Marseille',
    codePostal: '13001',
    dateCreation: '2024-03-10',
  },
];

export const projetsData: Projet[] = [
  {
    id: '1',
    nom: 'Rénovation Appartement Martin',
    description: 'Rénovation complète d\'un appartement de 80m²',
    clientId: '1',
    adresse: '15 rue de la Paix, 75001 Paris',
    dateDebut: '2024-06-01',
    dateFin: null,
    statut: 'en_cours',
    budget: 45000,
    depenses: 28000,
  },
  {
    id: '2',
    nom: 'Construction Maison Dupont',
    description: 'Construction d\'une maison individuelle de 120m²',
    clientId: '2',
    adresse: '42 avenue Victor Hugo, 69002 Lyon',
    dateDebut: '2024-04-15',
    dateFin: '2024-11-30',
    statut: 'termine',
    budget: 250000,
    depenses: 245000,
  },
  {
    id: '3',
    nom: 'Extension Garage Bernard',
    description: 'Extension d\'un garage existant + création atelier',
    clientId: '3',
    adresse: '8 boulevard Gambetta, 13001 Marseille',
    dateDebut: '2024-08-01',
    dateFin: null,
    statut: 'en_attente',
    budget: 35000,
    depenses: 0,
  },
];

export const facturesData: Facture[] = [
  {
    id: '1',
    numero: 'FAC-2024-001',
    clientId: '1',
    projetId: '1',
    dateEmission: '2024-06-15',
    dateEcheance: '2024-07-15',
    montantHT: 15000,
    tva: 3000,
    montantTTC: 18000,
    statut: 'payee',
    lignes: [
      { id: '1', description: 'Démolition et évacuation', quantite: 1, prixUnitaire: 5000, montant: 5000 },
      { id: '2', description: 'Plâtrerie', quantite: 40, prixUnitaire: 150, montant: 6000 },
      { id: '3', description: 'Électricité', quantite: 1, prixUnitaire: 4000, montant: 4000 },
    ],
  },
  {
    id: '2',
    numero: 'FAC-2024-002',
    clientId: '2',
    projetId: '2',
    dateEmission: '2024-11-30',
    dateEcheance: '2024-12-30',
    montantHT: 125000,
    tva: 25000,
    montantTTC: 150000,
    statut: 'envoyee',
    lignes: [
      { id: '1', description: 'Gros œuvre', quantite: 1, prixUnitaire: 80000, montant: 80000 },
      { id: '2', description: 'Second œuvre', quantite: 1, prixUnitaire: 45000, montant: 45000 },
    ],
  },
  {
    id: '3',
    numero: 'FAC-2024-003',
    clientId: '1',
    projetId: '1',
    dateEmission: '2024-09-01',
    dateEcheance: '2024-10-01',
    montantHT: 10000,
    tva: 2000,
    montantTTC: 12000,
    statut: 'en_retard',
    lignes: [
      { id: '1', description: 'Carrelage salle de bain', quantite: 15, prixUnitaire: 400, montant: 6000 },
      { id: '2', description: 'Plomberie', quantite: 1, prixUnitaire: 4000, montant: 4000 },
    ],
  },
];

export const equipementsData: Equipement[] = [
  {
    id: '1',
    nom: 'Bétonnière 350L',
    description: 'Bétonnière électrique grande capacité',
    categorie: 'Gros matériel',
    quantite: 2,
    prixAchat: 1500,
    dateAchat: '2023-03-15',
    statut: 'disponible',
  },
  {
    id: '2',
    nom: 'Échafaudage mobile',
    description: 'Échafaudage aluminium 6m',
    categorie: 'Sécurité',
    quantite: 3,
    prixAchat: 2500,
    dateAchat: '2023-06-20',
    statut: 'en_utilisation',
  },
  {
    id: '3',
    nom: 'Perceuse Hilti',
    description: 'Perceuse-visseuse sans fil professionnelle',
    categorie: 'Outillage électrique',
    quantite: 5,
    prixAchat: 450,
    dateAchat: '2024-01-10',
    statut: 'disponible',
  },
  {
    id: '4',
    nom: 'Compresseur 100L',
    description: 'Compresseur d\'air 100 litres',
    categorie: 'Gros matériel',
    quantite: 1,
    prixAchat: 800,
    dateAchat: '2023-09-05',
    statut: 'en_maintenance',
  },
  {
    id: '5',
    nom: 'Niveau laser',
    description: 'Niveau laser rotatif professionnel',
    categorie: 'Mesure',
    quantite: 2,
    prixAchat: 350,
    dateAchat: '2024-02-28',
    statut: 'disponible',
  },
];

// Fonction utilitaire pour obtenir le nom complet d'un client
export function getClientNom(clientId: string): string {
  const client = clientsData.find(c => c.id === clientId);
  return client ? `${client.prenom} ${client.nom}` : 'Client inconnu';
}

// Fonction utilitaire pour obtenir le nom d'un projet
export function getProjetNom(projetId: string): string {
  const projet = projetsData.find(p => p.id === projetId);
  return projet ? projet.nom : 'Projet inconnu';
}

// Fonction utilitaire pour formater un statut (remplace les underscores par des espaces)
export function formatStatus(status: string): string {
  return status.replace(/_/g, ' ');
}
