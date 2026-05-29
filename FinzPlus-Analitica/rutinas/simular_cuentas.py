import random


def simular_cuentas_sucias(numero_simulaciones):
    usuarios_id = ["usr101", "usr102", "usr103", "usr104", "usr105"]
    nombres_cuenta = ["Ahorros", "Nómina", "Corriente", "Inversión", "Fondo Emergencia"]
    bancos_externos = ["BANCO-001", "BANCO-045", "BANCO-300", "BANCO-420"]
    simulaciones = []

    for i in range(numero_simulaciones):
        simulacion = {
            "id": i + 1,
            "usuario_id": random.choice(usuarios_id),
            "nombre": random.choice(nombres_cuenta),
            "saldo_actual": round(random.uniform(1000, 5000000), 2),
            "es_sincronizada": random.choice([True, False]),
            "id_banco_externo": random.choice(bancos_externos)
        }

        probabilidad_error = random.random()
        if probabilidad_error < 0.1:
            simulacion["id"] = None
        elif probabilidad_error < 0.2:
            simulacion["nombre"] = random.choice(["ERROR_SISTEMA", "CUENTA_PRUEBA"])
        elif probabilidad_error < 0.3:
            simulacion["saldo_actual"] = random.choice([0, -5000, None])
        elif probabilidad_error < 0.4:
            simulacion["usuario_id"] = " " + simulacion["usuario_id"].upper()
        elif probabilidad_error < 0.5:
            simulacion["id_banco_externo"] = None

        simulaciones.append(simulacion)

    return simulaciones
