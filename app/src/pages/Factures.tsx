import { facturesData, getClientNom, getProjetNom, formatStatus } from '../utils/data';
import './Factures.css';

function Factures() {
  const formatMontant = (montant: number): string => {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(montant);
  };

  const formatDate = (date: string): string => {
    return new Date(date).toLocaleDateString('fr-FR');
  };

  const totalFactures = facturesData.reduce((sum, f) => sum + f.montantTTC, 0);
  const totalPayees = facturesData
    .filter(f => f.statut === 'payee')
    .reduce((sum, f) => sum + f.montantTTC, 0);
  const totalEnAttente = facturesData
    .filter(f => f.statut === 'envoyee' || f.statut === 'en_retard')
    .reduce((sum, f) => sum + f.montantTTC, 0);

  return (
    <div className="factures-page">
      <div className="page-header">
        <h1>📄 Gestion des Factures</h1>
        <button className="btn-primary">+ Nouvelle facture</button>
      </div>

      <div className="factures-summary">
        <div className="summary-stat">
          <div className="summary-stat-icon">💰</div>
          <div className="summary-stat-content">
            <span className="summary-stat-value">{formatMontant(totalFactures)}</span>
            <span className="summary-stat-label">Total facturé</span>
          </div>
        </div>
        <div className="summary-stat success">
          <div className="summary-stat-icon">✅</div>
          <div className="summary-stat-content">
            <span className="summary-stat-value">{formatMontant(totalPayees)}</span>
            <span className="summary-stat-label">Montant encaissé</span>
          </div>
        </div>
        <div className="summary-stat warning">
          <div className="summary-stat-icon">⏳</div>
          <div className="summary-stat-content">
            <span className="summary-stat-value">{formatMontant(totalEnAttente)}</span>
            <span className="summary-stat-label">En attente</span>
          </div>
        </div>
      </div>

      <div className="factures-list">
        {facturesData.map(facture => (
          <div key={facture.id} className={`facture-card status-border-${facture.statut}`}>
            <div className="facture-header">
              <div className="facture-numero">
                <span className="numero">{facture.numero}</span>
                <span className={`status-badge status-${facture.statut}`}>
                  {formatStatus(facture.statut)}
                </span>
              </div>
              <div className="facture-montant">
                <span className="montant-ttc">{formatMontant(facture.montantTTC)}</span>
                <span className="montant-ht">HT: {formatMontant(facture.montantHT)}</span>
              </div>
            </div>

            <div className="facture-info">
              <div className="info-row">
                <span className="info-label">Client:</span>
                <span className="info-value">{getClientNom(facture.clientId)}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Projet:</span>
                <span className="info-value">{getProjetNom(facture.projetId)}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Émission:</span>
                <span className="info-value">{formatDate(facture.dateEmission)}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Échéance:</span>
                <span className={`info-value ${facture.statut === 'en_retard' ? 'overdue' : ''}`}>
                  {formatDate(facture.dateEcheance)}
                </span>
              </div>
            </div>

            <div className="facture-lignes">
              <h4>Détail des prestations</h4>
              <table>
                <thead>
                  <tr>
                    <th>Description</th>
                    <th>Qté</th>
                    <th>P.U.</th>
                    <th>Montant</th>
                  </tr>
                </thead>
                <tbody>
                  {facture.lignes.map(ligne => (
                    <tr key={ligne.id}>
                      <td>{ligne.description}</td>
                      <td>{ligne.quantite}</td>
                      <td>{formatMontant(ligne.prixUnitaire)}</td>
                      <td>{formatMontant(ligne.montant)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr>
                    <td colSpan={3}>Total HT</td>
                    <td>{formatMontant(facture.montantHT)}</td>
                  </tr>
                  <tr>
                    <td colSpan={3}>TVA (20%)</td>
                    <td>{formatMontant(facture.tva)}</td>
                  </tr>
                  <tr className="total-row">
                    <td colSpan={3}>Total TTC</td>
                    <td>{formatMontant(facture.montantTTC)}</td>
                  </tr>
                </tfoot>
              </table>
            </div>

            <div className="facture-actions">
              <button className="btn-secondary">Voir PDF</button>
              <button className="btn-secondary">Envoyer</button>
              {facture.statut !== 'payee' && (
                <button className="btn-success">Marquer payée</button>
              )}
              <button className="btn-icon">✏️</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Factures;
