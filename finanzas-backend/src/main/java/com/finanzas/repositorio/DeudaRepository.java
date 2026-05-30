package com.finanzas.repositorio;

import com.finanzas.modelo.Deuda;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DeudaRepository extends JpaRepository<Deuda, Long> {
    List<Deuda> findByUsuarioEmail(String usuarioEmail);
}
