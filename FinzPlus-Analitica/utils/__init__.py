"""
Paquete de utilidades para FinzPlus
Contiene funciones de simulación y transformación de datos
"""

from .simulacion import simular_Categorias
from .simularcuentas import generar_metas, generar_deudas

__all__ = ['simular_Categorias', 'generar_metas', 'generar_deudas']
