import { useState, useEffect } from 'react';

const API = '/api';

const ROL_LABELS = {
    ADMIN:   { label: 'Admin',   color: '#dc2626' },
    PREMIUM: { label: 'Premium', color: '#7c3aed' },
    CLIENTE: { label: 'Cliente', color: '#6b7280' },
};

export default function AdminPanel() {
    const [usuarios,  setUsuarios]  = useState([]);
    const [cargando,  setCargando]  = useState(true);
    const [error,     setError]     = useState('');
    const [guardando, setGuardando] = useState(null);

    useEffect(() => {
        fetch(`${API}/usuarios`, { credentials: 'include' })
            .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
            .then(setUsuarios)
            .catch(() => setError('No se pudieron cargar los usuarios.'))
            .finally(() => setCargando(false));
    }, []);

    const cambiarRol = async (id, nuevoRol) => {
        setGuardando(id);
        try {
            const res = await fetch(`${API}/usuarios/${id}/rol`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ rol: nuevoRol }),
            });
            if (!res.ok) throw new Error();
            setUsuarios(prev => prev.map(u => u.id === id ? { ...u, rol: nuevoRol } : u));
        } catch {
            setError('No se pudo cambiar el rol. Verifica la conexión.');
        } finally {
            setGuardando(null);
        }
    };

    const totalPorRol = (rol) => usuarios.filter(u => u.rol === rol).length;

    return (
        <div>
            <div className="finz-dash-header">
                <div>
                    <div className="finz-dash-header__title">Panel de Administración</div>
                    <div className="finz-dash-header__sub">Gestión de usuarios y roles del sistema</div>
                </div>
            </div>

            {/* Resumen de roles */}
            <div className="row g-3 mb-4">
                {[
                    { rol: 'ADMIN',   label: 'Administradores', color: '#dc2626', bg: '#fee2e2' },
                    { rol: 'PREMIUM', label: 'Usuarios Premium', color: '#7c3aed', bg: '#ede9fe' },
                    { rol: 'CLIENTE', label: 'Clientes',         color: '#6b7280', bg: '#f3f4f6' },
                ].map(({ rol, label, color, bg }) => (
                    <div className="col-md-4" key={rol}>
                        <div className="finz-stat-card" style={{ borderLeft: `4px solid ${color}` }}>
                            <div className="finz-stat-card__label">{label}</div>
                            <div className="finz-stat-card__value" style={{ color }}>{totalPorRol(rol)}</div>
                        </div>
                    </div>
                ))}
            </div>

            {error && <div className="finz-alert finz-alert--danger mb-3">{error}</div>}

            <div className="finz-card">
                <div className="finz-card__title">Usuarios registrados</div>

                {cargando ? (
                    <div style={{ padding: '32px', textAlign: 'center', color: 'var(--finz-gray-400)' }}>
                        Cargando usuarios...
                    </div>
                ) : (
                    <div style={{ overflowX: 'auto' }}>
                        <table className="finz-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nombre</th>
                                    <th>Correo</th>
                                    <th>Teléfono</th>
                                    <th>Rol actual</th>
                                    <th>Cambiar rol</th>
                                    <th>Registrado</th>
                                </tr>
                            </thead>
                            <tbody>
                                {usuarios.map(u => {
                                    const rolInfo = ROL_LABELS[u.rol] ?? ROL_LABELS.CLIENTE;
                                    return (
                                        <tr key={u.id}>
                                            <td style={{ color: 'var(--finz-gray-400)', fontSize: '12px' }}>#{u.id}</td>
                                            <td style={{ fontWeight: 600 }}>{u.nombre}</td>
                                            <td style={{ color: 'var(--finz-gray-500)' }}>{u.email}</td>
                                            <td>{u.telefono || '—'}</td>
                                            <td>
                                                <span className="finz-badge" style={{ background: rolInfo.color }}>
                                                    {rolInfo.label}
                                                </span>
                                            </td>
                                            <td>
                                                <select
                                                    className="finz-select"
                                                    style={{ width: 'auto', padding: '4px 8px', fontSize: '13px' }}
                                                    value={u.rol ?? 'CLIENTE'}
                                                    disabled={guardando === u.id}
                                                    onChange={e => cambiarRol(u.id, e.target.value)}
                                                >
                                                    <option value="CLIENTE">Cliente</option>
                                                    <option value="PREMIUM">Premium</option>
                                                    <option value="ADMIN">Admin</option>
                                                </select>
                                            </td>
                                            <td style={{ color: 'var(--finz-gray-400)', fontSize: '12px' }}>
                                                {u.fechaCreacion
                                                    ? new Date(u.fechaCreacion).toLocaleDateString('es-CO')
                                                    : '—'}
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>

            {/* Info de funciones por plan */}
            <div className="row g-3 mt-4">
                {[
                    {
                        rol: 'CLIENTE', color: '#6b7280', features: [
                            'Dashboard de ingresos y gastos',
                            'Gestión de cuentas bancarias',
                            'Registro de obligaciones/deudas',
                            'Historial de movimientos',
                        ]
                    },
                    {
                        rol: 'PREMIUM', color: '#7c3aed', features: [
                            'Todo lo del plan Cliente',
                            'Gestión de metas de ahorro',
                            'Analítica con gráficas (Python/Flask)',
                            'Reportes de deudas y metas',
                        ]
                    },
                    {
                        rol: 'ADMIN', color: '#dc2626', features: [
                            'Todo lo del plan Premium',
                            'Panel de administración de usuarios',
                            'Cambio de roles en tiempo real',
                            'Visibilidad total del sistema',
                        ]
                    },
                ].map(({ rol, color, features }) => (
                    <div className="col-md-4" key={rol}>
                        <div className="finz-card" style={{ borderTop: `3px solid ${color}` }}>
                            <div className="finz-card__title" style={{ color }}>Plan {rol}</div>
                            <ul style={{ paddingLeft: '16px', margin: 0 }}>
                                {features.map(f => (
                                    <li key={f} style={{ fontSize: '13px', color: 'var(--finz-gray-600)', marginBottom: '6px' }}>
                                        {f}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
