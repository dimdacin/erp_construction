import { clientsData, projetsData, facturesData } from '../utils/data';
import './Clients.css';

function Clients() {
  const getClientStats = (clientId: string) => {
    const projets = projetsData.filter(p => p.clientId === clientId);
    const factures = facturesData.filter(f => f.clientId === clientId);
    const totalFacture = factures.reduce((sum, f) => sum + f.montantTTC, 0);
    return { projets: projets.length, totalFacture };
  };

  const formatMontant = (montant: number): string => {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(montant);
  };

  return (
    <div className="clients-page">
      <div className="page-header">
        <h1>👥 Gestion des Clients</h1>
        <button className="btn-primary">+ Nouveau client</button>
      </div>

      <div className="clients-stats">
        <div className="stat-mini">
          <span className="stat-mini-value">{clientsData.length}</span>
          <span className="stat-mini-label">Clients enregistrés</span>
        </div>
        <div className="stat-mini">
          <span className="stat-mini-value">{projetsData.length}</span>
          <span className="stat-mini-label">Projets associés</span>
        </div>
      </div>

      <div className="clients-table-container">
        <table className="clients-table">
          <thead>
            <tr>
              <th>Client</th>
              <th>Email</th>
              <th>Téléphone</th>
              <th>Ville</th>
              <th>Projets</th>
              <th>Total facturé</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {clientsData.map(client => {
              const stats = getClientStats(client.id);
              return (
                <tr key={client.id}>
                  <td>
                    <div className="client-name">
                      <div className="client-avatar">
                        {client.prenom.charAt(0)}{client.nom.charAt(0)}
                      </div>
                      <div className="client-info">
                        <span className="name">{client.prenom} {client.nom}</span>
                        <span className="address">{client.adresse}</span>
                      </div>
                    </div>
                  </td>
                  <td>
                    <a href={`mailto:${client.email}`} className="email-link">{client.email}</a>
                  </td>
                  <td>{client.telephone}</td>
                  <td>{client.ville} ({client.codePostal})</td>
                  <td>
                    <span className="project-count">{stats.projets}</span>
                  </td>
                  <td className="montant">{formatMontant(stats.totalFacture)}</td>
                  <td>
                    <div className="table-actions">
                      <button className="btn-table" title="Voir détails">👁️</button>
                      <button className="btn-table" title="Modifier">✏️</button>
                      <button className="btn-table danger" title="Supprimer">🗑️</button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="clients-cards-mobile">
        {clientsData.map(client => {
          const stats = getClientStats(client.id);
          return (
            <div key={client.id} className="client-card">
              <div className="client-card-header">
                <div className="client-avatar-large">
                  {client.prenom.charAt(0)}{client.nom.charAt(0)}
                </div>
                <div className="client-card-info">
                  <h3>{client.prenom} {client.nom}</h3>
                  <p>{client.ville}</p>
                </div>
              </div>
              <div className="client-card-details">
                <p>📧 {client.email}</p>
                <p>📱 {client.telephone}</p>
                <p>📍 {client.adresse}, {client.codePostal} {client.ville}</p>
              </div>
              <div className="client-card-stats">
                <div className="card-stat">
                  <span className="value">{stats.projets}</span>
                  <span className="label">Projets</span>
                </div>
                <div className="card-stat">
                  <span className="value">{formatMontant(stats.totalFacture)}</span>
                  <span className="label">Total facturé</span>
                </div>
              </div>
              <div className="client-card-actions">
                <button className="btn-secondary">Voir profil</button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Clients;
