import os
import time 
from tabulate import tabulate

usuarios = [{"encargado": "123"}, {"encargado2": "321"}]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ver_mascotas(mascota):
    for mascota in mascotas:
        print(tabulate([[mascota[0],mascota[1],mascota[2],mascota[3]]],tablefmt="github"))
    input("Pulse Enter para continuar...")
    os.system("cls")

def eliminar_mascota(mascotas):
    encontrado = False
    nombre = input("Diga el nombre de la mascota adoptada: ")
    for i in mascotas:
        if nombre in i:
            encontrado = True
            break
    if encontrado:
        mascotas.remove(i)
        print("mascota adoptada")
    else:
        print("mascota no encontrada.")
    input("Pulse Enter para continuar...")

def agregar_mascota(mascotas):
    nombre = input("Ingrese nombre: ")
    encontrado=False
    for mascota in mascotas:
        if nombre in mascota:
            encontrado=True
            break
        else:
            pass
    if encontrado==False:
        edad = input("Ingrese edad: ")
        raza = input("Ingrese raza: ")
        estado = input("Ingrese estado: ")
        aux = [nombre, edad, raza, estado]
        mascotas.append(aux)
        print("mascota agregado.")
    #Empieza proceso de edicion
    else:
        print("No se encontró la mascota")
    input("Pulse Enter para continuar...")



def editar_estado_mascota(mascotas): 
    nombre= input("ingrese nombre: ")
    encontrado=False
    for mascota in mascotas:
        if nombre in mascota:
            encontrado=True 
            estado=input("ingrese el nuevo estado de la mascota: ")
            mascota[3]=estado

        else:
            pass
    if encontrado==False:
        print("Mascota no encontrada")
    input("Pulse Enter para continuar...")



while True:
    userBan = False
    acceso = False
    user = input("Ingrese su Usuario\n")
    password = input("Ingrese su clave\n")
    for x in usuarios:
        if user in x:
            userBan = True
            clave = x[user]
            break

    if userBan:
        if clave == password:
            print("Bienvenido")
            acceso = True
            break
        else:
            print("Usuario y/o Clave incorrecta")
    else:
        print("Usuario y/o Clave incorrecta")

    time.sleep(3)
    clear_screen()

if acceso:
    print("Veterinaria")
    mascotas = [["13", "Firulais", "Labrador","espera"], ["3", "Doki", "Can","disponible"], ["13", "chomuske", "siberiano","disponible"]]

    while True:
        print("1. Ver listado de mascotas")
        print("2. Eliminar mascota")
        print("3. Agregar mascota")
        print("4. Editar estado de mascota")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion =='1':
            ver_mascotas(mascotas)
        elif opcion == '2':
            eliminar_mascota(mascotas)
        elif opcion == '3':
            agregar_mascota(mascotas)
        elif opcion == '4':
            editar_estado_mascota(mascotas)
        elif opcion == '5':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")