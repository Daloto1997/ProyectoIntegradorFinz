# FinzPlus - Guía Rápida de Uso

## 🚀 Inicio Rápido

### 1. Ejecutar el programa principal
```bash
python main.py
```

### 2. Verificar que todos los módulos funcionan
```bash
python test_imports.py
```

---

## 📂 Estructura de Carpetas

```
proyecto/
├── main.py              ← EJECUTAR ESTO
├── config.py            ← Configuración global
├── test_imports.py      ← Prueba de módulos
│
├── utils/               ← Funciones de simulación
│   ├── simulacion.py
│   └── simularcuentas.py
│
├── notebook/            ← Funciones de limpieza
│   ├── limpieza.py
│   ├── limpiezaDeudas.py
│   └── limpiezaMetas.py
│
├── outputs/             ← Resultados guardados aquí
│   ├── categorias_limpias.csv
│   ├── metas_limpias.csv
│   └── deudas_limpias.csv
│
└── README.md            ← Documentación completa
```

---

## 📊 ¿Qué hace main.py?

1. **Genera datos simulados**
   - 100,000 transacciones
   - 100 metas de ahorro
   - 100 deudas

2. **Convierte a DataFrames**
   - Estructura los datos para análisis

3. **Limpia los datos**
   - Elimina valores inválidos
   - Normaliza formatos
   - Elimina duplicados

4. **Muestra resultados**
   - Primeras 10 filas de cada dataset
   - Total de registros válidos

5. **Guarda en CSV**
   - `outputs/categorias_limpias.csv`
   - `outputs/metas_limpias.csv`
   - `outputs/deudas_limpias.csv`

---

## 🔧 Personalización

Editar `config.py` para cambiar:
- Cantidad de datos a generar
- Usuarios, tipos, colores disponibles
- Nombres de metas y deudas
- Directorios de salida

---

## ✅ Validación

Todo funcionando correctamente ✓
- main.py: Ejecutado exitosamente
- test_imports.py: 6/6 módulos OK
- Outputs generados correctamente

---

## 📧 Soporte

Si encuentra errores, verifique:
1. Python 3.8+ instalado
2. Dependencias: `pip install -r requirements.txt`
3. Archivos en la ruta correcta
4. Permisos de escritura en la carpeta

Vea `CAMBIOS.md` para detalles de las mejoras realizadas.
