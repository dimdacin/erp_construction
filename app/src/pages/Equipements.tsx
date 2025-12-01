import { equipementsData } from '../utils/data';
import './Equipements.css';

function Equipements() {
  const formatMontant = (montant: number): string => {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(montant);
  };

  const formatDate = (date: string): string => {
    return new Date(date).toLocaleDateString('fr-FR');
  };

  const getStatusLabel = (statut: string): string => {
    const labels: Record<string, string> = {
      'disponible': 'Disponible',
      'en_utilisation': 'En utilisation',
      'en_maintenance': 'En maintenance',
      'hors_service': 'Hors service',
    };
    return labels[statut] || statut;
  };

  const categories = [...new Set(equipementsData.map(e => e.categorie))];
  const totalValeur = equipementsData.reduce((sum, e) => sum + (e.prixAchat * e.quantite), 0);

  return (
    <div className="equipements-page">
      <div className="page-header">
        <h1>🔧 Gestion des Équipements</h1>
        <button className="btn-primary">+ Nouvel équipement</button>
      </div>

      <div className="equipements-summary">
        <div className="summary-stat">
          <div className="summary-stat-icon">📦</div>
          <div className="summary-stat-content">
            <span className="summary-stat-value">{equipementsData.length}</span>
            <span className="summary-stat-label">Types d'équipements</span>
          </div>
        </div>
        <div className="summary-stat">
          <div className="summary-stat-icon">🔢</div>
          <div className="summary-stat-content">
            <span className="summary-stat-value">{equipementsData.reduce((sum, e) => sum + e.quantite, 0)}</span>
            <span className="summary-stat-label">Quantité totale</span>
          </div>
        </div>
        <div className="summary-stat success">
          <div className="summary-stat-icon">✅</div>
          <div className="summary-stat-content">
            <span className="summary-stat-value">{equipementsData.filter(e => e.statut === 'disponible').length}</span>
            <span className="summary-stat-label">Disponibles</span>
          </div>
        </div>
        <div className="summary-stat">
          <div className="summary-stat-icon">💰</div>
          <div className="summary-stat-content">
            <span className="summary-stat-value">{formatMontant(totalValeur)}</span>
            <span className="summary-stat-label">Valeur du parc</span>
          </div>
        </div>
      </div>

      <div className="equipements-filters">
        <div className="filter-group">
          <label>Catégorie:</label>
          <select>
            <option value="">Toutes</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label>Statut:</label>
          <select>
            <option value="">Tous</option>
            <option value="disponible">Disponible</option>
            <option value="en_utilisation">En utilisation</option>
            <option value="en_maintenance">En maintenance</option>
            <option value="hors_service">Hors service</option>
          </select>
        </div>
      </div>

      <div className="equipements-grid">
        {equipementsData.map(equipement => (
          <div key={equipement.id} className={`equipement-card status-${equipement.statut}`}>
            <div className="equipement-header">
              <span className="equipement-categorie">{equipement.categorie}</span>
              <span className={`status-dot status-dot-${equipement.statut}`}></span>
            </div>
            
            <h3 className="equipement-nom">{equipement.nom}</h3>
            <p className="equipement-description">{equipement.description}</p>

            <div className="equipement-details">
              <div className="detail">
                <span className="detail-label">Quantité</span>
                <span className="detail-value">{equipement.quantite}</span>
              </div>
              <div className="detail">
                <span className="detail-label">Prix d'achat</span>
                <span className="detail-value">{formatMontant(equipement.prixAchat)}</span>
              </div>
              <div className="detail">
                <span className="detail-label">Date d'achat</span>
                <span className="detail-value">{formatDate(equipement.dateAchat)}</span>
              </div>
            </div>

            <div className="equipement-footer">
              <span className={`status-badge status-badge-${equipement.statut}`}>
                {getStatusLabel(equipement.statut)}
              </span>
              <div className="equipement-actions">
                <button className="btn-icon-small" title="Modifier">✏️</button>
                <button className="btn-icon-small" title="Maintenance">🔧</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Equipements;
