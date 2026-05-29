package com.finanzas.servicio;

import com.finanzas.excepcion.ResourceNotFoundException;
import com.finanzas.modelo.RolUsuario;
import com.finanzas.modelo.Usuario;
import com.finanzas.repositorio.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UsuarioService {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional
    public Usuario save(Usuario usuario) {
        if (usuario.getPassword() != null && !usuario.getPassword().startsWith("$2")) {
            usuario.setPassword(passwordEncoder.encode(usuario.getPassword()));
        }
        // El primer usuario registrado se convierte en ADMIN automáticamente
        if (usuarioRepository.count() == 0) {
            usuario.setRol(RolUsuario.ADMIN);
        } else if (usuario.getRol() == null) {
            usuario.setRol(RolUsuario.CLIENTE);
        }
        return usuarioRepository.save(usuario);
    }

    public Optional<Usuario> findByEmail(String email) {
        return usuarioRepository.findByEmail(email);
    }

    public List<Usuario> findAll() {
        return usuarioRepository.findAll();
    }

    public Usuario findById(Long id) {
        return usuarioRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Usuario no encontrado con id: " + id));
    }

    @Transactional
    public Usuario update(Long id, Usuario usuarioActualizado) {
        Usuario existente = findById(id);
        existente.setNombre(usuarioActualizado.getNombre());
        existente.setEmail(usuarioActualizado.getEmail());
        existente.setTelefono(usuarioActualizado.getTelefono());
        existente.setDireccion(usuarioActualizado.getDireccion());
        // Solo actualizar el password si viene uno nuevo en el request
        if (usuarioActualizado.getPassword() != null && !usuarioActualizado.getPassword().isEmpty()) {
            existente.setPassword(passwordEncoder.encode(usuarioActualizado.getPassword()));
        }
        return usuarioRepository.save(existente);
    }

    @Transactional
    public Usuario cambiarRol(Long id, RolUsuario nuevoRol) {
        Usuario usuario = findById(id);
        usuario.setRol(nuevoRol);
        return usuarioRepository.save(usuario);
    }

    @Transactional
    public void deleteById(Long id) {
        findById(id);
        usuarioRepository.deleteById(id);
    }
}
