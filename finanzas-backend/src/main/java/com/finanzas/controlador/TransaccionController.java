package com.finanzas.controlador;

import com.finanzas.dto.TransaccionRequest;
import com.finanzas.modelo.Transaccion;
import com.finanzas.servicio.TransaccionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/transacciones")
@RequiredArgsConstructor
public class TransaccionController {

    private final TransaccionService transaccionService;

    @PostMapping
    public ResponseEntity<Transaccion> create(@RequestBody TransaccionRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(transaccionService.save(request));
    }

    @GetMapping
    public ResponseEntity<List<Transaccion>> findAll() {
        return ResponseEntity.ok(transaccionService.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Transaccion> findById(@PathVariable Long id) {
        return ResponseEntity.ok(transaccionService.findById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Transaccion> update(@PathVariable Long id, @RequestBody TransaccionRequest request) {
        return ResponseEntity.ok(transaccionService.update(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        transaccionService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
