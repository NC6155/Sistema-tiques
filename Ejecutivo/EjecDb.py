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
        while len(idTique)>3:
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
                while len(fono)>9:
                    fono=input("Error, ingrese fono: ")
                
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
                
                areaDer=input("Ingrese el area a derivar: ")
                while len(areaDer)>30:
                    areaDer=input("Error, ingrese el area a derivar: ")
                
                fechaCr=time.localtime()
                fechaCr=time.strftime('%d/%m/%Y',fechaCr) #Se crean fechas de creación y modificación, luego se pasan al estándar de fechas
                fechaMo=time.localtime()
                fechaMo=time.strftime('%d/%m/%Y',fechaMo) #La fecha de modificación será la misma de creación hasta que ocurra un cambio

                sql2="select rutEjec from Ejecutivo where nombreEjec="+repr(nombre) #Busca el rut del ejecutivo usando su nombre
                try:
                    self.cursor.execute(sql2)
                    if self.cursor.fetchone()!=None:
                        rutEjec=self.cursor.fetchone()
                except Exception as err:
                    print(err)

                sql3="select rutJefe from JefeMesa"
                try:
                    self.cursor.execute(sql3)
                    if self.cursor.fetchone()!=None:
                        rutJefe=self.cursor.fetchone()
                except Exception as err:
                    print(err)                          #Busca al primer jefe de mesa por su rut

                sql4="insert into Tiques values("+repr(idTique)+","+repr(nomCli)+","+repr(rutCli)+","+repr(fono)+","+repr(corrElec)+","+repr(tipoTique)+","+repr(criticidad)+","\
                    +repr(detalleServ)+","+repr(areaDer)+",A resolución, Sin observación"\
                    +repr(fechaCr)+",'%d/%m/%Y'),"+repr(fechaMo)+",'%d/%m/%Y'),"+repr(rutEjec)+","+repr(rutEjec)+","+repr(rutJefe)+")" #Se crean dos columnas usando al rutEjec, una será modificada por el ejecutivo del área y la otra es una foránea llamando directamente al rutEjec
                try:
                    self.cursor.execute(sql4)
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
            print("{:10}{:20}{:12}{:12}{:20}{:12}"\
                .format("Id Tique","Nombre Cl.","Rut Cl.","Tipo tique","Area der.","Rut Ejec."))

            print("{:<10}{:20}{:12}{:12}{:20}{:12}".\
                format(prevTique[0],prevTique[1],prevTique[2],prevTique[5],prevTique[9],prevTique[13]))
        return rutEjec #Envía el rut del ejecutivo que creó el tique
    

    def tomaTique(self):
        idTique=int(input("Ingrese ID de tique: "))
        sql1="select * from Tiques where idTique="+repr(idTique)
        rutEjecMo=self.crearTique() #Recibe el rut del ejecutivo
        try:
            self.cursor.execute(sql1)
            tique=self.cursor.fetchone()
            if tique!=None:
                if tique[10]=="A resolución": #Verifica que el estado del tique sea el de "A resolución"
                    fechaMo=time.localtime()
                    fechaMo=time.strftime('%d/%m/%Y',fechaMo)
                    sql2="update Tiques set fechaMo=str_to_date("+repr(fechaMo)+",%d/%m/%Y) where idTique="+repr(idTique) #Actualiza la fecha de modificación
                    try:
                        self.cursor.execute(sql2)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)
                    print(tabulate([[tique[0],tique[1],tique[2],tique[3],tique[5],tique[6],tique[7],tique[8],tique[13]]],tablefmt="github"))
                    estado=input("Escoja el estado del tique según su criterio (Resuelto, No aplicable): ").capitalize()
                    while estado!="Resuelto" or estado!="No aplicable":
                        estado=input("Error, escoja el estado del tique según su criterio (Resuelto, No aplicable): ").capitalize()
                    sql3="update Tiques set estado="+repr(estado)+"where idTique="+repr(idTique)
                    try:
                        self.cursor.execute(sql3)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)
                    observ=input("Deje su observación acá: ")
                    while len(observ)>50:
                        observ=input("Error, deje su observación acá: ")
                    sql4="update Tiques set observEjec="+repr(observ)+"where idTique="+repr(idTique)
                    try:
                        self.cursor.execute(sql4)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()
                        print(err)
                    sql5="update Tiques set rutEjecMo="+repr(rutEjecMo)+"where idTique="+repr(idTique) #Cambia al ejecutivo que modificó el tique
                    try:
                        self.cursor.execute(sql5)
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
