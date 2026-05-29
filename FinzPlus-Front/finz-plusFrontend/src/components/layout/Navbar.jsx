import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const BADGE_COLORS = {
    ADMIN:    { bg: '#dc2626', text: 'ADMIN' },
    PREMIUM:  { bg: '#7c3aed', text: 'PREMIUM' },
    CLIENTE:  { bg: '#6b7280', text: 'CLIENTE' },
};

export default function Navbar() {
    const { usuario, logout, esAdmin, esPremium } = useAuth();
    const navigate  = useNavigate();
    const location  = useLocation();

    const manejarLogout = () => {
        logout();
        navigate('/');
    };

    const badge = BADGE_COLORS[usuario?.rol] ?? BADGE_COLORS.CLIENTE;

    if (!usuario) {
        // Navbar mínimo para páginas públicas
        return (
            <nav className="finz-navbar">
                <div className="finz-navbar__brand">
                    <span className="finz-navbar__logo">Finz<span>+</span></span>
                </div>
                <div className="finz-navbar__actions">
                    <Link to="/" className={`finz-nav-link ${location.pathname === '/' ? 'active' : ''}`}>Iniciar sesión</Link>
                    <Link to="/registro" className="finz-btn finz-btn--outline-sm">Registrarse</Link>
                </div>
            </nav>
        );
    }

    return (
        <nav className="finz-navbar finz-navbar--auth">
            <div className="finz-navbar__brand">
                <Link to="/dashboard" className="finz-navbar__logo">Finz<span>+</span></Link>
            </div>

            <div className="finz-navbar__links">
                <Link to="/dashboard" className={`finz-nav-link ${location.pathname === '/dashboard' ? 'active' : ''}`}>
                    Dashboard
                </Link>

                {esPremium ? (
                    <Link to="/analitica" className={`finz-nav-link ${location.pathname === '/analitica' ? 'active' : ''}`}>
                        Analítica
                    </Link>
                ) : (
                    <span
                        className="finz-nav-link finz-nav-link--locked"
                        title="Disponible en el plan Premium"
                        style={{ cursor: 'default' }}
                    >
                        Analítica 🔒
                    </span>
                )}

                {esAdmin && (
                    <Link to="/admin" className={`finz-nav-link finz-nav-link--admin ${location.pathname === '/admin' ? 'active' : ''}`}>
                        Panel Admin
                    </Link>
                )}
            </div>

            <div className="finz-navbar__user">
                <span className="finz-badge" style={{ background: badge.bg }}>{badge.text}</span>
                <span className="finz-navbar__nombre">{usuario.nombre}</span>
                <button onClick={manejarLogout} className="finz-btn finz-btn--logout">
                    Cerrar sesión
                </button>
            </div>
        </nav>
    );
}
