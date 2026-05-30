package com.finanzas.modelo;

import jakarta.persistence.*;
import lombok.*;
import com.fasterxml.jackson.annotation.JsonIgnore;

import java.math.BigDecimal;
import java.util.List;

@Entity
@Table(name = "cuentas")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Cuenta {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String nombre; // Ej: "Bancolombia", "Nequi", "Efectivo"

    @Column(name = "usuario_email", length = 100)
    private String usuarioEmail;

    @Column(length = 30)
    @Builder.Default
    private String tipo = "AHORROS"; // AHORROS | CORRIENTE | TARJETA | BILLETERA | EFECTIVO | OTRO

    @Column(name = "saldo_actual", nullable = false, precision = 15, scale = 2)
    @Builder.Default
    private BigDecimal saldoActual = BigDecimal.ZERO;

    @JsonIgnore
    @OneToMany(mappedBy = "cuenta", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Transaccion> transacciones;
}

