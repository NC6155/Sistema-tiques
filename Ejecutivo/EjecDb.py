import time
import mysql.connector
from tabulate import tabulate

class DatabaseEjec():
    def __init__(self):
            self.conexion=mysql.connector.connect(
                user='root',
                password='inacap2023',
                host='localhost',
                database='mesaAyuda',
                auth_plugin='mysql_native_password'
                )

            self.cursor=self.conexion.cursor()
        
    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()
    
    def crearTique(self, nombre): #Envía el nombre del ejecutivo para luego buscar su rut
        idTique=int(input("Ingrese ID de tique: "))
        while len(str(idTique))>3:
            idTique=int(input("Error, ingrese ID de tique: "))
        sql1="select * from Tiques where idTique="+repr(idTique)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone()==None: #Detecta si existe el tique con esa id, si no, se crea
                nomCli=input("Ingrese el nombre del cliente: ")#Ingresa los datos del tique
                while len(nomCli)>20:
                    nomCli=input("Error, ingrese el nombre del cliente: ")

                rutCli=input("Ingrese RUT del cliente: ")
                while len(rutCli)>12 and len(rutCli)<12:
                    rutCli=input("Error, ingrese RUT del cliente: ")

                fono=int(input("Ingrese fono: "))
                while len(str(fono))>9:
                    fono=int(input("Error, ingrese fono: "))
                
                corrElec=input("Ingrese el correo electronico: ")
                while len(corrElec)>20:
                    corrElec=input("Error, ingrese el correo electronico: ")
                
                while True:
                    tipoTique=input("Elija el tipo de tique\n\
                                    Felicitacion(F)\n\
                                    Consulta(C)\n\
                                    Reclamo(R)\n\
                                    Problema(P)\n\
                                    : ").lower()
                    if tipoTique=="f":
                        tipoTique="Felicitacion"
                        break
                    elif tipoTique=="c":
                        tipoTique="Consulta"
                        break
                    elif tipoTique=="r":
                        tipoTique="Reclamo"
                        break
                    elif tipoTique=="p":
                        tipoTique="Problema"
                        break
                    else:
                        pass
                
                criticidad=input("Ingrese criticidad: ")
                while len(criticidad)>15:
                    criticidad=input("Error, ingrese criticidad: ")

                detalleServ=input("Ingrese el detalle del servicio: ")
                while len(detalleServ)>200:
                    detalleServ=input("Error, ingrese el detalle del servicio: ")
                
                detalleProb=input("Ingrese el detalle del problema: ")
                while len(detalleServ)>200:
                    detalleProb=input("Error, ingrese el detalle del problema: ")

                areaDer=input("Ingrese el area a derivar: ")
                while len(areaDer)>30:
                    areaDer=input("Error, ingrese el area a derivar: ")
                
                fechaCr=time.localtime()
                fechaCr=time.strftime('%Y/%m/%d',fechaCr) #Se crean fechas de creación y modificación, luego se pasan al estándar de fechas
                fechaMo=time.localtime()
                fechaMo=time.strftime('%Y/%m/%d',fechaMo) #La fecha de modificación será la misma de creación hasta que ocurra un cambio

                sql2="select rutEjec from Ejecutivo where nombreEjec="+repr(nombre) #Busca el rut del ejecutivo usando su nombre
                try:
                    self.cursor.execute(sql2)
                    rutEjec=self.cursor.fetchone()
                except Exception as err:
                    print(err)
                
                rutJefe=input("Ingrese el rut del jefe de mesa encargado del tique: ")
                while len(rutJefe)>12:
                    rutJefe=input("Error, ingrese el rut del jefe de mesa encargado del tique: ")
                sql4="select * from JefeMesa where rutJefe="+repr(rutJefe)+";"
                try:
                    self.cursor.execute(sql4) #Revisa que el rut ingresado esté correcto, si no, ingresa el campo rutJefeAdmin en su lugar
                    if self.cursor.fetchone()!=None:
                        pass
                    else:
                        print("El rut del jefe es incorrecto, en su lugar se utilizará el rut del jefe que administre al usuario")
                        sql5="select rutJefeAdmin from Ejecutivo where nombreEjec="+repr(nombre)+";"
                        try:
                            self.cursor.execute(sql5)
                            rutJefe=self.cursor.fetchone()
                            rutJefe=rutJefe[0] #Arregla el campo rutJefe de tupla a string al transformarlo en su primer (y único) campo, esto es para ahorrarse problemas a la hora de insertar el campo dentro de la tabla
                        except Exception as err:
                            print(err)
                except Exception as err:
                    self.conexion.rollback()
                    print(err)   

                sql6="insert into Tiques values("+repr(idTique)+","+repr(nomCli)+","+repr(rutCli)+","+repr(fono)+","+repr(corrElec)+","+repr(tipoTique)+","+repr(criticidad)+","\
                    +repr(detalleServ)+","+repr(detalleProb)+","+repr(areaDer)+",'A resolución', 'Sin observación',"\
                    +repr(fechaCr)+","+repr(fechaMo)+","+repr(rutEjec[0])+","+repr(rutEjec[0])+","+repr(rutJefe)+");" #Se crean dos columnas usando al rutEjec, una será modificada por el ejecutivo del área y la otra es una foránea llamando directamente al rutEjec
                try:
                    self.cursor.execute(sql6)
                    self.conexion.commit()
                except Exception as err:
                    self.conexion.rollback()
                    print(err)                  #Ingresa los valores entregados a la tabla de tiques
            else:
                print("Ya existe ese código")
                
        
        except Exception as err:
            print(err)

        self.cursor.execute(sql1)
        prevTique=self.cursor.fetchone()
        if prevTique!=None:
            print("Resumen de campos ingresados: \n")
            print(tabulate([[idTique,rutCli,corrElec,areaDer,tipoTique,rutJefe]],tablefmt="github"))
    

    def tomaTique(self,nombre):
        idTique=int(input("Ingrese ID de tique: "))
        sql1="select * from Tiques where idTique="+repr(idTique)+";"

        try:
            self.cursor.execute(sql1)
            tique=self.cursor.fetchone()
            if tique!=None:
                if tique[10]=="A resolución": #Verifica que el estado del tique sea el de "A resolución"
                    fechaMo=time.localtime()
                    fechaMo=time.strftime('%Y/%m/%d',fechaMo)
                    sql2="update Tiques set fechaMo="+repr(fechaMo)+" where idTique="+repr(idTique) #Actualiza la fecha de modificación
                    try:
                        self.cursor.execute(sql2)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)
                    print(tabulate([[tique[0],tique[1],tique[2],tique[3],tique[5],tique[6],tique[7],tique[8],tique[13]]],tablefmt="github"))
                    estado=input("Escoja el estado del tique según su criterio (Resuelto, No aplicable): ").capitalize()
                    while estado!="Resuelto" and estado!="No aplicable":
                        estado=input("Error, escoja el estado del tique según su criterio (Resuelto, No aplicable): ").capitalize()
                    sql3="update Tiques set estado="+repr(estado)+" where idTique="+repr(idTique)
                    try:
                        self.cursor.execute(sql3)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)
                    observ=input("Deje su observación acá: ")
                    while len(observ)>50:
                        observ=input("Error, deje su observación acá: ")
                    sql4="update Tiques set observEjec="+repr(observ)+" where idTique="+repr(idTique)
                    try:
                        self.cursor.execute(sql4)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)
                    sql5="select rutEjec from Ejecutivo where nombreEjec="+repr(nombre) #Busca el rut del ejecutivo usando su nombre
                    try:
                        self.cursor.execute(sql5)
                        rutEjecMo=self.cursor.fetchone()
                    except Exception as err:
                        print(err)
                    sql6="update Tiques set rutEjecMo="+repr(rutEjecMo[0])+" where idTique="+repr(idTique) #Cambia al ejecutivo que modificó el tique
                    try:
                        self.cursor.execute(sql6)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)
                    print("Toma de tique realizada correctamente")
                else:
                    print("Tique ya resuelto")
            else:
                print("Tique no existe")            
        except Exception as err:
            print(err)
