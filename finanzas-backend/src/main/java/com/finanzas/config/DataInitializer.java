package com.finanzas.config;

import com.finanzas.modelo.Categoria;
import com.finanzas.repositorio.CategoriaRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final CategoriaRepository categoriaRepository;

    @Override
    public void run(String... args) {
        if (categoriaRepository.count() > 0) return;

        List<Categoria> defaults = List.of(
            Categoria.builder().nombre("Alimentación").tipo("GASTO").color("#ef4444").build(),
            Categoria.builder().nombre("Transporte").tipo("GASTO").color("#f97316").build(),
            Categoria.builder().nombre("Hogar").tipo("GASTO").color("#eab308").build(),
            Categoria.builder().nombre("Salud").tipo("GASTO").color("#22c55e").build(),
            Categoria.builder().nombre("Educación").tipo("GASTO").color("#3b82f6").build(),
            Categoria.builder().nombre("Ocio").tipo("GASTO").color("#a855f7").build(),
            Categoria.builder().nombre("Ropa").tipo("GASTO").color("#ec4899").build(),
            Categoria.builder().nombre("Servicios").tipo("GASTO").color("#6b7280").build(),
            Categoria.builder().nombre("Salario").tipo("INGRESO").color("#10b981").build(),
            Categoria.builder().nombre("Freelance").tipo("INGRESO").color("#14b8a6").build(),
            Categoria.builder().nombre("Inversiones").tipo("INGRESO").color("#8b5cf6").build(),
            Categoria.builder().nombre("Otros ingresos").tipo("INGRESO").color("#64748b").build()
        );

        categoriaRepository.saveAll(defaults);
    }
}
