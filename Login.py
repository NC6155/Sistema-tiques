import mysql.connector
from Ejecutivo import Ejec
from Ejecutivo import EjecDb
from JefeMesa import JefeMesa
from JefeMesa import JefeMDB
from hashlib import md5
from pwinput import pwinput

class DatabaseMD5():
    def __init__(self):
            self.conexion=mysql.connector.connect(
                user='root',
                password='inacap2023',
                host='localhost',
                database='mesaAyuda',
                auth_plugin='mysql_native_password'
                )

            self.cursor=self.conexion.cursor()
    
    def login(self):
        nombre=input("Ingrese nombre del usuario: ")
        password=pwinput("Ingrese password: ")
        return nombre, password
    
    def detectarUsuario(self, nombre):
        #Primero busca por los jefes de mesa
        #nombre,password=self.login() #Se deja la variable contraseña inerte a cambio de dejar el nombre en una variable
        tipoUsuario=None
        sql1="select * from JefeMesa where nombreJefe="+repr(nombre)
        try:
            self.cursor.execute(sql1)
            result=self.cursor.fetchone()
            if result!=None:
                tipoUsuario="Jefe"
            #Si no hay jefes de mesa, busca ejecutivos
            else:
                sql1="select * from Ejecutivo where nombreEjec="+repr(nombre)
                try:
                    self.cursor.execute(sql1)
                    result=self.cursor.fetchone()
                    if result!=None:
                        tipoUsuario="Ejec"
                    else:
                        print("No existen usuarios con ese nombre")
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)
        return tipoUsuario
    
    def iniciarSesion(self):
        nombre,password=self.login()
        tipoUsuario=self.detectarUsuario(nombre)
        print(nombre, password, tipoUsuario)
        #Detecta el tipo de usuario y loguea dependiendo de su tipo
        if tipoUsuario=="Jefe":
            sql1="select*from jefeMesa where nombreJefe="+repr(nombre)+"and contrasenaJefe="+repr(password)+";"
            try:
                self.cursor.execute(sql1)
                result=self.cursor.fetchone()
            except Exception as err:
                self.conexion.rollback()
                print(err)
            if result!=None and result[2]==nombre and result[1]==password:
                JefeMesa.OpcionesJefe()
            else:
                print(result)
        elif tipoUsuario=="Ejec":
            sql1="select*from Ejecutivo where nombreEjec="+repr(nombre)+"and contrasenaEjec="+repr(password)+";"
            try:
                self.cursor.execute(sql1)
                result=self.cursor.fetchone()
            except Exception as err:
                self.conexion.rollback()
                print(err)
            if result!=None and result[2]==nombre and result[3]==password:
                if result[4]=="no":
                    print("Acceso denegado") #Pregunta por el acceso del Ejecutivo en el sistema
                else:
                    Ejec.OpcionesEjec(nombre)    
        else:
            print("Error al iniciar sesión")