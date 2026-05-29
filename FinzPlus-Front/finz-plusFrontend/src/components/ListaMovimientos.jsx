export default function ListaMovimientos({ movimientos, formatoMoneda, onEliminar }) {
    return (
        <div className="table-responsive">
            <table className="table table-hover align-middle">
                <thead className="table-light">
                    <tr>
                        <th>Concepto</th>
                        <th>Categoría</th>
                        <th>Fecha</th>
                        <th className="text-end">Monto</th>
                        <th className="text-end">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {movimientos.length === 0 ? (
                        <tr>
                            <td colSpan="4" className="text-center text-muted py-4">
                                No hay movimientos registrados aún.
                            </td>
                        </tr>
                    ) : (
                        movimientos.map((mov, index) => (
                            <tr key={index}>
                                <td>{mov.descripcion}</td>
                                <td><span className="badge bg-info text-dark">{mov.categoria?.nombre || mov.categoria || '—'}</span></td>
                                <td>{mov.fecha}</td>
                                        <td className={`text-end fw-bold ${mov.monto >= 0 ? 'text-success' : 'text-danger'}`}>
                                            {formatoMoneda(mov.monto)}
                                        </td>
                                        <td className="text-end">
                                            {onEliminar ? (
                                                <button className="btn btn-sm btn-outline-danger" onClick={async () => {
                                                    if (!window.confirm('¿Eliminar este movimiento?')) return;
                                                    try {
                                                        await onEliminar(mov.id ?? index);
                                                    } catch (err) {
                                                        console.error('Error eliminando movimiento:', err);
                                                    }
                                                }}>Eliminar</button>
                                            ) : null}
                                        </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}