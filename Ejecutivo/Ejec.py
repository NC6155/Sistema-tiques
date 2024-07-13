from .EjecDb import *
from os import system
from Login import *
db=DatabaseEjec()

def OpcionesEjec(nombre):
    while True:
        nombreU=nombre
        eleccion=input("Escoja la operación que desea hacer:\n\
                       Crear tique (C)\n\
                       Tomar tique (T)\n\
                       Salir(S)\n\
                       : ").upper()
        if eleccion=="C":
            db.crearTique(nombreU)
        elif eleccion=="T":
            db.tomaTique()
        elif eleccion=="S":
            db.cerrarBD()
            break
        else:
            print("Error de escritura")
        
        input("Pulse Enter para continuar...")
        system("cls")