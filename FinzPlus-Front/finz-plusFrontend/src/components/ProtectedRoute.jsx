import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children, soloAdmin = false, soloPremium = false }) {
    const { usuario, esAdmin, esPremium } = useAuth();

    if (!usuario) return <Navigate to="/" replace />;
    if (soloAdmin && !esAdmin) return <Navigate to="/dashboard" replace />;
    if (soloPremium && !esPremium) return <Navigate to="/dashboard" replace />;

    return children;
}
