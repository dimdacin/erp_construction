import { projetsData, clientsData, facturesData, equipementsData, formatStatus } from '../utils/data';
import './Dashboard.css';

function Dashboard() {
  // Calcul des statistiques
  const projetsEnCours = projetsData.filter(p => p.statut === 'en_cours').length;
  const chiffreAffaires = facturesData
    .filter(f => f.statut === 'payee')
    .reduce((sum, f) => sum + f.montantTTC, 0);
  const facturesEnAttente = facturesData.filter(f => f.statut === 'envoyee' || f.statut === 'en_retard').length;
  const equipementsDisponibles = equipementsData.filter(e => e.statut === 'disponible').length;

  const formatMontant = (montant: number): string => {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(montant);
  };

  return (
    <div className="dashboard">
      <h1>Tableau de bord</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📁</div>
          <div className="stat-content">
            <div className="stat-value">{projetsData.length}</div>
            <div className="stat-label">Projets totaux</div>
          </div>
        </div>
        
        <div className="stat-card highlight">
          <div className="stat-icon">🚧</div>
          <div className="stat-content">
            <div className="stat-value">{projetsEnCours}</div>
            <div className="stat-label">Projets en cours</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <div className="stat-value">{clientsData.length}</div>
            <div className="stat-label">Clients</div>
          </div>
        </div>
        
        <div className="stat-card success">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <div className="stat-value">{formatMontant(chiffreAffaires)}</div>
            <div className="stat-label">Chiffre d'affaires</div>
          </div>
        </div>
        
        <div className="stat-card warning">
          <div className="stat-icon">📄</div>
          <div className="stat-content">
            <div className="stat-value">{facturesEnAttente}</div>
            <div className="stat-label">Factures en attente</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🔧</div>
          <div className="stat-content">
            <div className="stat-value">{equipementsDisponibles}</div>
            <div className="stat-label">Équipements disponibles</div>
          </div>
        </div>
      </div>

      <div className="dashboard-sections">
        <section className="dashboard-section">
          <h2>📁 Projets récents</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Projet</th>
                  <th>Statut</th>
                  <th>Budget</th>
                  <th>Progression</th>
                </tr>
              </thead>
              <tbody>
                {projetsData.slice(0, 5).map(projet => (
                  <tr key={projet.id}>
                    <td>{projet.nom}</td>
                    <td>
                      <span className={`status-badge status-${projet.statut}`}>
                        {formatStatus(projet.statut)}
                      </span>
                    </td>
                    <td>{formatMontant(projet.budget)}</td>
                    <td>
                      <div className="progress-bar">
                        <div 
                          className="progress-fill" 
                          style={{ width: `${Math.min(100, (projet.depenses / projet.budget) * 100)}%` }}
                        ></div>
                      </div>
                      <span className="progress-text">
                        {Math.round((projet.depenses / projet.budget) * 100)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="dashboard-section">
          <h2>📄 Factures récentes</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Numéro</th>
                  <th>Montant TTC</th>
                  <th>Échéance</th>
                  <th>Statut</th>
                </tr>
              </thead>
              <tbody>
                {facturesData.slice(0, 5).map(facture => (
                  <tr key={facture.id}>
                    <td>{facture.numero}</td>
                    <td>{formatMontant(facture.montantTTC)}</td>
                    <td>{new Date(facture.dateEcheance).toLocaleDateString('fr-FR')}</td>
                    <td>
                      <span className={`status-badge status-${facture.statut}`}>
                        {formatStatus(facture.statut)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Dashboard;
