package com.finanzas.repositorio;

import com.finanzas.modelo.Cuenta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Repository;


@Repository
public interface CuentaRepository extends JpaRepository<Cuenta, Long> {

    @NonNull
    Cuenta save(@NonNull Cuenta cuenta);
}

