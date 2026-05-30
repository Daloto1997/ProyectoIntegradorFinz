import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Proxy de Vite redirige /flask → localhost:5001 (sin CORS)
const FLASK_URL = '/flask';

function SeccionGraficas({ titulo, badge, graficas, titulos, mensajeVacio }) {
    return (
        <section className="mb-5">
            <div className="d-flex align-items-center mb-3">
                <span className={`badge ${badge} me-2 fs-6`}>{titulo}</span>
                <hr className="flex-grow-1" />
            </div>
            {graficas && Object.keys(graficas).length > 0 ? (
                <div className="row g-4">
                    {Object.entries(graficas).map(([clave, imagen]) => (
                        <div key={clave} className="col-md-6">
                            <div className="card shadow-sm h-100">
                                <div className="card-header bg-white border-0 pb-0">
                                    <small className="text-muted fw-semibold">{titulos[clave] || clave}</small>
                                </div>
                                <div className="card-body p-2">
                                    <img src={imagen} alt={titulos[clave] || clave} className="img-fluid rounded" />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="alert alert-secondary">{mensajeVacio}</div>
            )}
        </section>
    );
}

export default function Analitica() {
    const [graficasTransacciones, setGraficasTransacciones] = useState(null);
    const [graficasMetas,         setGraficasMetas]         = useState(null);
    const [graficasDeudas,        setGraficasDeudas]        = useState(null);
    const [graficasUsuarios,      setGraficasUsuarios]      = useState(null);
    const [cargando,              setCargando]              = useState(true);
    const [servidorOffline,       setServidorOffline]       = useState(false);
    const navigate = useNavigate();
    const { usuario, esAdmin } = useAuth();

    useEffect(() => {
        const cargarGraficas = async () => {
            try {
                const salud = await fetch(`${FLASK_URL}/api/salud`);
                if (!salud.ok) { setServidorOffline(true); return; }

                const emailParam = usuario?.email
                    ? `?usuarioEmail=${encodeURIComponent(usuario.email)}`
                    : '';

                const endpoints = [
                    fetch(`${FLASK_URL}/api/graficas/transacciones${emailParam}`),
                    fetch(`${FLASK_URL}/api/graficas/metas${emailParam}`),
                    fetch(`${FLASK_URL}/api/graficas/deudas${emailParam}`),
                ];
                if (esAdmin) endpoints.push(fetch(`${FLASK_URL}/api/graficas/usuarios`));

                const [resTrans, resMetas, resDeudas, resUsers] = await Promise.all(endpoints);

                if (resTrans.ok)  setGraficasTransacciones(await resTrans.json());
                if (resMetas.ok)  setGraficasMetas(await resMetas.json());
                if (resDeudas.ok) setGraficasDeudas(await resDeudas.json());
                if (esAdmin && resUsers?.ok) setGraficasUsuarios(await resUsers.json());

            } catch {
                setServidorOffline(true);
            } finally {
                setCargando(false);
            }
        };
        cargarGraficas();
    }, []);

    const titulos = {
        // Transacciones
        proporcion:         "Ingresos vs Egresos",
        tendencia:          "Volumen de Transacciones por Mes",
        egresos_categoria:  "Egresos por Categoría",
        mapa_calor:         "Densidad: Cuentas vs Categorías",
        alto_valor:         "Transacciones de Alto Valor (> $1.5M)",
        // Metas
        cronograma:         "Cronograma de Cumplimiento de Metas",
        metas_ambiciosas:   "Metas de Gran Volumen (≥ 5M)",
        metas_sin_iniciar:  "Metas Sin Iniciar por Categoría",
        mapa_usuarios:      "Actividad de Ahorro por Usuario",
        // Deudas
        deudas_por_tipo:    "Deudas de Alto Valor por Tipo",
        acreedores:         "Distribución de Acreedores",
        deudas_intactas:    "Concentración de Deudas Sin Abonar",
        // Usuarios (Admin)
        roles:              "Distribución por Plan/Rol",
        crecimiento:        "Crecimiento Mensual de Usuarios",
        totales_rol:        "Total de Usuarios por Plan",
        actividad_diaria:   "Actividad de Registros (Últimos 30 Días)",
    };

    return (
        <div className="container py-4">

            {/* Encabezado */}
            <div className="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h2 className="text-primary mb-0">Analítica Finz+</h2>
                    <p className="text-muted small mb-0">Reportes generados por el servidor Python</p>
                </div>
                <button
                    className="btn btn-outline-secondary"
                    onClick={() => navigate('/dashboard')}
                >
                    ← Volver al Dashboard
                </button>
            </div>

            {/* Estado: cargando */}
            {cargando && (
                <div className="text-center py-5">
                    <div className="spinner-border text-primary mb-3" role="status" />
                    <p className="text-muted">Generando gráficas desde el servidor Python...</p>
                    <small className="text-muted">Esto puede tardar unos segundos la primera vez</small>
                </div>
            )}

            {/* Estado: servidor offline */}
            {servidorOffline && (
                <div>
                    <div className="finz-alert finz-alert--warning mb-4">
                        <strong>Servidor de analítica no disponible</strong>
                        <p style={{ margin: '6px 0 8px', fontSize: '13px' }}>
                            El servidor Python (Flask) no está corriendo. Las gráficas se generan desde ese servidor.
                            Para activarlo, ejecuta en una terminal:
                        </p>
                        <pre style={{ background: '#1f2937', color: '#d1fae5', padding: '12px', borderRadius: '8px', fontSize: '12px', margin: 0 }}>
                            cd FinzPlus-Analitica{'\n'}
                            pip install -r requirements.txt{'\n'}
                            python servidor_flask.py
                        </pre>
                    </div>

                    {/* Vista previa de qué gráficas habrá cuando esté activo */}
                    <div className="row g-3">
                        {[
                            { titulo: 'Ingresos vs Egresos',                    icono: '🍩', color: '#25c974' },
                            { titulo: 'Volumen de transacciones por mes',        icono: '📈', color: '#3b82f6' },
                            { titulo: 'Egresos por categoría',                  icono: '📊', color: '#f59e0b' },
                            { titulo: 'Densidad: Cuentas vs Categorías',        icono: '🔥', color: '#8b5cf6' },
                            { titulo: 'Transacciones de alto valor',            icono: '💸', color: '#ef4444' },
                            { titulo: 'Cronograma de metas',                    icono: '🎯', color: '#10b981' },
                            { titulo: 'Deudas por tipo',                        icono: '🏦', color: '#ec4899' },
                            { titulo: 'Comportamiento de usuarios (Admin)',      icono: '👥', color: '#dc2626' },
                        ].map(g => (
                            <div key={g.titulo} className="col-md-6">
                                <div className="finz-card" style={{ borderLeft: `4px solid ${g.color}`, minHeight: '140px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: '8px', opacity: 0.6 }}>
                                    <span style={{ fontSize: '36px' }}>{g.icono}</span>
                                    <span style={{ fontSize: '13px', color: 'var(--finz-gray-500)', textAlign: 'center' }}>
                                        {g.titulo}
                                    </span>
                                    <span style={{ fontSize: '11px', color: 'var(--finz-gray-400)' }}>
                                        Disponible cuando Flask esté activo
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Contenido: gráficas cargadas */}
            {!cargando && !servidorOffline && (
                <>
                    {/* --- SECCIÓN USUARIOS (solo Admin) --- */}
                    {esAdmin && (
                        <SeccionGraficas
                            titulo="Comportamiento de Usuarios (Admin)"
                            badge="bg-danger"
                            graficas={graficasUsuarios}
                            titulos={titulos}
                            mensajeVacio="Sin datos de usuarios para graficar."
                        />
                    )}

                    {/* --- SECCIÓN TRANSACCIONES --- */}
                    <SeccionGraficas
                        titulo="Análisis de Transacciones"
                        badge="bg-primary"
                        graficas={graficasTransacciones}
                        titulos={titulos}
                        mensajeVacio="Sin datos de transacciones para graficar."
                    />

                    {/* --- SECCIÓN METAS --- */}
                    <SeccionGraficas
                        titulo="Metas de Ahorro"
                        badge="bg-success"
                        graficas={graficasMetas}
                        titulos={titulos}
                        mensajeVacio="Sin datos de metas para graficar."
                    />

                    {/* --- SECCIÓN DEUDAS --- */}
                    <SeccionGraficas
                        titulo="Control de Deudas"
                        badge="bg-danger"
                        graficas={graficasDeudas}
                        titulos={titulos}
                        mensajeVacio="Sin datos de deudas para graficar."
                    />
                </>
            )}
        </div>
    );
}
