package com.finanzas.dto;

import java.math.BigDecimal;

public record TransaccionRequest(
        Long cuentaId,
        Long categoriaId,
        BigDecimal monto,
        String tipo,
        String fecha,
        String descripcion
) {}
