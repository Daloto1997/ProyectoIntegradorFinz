from datetime import datetime, timedelta
import random

def generar_transacciones(num_registros):
    # Semillas para transacciones financieras
    tipos_base = ["Ingreso", "Egreso"]
    categorias_id = [101, 102, 103, 104, 105]
    descripciones = ["Pago nómina", "Compra supermercado", "Pago arriendo", "Transferencia", "Cena"]
    fechaInicio = datetime(2024, 1, 1)

    transacciones = []
    for i in range(num_registros):
        transaccion = {
            "id": i,
            "usuario_id": random.randint(1, 500), # Referencia a la tabla Usuarios
            "cuenta_id": random.randint(1, 10),
            "categoria_id": random.choice(categorias_id),
            "monto": round(random.uniform(10000, 2000000), 2),
            "tipo": random.choice(tipos_base),
            "fecha": (fechaInicio + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "descripcion": random.choice(descripciones)
        }

        # --- Inyectando errores controlados ---
        probabilidad_error = random.random()

        if probabilidad_error < 0.15:
            # ERROR 1: Monto negativo o cero (Error financiero)
            transaccion["monto"] = random.choice([0, -50000])
            
        elif probabilidad_error < 0.30:
            # ERROR 2: Tipo de transacción inválido (Para el .isin)
            transaccion["tipo"] = "Prestamo" 
            
        elif probabilidad_error < 0.45:
            # ERROR 3: Descripción con espacios o mayúsculas (Para el .strip)
            transaccion["descripcion"] = transaccion["descripcion"].upper()
            
        elif probabilidad_error < 0.60:
            # ERROR 4: IDs faltantes (Para el dropna)
            transaccion["usuario_id"] = None
            
        elif probabilidad_error < 0.75:
            # ERROR 5: Fecha nula
            transaccion["fecha"] = None

        transacciones.append(transaccion)

    return transacciones
