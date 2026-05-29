import random

from datetime import datetime,timedelta

def simular_Categorias(numeroSimulaciones):

    usuarios_id=["am001","am045","am300","am401","am420"]
    nombres=["pedro","kelly","daniela", "andersson", "aleja"]
    tipos=["gasto", "ahorro", "inversión", "ocio", "servicios publicos"]
    colores= ["verde", "rojo", "azul", "morado", "negro"]
    montos = [1000,50000,800000,9000000,5000]
    fechaTransaccion=datetime(2026,1,2)

    simulaciones=[]
    for _ in range(numeroSimulaciones):

        simulacion={
            "id":random.randint(0,500),
            "nombre":random.choice(nombres),
            "tipo":random.choice(tipos),
            "usuario_id":random.choice(usuarios_id),
            "color":random.choice(colores),
            "monto":random.choice(montos),
            "fecha":fechaTransaccion+timedelta(days=random.randint(0,60))
        }

        #Inyectando errores controlados 
        probabilidadError=random.random()
        if(probabilidadError<0.8):
            simulacion["id"]=None
        elif(probabilidadError<0.7):
            simulacion["nombre"]=random.choice(["lugar de viaje","casa limpia"])
        elif(probabilidadError<0.6):
            simulacion["tipo"]=random.choice(["perro", "mosquito"])
        elif(probabilidadError<0.5):
            simulacion["color"]=None
        elif(probabilidadError<0.4):
            simulacion["monto"]=random.choice([0,-9000000,None])
        elif(probabilidadError<0.3):
            simulacion["usuario_id"]=" "+simulacion["usuario_id"].upper()
        elif(probabilidadError<0.2):
            simulacion["fecha"]=None

        simulaciones.append(simulacion)
    return simulaciones
