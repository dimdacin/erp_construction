import { projetsData, getClientNom } from '../utils/data';
import './Projets.css';

function Projets() {
  const formatMontant = (montant: number): string => {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(montant);
  };

  const formatDate = (date: string | null): string => {
    if (!date) return '-';
    return new Date(date).toLocaleDateString('fr-FR');
  };

  return (
    <div className="projets-page">
      <div className="page-header">
        <h1>📁 Gestion des Projets</h1>
        <button className="btn-primary">+ Nouveau projet</button>
      </div>

      <div className="projets-summary">
        <div className="summary-card">
          <span className="summary-value">{projetsData.length}</span>
          <span className="summary-label">Total</span>
        </div>
        <div className="summary-card">
          <span className="summary-value">{projetsData.filter(p => p.statut === 'en_attente').length}</span>
          <span className="summary-label">En attente</span>
        </div>
        <div className="summary-card active">
          <span className="summary-value">{projetsData.filter(p => p.statut === 'en_cours').length}</span>
          <span className="summary-label">En cours</span>
        </div>
        <div className="summary-card success">
          <span className="summary-value">{projetsData.filter(p => p.statut === 'termine').length}</span>
          <span className="summary-label">Terminés</span>
        </div>
      </div>

      <div className="projets-grid">
        {projetsData.map(projet => (
          <div key={projet.id} className="projet-card">
            <div className="projet-header">
              <h3>{projet.nom}</h3>
              <span className={`status-badge status-${projet.statut}`}>
                {projet.statut.replace('_', ' ')}
              </span>
            </div>
            
            <p className="projet-description">{projet.description}</p>
            
            <div className="projet-details">
              <div className="detail-row">
                <span className="detail-label">👤 Client:</span>
                <span className="detail-value">{getClientNom(projet.clientId)}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">📍 Adresse:</span>
                <span className="detail-value">{projet.adresse}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">📅 Début:</span>
                <span className="detail-value">{formatDate(projet.dateDebut)}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">📅 Fin:</span>
                <span className="detail-value">{formatDate(projet.dateFin)}</span>
              </div>
            </div>

            <div className="projet-budget">
              <div className="budget-header">
                <span>Budget: {formatMontant(projet.budget)}</span>
                <span>Dépensé: {formatMontant(projet.depenses)}</span>
              </div>
              <div className="progress-bar-large">
                <div 
                  className={`progress-fill ${projet.depenses > projet.budget ? 'over-budget' : ''}`}
                  style={{ width: `${Math.min(100, (projet.depenses / projet.budget) * 100)}%` }}
                ></div>
              </div>
              <div className="budget-footer">
                <span className={projet.depenses > projet.budget ? 'over-budget-text' : ''}>
                  {projet.depenses > projet.budget ? 'Dépassement: ' : 'Reste: '}
                  {formatMontant(Math.abs(projet.budget - projet.depenses))}
                </span>
              </div>
            </div>

            <div className="projet-actions">
              <button className="btn-secondary">Voir détails</button>
              <button className="btn-icon">✏️</button>
              <button className="btn-icon danger">🗑️</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Projets;
