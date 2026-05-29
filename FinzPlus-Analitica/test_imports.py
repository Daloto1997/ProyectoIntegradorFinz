"""
Script de prueba para verificar que todos los módulos funcionen correctamente
"""

import sys

def test_imports():
    """Prueba que todos los imports funcionen correctamente"""
    print("=" * 80)
    print("PRUEBA DE IMPORTS - FinzPlus")
    print("=" * 80)
    
    tests_passed = 0
    tests_failed = 0
    
    tests = [
        ("pandas", "import pandas as pd"),
        ("utils.simulacion", "from utils.simulacion import simular_Categorias"),
        ("utils.simularcuentas", "from utils.simularcuentas import generar_metas, generar_deudas"),
        ("notebook.limpieza", "from notebook.limpieza import limpiar_datos"),
        ("notebook.limpiezaDeudas", "from notebook.limpiezaDeudas import limpiar_datos_deudas"),
        ("notebook.limpiezaMetas", "from notebook.limpiezaMetas import limpiar_datos_metas"),
    ]
    
    for module_name, import_statement in tests:
        try:
            exec(import_statement)
            print(f"✅ {module_name:<40} OK")
            tests_passed += 1
        except Exception as e:
            print(f"❌ {module_name:<40} ERROR: {str(e)}")
            tests_failed += 1
    
    print("\n" + "=" * 80)
    print(f"RESULTADOS: {tests_passed} OK | {tests_failed} ERRORES")
    print("=" * 80)
    
    return tests_failed == 0


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
