package com.finanzas.modelo;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "deudas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Deuda {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "usuario_email", length = 100)
    private String usuarioEmail;

    @Column(name = "persona_entidad", nullable = false, length = 100)
    private String personaEntidad;

    @Column(name = "monto_total", nullable = false, precision = 15, scale = 2)
    private BigDecimal montoTotal;

    @Column(name = "monto_pagado", precision = 15, scale = 2)
    @Builder.Default
    private BigDecimal montoPagado = BigDecimal.ZERO;

    @Column(nullable = false, length = 20)
    private String tipo; // POR_COBRAR | POR_PAGAR

    @Column(name = "fecha_vencimiento")
    private LocalDate fechaVencimiento;
}

