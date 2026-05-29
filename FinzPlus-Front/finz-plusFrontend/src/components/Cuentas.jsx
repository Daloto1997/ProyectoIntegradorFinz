import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { finzService } from '../services/finzService';

const TIPOS = [
    { value: 'AHORROS',   label: 'Cuenta de ahorros',   icono: '🏦' },
    { value: 'CORRIENTE', label: 'Cuenta corriente',     icono: '💳' },
    { value: 'TARJETA',   label: 'Tarjeta de crédito',   icono: '💳' },
    { value: 'BILLETERA', label: 'Billetera digital',     icono: '📱' },
    { value: 'EFECTIVO',  label: 'Efectivo',              icono: '💵' },
    { value: 'OTRO',      label: 'Otro',                  icono: '📂' },
];

const formatCOP = (valor) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(valor ?? 0);

export default function Cuentas() {
    const { register, handleSubmit, reset, formState: { errors } } = useForm({
        defaultValues: { tipo: 'AHORROS' }
    });
    const [cuentas,   setCuentas]   = useState([]);
    const [error,     setError]     = useState(null);
    const [guardando, setGuardando] = useState(false);

    useEffect(() => {
        finzService.obtenerCuentas()
            .then(lista => setCuentas(lista))
            .catch(() => setError('No se pudieron cargar las cuentas.'));
    }, []);

    const onSubmit = async (data) => {
        setGuardando(true);
        setError(null);
        try {
            const nueva = await finzService.guardarCuenta({
                nombre:      data.nombre,
                tipo:        data.tipo,
                saldoActual: parseFloat(data.saldo) || 0,
            });
            setCuentas(prev => [...prev, nueva]);
            reset({ tipo: 'AHORROS' });
        } catch (err) {
            setError(`No se pudo guardar: ${err.message}`);
        } finally {
            setGuardando(false);
        }
    };

    const eliminar = async (id) => {
        if (!window.confirm('¿Eliminar esta cuenta?')) return;
        const ok = await finzService.eliminarCuenta(id);
        if (ok) setCuentas(prev => prev.filter(c => String(c.id) !== String(id)));
        else setError('No se pudo eliminar la cuenta.');
    };

    const saldoTotal = cuentas.reduce((acc, c) => acc + Number(c.saldoActual ?? 0), 0);

    return (
        <div className="card shadow-sm h-100">
            <div className="card-body">
                <h5 className="card-title mb-1">Cuentas y billeteras</h5>
                <p className="text-muted small mb-3">
                    Registra cada lugar donde guardas dinero: banco, Nequi, efectivo, etc.
                </p>

                {error && <div className="alert alert-danger py-2 small">{error}</div>}

                <form onSubmit={handleSubmit(onSubmit)}>
                    {/* Tipo de cuenta */}
                    <div className="mb-3">
                        <label className="form-label small fw-semibold">Tipo de cuenta</label>
                        <select
                            className="form-select"
                            {...register('tipo', { required: true })}
                        >
                            {TIPOS.map(t => (
                                <option key={t.value} value={t.value}>
                                    {t.icono}  {t.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Nombre / banco */}
                    <div className="mb-3">
                        <label className="form-label small fw-semibold">
                            Banco o nombre que le das
                        </label>
                        <input
                            type="text"
                            className={`form-control ${errors.nombre ? 'is-invalid' : ''}`}
                            placeholder="Ej: Bancolombia, Nequi, Davivienda, Efectivo casa..."
                            {...register('nombre', { required: 'Escribe un nombre para identificar la cuenta' })}
                        />
                        {errors.nombre && (
                            <div className="invalid-feedback">{errors.nombre.message}</div>
                        )}
                        <div className="form-text">
                            Ponle el nombre que quieras para reconocerla fácilmente.
                        </div>
                    </div>

                    {/* Saldo actual */}
                    <div className="mb-3">
                        <label className="form-label small fw-semibold">
                            ¿Cuánto tienes en esta cuenta ahora? (COP)
                        </label>
                        <input
                            type="number"
                            min="0"
                            step="any"
                            className={`form-control ${errors.saldo ? 'is-invalid' : ''}`}
                            placeholder="Ej: 500000"
                            {...register('saldo', {
                                required: 'Ingresa el saldo actual (puede ser 0)',
                                valueAsNumber: true,
                                min: { value: 0, message: 'El saldo no puede ser negativo' }
                            })}
                        />
                        {errors.saldo && (
                            <div className="invalid-feedback">{errors.saldo.message}</div>
                        )}
                    </div>

                    <button type="submit" disabled={guardando} className="btn btn-success w-100">
                        {guardando ? 'Guardando...' : '+ Agregar cuenta'}
                    </button>
                </form>

                {/* Lista de cuentas */}
                {cuentas.length > 0 && (
                    <div className="mt-4">
                        <div className="d-flex justify-content-between align-items-center mb-2">
                            <span className="small fw-semibold text-muted">MIS CUENTAS</span>
                            <span className="badge bg-success">
                                Total: {formatCOP(saldoTotal)}
                            </span>
                        </div>
                        {cuentas.map((c, i) => {
                            const tipoInfo = TIPOS.find(t => t.value === c.tipo) ?? TIPOS[5];
                            return (
                                <div
                                    key={c.id ?? i}
                                    className="d-flex justify-content-between align-items-center py-2"
                                    style={{ borderBottom: '1px solid #f0f0f0' }}
                                >
                                    <div className="d-flex align-items-center gap-2">
                                        <span style={{ fontSize: '20px' }}>{tipoInfo.icono}</span>
                                        <div>
                                            <div className="fw-semibold small">{c.nombre}</div>
                                            <div className="text-muted" style={{ fontSize: '11px' }}>
                                                {tipoInfo.label}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="d-flex align-items-center gap-2">
                                        <span className="fw-semibold small text-success">
                                            {formatCOP(c.saldoActual)}
                                        </span>
                                        <button
                                            className="btn btn-sm btn-outline-danger"
                                            style={{ padding: '2px 8px', fontSize: '11px' }}
                                            onClick={() => eliminar(c.id)}
                                        >
                                            ✕
                                        </button>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
}
