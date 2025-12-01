// Types pour l'ERP Construction

export interface Client {
  id: string;
  nom: string;
  prenom: string;
  email: string;
  telephone: string;
  adresse: string;
  ville: string;
  codePostal: string;
  dateCreation: string;
}

export interface Projet {
  id: string;
  nom: string;
  description: string;
  clientId: string;
  adresse: string;
  dateDebut: string;
  dateFin: string | null;
  statut: 'en_attente' | 'en_cours' | 'termine' | 'annule';
  budget: number;
  depenses: number;
}

export interface Facture {
  id: string;
  numero: string;
  clientId: string;
  projetId: string;
  dateEmission: string;
  dateEcheance: string;
  montantHT: number;
  tva: number;
  montantTTC: number;
  statut: 'brouillon' | 'envoyee' | 'payee' | 'en_retard';
  lignes: LigneFacture[];
}

export interface LigneFacture {
  id: string;
  description: string;
  quantite: number;
  prixUnitaire: number;
  montant: number;
}

export interface Equipement {
  id: string;
  nom: string;
  description: string;
  categorie: string;
  quantite: number;
  prixAchat: number;
  dateAchat: string;
  statut: 'disponible' | 'en_utilisation' | 'en_maintenance' | 'hors_service';
}

export interface StatsDashboard {
  nombreProjets: number;
  projetsEnCours: number;
  nombreClients: number;
  chiffreAffaires: number;
  facturesEnAttente: number;
  equipementsActifs: number;
}
