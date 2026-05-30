package com.finanzas.servicio;

import com.finanzas.excepcion.ResourceNotFoundException;
import com.finanzas.modelo.Cuenta;
import com.finanzas.repositorio.CuentaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class CuentaService {

    private final CuentaRepository cuentaRepository;

    @Transactional
    public Cuenta save(Cuenta cuenta) {
        return cuentaRepository.save(cuenta);
    }

    public List<Cuenta> findAll(String usuarioEmail) {
        if (usuarioEmail != null && !usuarioEmail.isBlank()) {
            return cuentaRepository.findByUsuarioEmail(usuarioEmail);
        }
        return cuentaRepository.findAll();
    }

    public Cuenta findById(Long id) {
        return cuentaRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Cuenta no encontrada con id: " + id));
    }

    @Transactional
    public Cuenta update(Long id, Cuenta cuentaActualizada) {
        Cuenta existente = findById(id);
        existente.setNombre(cuentaActualizada.getNombre());
        existente.setSaldoActual(cuentaActualizada.getSaldoActual());
        existente.setTipo(cuentaActualizada.getTipo());
        return cuentaRepository.save(existente);
    }

    @Transactional
    public void deleteById(Long id) {
        findById(id);
        cuentaRepository.deleteById(id);
    }
}
