import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { finzService } from '../services/finzService';

const formatCOP = (v) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v ?? 0);

const formatFecha = (f) => {
    if (!f) return '—';
    try { return new Date(f).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' }); }
    catch { return f; }
};

export default function Deudas() {
    const { register, handleSubmit, reset, formState: { errors } } = useForm();
    const [listaDeudas, setListaDeudas] = useState([]);
    const [error,       setError]       = useState(null);
    const [exito,       setExito]       = useState(false);
    const [pagandoId,   setPagandoId]   = useState(null);
    const [montoPago,   setMontoPago]   = useState('');

    useEffect(() => {
        finzService.obtenerDeudas()
            .then(setListaDeudas)
            .catch(() => setError('No se pudieron cargar las deudas.'));
    }, []);

    const onSubmit = async (data) => {
        try {
            const guardada = await finzService.guardarDeuda({
                personaEntidad:   data.personaEntidad,
                montoTotal:       parseFloat(data.montoTotal),
                montoPagado:      0,
                tipo:             data.tipo,
                fechaVencimiento: data.fechaVencimiento || null,
            });
            setListaDeudas(prev => [...prev, guardada]);
            reset();
            setError(null);
            setExito(true);
            setTimeout(() => setExito(false), 3000);
        } catch (err) {
            setError(`No se pudo guardar: ${err.message}`);
        }
    };

    const registrarPago = async (deuda) => {
        const pago = parseFloat(montoPago);
        if (!pago || pago <= 0) return;
        const nuevoMontoPagado = Math.min(
            Number(deuda.montoTotal),
            Number(deuda.montoPagado ?? 0) + pago
        );
        try {
            const actualizada = await finzService.actualizarDeuda(deuda.id, {
                personaEntidad:   deuda.personaEntidad,
                montoTotal:       deuda.montoTotal,
                montoPagado:      nuevoMontoPagado,
                tipo:             deuda.tipo,
                fechaVencimiento: deuda.fechaVencimiento || null,
            });
            setListaDeudas(prev => prev.map(d => String(d.id) === String(deuda.id) ? actualizada : d));
            setPagandoId(null);
            setMontoPago('');
        } catch (err) {
            setError(`No se pudo registrar el pago: ${err.message}`);
        }
    };

    const eliminar = async (id) => {
        if (!window.confirm('¿Eliminar esta deuda?')) return;
        const ok = await finzService.eliminarDeuda(id);
        if (ok) setListaDeudas(prev => prev.filter(d => String(d.id) !== String(id)));
        else setError('No se pudo eliminar.');
    };

    const calcPct = (d) => {
        const total = Number(d.montoTotal) || 0;
        const pagado = Number(d.montoPagado) || 0;
        return total > 0 ? Math.min(100, Math.round((pagado / total) * 100)) : 0;
    };

    return (
        <div className="container-fluid mt-4">
            <div className="row g-4">

                {/* FORMULARIO */}
                <div className="col-md-5">
                    <div className="card p-4 shadow-sm">
                        <h5 className="mb-3">Registrar Obligación</h5>
                        {error && <div className="alert alert-danger py-2 small">{error}</div>}
                        {exito && <div className="alert alert-success py-2 small">✓ Obligación registrada.</div>}
                        <form onSubmit={handleSubmit(onSubmit)}>
                            <div className="mb-3">
                                <label className="form-label small fw-semibold">Acreedor / Entidad</label>
                                <input type="text" className={`form-control ${errors.personaEntidad ? 'is-invalid' : ''}`}
                                    placeholder="Ej: Banco de Bogotá"
                                    {...register('personaEntidad', { required: 'Campo obligatorio' })} />
                                {errors.personaEntidad && <div className="invalid-feedback">{errors.personaEntidad.message}</div>}
                            </div>
                            <div className="mb-3">
                                <label className="form-label small fw-semibold">Monto total ($)</label>
                                <input type="number" className={`form-control ${errors.montoTotal ? 'is-invalid' : ''}`}
                                    placeholder="0"
                                    {...register('montoTotal', { required: 'Obligatorio', min: { value: 1, message: 'Mayor a 0' } })} />
                                {errors.montoTotal && <div className="invalid-feedback">{errors.montoTotal.message}</div>}
                            </div>
                            <div className="mb-3">
                                <label className="form-label small fw-semibold">Tipo</label>
                                <select className="form-select" {...register('tipo', { required: true })}>
                                    <option value="POR_PAGAR">Por pagar (debo)</option>
                                    <option value="POR_COBRAR">Por cobrar (me deben)</option>
                                </select>
                            </div>
                            <div className="mb-3">
                                <label className="form-label small fw-semibold">Fecha de vencimiento</label>
                                <input type="date" className="form-control" {...register('fechaVencimiento')} />
                            </div>
                            <button type="submit" className="btn btn-primary w-100">Guardar obligación</button>
                        </form>
                    </div>
                </div>

                {/* TABLA */}
                <div className="col-md-7">
                    <div className="card p-4 shadow-sm">
                        <h5 className="mb-4">Panel de Obligaciones</h5>
                        {listaDeudas.length === 0 ? (
                            <div className="text-center text-muted py-4">No hay obligaciones registradas.</div>
                        ) : (
                            listaDeudas.map((deuda) => {
                                const pct = calcPct(deuda);
                                const completada = pct >= 100;
                                return (
                                    <div key={deuda.id} className="mb-4 pb-3" style={{ borderBottom: '1px solid #f0f0f0' }}>
                                        <div className="d-flex justify-content-between align-items-start mb-1">
                                            <div>
                                                <strong>{deuda.personaEntidad}</strong>
                                                <span className={`badge ms-2 ${deuda.tipo === 'POR_COBRAR' ? 'bg-info text-dark' : 'bg-danger'}`}>
                                                    {deuda.tipo === 'POR_COBRAR' ? 'Me deben' : 'Debo'}
                                                </span>
                                                <div style={{ fontSize: '12px', color: '#94a3b8' }}>
                                                    Vence: {formatFecha(deuda.fechaVencimiento)}
                                                </div>
                                            </div>
                                            <div className="d-flex gap-1">
                                                {!completada && (
                                                    <button className="btn btn-sm btn-outline-success"
                                                        style={{ fontSize: '11px' }}
                                                        onClick={() => { setPagandoId(deuda.id); setMontoPago(''); }}>
                                                        + Registrar pago
                                                    </button>
                                                )}
                                                <button className="btn btn-sm btn-outline-danger"
                                                    style={{ fontSize: '11px' }}
                                                    onClick={() => eliminar(deuda.id)}>✕</button>
                                            </div>
                                        </div>

                                        <div className="progress mb-1" style={{ height: '10px' }}>
                                            <div className={`progress-bar ${completada ? 'bg-success' : 'bg-warning'}`}
                                                style={{ width: `${pct}%` }} />
                                        </div>
                                        <div className="d-flex justify-content-between">
                                            <small className="text-muted">
                                                Pagado: {formatCOP(deuda.montoPagado)} / {formatCOP(deuda.montoTotal)}
                                            </small>
                                            <small className={completada ? 'text-success fw-bold' : 'text-muted'}>
                                                {completada ? '✓ Completada' : `${pct}%`}
                                            </small>
                                        </div>

                                        {pagandoId === deuda.id && (
                                            <div className="d-flex gap-2 mt-2">
                                                <input type="number" min="1" className="form-control form-control-sm"
                                                    placeholder="¿Cuánto abonás? ($)"
                                                    value={montoPago}
                                                    onChange={e => setMontoPago(e.target.value)}
                                                    autoFocus />
                                                <button className="btn btn-sm btn-success"
                                                    onClick={() => registrarPago(deuda)}>✓</button>
                                                <button className="btn btn-sm btn-secondary"
                                                    onClick={() => setPagandoId(null)}>✕</button>
                                            </div>
                                        )}
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
