"""
Configuración del Proyecto FinzPlus
Define constantes y parámetros globales
"""

# ============================================================================
# CONFIGURACIÓN DE SIMULACIÓN
# ============================================================================
CANTIDAD_TRANSACCIONES = 100000
CANTIDAD_METAS = 100
CANTIDAD_DEUDAS = 100

# Usuarios para simulación
USUARIOS_ID = ["am001", "am045", "am300", "am401", "am420"]

# Tipos de transacciones
TIPOS_TRANSACCIONES = ["gasto", "ahorro", "inversión", "ocio", "servicios publicos"]

# Colores asociados a categorías
COLORES = ["verde", "rojo", "azul", "morado", "negro"]

# Montos posibles
MONTOS = [1000, 50000, 800000, 9000000, 5000]

# Metas predefinidas
METAS_NOMBRES = ["Fondo de Emergencia", "Viaje a Europa", "Cuota Inicial Carro", 
                 "Ahorro Navidad", "PC Gamer"]

# Deudas predefinidas
DEUDAS_ENTIDADES = ["Banco Alpha", "Tarjeta de Crédito Visa", "Prestamo Familiar", 
                    "Icetex", "Almacenes Éxito"]
DEUDAS_TIPOS = ["Bancaria", "Personal", "Comercial"]

# ============================================================================
# CONFIGURACIÓN DE LIMPIEZA
# ============================================================================
MONTO_MINIMO = 50000  # Monto mínimo para considerar una transacción válida
FECHA_DEFAULT = "2026-01-01"

# ============================================================================
# CONFIGURACIÓN DE ARCHIVOS
# ============================================================================
OUTPUT_DIR = "outputs"
OUTPUT_CATEGORIAS = f"{OUTPUT_DIR}/categorias_limpias.csv"
OUTPUT_METAS = f"{OUTPUT_DIR}/metas_limpias.csv"
OUTPUT_DEUDAS = f"{OUTPUT_DIR}/deudas_limpias.csv"

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================
LOG_LEVEL = "INFO"
MOSTRAR_DETALLES = True
