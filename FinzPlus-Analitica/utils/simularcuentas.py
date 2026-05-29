import random
from datetime import datetime, timedelta

def generar_metas(cantidad):
    nombres_metas = ["Fondo de Emergencia", "Viaje a Europa", "Cuota Inicial Carro", "Ahorro Navidad", "PC Gamer"]
    metas = []
    
    # Actualizado a 2026 para que las metas sean a futuro desde hoy
    fecha_base = datetime(2026, 1, 1)
    
    for i in range(cantidad):
        monto_obj = random.randint(1000000, 20000000) # De 1 a 20 millones
        monto_act = random.randint(0, monto_obj)      # Nunca mayor al objetivo
        
        meta = {
            "id": i + 1, # Corrección: Simulamos el IDENTITY(1,1) de tu tabla para evitar IDs duplicados
            "usuario_id": random.randint(1, 50),
            "nombre": random.choice(nombres_metas),
            "monto_objetivo": monto_obj,
            "monto_actual": monto_act,
            "fecha_limite": (fecha_base + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        }
        metas.append(meta)
    return metas

def generar_deudas(cantidad):
    entidades = ["Banco Alpha", "Tarjeta de Crédito Visa", "Prestamo Familiar", "Icetex", "Almacenes Éxito"]
    tipos = ["Bancaria", "Personal", "Comercial"]
    deudas = []
    
    fecha_base = datetime(2026, 1, 1)
    
    for i in range(cantidad):
        monto_t = random.randint(500000, 10000000)
        monto_p = random.randint(0, monto_t)
        
        deuda = {
            "id": i + 1, # Corrección: IDs secuenciales (1, 2, 3...)
            "usuario_id": random.randint(1, 50),
            "persona_entidad": random.choice(entidades),
            "monto_total": monto_t,
            "monto_pagado": monto_p,
            "tipo": random.choice(tipos),
            "fecha_vencimiento": (fecha_base + timedelta(days=random.randint(10, 180))).strftime("%Y-%m-%d")
        }
        deudas.append(deuda)
    return deudas
