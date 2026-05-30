package com.finanzas.controlador;

import com.finanzas.modelo.Deuda;
import com.finanzas.servicio.DeudaService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/deudas")
@RequiredArgsConstructor
public class DeudaController {

    private final DeudaService deudaService;

    @PostMapping
    public ResponseEntity<Deuda> create(@RequestBody Deuda deuda) {
        return ResponseEntity.status(HttpStatus.CREATED).body(deudaService.save(deuda));
    }

    @GetMapping
    public ResponseEntity<List<Deuda>> findAll(@RequestParam(required = false) String usuarioEmail) {
        return ResponseEntity.ok(deudaService.findAll(usuarioEmail));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Deuda> findById(@PathVariable Long id) {
        return ResponseEntity.ok(deudaService.findById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Deuda> update(@PathVariable Long id, @RequestBody Deuda deuda) {
        return ResponseEntity.ok(deudaService.update(id, deuda));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        deudaService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
