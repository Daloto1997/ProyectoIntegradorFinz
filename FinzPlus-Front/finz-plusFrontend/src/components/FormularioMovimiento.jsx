import { useEffect, useRef, useState } from 'react';
import { finzService } from '../services/finzService';

export default function FormularioMovimiento({ alGuardar }) {
    const descRef   = useRef();
    const montoRef  = useRef();
    const [tipo,     setTipo]     = useState('GASTO');
    const [catId,    setCatId]    = useState('');
    const [cuentaId, setCuentaId] = useState('');
    const [categorias, setCategorias] = useState([]);
    const [cuentas,    setCuentas]    = useState([]);
    const [error,      setError]      = useState(null);
    const [guardando,  setGuardando]  = useState(false);

    useEffect(() => {
        finzService.obtenerCategorias().then(lista => {
            if (lista.length) {
                setCategorias(lista);
                const primeraGasto = lista.find(c => c.tipo === 'GASTO');
                setCatId(String((primeraGasto ?? lista[0]).id));
            }
        });
        finzService.obtenerCuentas().then(lista => {
            if (lista.length) {
                setCuentas(lista);
                setCuentaId(String(lista[0].id));
            }
        });
    }, []);

    // Al cambiar entre INGRESO y GASTO, resetear la categoría a la primera del nuevo tipo
    useEffect(() => {
        if (!categorias.length) return;
        const filtradas = categorias.filter(c => !c.tipo || c.tipo === tipo);
        if (filtradas.length) {
            setCatId(String(filtradas[0].id ?? filtradas[0].nombre ?? filtradas[0]));
        }
    }, [tipo, categorias]);

    const manejarEnvio = async (e) => {
        e.preventDefault();
        const descripcion = descRef.current.value.trim();
        const montoRaw    = montoRef.current.value;
        const monto       = Math.abs(parseFloat(montoRaw));

        if (!descripcion || !montoRaw || monto === 0 || !cuentaId) {
            setError('Por favor completa todos los campos con valores válidos.');
            return;
        }
        setError(null);
        setGuardando(true);

        const catSeleccionada   = categorias.find(c => String(c.id ?? c.nombre ?? c) === catId);
        const cuentaSeleccionada = cuentas.find(c => String(c.id) === cuentaId);

        const nuevoMov = {
            descripcion,
            monto: tipo === 'GASTO' ? -Math.abs(monto) : Math.abs(monto),
            tipo,
            fecha: new Date().toISOString().slice(0, 19),
            categoria: catSeleccionada ? { id: catSeleccionada.id } : null,
            cuenta:    cuentaSeleccionada ? { id: cuentaSeleccionada.id } : null,
        };

        try {
            await finzService.guardarTransaccion(nuevoMov);
            alGuardar();
            descRef.current.value  = '';
            montoRef.current.value = '';
            descRef.current.focus();
        } catch (err) {
            setError(`No se pudo guardar: ${err.message}`);
        } finally {
            setGuardando(false);
        }
    };

    const categoriasFiltradas = categorias.filter(c =>
        !c.tipo || c.tipo === tipo || c.tipo === tipo.toUpperCase()
    );

    return (
        <form onSubmit={manejarEnvio} className="finz-card finz-card--form mb-4">
            <h6 className="finz-form__title">Registrar Movimiento</h6>

            {error && <div className="finz-alert finz-alert--danger">{error}</div>}

            {/* Selector INGRESO / GASTO */}
            <div className="finz-tipo-selector mb-3">
                <button
                    type="button"
                    className={`finz-tipo-btn ${tipo === 'INGRESO' ? 'finz-tipo-btn--ingreso active' : ''}`}
                    onClick={() => setTipo('INGRESO')}
                >
                    + Ingreso
                </button>
                <button
                    type="button"
                    className={`finz-tipo-btn ${tipo === 'GASTO' ? 'finz-tipo-btn--gasto active' : ''}`}
                    onClick={() => setTipo('GASTO')}
                >
                    - Gasto
                </button>
            </div>

            <div className="row g-3">
                <div className="col-md-5">
                    <label className="finz-label">Descripción</label>
                    <input ref={descRef} type="text" className="finz-input" placeholder={tipo === 'INGRESO' ? '¿De dónde provino?' : '¿En qué gastaste?'} required />
                </div>

                <div className="col-md-3">
                    <label className="finz-label">Monto ($)</label>
                    <input ref={montoRef} type="number" min="1" step="any" className="finz-input" placeholder="50000" required />
                </div>

                <div className="col-md-4">
                    <label className="finz-label">Categoría</label>
                    <select className="finz-select" value={catId} onChange={e => setCatId(e.target.value)}>
                        {categoriasFiltradas.map(c => (
                            <option key={c.id ?? c.nombre ?? c} value={c.id ?? c.nombre ?? c}>
                                {c.nombre ?? c}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="col-md-6">
                    <label className="finz-label">Cuenta</label>
                    <select className="finz-select" value={cuentaId} onChange={e => setCuentaId(e.target.value)}>
                        <option value="">Selecciona una cuenta</option>
                        {cuentas.map(c => (
                            <option key={c.id} value={c.id}>{c.nombre}</option>
                        ))}
                    </select>
                </div>

                <div className="col-md-6 d-flex align-items-end">
                    <button
                        type="submit"
                        disabled={guardando}
                        className={`finz-btn w-100 ${tipo === 'INGRESO' ? 'finz-btn--ingreso' : 'finz-btn--gasto'}`}
                    >
                        {guardando ? 'Guardando...' : `Añadir ${tipo === 'INGRESO' ? 'Ingreso' : 'Gasto'}`}
                    </button>
                </div>
            </div>
        </form>
    );
}
