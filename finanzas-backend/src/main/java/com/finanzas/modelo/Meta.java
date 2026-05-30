package com.finanzas.modelo;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "metas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Meta {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "usuario_email", length = 100)
    private String usuarioEmail;

    @Column(nullable = false, length = 100)
    private String nombre;

    @Column(name = "monto_objetivo", nullable = false, precision = 15, scale = 2)
    private BigDecimal montoObjetivo;

    @Column(name = "monto_actual", precision = 15, scale = 2)
    @Builder.Default
    private BigDecimal montoActual = BigDecimal.ZERO;

    @Column(name = "fecha_limite")
    private LocalDate fechaLimite;
}

