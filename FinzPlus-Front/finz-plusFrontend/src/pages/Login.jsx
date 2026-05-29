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

    const cargarDemoData = () => {
        localStorage.setItem('finz_cuentas', JSON.stringify([
            { id: 1, nombre: 'Bancolombia', tipo: 'AHORROS',   saldoActual: 2500000 },
            { id: 2, nombre: 'Nequi',       tipo: 'BILLETERA', saldoActual: 150000  },
            { id: 3, nombre: 'Efectivo',    tipo: 'EFECTIVO',  saldoActual: 80000   },
        ]));
        localStorage.setItem('finz_movimientos', JSON.stringify([
            { id: 1, descripcion: 'Salario mayo',      monto: 3500000,  tipo: 'INGRESO', fecha: '2026-05-01T08:00:00', categoria: { nombre: 'Salario' },      cuenta: { nombre: 'Bancolombia' } },
            { id: 2, descripcion: 'Mercado semanal',   monto: -185000,  tipo: 'GASTO',   fecha: '2026-05-05T12:00:00', categoria: { nombre: 'Alimentación' }, cuenta: { nombre: 'Bancolombia' } },
            { id: 3, descripcion: 'Recarga Nequi',     monto: -50000,   tipo: 'GASTO',   fecha: '2026-05-08T10:00:00', categoria: { nombre: 'Transporte' },   cuenta: { nombre: 'Nequi' } },
            { id: 4, descripcion: 'Freelance diseño',  monto: 800000,   tipo: 'INGRESO', fecha: '2026-05-12T15:00:00', categoria: { nombre: 'Freelance' },    cuenta: { nombre: 'Bancolombia' } },
            { id: 5, descripcion: 'Netflix',           monto: -47900,   tipo: 'GASTO',   fecha: '2026-05-15T09:00:00', categoria: { nombre: 'Ocio' },         cuenta: { nombre: 'Nequi' } },
            { id: 6, descripcion: 'Domicilio comida',  monto: -35000,   tipo: 'GASTO',   fecha: '2026-05-20T19:00:00', categoria: { nombre: 'Alimentación' }, cuenta: { nombre: 'Nequi' } },
        ]));
        localStorage.setItem('finz_metas', JSON.stringify([
            { id: 1, nombre: 'Viaje a Cartagena', montoObjetivo: 2000000, montoActual: 650000,  fechaLimite: '2026-12-01' },
            { id: 2, nombre: 'Fondo emergencias',  montoObjetivo: 5000000, montoActual: 1200000, fechaLimite: '2026-08-01' },
        ]));
        localStorage.setItem('finz_deudas', JSON.stringify([
            { id: 1, personaEntidad: 'Banco de Occidente', montoTotal: 1500000, montoPagado: 300000, tipo: 'POR_PAGAR',  fechaVencimiento: '2026-09-01' },
            { id: 2, personaEntidad: 'Juan (amigo)',        montoTotal: 200000,  montoPagado: 0,      tipo: 'POR_COBRAR', fechaVencimiento: null },
        ]));
    };

    const manejarLogin = async (e) => {
        e.preventDefault();
        setError('');
        setCargando(true);
        try {
            const usuario = await finzService.loginUsuario(email, password);
            if (usuario) {
                login(usuario);
                navigate('/dashboard');
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

                {/* Botones de demo — solo para revisar el diseño sin backend */}
                <div style={{ marginTop: '24px', borderTop: '1px solid var(--finz-border)', paddingTop: '16px' }}>
                    <p style={{ fontSize: '11px', color: 'var(--finz-gray-400)', textAlign: 'center', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                        Vista previa sin servidor
                    </p>
                    <div style={{ display: 'flex', gap: '8px' }}>
                        {[
                            { rol: 'ADMIN',   nombre: 'Daniela López', email: 'daniela@finz.co', id: 1 },
                            { rol: 'PREMIUM', nombre: 'Carlos Pérez',  email: 'carlos@finz.co',  id: 2 },
                            { rol: 'CLIENTE', nombre: 'Ana García',    email: 'ana@finz.co',     id: 3 },
                        ].map(u => (
                            <button key={u.rol} className="finz-btn finz-btn--ghost" style={{ flex: 1, fontSize: '12px' }}
                                onClick={() => {
                                    cargarDemoData();
                                    login(u);
                                    navigate('/dashboard');
                                }}>
                                {u.rol}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
