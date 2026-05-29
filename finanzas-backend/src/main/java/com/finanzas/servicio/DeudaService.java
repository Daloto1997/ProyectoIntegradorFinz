package com.finanzas.servicio;

import com.finanzas.excepcion.ResourceNotFoundException;
import com.finanzas.modelo.Deuda;
import com.finanzas.repositorio.DeudaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class DeudaService {

    private final DeudaRepository deudaRepository;

    @Transactional
    public Deuda save(Deuda deuda) {
        return deudaRepository.save(deuda);
    }

    public List<Deuda> findAll() {
        return deudaRepository.findAll();
    }

    public Deuda findById(Long id) {
        return deudaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Deuda no encontrada con id: " + id));
    }

    @Transactional
    public Deuda update(Long id, Deuda deudaActualizada) {
        Deuda existente = findById(id);
        existente.setPersonaEntidad(deudaActualizada.getPersonaEntidad());
        existente.setMontoTotal(deudaActualizada.getMontoTotal());
        existente.setMontoPagado(deudaActualizada.getMontoPagado());
        existente.setTipo(deudaActualizada.getTipo());
        existente.setFechaVencimiento(deudaActualizada.getFechaVencimiento());
        return deudaRepository.save(existente);
    }

    @Transactional
    public void deleteById(Long id) {
        findById(id);
        deudaRepository.deleteById(id);
    }
}
