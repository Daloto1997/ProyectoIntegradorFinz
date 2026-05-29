import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/layout/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Registro from './pages/Registro';
import Dashboard from './pages/Dashboard';
import Analitica from './pages/Analitica';
import AdminPanel from './pages/AdminPanel';

function App() {
    return (
        <AuthProvider>
            <Router>
                <Navbar />
                <main className="finz-main">
                    <Routes>
                        <Route path="/" element={<Login />} />
                        <Route path="/registro" element={<Registro />} />
                        <Route path="/dashboard" element={
                            <ProtectedRoute><Dashboard /></ProtectedRoute>
                        } />
                        <Route path="/analitica" element={
                            <ProtectedRoute soloPremium><Analitica /></ProtectedRoute>
                        } />
                        <Route path="/admin" element={
                            <ProtectedRoute soloAdmin><AdminPanel /></ProtectedRoute>
                        } />
                    </Routes>
                </main>
            </Router>
        </AuthProvider>
    );
}

export default App;
