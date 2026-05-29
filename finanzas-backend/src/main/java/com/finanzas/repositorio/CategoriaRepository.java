package com.finanzas.repositorio;

import com.finanzas.modelo.Categoria;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface CategoriaRepository extends JpaRepository<Categoria, Long> {

    List<Categoria> findByTipo(String tipo);

    // Devuelve categorías globales (usuario IS NULL) para el DataInitializer y el seed
    List<Categoria> findByUsuarioIsNull();

    @NonNull
    Categoria save(@NonNull Categoria categoria);

    void delete(@NonNull Categoria categoria);
}

