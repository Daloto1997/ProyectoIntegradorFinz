package com.finanzas.servicio;

import com.finanzas.dto.TransaccionRequest;
import com.finanzas.excepcion.ResourceNotFoundException;
import com.finanzas.modelo.Categoria;
import com.finanzas.modelo.Cuenta;
import com.finanzas.modelo.Transaccion;
import com.finanzas.repositorio.CategoriaRepository;
import com.finanzas.repositorio.CuentaRepository;
import com.finanzas.repositorio.TransaccionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TransaccionService {

    private final TransaccionRepository transaccionRepository;
    private final CuentaRepository cuentaRepository;
    private final CategoriaRepository categoriaRepository;

    @Transactional
    public Transaccion save(TransaccionRequest request) {
        Cuenta cuenta = cuentaRepository.findById(request.cuentaId())
                .orElseThrow(() -> new ResourceNotFoundException("Cuenta no encontrada con id: " + request.cuentaId()));

        Categoria categoria = null;
        if (request.categoriaId() != null) {
            categoria = categoriaRepository.findById(request.categoriaId())
                    .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con id: " + request.categoriaId()));
        }

        LocalDateTime fecha = request.fecha() != null
                ? LocalDateTime.parse(request.fecha(), DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss"))
                : LocalDateTime.now();

        Transaccion transaccion = Transaccion.builder()
                .cuenta(cuenta)
                .categoria(categoria)
                .monto(request.monto())
                .tipo(request.tipo() != null ? request.tipo().toUpperCase() : "GASTO")
                .fecha(fecha)
                .descripcion(request.descripcion())
                .build();

        // Actualizar saldo de la cuenta (monto positivo = ingreso, negativo = gasto)
        cuenta.setSaldoActual(cuenta.getSaldoActual().add(request.monto()));
        cuentaRepository.save(cuenta);

        return transaccionRepository.save(transaccion);
    }

    public List<Transaccion> findAll(String usuarioEmail) {
        if (usuarioEmail != null && !usuarioEmail.isBlank()) {
            return transaccionRepository.findByCuentaUsuarioEmail(usuarioEmail);
        }
        return transaccionRepository.findAll();
    }

    public Transaccion findById(Long id) {
        return transaccionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Transacción no encontrada con id: " + id));
    }

    @Transactional
    public Transaccion update(Long id, TransaccionRequest request) {
        Transaccion existente = findById(id);

        if (request.cuentaId() != null) {
            Cuenta cuenta = cuentaRepository.findById(request.cuentaId())
                    .orElseThrow(() -> new ResourceNotFoundException("Cuenta no encontrada con id: " + request.cuentaId()));
            existente.setCuenta(cuenta);
        }
        if (request.categoriaId() != null) {
            Categoria categoria = categoriaRepository.findById(request.categoriaId())
                    .orElseThrow(() -> new ResourceNotFoundException("Categoría no encontrada con id: " + request.categoriaId()));
            existente.setCategoria(categoria);
        }
        if (request.monto() != null) existente.setMonto(request.monto());
        if (request.tipo() != null) existente.setTipo(request.tipo().toUpperCase());
        if (request.descripcion() != null) existente.setDescripcion(request.descripcion());

        return transaccionRepository.save(existente);
    }

    @Transactional
    public void deleteById(Long id) {
        Transaccion t = findById(id);
        // Revertir el efecto en el saldo de la cuenta
        Cuenta cuenta = t.getCuenta();
        cuenta.setSaldoActual(cuenta.getSaldoActual().subtract(t.getMonto()));
        cuentaRepository.save(cuenta);
        transaccionRepository.deleteById(id);
    }
}
