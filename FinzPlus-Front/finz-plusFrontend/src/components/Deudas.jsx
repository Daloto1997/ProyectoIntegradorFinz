import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { finzService } from '../services/finzService';

export default function Deudas() {
  const { register, handleSubmit, reset, formState: { errors } } = useForm();
  const [listaDeudas, setListaDeudas] = useState([]);
  const [error, setError] = useState(null);

  // Cargar deudas al montar el componente
  useEffect(() => {
    const cargarDeudas = async () => {
      try {
        const deudasGuardadas = await finzService.obtenerDeudas();
        setListaDeudas(deudasGuardadas);
      } catch (err) {
        console.error('Error cargando deudas:', err);
        setError('No se pudieron cargar las deudas.');
      }
    };
    cargarDeudas();
  }, []);

  // Registrar nueva deuda
  const onSubmit = async (data) => {
    const nuevaDeuda = {
      personaEntidad: data.personaEntidad,
      montoTotal: parseFloat(data.montoTotal),
      montoPagado: 0,
      tipo: data.tipo,
      fechaVencimiento: data.fechaVencimiento || null
    };

    try {
      const deudaGuardada = await finzService.guardarDeuda(nuevaDeuda);
      setListaDeudas([...listaDeudas, deudaGuardada]);
      reset();
      setError(null);
    } catch (err) {
      console.error('Error guardando deuda:', err);
      setError(`No se pudo guardar la deuda: ${err.message}`);
    }
  };

  // Calcular el porcentaje pagado de una deuda
  const calcularPorcentaje = (deuda) => {
    const total = Number(deuda.montoTotal) || 0;
    const pagado = Number(deuda.montoPagado) || 0;
    return total > 0 ? Math.min(100, Math.round((pagado / total) * 100)) : 0;
  };

  return (
    <div className="container-fluid mt-4">
      <div className="row g-4">

        {/* FORMULARIO */}
        <div className="col-md-5">
          <div className="card p-4 shadow-sm">
            <h5 className="mb-3 font-weight-bold">Registrar Obligación</h5>
            {error && <div className="alert alert-danger py-2 small">{error}</div>}
            <form onSubmit={handleSubmit(onSubmit)}>

              <div className="mb-3">
                <label className="form-label small">Acreedor / Entidad</label>
                <input
                  type="text"
                  className={`form-control ${errors.personaEntidad ? 'is-invalid' : ''}`}
                  placeholder="Ej. Banco de Bogotá"
                  {...register("personaEntidad", { required: "Campo obligatorio" })}
                />
                {errors.personaEntidad && <div className="invalid-feedback">{errors.personaEntidad.message}</div>}
              </div>

              <div className="mb-3">
                <label className="form-label small">Monto Total</label>
                <input
                  type="number"
                  className={`form-control ${errors.montoTotal ? 'is-invalid' : ''}`}
                  placeholder="0"
                  {...register("montoTotal", { required: "Campo obligatorio", min: { value: 1, message: 'Debe ser mayor a 0' } })}
                />
                {errors.montoTotal && <div className="invalid-feedback">{errors.montoTotal.message}</div>}
              </div>

              <div className="mb-3">
                <label className="form-label small">Tipo</label>
                <select className="form-select" {...register("tipo", { required: true })}>
                  <option value="POR_PAGAR">Por pagar</option>
                  <option value="POR_COBRAR">Por cobrar</option>
                </select>
              </div>

              <div className="mb-3">
                <label className="form-label small">Fecha de vencimiento</label>
                <input
                  type="date"
                  className="form-control"
                  {...register("fechaVencimiento")}
                />
              </div>

              <button type="submit" className="btn btn-primary w-100">Guardar deuda</button>
            </form>
          </div>
        </div>

        {/* TABLA DE CONTROL */}
        <div className="col-md-7">
          <div className="card p-4 shadow-sm">
            <h5 className="mb-4 font-weight-bold">Panel de Control de Obligaciones</h5>
            <div className="table-responsive">
              <table className="table align-middle">
                <thead>
                  <tr className="small text-muted">
                    <th>ACREEDOR</th>
                    <th>MONTO</th>
                    <th>PROGRESO</th>
                    <th>TIPO</th>
                    <th>VENCE</th>
                    <th className="text-end">ACCIONES</th>
                  </tr>
                </thead>
                <tbody>
                  {listaDeudas.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="text-center text-muted py-4">No hay deudas registradas.</td>
                    </tr>
                  ) : (
                    listaDeudas.map((deuda) => {
                      const porcentaje = calcularPorcentaje(deuda);
                      return (
                        <tr key={deuda.id}>
                          <td><strong>{deuda.personaEntidad}</strong></td>
                          <td>${Number(deuda.montoTotal || 0).toLocaleString()}</td>
                          <td style={{ minWidth: '120px' }}>
                            <div className="progress mb-1" style={{ height: '10px' }}>
                              <div
                                className={`progress-bar ${porcentaje >= 100 ? 'bg-success' : 'bg-warning'}`}
                                style={{ width: `${porcentaje}%` }}
                              />
                            </div>
                            <small className="text-muted">{porcentaje}% pagado</small>
                            {porcentaje >= 100 && <span className="badge bg-success ms-2">¡PAGADA!</span>}
                          </td>
                          <td>
                            <span className={`badge ${deuda.tipo === 'POR_COBRAR' ? 'bg-info text-dark' : 'bg-danger'}`}>
                              {deuda.tipo === 'POR_COBRAR' ? 'Por cobrar' : 'Por pagar'}
                            </span>
                          </td>
                          <td>{deuda.fechaVencimiento || '—'}</td>
                          <td className="text-end">
                            <button
                              className="btn btn-sm btn-outline-danger"
                              onClick={async () => {
                                if (!window.confirm('¿Eliminar esta deuda?')) return;
                                try {
                                  const ok = await finzService.eliminarDeuda(deuda.id);
                                  if (ok) setListaDeudas(listaDeudas.filter(d => String(d.id) !== String(deuda.id)));
                                } catch (err) {
                                  console.error('Error eliminando deuda:', err);
                                  setError('No se pudo eliminar la deuda.');
                                }
                              }}
                            >Eliminar</button>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
