import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { finzService } from '../services/finzService';

import { useAuth } from '../context/AuthContext';

export default function Login() {
    const [email,    setEmail]    = useState('');
    const [password, setPassword] = useState('');
    const [error,    setError]    = useState('');
    const [cargando, setCargando] = useState(false);
    const navigate = useNavigate();
    const { login } = useAuth();

    const manejarLogin = async (e) => {
        e.preventDefault();
        setError('');
        setCargando(true);
        try {
            const usuario = await finzService.loginUsuario(email, password);
            if (usuario) {
                login(usuario);
                const cuentas = await finzService.obtenerCuentas();
                navigate(cuentas.length === 0 ? '/setup' : '/dashboard');
            }
        } catch (err) {
            const msg = err?.message || '';
            if (msg.toLowerCase().includes('credencial') || msg.toLowerCase().includes('unauthorized') || msg.includes('401')) {
                setError('Correo o contraseña incorrectos. Verifica tus datos.');
            } else {
                setError(msg || 'Error al conectar con el servidor. Intenta de nuevo.');
            }
        } finally {
            setCargando(false);
        }
    };

    return (
        <div className="finz-auth-page">
            <div className="finz-auth-card">
                <div className="finz-auth-card__logo">Finz<span>+</span></div>
                <div className="finz-auth-card__subtitle">Tu gestor financiero personal</div>

                {error && <div className="finz-alert finz-alert--danger">{error}</div>}

                <form onSubmit={manejarLogin}>
                    <div className="mb-3">
                        <label className="finz-label">Correo electrónico</label>
                        <input
                            type="email"
                            className="finz-input"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                            placeholder="tu@correo.com"
                            required
                            autoFocus
                        />
                    </div>
                    <div style={{ marginBottom: '20px' }}>
                        <label className="finz-label">Contraseña</label>
                        <input
                            type="password"
                            className="finz-input"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                            placeholder="••••••••"
                            required
                        />
                    </div>
                    <button type="submit" disabled={cargando} className="finz-btn finz-btn--primary w-100">
                        {cargando ? 'Ingresando...' : 'Ingresar'}
                    </button>
                </form>

                <div className="finz-auth-card__footer">
                    ¿No tienes cuenta? <Link to="/registro">Regístrate aquí</Link>
                </div>
            </div>
        </div>
    );
}
