/* 📂 ARCHIVO: src/services/finzService.js (SINCRO TOTAL) */

// Usamos proxy Vite para evitar bloqueos CORS en desarrollo.
const API_BASE = '/api';
const AUTH_BASE = `${API_BASE}/auth`;

const KEYS = {
    USUARIO: 'finz_usuario_sesion',
    MOVIMIENTOS: 'finz_movimientos',
    CUENTAS: 'finz_cuentas',
    METAS: 'finz_metas',
    DEUDAS_KEY: 'finz_deudas'
};

export const finzService = {
    // --- 🔑 HU 04: Login de Usuarios ---
    loginUsuario: async (email, password) => {
        try {
            // Intentamos POST primero.
            const response = await fetch(`${AUTH_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                if ([403, 405, 415].includes(response.status)) {
                    const formResponse = await fetch(`${AUTH_BASE}/login`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        credentials: 'include',
                        body: new URLSearchParams({ email, password }).toString()
                    });

                    if (formResponse.ok) {
                        const usuarioLogueado = await formResponse.json();
                        localStorage.setItem(KEYS.USUARIO, JSON.stringify(usuarioLogueado));
                        return usuarioLogueado;
                    }

                    if (formResponse.status === 401) throw new Error('Credenciales incorrectas');
                    let mensajeErrorForm = formResponse.statusText;
                    try {
                        const payload = await formResponse.json();
                        if (payload?.message) mensajeErrorForm = payload.message;
                    } catch (parseError) {
                        console.warn('No se pudo parsear el error de login form:', parseError);
                    }
                    throw new Error(`Error en el servidor al iniciar sesión (form): ${mensajeErrorForm}`);
                }

                if (response.status === 401) throw new Error('Credenciales incorrectas');

                let mensajeError = response.statusText;
                try {
                    const payload = await response.json();
                    if (payload?.message) mensajeError = payload.message;
                } catch (parseError) {
                    console.warn('No se pudo parsear el error de login:', parseError);
                }
                throw new Error(`Error en el servidor al iniciar sesión: ${mensajeError}`);
            }

            const usuarioLogueado = await response.json();
            localStorage.setItem(KEYS.USUARIO, JSON.stringify(usuarioLogueado));
            return usuarioLogueado;
        } catch (error) {
            console.error('Error en loginUsuario:', error);
            throw error;
        }
    },

    // --- 📝 HU 05: Registro de Usuarios ---
    registrarUsuario: async (datosUsuario) => {
        try {
            const response = await fetch(`${API_BASE}/usuarios`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(datosUsuario)
            });

            if (!response.ok) {
                let mensajeError = response.statusText;
                try {
                    const payload = await response.json();
                    if (payload?.message) mensajeError = payload.message;
                    else if (typeof payload === 'string') mensajeError = payload;
                } catch {
                    const texto = await response.text().catch(() => '');
                    if (texto) mensajeError = texto;
                }

                throw new Error(`Error al registrar el usuario: ${response.status} ${mensajeError}`);
            }

            return true;
        } catch (error) {
            console.error('Error en registrarUsuario:', error);
            throw error;
        }
    },

    obtenerUsuarioLogueado: () => {
        return JSON.parse(localStorage.getItem(KEYS.USUARIO));
    },

    adjuntarUsuario: (payload) => {
        const usuario = finzService.obtenerUsuarioLogueado();
        return usuario?.email ? { ...payload, usuarioEmail: usuario.email } : payload;
    },

    leerLocal: (key) => {
        return JSON.parse(localStorage.getItem(key)) || [];
    },

    escribirLocal: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },

    emailParam: () => {
        const u = finzService.obtenerUsuarioLogueado();
        return u?.email ? `?usuarioEmail=${encodeURIComponent(u.email)}` : '';
    },

    obtenerCategorias: async () => {
        try {
            const response = await fetch(`${API_BASE}/categorias`, {
                credentials: 'include'
            });
            if (!response.ok) throw new Error('No se pudo cargar la lista de categorías');
            const payload = await response.json();
            return Array.isArray(payload) ? payload : Array.isArray(payload?.data) ? payload.data : [];
        } catch (error) {
            console.warn('Error al obtener categorías:', error);
            return [
                { id: 1, nombre: 'Alimentación', tipo: 'GASTO' },
                { id: 2, nombre: 'Transporte', tipo: 'GASTO' },
                { id: 3, nombre: 'Hogar', tipo: 'GASTO' },
                { id: 4, nombre: 'Ocio', tipo: 'GASTO' }
            ];
        }
    },

    obtenerTransacciones: async () => {
        try {
            const response = await fetch(`${API_BASE}/transacciones${finzService.emailParam()}`, {
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudieron cargar las transacciones:', response.status);
                return finzService.leerLocal(KEYS.MOVIMIENTOS);
            }
            const payload = await response.json();
            const transacciones = Array.isArray(payload) ? payload : payload?.data ?? [];
            if (transacciones.length === 0) {
                return finzService.leerLocal(KEYS.MOVIMIENTOS);
            }
            return transacciones;
        } catch (error) {
            console.warn('Error al obtener transacciones:', error);
            return finzService.leerLocal(KEYS.MOVIMIENTOS);
        }
    },

    guardarTransaccion: async (transaccion) => {
        // El backend ahora espera un TransaccionRequest con cuentaId y categoriaId (no objetos anidados)
        const cuentaId    = transaccion.cuenta?.id ?? transaccion.cuenta ?? null;
        const categoriaId = transaccion.categoria?.id ?? transaccion.categoria ?? null;
        const monto       = Math.abs(Number(transaccion.monto));
        const payload = {
            cuentaId,
            categoriaId,
            descripcion: transaccion.descripcion || transaccion.concepto || '',
            monto: (transaccion.tipo || '').toUpperCase() === 'GASTO' ? -monto : monto,
            tipo: (transaccion.tipo || 'GASTO').toUpperCase(),
            fecha: transaccion.fecha || new Date().toISOString().slice(0, 19),
        };
        const payloadConUsuario = finzService.adjuntarUsuario(payload);

        try {
            const response = await fetch(`${API_BASE}/transacciones`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(payloadConUsuario)
            });

            if (!response.ok) {
                let mensajeError = response.statusText;
                try {
                    const body = await response.json();
                    if (body?.message) mensajeError = body.message;
                    else if (typeof body === 'string') mensajeError = body;
                } catch {
                    const texto = await response.text().catch(() => '');
                    if (texto) {
                        mensajeError = texto;
                        console.error('Respuesta del servidor (transacciones):', texto);
                    }
                }
                const transacciones = finzService.leerLocal(KEYS.MOVIMIENTOS);
                transacciones.push(payload);
                finzService.escribirLocal(KEYS.MOVIMIENTOS, transacciones);
                throw new Error(`Error backend guardando transacción: ${response.status} ${mensajeError}`);
            }

            const saved = await response.json();
            return saved;
        } catch (error) {
            console.warn('Error en guardarTransaccion, fallback a local:', error);
            const transacciones = finzService.leerLocal(KEYS.MOVIMIENTOS);
            transacciones.push(payload);
            finzService.escribirLocal(KEYS.MOVIMIENTOS, transacciones);
            throw error;
        }
    },

    obtenerCuentas: async () => {
        try {
            const response = await fetch(`${API_BASE}/cuentas${finzService.emailParam()}`, {
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudieron cargar las cuentas:', response.status);
                return finzService.leerLocal(KEYS.CUENTAS);
            }
            const payload = await response.json();
            const cuentas = Array.isArray(payload) ? payload : payload?.data ?? [];
            return cuentas.length ? cuentas : finzService.leerLocal(KEYS.CUENTAS);
        } catch (error) {
            console.warn('Error al obtener cuentas:', error);
            return finzService.leerLocal(KEYS.CUENTAS);
        }
    },

    guardarCuenta: async (cuenta) => {
        const payload = {
            nombre: cuenta.nombre,
            tipo: cuenta.tipo ?? 'AHORROS',
            saldoActual: cuenta.saldoActual ?? cuenta.saldo ?? 0
        };
        const payloadConUsuario = finzService.adjuntarUsuario(payload);

        try {
            const response = await fetch(`${API_BASE}/cuentas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(payloadConUsuario)
            });
            if (!response.ok) {
                let mensajeError = response.statusText;
                try {
                    const body = await response.json();
                    if (body?.message) mensajeError = body.message;
                    else if (typeof body === 'string') mensajeError = body;
                } catch {
                    const texto = await response.text().catch(() => '');
                    if (texto) {
                        mensajeError = texto;
                        console.error('Respuesta del servidor (cuentas):', texto);
                    }
                }
                const cuentas = finzService.leerLocal(KEYS.CUENTAS);
                cuentas.push(payload);
                finzService.escribirLocal(KEYS.CUENTAS, cuentas);
                throw new Error(`Error backend guardando cuenta: ${response.status} ${mensajeError}`);
            }
            const saved = await response.json();
            return saved;
        } catch (error) {
            console.warn('Error en guardarCuenta, fallback a local:', error);
            const cuentas = finzService.leerLocal(KEYS.CUENTAS);
            cuentas.push(payload);
            finzService.escribirLocal(KEYS.CUENTAS, cuentas);
            throw error;
        }
    },

    obtenerDeudas: async () => {
        try {
            const response = await fetch(`${API_BASE}/deudas${finzService.emailParam()}`, {
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudieron cargar las deudas:', response.status);
                return finzService.leerLocal(KEYS.DEUDAS_KEY).filter(deuda => !usuarioEmail || deuda.usuarioEmail === usuarioEmail);
            }
            const payload = await response.json();
            const deudas = Array.isArray(payload) ? payload : payload?.data ?? [];
            return deudas.length ? deudas : finzService.leerLocal(KEYS.DEUDAS_KEY);
        } catch (error) {
            console.warn('Error al obtener deudas:', error);
            return finzService.leerLocal(KEYS.DEUDAS_KEY);
        }
    },

    guardarDeuda: async (nuevaDeuda) => {
        const payload = finzService.adjuntarUsuario({
            personaEntidad: nuevaDeuda.acreedor || nuevaDeuda.personaEntidad || '',
            montoTotal: nuevaDeuda.montoTotal,
            montoPagado: nuevaDeuda.montoPagado ?? 0,
            tipo: nuevaDeuda.tipo || 'POR_PAGAR',
            fechaVencimiento: nuevaDeuda.fechaVencimiento || null
        });

        try {
            const response = await fetch(`${API_BASE}/deudas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                console.warn('No se pudo guardar la deuda en backend:', response.status);
                try {
                    const texto = await response.text();
                    console.error('Respuesta del servidor:', texto);
                } catch (e) { console.warn('No se pudo leer body de respuesta:', e); }
                const deudas = finzService.leerLocal(KEYS.DEUDAS_KEY);
                const deudaLocal = { ...payload, id: Date.now() };
                deudas.push(deudaLocal);
                finzService.escribirLocal(KEYS.DEUDAS_KEY, deudas);
                return deudaLocal;
            }
            const saved = await response.json();
            return saved;
        } catch (error) {
            console.warn('Error en guardarDeuda, fallback a local:', error);
            const deudas = finzService.leerLocal(KEYS.DEUDAS_KEY);
            const deudaLocal = { ...payload, id: Date.now() };
            deudas.push(deudaLocal);
            finzService.escribirLocal(KEYS.DEUDAS_KEY, deudas);
            return deudaLocal;
        }
    },

    actualizarDeuda: async (id, cambios) => {
        try {
            const response = await fetch(`${API_BASE}/deudas/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(cambios)
            });
            if (!response.ok) {
                let mensajeError = response.statusText;
                try {
                    const payload = await response.json();
                    if (payload?.message) mensajeError = payload.message;
                } catch (error) {
                    console.warn('No se pudo parsear el error al actualizar deuda:', error);
                }
                throw new Error(`Error al actualizar la deuda: ${mensajeError}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error en actualizarDeuda:', error);
            throw error;
        }
    },

    obtenerMetas: async () => {
        try {
            const response = await fetch(`${API_BASE}/metas${finzService.emailParam()}`, {
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudieron cargar las metas:', response.status);
                return finzService.leerLocal(KEYS.METAS);
            }
            const payload = await response.json();
            const metas = Array.isArray(payload) ? payload : payload?.data ?? [];
            return metas.length ? metas : finzService.leerLocal(KEYS.METAS);
        } catch (error) {
            console.warn('Error al obtener metas:', error);
            return finzService.leerLocal(KEYS.METAS);
        }
    },

    guardarMeta: async (meta) => {
        const payload = finzService.adjuntarUsuario({
            nombre: meta.nombre || meta.titulo || '',
            montoObjetivo: meta.montoObjetivo,
            montoActual: meta.montoActual ?? 0,
            fechaLimite: meta.fechaLimite || null
        });

        try {
            const response = await fetch(`${API_BASE}/metas`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                let mensajeError = response.statusText;
                try {
                    const body = await response.json();
                    if (body?.message) mensajeError = body.message;
                    else if (typeof body === 'string') mensajeError = body;
                } catch {
                    const texto = await response.text().catch(() => '');
                    if (texto) mensajeError = texto;
                }
                const metas = finzService.leerLocal(KEYS.METAS);
                const metaLocal = { ...payload, id: Date.now() };
                metas.push(metaLocal);
                finzService.escribirLocal(KEYS.METAS, metas);
                throw new Error(`Error backend guardando meta: ${response.status} ${mensajeError}`);
            }
            const saved = await response.json();
            return saved;
        } catch (error) {
            console.warn('Error en guardarMeta, fallback a local:', error);
            const metas = finzService.leerLocal(KEYS.METAS);
            const metaLocal = { ...payload, id: Date.now() };
            metas.push(metaLocal);
            finzService.escribirLocal(KEYS.METAS, metas);
            throw error;
        }
    },

    actualizarMeta: async (id, cambios) => {
        try {
            const response = await fetch(`${API_BASE}/metas/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(cambios)
            });
            if (!response.ok) throw new Error(response.statusText);
            return await response.json();
        } catch (error) {
            console.error('Error en actualizarMeta:', error);
            throw error;
        }
    },

    eliminarCuenta: async (id) => {
        try {
            const response = await fetch(`${API_BASE}/cuentas/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudo eliminar la cuenta en backend:', response.status);
                // fallback: remove from local
                const cuentas = finzService.leerLocal(KEYS.CUENTAS).filter(c => String(c.id) !== String(id));
                finzService.escribirLocal(KEYS.CUENTAS, cuentas);
                return false;
            }
            return true;
        } catch (error) {
            console.warn('Error en eliminarCuenta, fallback local:', error);
            const cuentas = finzService.leerLocal(KEYS.CUENTAS).filter(c => String(c.id) !== String(id));
            finzService.escribirLocal(KEYS.CUENTAS, cuentas);
            return false;
        }
    },

    eliminarTransaccion: async (id) => {
        try {
            const response = await fetch(`${API_BASE}/transacciones/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudo eliminar la transacción en backend:', response.status);
                const trans = finzService.leerLocal(KEYS.MOVIMIENTOS).filter(t => String(t.id) !== String(id));
                finzService.escribirLocal(KEYS.MOVIMIENTOS, trans);
                return false;
            }
            return true;
        } catch (error) {
            console.warn('Error en eliminarTransaccion, fallback local:', error);
            const trans = finzService.leerLocal(KEYS.MOVIMIENTOS).filter(t => String(t.id) !== String(id));
            finzService.escribirLocal(KEYS.MOVIMIENTOS, trans);
            return false;
        }
    },

    eliminarMeta: async (id) => {
        try {
            const response = await fetch(`${API_BASE}/metas/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudo eliminar la meta en backend:', response.status);
                const metas = finzService.leerLocal(KEYS.METAS).filter(m => String(m.id) !== String(id));
                finzService.escribirLocal(KEYS.METAS, metas);
                return false;
            }
            return true;
        } catch (error) {
            console.warn('Error en eliminarMeta, fallback local:', error);
            const metas = finzService.leerLocal(KEYS.METAS).filter(m => String(m.id) !== String(id));
            finzService.escribirLocal(KEYS.METAS, metas);
            return false;
        }
    },

    eliminarDeuda: async (id) => {
        try {
            const response = await fetch(`${API_BASE}/deudas/${id}`, {
                method: 'DELETE',
                credentials: 'include'
            });
            if (!response.ok) {
                console.warn('No se pudo eliminar la deuda en backend:', response.status);
                const deudas = finzService.leerLocal(KEYS.DEUDAS_KEY).filter(d => String(d.id) !== String(id));
                finzService.escribirLocal(KEYS.DEUDAS_KEY, deudas);
                return false;
            }
            return true;
        } catch (error) {
            console.warn('Error en eliminarDeuda, fallback local:', error);
            const deudas = finzService.leerLocal(KEYS.DEUDAS_KEY).filter(d => String(d.id) !== String(id));
            finzService.escribirLocal(KEYS.DEUDAS_KEY, deudas);
            return false;
        }
    },

    obtenerMovimientos: () => {
        return JSON.parse(localStorage.getItem(KEYS.MOVIMIENTOS)) || [];
    },

    cerrarSesion: () => {
        localStorage.removeItem(KEYS.USUARIO);
    },

    guardarMovimiento: (nuevoMovimiento) => {
        const todos = JSON.parse(localStorage.getItem(KEYS.MOVIMIENTOS)) || [];
        todos.push(nuevoMovimiento);
        localStorage.setItem(KEYS.MOVIMIENTOS, JSON.stringify(todos));
    }
};

export default finzService;
