import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { finzService } from '../services/finzService';

const formatCOP = (valor) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(valor ?? 0);

export default function Metas() {
    const { register, handleSubmit, reset, formState: { errors } } = useForm();
    const [metas,      setMetas]      = useState([]);
    const [error,      setError]      = useState(null);
    const [exito,      setExito]      = useState(false);
    const [abonandoId, setAbonandoId] = useState(null);
    const [montoAbono, setMontoAbono] = useState('');
    const [guardando,  setGuardando]  = useState(false);

    useEffect(() => {
        finzService.obtenerMetas()
            .then(setMetas)
            .catch(() => setError('No se pudieron cargar las metas.'));
    }, []);

    const onSubmit = async (data) => {
        setGuardando(true);
        try {
            const metaGuardada = await finzService.guardarMeta({
                nombre:        data.titulo,
                montoObjetivo: parseFloat(data.montoObjetivo),
                montoActual:   parseFloat(data.montoActual || 0),
                fechaLimite:   data.fechaLimite || null,
            });
            setMetas(prev => [...prev, metaGuardada]);
            reset({ titulo: '', montoObjetivo: '', montoActual: '', fechaLimite: '' });
            setError(null);
            setExito(true);
            setTimeout(() => setExito(false), 3000);
        } catch (err) {
            setError(`No se pudo guardar: ${err.message}`);
        } finally {
            setGuardando(false);
        }
    };

    const confirmarAbono = async (meta) => {
        const abono = parseFloat(montoAbono);
        if (!abono || abono <= 0) return;
        try {
            const actualizado = await finzService.actualizarMeta(meta.id, {
                nombre:        meta.nombre,
                montoObjetivo: meta.montoObjetivo,
                montoActual:   Number(meta.montoActual ?? 0) + abono,
                fechaLimite:   meta.fechaLimite || null,
            });
            setMetas(prev => prev.map(m => String(m.id) === String(meta.id) ? actualizado : m));
            setAbonandoId(null);
            setMontoAbono('');
        } catch (err) {
            setError(`No se pudo abonar: ${err.message}`);
        }
    };

    const eliminarMeta = async (id) => {
        if (!window.confirm('¿Eliminar esta meta?')) return;
        const ok = await finzService.eliminarMeta(id);
        if (ok) setMetas(prev => prev.filter(m => String(m.id) !== String(id)));
        else setError('No se pudo eliminar la meta.');
    };

    return (
        <div className="card shadow-sm h-100">
            <div className="card-body">
                <h5 className="card-title mb-3">Metas de ahorro</h5>

                <form onSubmit={handleSubmit(onSubmit)}>
                    <div className="mb-2">
                        <label className="form-label small fw-semibold">Nombre de la meta</label>
                        <input type="text" className={`form-control ${errors.titulo ? 'is-invalid' : ''}`}
                            placeholder="Ej: Viaje a Cartagena"
                            {...register('titulo', { required: 'El nombre es obligatorio' })} />
                        {errors.titulo && <div className="invalid-feedback">{errors.titulo.message}</div>}
                    </div>

                    <div className="row g-2 mb-2">
                        <div className="col-6">
                            <label className="form-label small fw-semibold">Monto objetivo ($)</label>
                            <input type="number" className={`form-control ${errors.montoObjetivo ? 'is-invalid' : ''}`}
                                placeholder="0"
                                {...register('montoObjetivo', { required: 'Obligatorio', min: { value: 1, message: 'Mayor a 0' } })} />
                            {errors.montoObjetivo && <div className="invalid-feedback">{errors.montoObjetivo.message}</div>}
                        </div>
                        <div className="col-6">
                            <label className="form-label small fw-semibold">Ya tengo ($)</label>
                            <input type="number" className="form-control" placeholder="0"
                                {...register('montoActual', { min: { value: 0, message: 'No negativo' } })} />
                        </div>
                    </div>

                    <div className="mb-3">
                        <label className="form-label small fw-semibold">Fecha límite</label>
                        <input type="date" className="form-control" {...register('fechaLimite')} />
                    </div>

                    <button type="submit" disabled={guardando} className="btn btn-primary w-100">
                        {guardando ? 'Guardando...' : 'Agregar meta'}
                    </button>
                </form>

                {error && <div className="alert alert-danger  mt-3 py-2 small">{error}</div>}
                {exito && <div className="alert alert-success mt-3 py-2 small">✓ Meta agregada correctamente.</div>}

                <div className="mt-4">
                    {metas.length === 0 ? (
                        <div className="text-center text-muted py-3 small">No hay metas registradas.</div>
                    ) : (
                        metas.map((meta) => {
                            const actual    = Number(meta.montoActual ?? 0);
                            const objetivo  = Number(meta.montoObjetivo ?? 0);
                            const pct       = objetivo > 0 ? Math.min(100, Math.round((actual / objetivo) * 100)) : 0;
                            const completada = pct >= 100;

                            return (
                                <div key={meta.id} className="mb-4 pb-3" style={{ borderBottom: '1px solid #f0f0f0' }}>
                                    <div className="d-flex justify-content-between align-items-start mb-1">
                                        <div>
                                            <strong style={{ fontSize: '14px' }}>{meta.nombre}</strong>
                                            {meta.fechaLimite && (
                                                <div style={{ fontSize: '11px', color: '#94a3b8' }}>
                                                    Límite: {new Date(meta.fechaLimite).toLocaleDateString('es-CO')}
                                                </div>
                                            )}
                                        </div>
                                        <div className="d-flex gap-1">
                                            {!completada && (
                                                <button className="btn btn-sm btn-outline-success"
                                                    style={{ fontSize: '11px', padding: '2px 8px' }}
                                                    onClick={() => { setAbonandoId(meta.id); setMontoAbono(''); }}>
                                                    + Abonar
                                                </button>
                                            )}
                                            <button className="btn btn-sm btn-outline-danger"
                                                style={{ fontSize: '11px', padding: '2px 8px' }}
                                                onClick={() => eliminarMeta(meta.id)}>✕</button>
                                        </div>
                                    </div>

                                    <div className="progress mb-1" style={{ height: '12px' }}>
                                        <div className={`progress-bar ${completada ? 'bg-success' : 'bg-primary'}`}
                                            role="progressbar" style={{ width: `${pct}%` }} />
                                    </div>

                                    <div className="d-flex justify-content-between">
                                        <small className="text-muted">{formatCOP(actual)} ahorrados</small>
                                        <small className="text-muted">{pct}% — Meta: {formatCOP(objetivo)}</small>
                                    </div>
                                    {completada && <span className="badge bg-success mt-1">🎉 ¡Meta alcanzada!</span>}

                                    {abonandoId === meta.id && (
                                        <div className="d-flex gap-2 mt-2">
                                            <input
                                                type="number" min="1" className="form-control form-control-sm"
                                                placeholder="¿Cuánto abonás? ($)"
                                                value={montoAbono}
                                                onChange={e => setMontoAbono(e.target.value)}
                                                autoFocus
                                            />
                                            <button className="btn btn-sm btn-success"
                                                onClick={() => confirmarAbono(meta)}>✓</button>
                                            <button className="btn btn-sm btn-secondary"
                                                onClick={() => setAbonandoId(null)}>✕</button>
                                        </div>
                                    )}
                                </div>
                            );
                        })
                    )}
                </div>
            </div>
        </div>
    );
}
