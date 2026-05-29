package com.finanzas.servicio;

import com.finanzas.excepcion.ResourceNotFoundException;
import com.finanzas.modelo.Categoria;
import com.finanzas.repositorio.CategoriaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class CategoriaService {

    private final CategoriaRepository categoriaRepository;

    @Transactional
    public Categoria save(Categoria categoria) {
        return categoriaRepository.save(categoria);
    }

    public List<Categoria> findAll() {
        return categoriaRepository.findAll();
    }

    public List<Categoria> findByTipo(String tipo) {
        return categoriaRepository.findByTipo(tipo);
    }

    public Categoria findById(Long id) {
        return categoriaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con id: " + id));
    }

    @Transactional
    public Categoria update(Long id, Categoria categoriaActualizada) {
        Categoria existente = findById(id);
        existente.setNombre(categoriaActualizada.getNombre());
        existente.setTipo(categoriaActualizada.getTipo());
        existente.setColor(categoriaActualizada.getColor());
        return categoriaRepository.save(existente);
    }

    @Transactional
    public void deleteById(Long id) {
        findById(id);
        categoriaRepository.deleteById(id);
    }
}
