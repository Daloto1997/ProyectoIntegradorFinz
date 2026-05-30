const formatFecha = (fecha) => {
    if (!fecha) return '—';
    try {
        return new Date(fecha).toLocaleDateString('es-CO', {
            day: '2-digit', month: 'short', year: 'numeric'
        });
    } catch { return fecha; }
};

export default function ListaMovimientos({ movimientos, formatoMoneda, onEliminar }) {
    return (
        <div className="table-responsive">
            <table className="table table-hover align-middle">
                <thead className="table-light">
                    <tr>
                        <th>Concepto</th>
                        <th>Categoría</th>
                        <th>Cuenta</th>
                        <th>Fecha</th>
                        <th className="text-end">Monto</th>
                        <th className="text-end">Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {movimientos.length === 0 ? (
                        <tr>
                            <td colSpan="6" className="text-center text-muted py-4">
                                No hay movimientos registrados aún.
                            </td>
                        </tr>
                    ) : (
                        movimientos.map((mov, index) => (
                            <tr key={mov.id ?? index}>
                                <td>
                                    <span style={{ fontSize: '13px' }}>{mov.descripcion || '—'}</span>
                                    <div>
                                        <span className={`badge ${mov.tipo === 'INGRESO' ? 'bg-success' : 'bg-danger'}`} style={{ fontSize: '10px' }}>
                                            {mov.tipo}
                                        </span>
                                    </div>
                                </td>
                                <td>
                                    <span className="badge bg-info text-dark">
                                        {mov.categoria?.nombre || mov.categoria || '—'}
                                    </span>
                                </td>
                                <td style={{ fontSize: '12px', color: '#64748b' }}>
                                    {mov.cuenta?.nombre || '—'}
                                </td>
                                <td style={{ fontSize: '12px', color: '#64748b' }}>
                                    {formatFecha(mov.fecha)}
                                </td>
                                <td className={`text-end fw-bold ${Math.abs(Number(mov.monto)) === Number(mov.monto) && mov.tipo === 'INGRESO' ? 'text-success' : 'text-danger'}`}>
                                    {mov.tipo === 'INGRESO' ? '+' : '-'}{formatoMoneda(Math.abs(Number(mov.monto)))}
                                </td>
                                <td className="text-end">
                                    {onEliminar && (
                                        <button
                                            className="btn btn-sm btn-outline-danger"
                                            onClick={async () => {
                                                if (!window.confirm('¿Eliminar este movimiento?')) return;
                                                await onEliminar(mov.id ?? index);
                                            }}
                                        >✕</button>
                                    )}
                                </td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}
