import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { finzService } from '../services/finzService';
import { useAuth } from '../context/AuthContext';
import FormularioMovimiento from '../components/FormularioMovimiento';
import ListaMovimientos from '../components/ListaMovimientos';
import Deudas from '../components/Deudas';
import Cuentas from '../components/Cuentas';
import Metas from '../components/Metas';

const formatoMoneda = (valor) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(valor);

export default function Dashboard() {
    const [movimientos,   setMovimientos]   = useState([]);
    const [saldoCuentas,  setSaldoCuentas]  = useState(0);
    const { usuario, esPremium } = useAuth();
    const navigate = useNavigate();

    const cargarDatos = async () => {
        const [datos, cuentas] = await Promise.all([
            finzService.obtenerTransacciones(),
            finzService.obtenerCuentas()
        ]);
        setMovimientos(datos);
        setSaldoCuentas(cuentas.reduce((acc, c) => acc + Number(c.saldoActual ?? 0), 0));
    };

    const eliminarMovimiento = async (id) => {
        const ok = await finzService.eliminarTransaccion(id);
        if (ok) {
            setMovimientos(prev => prev.filter(m => String(m.id) !== String(id)));
        } else {
            await cargarDatos();
        }
    };

    useEffect(() => {
        cargarDatos();
    }, []);

    const ingresos = movimientos
        .filter(m => m.tipo === 'INGRESO')
        .reduce((acc, m) => acc + Math.abs(Number(m.monto)), 0);

    const gastos = movimientos
        .filter(m => m.tipo === 'GASTO')
        .reduce((acc, m) => acc + Math.abs(Number(m.monto)), 0);

    const saldoTotal = saldoCuentas;

    return (
        <div>
            {/* Header */}
            <div className="finz-dash-header">
                <div>
                    <div className="finz-dash-header__title">Bienvenido, {usuario?.nombre?.split(' ')[0]}</div>
                    <div className="finz-dash-header__sub">Aquí está el resumen de tus finanzas</div>
                </div>
                {esPremium && (
                    <div className="finz-dash-header__actions">
                        <button onClick={() => navigate('/analitica')} className="finz-btn finz-btn--ghost">
                            Ver Analítica
                        </button>
                    </div>
                )}
            </div>

            {/* KPI Cards */}
            <div className="row g-3 mb-4">
                <div className="col-md-4">
                    <div className="finz-stat-card finz-stat-card--saldo">
                        <div className="finz-stat-card__label">Saldo disponible</div>
                        <div className={`finz-stat-card__value ${saldoTotal >= 0 ? 'finz-stat-card__value--positive' : 'finz-stat-card__value--negative'}`}>
                            {formatoMoneda(saldoTotal)}
                        </div>
                        <div className="finz-stat-card__sub">
                            {saldoTotal === 0 ? 'Agrega tus cuentas para ver tu saldo' : 'Total en tus cuentas'}
                        </div>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="finz-stat-card finz-stat-card--ingreso">
                        <div className="finz-stat-card__label">Total ingresos</div>
                        <div className="finz-stat-card__value finz-stat-card__value--positive">
                            {formatoMoneda(ingresos)}
                        </div>
                        <div className="finz-stat-card__sub">Dinero que ha entrado</div>
                    </div>
                </div>
                <div className="col-md-4">
                    <div className="finz-stat-card finz-stat-card--gasto">
                        <div className="finz-stat-card__label">Total gastos</div>
                        <div className="finz-stat-card__value finz-stat-card__value--negative">
                            {formatoMoneda(gastos)}
                        </div>
                        <div className="finz-stat-card__sub">Dinero que ha salido</div>
                    </div>
                </div>
            </div>

            {/* Formulario de nuevo movimiento */}
            <FormularioMovimiento alGuardar={cargarDatos} />

            {/* Cuentas y Metas */}
            <div className="row g-3 mb-4">
                <div className="col-md-6">
                    <Cuentas />
                </div>
                <div className="col-md-6">
                    {esPremium ? (
                        <Metas />
                    ) : (
                        <div className="finz-premium-lock">
                            <Metas />
                            <div className="finz-premium-lock__overlay">
                                <div className="finz-premium-lock__icon">🔒</div>
                                <div className="finz-premium-lock__title">Función Premium</div>
                                <div className="finz-premium-lock__sub">Actualiza tu plan para gestionar metas</div>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Deudas */}
            <div className="finz-card mb-4">
                <div className="finz-card__title">Gestión de Obligaciones</div>
                <Deudas />
            </div>

            {/* Historial de movimientos */}
            <div className="finz-card">
                <div className="finz-card__title">Historial de Movimientos</div>
                <ListaMovimientos
                    movimientos={movimientos}
                    formatoMoneda={formatoMoneda}
                    onEliminar={eliminarMovimiento}
                />
            </div>
        </div>
    );
}
