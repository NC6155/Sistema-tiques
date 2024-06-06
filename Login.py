import mysql.connector
from hashlib import md5
from tabulate import tabulate
from pwinput import pwinput

class DatabaseMD5():
    def __init__(self):
            self.conexion=mysql.connector.connect(
                user='root',
                password='inacap2023',
                host='localhost',
                database='mesaAyuda'
                )

            self.cursor=self.conexion.cursor()
    
    def login(self):
        nombre=input("Ingrese nombre del usuario: ")
        password=pwinput("Ingrese password: ")
        password=md5(password.encode("utf-8")).hexdigest()
        return nombre, password
    
    def detectarUsuario(self):
        #Primero busca por los jefes de mesa
        nombre,password=self.login() #Se deja la variable contraseña inerte a cambio de dejar el nombre en una variable
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
        tipoUsuario=self.detectarUsuario()
        #Detecta el tipo de usuario y loguea dependiendo de su tipo
        if tipoUsuario=="Jefe":
            sql1="select*from jefeMesa where nombreJefe="+repr(nombre)+"and contrasenaJefe="+repr(password)+";"
            try:
                self.cursor.execute(sql1)
                result=self.cursor.fetchone()
            except Exception as err:
                self.conexion.rollback()
                print(err)
            if result!=None and result[0]==nombre and result[1]==password:
                pass
                #jefeMesa.opciones()
        elif tipoUsuario=="Ejec":
            sql1="select*from Ejecutivo where nombreEjec="+repr(nombre)+"and contrasenaEjec="+repr(password)+";"
            try:
                self.cursor.execute(sql1)
                result=self.cursor.fetchone()
            except Exception as err:
                self.conexion.rollback()
                print(err)
            if result!=None and result[0]==nombre and result[1]==password:
                pass
                #ejecutivo.opciones() #Nombres temporales, cambiandose si se necesita
        else:
            print("Error al iniciar sesión")