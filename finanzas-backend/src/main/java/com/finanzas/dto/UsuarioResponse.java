package com.finanzas.dto;

import com.finanzas.modelo.RolUsuario;
import com.finanzas.modelo.Usuario;

import java.time.LocalDateTime;

public record UsuarioResponse(
        Long id,
        String nombre,
        String email,
        String telefono,
        String direccion,
        LocalDateTime fechaCreacion,
        RolUsuario rol
) {

    public static UsuarioResponse from(Usuario usuario) {
        return new UsuarioResponse(
                usuario.getId(),
                usuario.getNombre(),
                usuario.getEmail(),
                usuario.getTelefono(),
                usuario.getDireccion(),
                usuario.getFechaCreacion(),
                usuario.getRol()
        );
    }
}
