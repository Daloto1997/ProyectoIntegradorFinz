import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Proxy de Vite redirige /flask → localhost:5001 (sin CORS)
const FLASK_URL = '/flask';

export default function Analitica() {
    const [graficasMetas, setGraficasMetas] = useState(null);
    const [graficasDeudas, setGraficasDeudas] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [servidorOffline, setServidorOffline] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const cargarGraficas = async () => {
            try {
                // Si el servidor no responde con 200, lo marcamos como offline
                const salud = await fetch(`${FLASK_URL}/api/salud`);
                if (!salud.ok) throw new Error('Flask offline');

                const [resMetas, resDeudas] = await Promise.all([
                    fetch(`${FLASK_URL}/api/graficas/metas`),
                    fetch(`${FLASK_URL}/api/graficas/deudas`)
                ]);

                if (resMetas.ok) setGraficasMetas(await resMetas.json());
                if (resDeudas.ok) setGraficasDeudas(await resDeudas.json());

                // Si ambas respuestas fallaron aunque el servidor esté "activo"
                if (!resMetas.ok && !resDeudas.ok) throw new Error('Sin datos del servidor');

            } catch {
                setServidorOffline(true);
            } finally {
                setCargando(false);
            }
        };

        cargarGraficas();
    }, []);

    // Titulos amigables para cada clave de gráfica
    const titulos = {
        cronograma:       "Cronograma de Cumplimiento de Metas",
        metas_ambiciosas: "Metas de Gran Volumen (≥ 5M)",
        metas_sin_iniciar:"Metas Sin Iniciar por Categoría",
        mapa_usuarios:    "Actividad de Ahorro por Usuario",
        deudas_por_tipo:  "Deudas de Alto Valor por Tipo",
        acreedores:       "Distribución de Acreedores",
        deudas_intactas:  "Concentración de Deudas Sin Abonar"
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
                            { titulo: 'Cronograma de cumplimiento de metas',   icono: '📈', color: '#10b981' },
                            { titulo: 'Metas de gran volumen (≥ 5M)',           icono: '🎯', color: '#3b82f6' },
                            { titulo: 'Metas sin iniciar por categoría',        icono: '📊', color: '#f59e0b' },
                            { titulo: 'Actividad de ahorro por usuario',        icono: '👥', color: '#8b5cf6' },
                            { titulo: 'Deudas de alto valor por tipo',          icono: '💸', color: '#ef4444' },
                            { titulo: 'Distribución de acreedores',             icono: '🏦', color: '#ec4899' },
                            { titulo: 'Concentración de deudas sin abonar',     icono: '⚠️', color: '#f97316' },
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
                    {/* --- SECCIÓN METAS --- */}
                    <section className="mb-5">
                        <div className="d-flex align-items-center mb-3">
                            <span className="badge bg-success me-2 fs-6">Metas de Ahorro</span>
                            <hr className="flex-grow-1" />
                        </div>

                        {graficasMetas && Object.keys(graficasMetas).length > 0 ? (
                            <div className="row g-4">
                                {Object.entries(graficasMetas).map(([clave, imagen]) => (
                                    <div key={clave} className="col-md-6">
                                        <div className="card shadow-sm h-100">
                                            <div className="card-header bg-white border-0 pb-0">
                                                <small className="text-muted fw-semibold">
                                                    {titulos[clave] || clave}
                                                </small>
                                            </div>
                                            <div className="card-body p-2">
                                                <img
                                                    src={imagen}
                                                    alt={titulos[clave] || clave}
                                                    className="img-fluid rounded"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="alert alert-secondary">Sin datos de metas para graficar.</div>
                        )}
                    </section>

                    {/* --- SECCIÓN DEUDAS --- */}
                    <section>
                        <div className="d-flex align-items-center mb-3">
                            <span className="badge bg-danger me-2 fs-6">Control de Deudas</span>
                            <hr className="flex-grow-1" />
                        </div>

                        {graficasDeudas && Object.keys(graficasDeudas).length > 0 ? (
                            <div className="row g-4">
                                {Object.entries(graficasDeudas).map(([clave, imagen]) => (
                                    <div key={clave} className="col-md-6">
                                        <div className="card shadow-sm h-100">
                                            <div className="card-header bg-white border-0 pb-0">
                                                <small className="text-muted fw-semibold">
                                                    {titulos[clave] || clave}
                                                </small>
                                            </div>
                                            <div className="card-body p-2">
                                                <img
                                                    src={imagen}
                                                    alt={titulos[clave] || clave}
                                                    className="img-fluid rounded"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="alert alert-secondary">Sin datos de deudas para graficar.</div>
                        )}
                    </section>
                </>
            )}
        </div>
    );
}
