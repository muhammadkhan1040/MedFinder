import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import SearchPage from './pages/Search';
import FormulaSearch from './pages/FormulaSearch';
import SymptomSearch from './pages/SymptomSearch';
import Contact from './pages/Contact';
import PrescriptionAssistant from './pages/PrescriptionAssistant';
import './styles/globals.css';

/**
 * MedFinder App
 * 
 * A beautiful pharmaceutical intelligence system frontend
 */
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/formula" element={<FormulaSearch />} />
          <Route path="/symptom-search" element={<SymptomSearch />} />
          <Route path="/prescription" element={<PrescriptionAssistant />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
