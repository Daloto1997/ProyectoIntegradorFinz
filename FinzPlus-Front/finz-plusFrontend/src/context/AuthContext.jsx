import { createContext, useContext, useState, useCallback } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [usuario, setUsuario] = useState(() => {
        try {
            const stored = localStorage.getItem('finz_usuario_sesion');
            return stored ? JSON.parse(stored) : null;
        } catch {
            return null;
        }
    });

    const login = useCallback((datosUsuario) => {
        localStorage.setItem('finz_usuario_sesion', JSON.stringify(datosUsuario));
        setUsuario(datosUsuario);
    }, []);

    const logout = useCallback(() => {
        localStorage.removeItem('finz_usuario_sesion');
        setUsuario(null);
    }, []);

    const esPremium = usuario?.rol === 'PREMIUM' || usuario?.rol === 'ADMIN';
    const esAdmin  = usuario?.rol === 'ADMIN';

    return (
        <AuthContext.Provider value={{ usuario, login, logout, esPremium, esAdmin }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider');
    return ctx;
}
