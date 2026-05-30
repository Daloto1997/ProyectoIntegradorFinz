import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Cuentas from '../components/Cuentas';

export default function Setup() {
    const { usuario } = useAuth();
    const navigate = useNavigate();
    const [listo, setListo] = useState(false);

    return (
        <div style={{ minHeight: '100vh', background: 'var(--finz-bg)', display: 'flex', alignItems: 'flex-start', justifyContent: 'center', paddingTop: '40px' }}>
            <div style={{ width: '100%', maxWidth: '560px', padding: '0 16px 40px' }}>

                {/* Encabezado de bienvenida */}
                <div style={{ textAlign: 'center', marginBottom: '32px' }}>
                    <div style={{ fontSize: '40px', marginBottom: '8px' }}>👋</div>
                    <h2 style={{ fontWeight: 700, color: 'var(--finz-dark)', margin: 0 }}>
                        Bienvenido, {usuario?.nombre?.split(' ')[0]}
                    </h2>
                    <p style={{ color: 'var(--finz-gray-500)', marginTop: '8px', fontSize: '15px' }}>
                        Antes de continuar, registra las cuentas donde guardas tu dinero.<br />
                        Así podrás asignarlas al registrar tus movimientos.
                    </p>

                    {/* Pasos */}
                    <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginTop: '20px' }}>
                        {['Registrar cuentas', 'Ir al Dashboard'].map((paso, i) => (
                            <div key={paso} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                <div style={{
                                    width: '24px', height: '24px', borderRadius: '50%', fontSize: '12px',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700,
                                    background: i === 0 ? 'var(--finz-primary)' : 'var(--finz-border)',
                                    color: i === 0 ? 'white' : 'var(--finz-gray-400)',
                                }}>
                                    {i + 1}
                                </div>
                                <span style={{ fontSize: '13px', color: i === 0 ? 'var(--finz-dark)' : 'var(--finz-gray-400)', fontWeight: i === 0 ? 600 : 400 }}>
                                    {paso}
                                </span>
                                {i < 1 && <span style={{ color: 'var(--finz-border)', margin: '0 4px' }}>→</span>}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Formulario de cuentas */}
                <Cuentas />

                {/* Botón continuar */}
                <div style={{ marginTop: '20px' }}>
                    <label style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px', cursor: 'pointer' }}>
                        <input type="checkbox" checked={listo} onChange={e => setListo(e.target.checked)} />
                        <span style={{ fontSize: '14px', color: 'var(--finz-gray-600)' }}>
                            Ya agregué mis cuentas, quiero continuar al Dashboard
                        </span>
                    </label>
                    <button
                        disabled={!listo}
                        onClick={() => navigate('/dashboard')}
                        className="finz-btn finz-btn--primary w-100"
                        style={{ opacity: listo ? 1 : 0.5 }}
                    >
                        Ir al Dashboard →
                    </button>
                    <button
                        onClick={() => navigate('/dashboard')}
                        style={{ width: '100%', marginTop: '10px', background: 'none', border: 'none', color: 'var(--finz-gray-400)', fontSize: '13px', cursor: 'pointer' }}
                    >
                        Omitir por ahora
                    </button>
                </div>
            </div>
        </div>
    );
}
