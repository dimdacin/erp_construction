import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Projets from './pages/Projets';
import Clients from './pages/Clients';
import Factures from './pages/Factures';
import Equipements from './pages/Equipements';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projets" element={<Projets />} />
            <Route path="/clients" element={<Clients />} />
            <Route path="/factures" element={<Factures />} />
            <Route path="/equipements" element={<Equipements />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
