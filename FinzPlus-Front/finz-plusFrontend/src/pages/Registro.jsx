import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { finzService } from '../services/finzService';

export default function Registro() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [error,       setError]       = useState('');
    const [exito,       setExito]       = useState(false);
    const [cargando,    setCargando]    = useState(false);
    const [planElegido, setPlanElegido] = useState('CLIENTE');
    const navigate = useNavigate();

    const alEnviar = async (datos) => {
        setError('');
        setCargando(true);
        try {
            await finzService.registrarUsuario(datos);
            setExito(true);
            setTimeout(() => navigate('/'), 2000);
        } catch (err) {
            const msg = err?.message || '';
            if (msg.toLowerCase().includes('correo') || msg.toLowerCase().includes('email') || msg.includes('409') || msg.includes('already')) {
                setError('Ese correo ya está registrado. Prueba con otro o inicia sesión.');
            } else {
                setError(msg || 'No se pudo crear la cuenta. Intenta de nuevo.');
            }
        } finally {
            setCargando(false);
        }
    };

    return (
        <div className="finz-auth-page" style={{ alignItems: 'flex-start', paddingTop: '40px' }}>
            <div className="finz-auth-card" style={{ maxWidth: '480px' }}>
                <div className="finz-auth-card__logo">Finz<span>+</span></div>
                <div className="finz-auth-card__subtitle">Crea tu cuenta en FinzPlus</div>

                {error  && <div className="finz-alert finz-alert--danger">{error}</div>}
                {exito  && <div className="finz-alert finz-alert--success">¡Cuenta creada! Redirigiendo al login...</div>}

                <form onSubmit={handleSubmit(alEnviar)}>
                    <div className="mb-3">
                        <label className="finz-label">Nombres completos</label>
                        <input
                            type="text"
                            className={`finz-input ${errors.nombre ? 'error' : ''}`}
                            {...register('nombre', { required: 'El nombre es obligatorio' })}
                        />
                        {errors.nombre && <div className="finz-error-msg">{errors.nombre.message}</div>}
                    </div>

                    <div className="mb-3">
                        <label className="finz-label">Correo electrónico</label>
                        <input
                            type="email"
                            className={`finz-input ${errors.email ? 'error' : ''}`}
                            placeholder="ejemplo@correo.com"
                            {...register('email', {
                                required: 'El correo es obligatorio',
                                pattern: { value: /^\S+@\S+$/i, message: 'Formato de correo inválido' }
                            })}
                        />
                        {errors.email && <div className="finz-error-msg">{errors.email.message}</div>}
                    </div>

                    <div className="mb-3">
                        <label className="finz-label">Contraseña</label>
                        <input
                            type="password"
                            autoComplete="new-password"
                            className={`finz-input ${errors.password ? 'error' : ''}`}
                            placeholder="Mínimo 4 caracteres"
                            {...register('password', {
                                required: 'La contraseña es obligatoria',
                                minLength: { value: 4, message: 'Mínimo 4 caracteres' }
                            })}
                        />
                        {errors.password && <div className="finz-error-msg">{errors.password.message}</div>}
                    </div>

                    <div className="row g-3 mb-3">
                        <div className="col-6">
                            <label className="finz-label">Teléfono / Celular</label>
                            <input
                                type="tel"
                                className={`finz-input ${errors.telefono ? 'error' : ''}`}
                                placeholder="3001234567"
                                {...register('telefono', {
                                    required: 'El teléfono es obligatorio',
                                    pattern: { value: /^[0-9]+$/, message: 'Solo números' }
                                })}
                            />
                            {errors.telefono && <div className="finz-error-msg">{errors.telefono.message}</div>}
                        </div>
                        <div className="col-6">
                            <label className="finz-label">Ciudad</label>
                            <input
                                type="text"
                                className={`finz-input ${errors.direccion ? 'error' : ''}`}
                                placeholder="Medellín"
                                {...register('direccion', { required: 'La ciudad es obligatoria' })}
                            />
                            {errors.direccion && <div className="finz-error-msg">{errors.direccion.message}</div>}
                        </div>
                    </div>

                    <div className="mb-3">
                        <label className="finz-label">Plan</label>
                        <div style={{ display: 'flex', gap: '10px' }}>
                            {[
                                { value: 'CLIENTE', label: 'Gratuito', desc: 'Dashboard, cuentas y deudas', color: '#25c974' },
                                { value: 'PREMIUM', label: 'Premium',  desc: 'Todo + metas y analítica',   color: '#7c3aed' },
                            ].map(plan => {
                                const seleccionado = planElegido === plan.value;
                                return (
                                    <label key={plan.value} onClick={() => setPlanElegido(plan.value)} style={{
                                        flex: 1,
                                        border: `2px solid ${seleccionado ? plan.color : 'var(--finz-border)'}`,
                                        borderRadius: '10px',
                                        padding: '12px',
                                        cursor: 'pointer',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        gap: '4px',
                                        background: seleccionado ? `${plan.color}15` : 'white',
                                        transition: 'all 0.2s ease',
                                    }}>
                                        <input type="radio" value={plan.value} {...register('rol')} style={{ display: 'none' }} defaultChecked={plan.value === 'CLIENTE'} />
                                        <span style={{ fontWeight: 700, fontSize: '14px', color: seleccionado ? plan.color : 'var(--finz-dark)' }}>
                                            {seleccionado ? '✓ ' : ''}{plan.label}
                                        </span>
                                        <span style={{ fontSize: '11px', color: 'var(--finz-gray-400)' }}>{plan.desc}</span>
                                    </label>
                                );
                            })}
                        </div>
                    </div>

                    <button type="submit" disabled={cargando || exito} className="finz-btn finz-btn--primary w-100">
                        {cargando ? 'Creando cuenta...' : 'Crear cuenta'}
                    </button>
                </form>

                <div className="finz-auth-card__footer">
                    ¿Ya tienes cuenta? <Link to="/">Inicia sesión</Link>
                </div>
            </div>
        </div>
    );
}
