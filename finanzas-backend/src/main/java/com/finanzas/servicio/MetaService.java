package com.finanzas.servicio;

import com.finanzas.excepcion.ResourceNotFoundException;
import com.finanzas.modelo.Meta;
import com.finanzas.repositorio.MetaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class MetaService {

    private final MetaRepository metaRepository;

    @Transactional
    public Meta save(Meta meta) {
        return metaRepository.save(meta);
    }

    public List<Meta> findAll(String usuarioEmail) {
        if (usuarioEmail != null && !usuarioEmail.isBlank()) {
            return metaRepository.findByUsuarioEmail(usuarioEmail);
        }
        return metaRepository.findAll();
    }

    public Meta findById(Long id) {
        return metaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Meta no encontrada con id: " + id));
    }

    @Transactional
    public Meta update(Long id, Meta metaActualizada) {
        Meta existente = findById(id);
        existente.setNombre(metaActualizada.getNombre());
        existente.setMontoObjetivo(metaActualizada.getMontoObjetivo());
        existente.setMontoActual(metaActualizada.getMontoActual());
        existente.setFechaLimite(metaActualizada.getFechaLimite());
        return metaRepository.save(existente);
    }

    @Transactional
    public void deleteById(Long id) {
        findById(id);
        metaRepository.deleteById(id);
    }
}
