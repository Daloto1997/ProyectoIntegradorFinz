package com.finanzas.controlador;

import com.finanzas.modelo.Meta;
import com.finanzas.servicio.MetaService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/metas")
@RequiredArgsConstructor
public class MetaController {

    private final MetaService metaService;

    @PostMapping
    public ResponseEntity<Meta> create(@RequestBody Meta meta) {
        return ResponseEntity.status(HttpStatus.CREATED).body(metaService.save(meta));
    }

    @GetMapping
    public ResponseEntity<List<Meta>> findAll(@RequestParam(required = false) String usuarioEmail) {
        return ResponseEntity.ok(metaService.findAll(usuarioEmail));
    }

    @GetMapping("/{id}")
    public ResponseEntity<Meta> findById(@PathVariable Long id) {
        return ResponseEntity.ok(metaService.findById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Meta> update(@PathVariable Long id, @RequestBody Meta meta) {
        return ResponseEntity.ok(metaService.update(id, meta));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        metaService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
