# FinzPlus - Sistema de Gestión Financiera

Sistema integral para la simulación, limpieza y análisis de datos financieros personales.

## 📋 Descripción del Proyecto

FinzPlus es un proyecto de Python que gestiona datos financieros incluyendo:
- **Transacciones y Categorías**: Registro y categorización de gastos/ingresos
- **Metas de Ahorro**: Seguimiento de objetivos financieros
- **Deudas**: Administración de deudas pendientes
- **Cuentas Bancarias**: Sincronización de múltiples cuentas

## 📁 Estructura del Proyecto

```
FinzPlus-develop/
├── main.py                              # Punto de entrada principal
├── requirements.txt                     # Dependencias del proyecto
├── README.md                            # Este archivo
│
├── utils/                               # Módulo de utilidades
│   ├── __init__.py
│   ├── simulacion.py                    # Simulación de categorías/transacciones
│   ├── simularcuentas.py                # Simulación de metas y deudas
│   └── simulacion_transacciones.py      # Funciones auxiliares
│
├── notebook/                            # Módulo de procesamiento de datos
│   ├── __init__.py
│   ├── limpieza.py                      # Limpieza de categorías
│   ├── limpiezaDeudas.py                # Limpieza de deudas
│   ├── limpiezaMetas.py                 # Limpieza de metas
│   ├── limpieza_transacciones.py        # Limpieza de transacciones
│   ├── transformacion_transacciones.py  # Transformación de datos
│   └── [otros archivos de análisis]
│
├── rutinas/                             # Rutinas especializadas
│   ├── __init__.py
│   ├── limpiar_cuentas.py               # Rutina de limpieza de cuentas
│   └── simular_cuentas.py               # Rutina de simulación de cuentas
│
├── outputs/                             # Archivos de salida (CSV, resultados)
└── .venv/                               # Entorno virtual de Python
```

## 🚀 Comenzar

### Requisitos Previos
- Python 3.8+
- pip o conda

### Instalación

1. **Clonar o descargar el repositorio**
```bash
cd FinzPlus-develop
```

2. **Crear e activar el entorno virtual**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

### Ejecución

Ejecutar el programa principal:
```bash
python main.py
```

**Salida esperada:**
- Genera 100,000 transacciones simuladas
- Genera 100 metas de ahorro simuladas
- Genera 100 deudas simuladas
- Limpia todos los datos eliminando registros inválidos
- Guarda resultados en `outputs/`:
  - `categorias_limpias.csv`
  - `metas_limpias.csv`
  - `deudas_limpias.csv`

## 📊 Características Principales

### 1. Simulación de Datos
- **Categorías**: Genera transacciones con tipos, montos, fechas
- **Metas**: Crea objetivos de ahorro con fechas límite
- **Deudas**: Simula deudas con vencimientos
- Inyección controlada de errores para testing

### 2. Limpieza de Datos
- Validación de tipos de datos
- Eliminación de valores nulos en campos obligatorios
- Filtrado de valores inválidos
- Normalización de formato de datos
- Eliminación de duplicados

### 3. Transformación
- Agrupaciones por categorías
- Análisis temporal (mensual, anual)
- Cálculos de proporciones
- Identificación de transacciones atípicas

## 🔧 Módulos Principales

### utils/
- **simulacion.py**: Genera datos simulados de categorías
- **simularcuentas.py**: Genera metas y deudas

### notebook/
- **limpieza.py**: Limpia categorías y transacciones
- **limpiezaDeudas.py**: Limpia deudas
- **limpiezaMetas.py**: Limpia metas
- **transformacion_transacciones.py**: Transforma datos para análisis

## 📝 Notas de Desarrollo

- Todos los archivos están configurados con Python 3.8+
- Se utiliza pandas para manipulación de datos
- Los datos se guardan en formato CSV
- Las rutas de salida están en la carpeta `outputs/`

## 🐛 Problemas Solucionados

✅ **main.py**: Corregido error de sintaxis (`:` por `=`)
✅ **main.py**: Definidas todas las variables correctamente
✅ **main.py**: Reorganizado con estructura y documentación clara
✅ **Módulos**: Creados archivos `__init__.py` para imports correctos
✅ **Imports**: Corregidos todos los imports entre módulos

## 📚 Dependencias

- **pandas** (3.0.2): Manipulación de datos
- **numpy** (2.4.4): Operaciones numéricas
- **python-dateutil** (2.9.0): Manejo de fechas

## 👥 Autor

Proyecto FinzPlus - Sistema de Gestión Financiera

---

**Última actualización**: 28 de Mayo de 2026