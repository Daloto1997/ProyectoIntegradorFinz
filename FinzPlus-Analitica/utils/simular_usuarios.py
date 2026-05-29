from datetime import datetime, timedelta
import random

def generar_usuarios(num_usuarios):
    # Semillas para generar datos aleatorios
    nombres_h = ["Juan", "Carlos", "Luis", "Miguel", "Pedro", "Jorge", "Andrés", "Anderson"]
    nombres_m = ["María", "Ana", "Sofía", "Laura", "Lucía", "Elena", "Marta", "Daniela", "Maria Alejandra"]
    apellidos = ["García", "Pérez", "López", "Martínez", "Sánchez", "Gómez", "Díaz", "Fernández", "Romero", "Vargas"]
    dominios = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"]
    roles_base = ["Admin", "Cliente", "Premium"]
    generos_base = ["Masculino", "Femenino", "Otro"]
    fechaInicio = datetime(2024, 1, 1)

    usuarios = []
    for i in range(num_usuarios):
        # 1. Determinamos el género para la lógica de nombres
        genero = random.choice(generos_base)
        
        if genero == "Masculino":
            nombre = random.choice(nombres_h)
        elif genero == "Femenino":
            nombre = random.choice(nombres_m)
        else:
            nombre = random.choice(nombres_h + nombres_m)

        apellido = random.choice(apellidos)
        nombre_completo = f"{nombre} {apellido}"
        email_base = nombre_completo.lower().replace(" ", ".")

        # 2. Creacion de las columnas del dataframe.
        usuario = {
            "id": i,
            "id_usuario": random.randint(9999, 99999999),
            "nombre_usuario": nombre_completo,
            "genero": genero, # Atributo agregad
            "email": f"{email_base}@{random.choice(dominios)}",
            "rol": random.choice(roles_base), 
            "fecha_creacion": (fechaInicio + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
            "password": hash(random.randint(100000, 999999))
        }

        # 3. Inyección de errores 
        probabilidad_error = random.random()

        if probabilidad_error < 0.10:            
            usuario["id_usuario"] = None            
            
        elif probabilidad_error < 0.20:
            usuario["nombre_usuario"] = usuario["nombre_usuario"].upper()

        elif probabilidad_error < 0.30:
            usuario["id_usuario"] = None
            
        elif probabilidad_error < 0.40:
            usuario["genero"] = "No especificado"
            
        elif probabilidad_error < 0.50:
            usuario["rol"] = "Usuario_Externo"
            
        elif probabilidad_error < 0.60:
            usuario["rol"] = random.choice(["Desconocido", "Dueño del chuzo"])
            
        elif probabilidad_error < 0.70:
            usuario["fecha_creacion"] = None

        usuarios.append(usuario)

    return usuarios
