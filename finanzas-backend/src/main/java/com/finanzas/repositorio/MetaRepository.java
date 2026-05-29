package com.finanzas.repositorio;

import com.finanzas.modelo.Meta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Repository;


@Repository
public interface MetaRepository extends JpaRepository<Meta, Long> {

    void delete(@NonNull Meta meta);

    @NonNull
    Meta save(@NonNull Meta meta);
}

