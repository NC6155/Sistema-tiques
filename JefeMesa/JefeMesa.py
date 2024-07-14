from .JefeMDB import *
from os import system
#from Login import *
db=DatabaseJefe()

def OpcionesJefe():
    while True:
        eleccion=input("Escoja la operación que desea hacer:\n\
                       Crear ejecutivo (C)\n\
                       Eliminar ejecutivo (E)\n\
                       Generar lista de tiques/Manejar tiques (G)\n\
                       Salir(S)\n\
                       : ").upper()
        if eleccion=="C":
            db.crearEjec()
        elif eleccion=="E":
            db.restringirAcc()
        elif eleccion=="G":
            db.filtradoTique()   
        elif eleccion=="S":
            db.cerrarBD()
            break
        else:
            print("Error de escritura")
        
        input("Pulse Enter para continuar...")
        system("cls")