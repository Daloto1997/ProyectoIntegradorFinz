import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { finzService } from '../services/finzService';

export default function Metas() {
  const { register, handleSubmit, reset, formState: { errors } } = useForm();
  const [metas, setMetas] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const cargarMetas = async () => {
      try {
        const lista = await finzService.obtenerMetas();
        setMetas(lista);
      } catch (err) {
        console.error('Error cargando metas:', err);
        setError('No se pudieron cargar las metas.');
      }
    };

    cargarMetas();
  }, []);

  const onSubmit = async (data) => {
    const nuevaMeta = {
      titulo: data.titulo,
      montoObjetivo: parseFloat(data.montoObjetivo),
      montoActual: parseFloat(data.montoActual || 0)
    };

    try {
      const metaGuardada = await finzService.guardarMeta(nuevaMeta);
      setMetas([...metas, metaGuardada]);
      reset();
      setError(null);
    } catch (err) {
      console.error('Error guardando meta:', err);
      setError(`No se pudo guardar la meta: ${err.message}`);
    }
  };

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">
        <h5 className="card-title mb-3">Metas</h5>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="mb-3">
            <label className="form-label small">Meta</label>
            <input
              type="text"
              className={`form-control ${errors.titulo ? 'is-invalid' : ''}`}
              {...register('titulo', { required: 'El título es obligatorio' })}
            />
            {errors.titulo && <div className="invalid-feedback">{errors.titulo.message}</div>}
          </div>

          <div className="mb-3">
            <label className="form-label small">Monto objetivo</label>
            <input
              type="number"
              className={`form-control ${errors.montoObjetivo ? 'is-invalid' : ''}`}
              {...register('montoObjetivo', { required: 'El monto objetivo es obligatorio', valueAsNumber: true, min: { value: 1, message: 'Debe ser mayor a 0' } })}
            />
            {errors.montoObjetivo && <div className="invalid-feedback">{errors.montoObjetivo.message}</div>}
          </div>

          <div className="mb-3">
            <label className="form-label small">Monto actual</label>
            <input
              type="number"
              className="form-control"
              {...register('montoActual', { valueAsNumber: true, min: { value: 0, message: 'No puede ser negativo' } })}
            />
          </div>

          <button type="submit" className="btn btn-primary w-100">Agregar meta</button>
        </form>

        {error && <div className="alert alert-danger mt-3 py-2">{error}</div>}

        <div className="mt-4">
          {metas.length === 0 ? (
            <div className="text-center text-muted py-4">No hay metas registradas.</div>
          ) : (
            metas.map((meta, index) => {
              const actual = meta.montoActual ?? meta.actual ?? 0;
              const objetivo = meta.montoObjetivo ?? meta.objetivo ?? 0;
              const porcentaje = objetivo > 0 ? Math.min(100, Math.round((actual / objetivo) * 100)) : 0;
              return (
                <div key={meta.id ?? index} className="mb-3">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <div className="d-flex align-items-center">
                      <strong>{meta.nombre || 'Meta'}</strong>
                      <button className="btn btn-sm btn-outline-danger ms-3" onClick={async () => {
                        if (!window.confirm('¿Eliminar esta meta?')) return;
                        try {
                          const ok = await finzService.eliminarMeta(meta.id ?? index);
                          if (ok) setMetas(metas.filter(m => String(m.id) !== String(meta.id ?? index)));
                        } catch (err) {
                          console.error('Error eliminando meta:', err);
                          setError('No se pudo eliminar la meta.');
                        }
                      }}>Eliminar</button>
                    </div>
                    <span className="badge bg-secondary">{porcentaje}%</span>
                  </div>
                  <div className="progress" style={{ height: '16px' }}>
                    <div className="progress-bar" role="progressbar" style={{ width: `${porcentaje}%` }} aria-valuenow={porcentaje} aria-valuemin="0" aria-valuemax="100">
                      {porcentaje}%
                    </div>
                  </div>
                  <small className="text-muted">{actual.toLocaleString()} / {objetivo.toLocaleString()}</small>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
