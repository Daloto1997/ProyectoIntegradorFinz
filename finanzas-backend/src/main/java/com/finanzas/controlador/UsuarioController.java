package com.finanzas.controlador;

import com.finanzas.dto.UsuarioResponse;
import com.finanzas.modelo.RolUsuario;
import com.finanzas.modelo.Usuario;
import com.finanzas.servicio.UsuarioService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/usuarios")
@RequiredArgsConstructor
public class UsuarioController {

    private final UsuarioService usuarioService;

    @PostMapping
    public ResponseEntity<UsuarioResponse> create(@RequestBody Usuario usuario) {
        Usuario guardado = usuarioService.save(usuario);
        return ResponseEntity.status(HttpStatus.CREATED).body(UsuarioResponse.from(guardado));
    }

    @GetMapping
    public ResponseEntity<List<UsuarioResponse>> findAll() {
        return ResponseEntity.ok(
            usuarioService.findAll().stream().map(UsuarioResponse::from).toList()
        );
    }

    @GetMapping("/{id}")
    public ResponseEntity<UsuarioResponse> findById(@PathVariable Long id) {
        return ResponseEntity.ok(UsuarioResponse.from(usuarioService.findById(id)));
    }

    @PutMapping("/{id}")
    public ResponseEntity<UsuarioResponse> update(@PathVariable Long id, @RequestBody Usuario usuario) {
        return ResponseEntity.ok(UsuarioResponse.from(usuarioService.update(id, usuario)));
    }

    // PATCH /usuarios/{id}/rol — usado por el panel admin para cambiar roles
    @PatchMapping("/{id}/rol")
    public ResponseEntity<UsuarioResponse> cambiarRol(@PathVariable Long id, @RequestBody Map<String, String> body) {
        String rolStr = body.get("rol");
        RolUsuario nuevoRol = RolUsuario.valueOf(rolStr.toUpperCase());
        return ResponseEntity.ok(UsuarioResponse.from(usuarioService.cambiarRol(id, nuevoRol)));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        usuarioService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
