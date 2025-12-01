import { NavLink } from 'react-router-dom';
import './Sidebar.css';

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>🏗️ ERP Construction</h1>
      </div>
      <nav className="sidebar-nav">
        <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          <span className="nav-icon">📊</span>
          Tableau de bord
        </NavLink>
        <NavLink to="/projets" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          <span className="nav-icon">📁</span>
          Projets
        </NavLink>
        <NavLink to="/clients" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          <span className="nav-icon">👥</span>
          Clients
        </NavLink>
        <NavLink to="/factures" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          <span className="nav-icon">📄</span>
          Factures
        </NavLink>
        <NavLink to="/equipements" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
          <span className="nav-icon">🔧</span>
          Équipements
        </NavLink>
      </nav>
      <div className="sidebar-footer">
        <p>© 2024 ERP Construction</p>
      </div>
    </aside>
  );
}

export default Sidebar;
