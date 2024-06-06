import mysql.connector
from tabulate import tabulate

class DatabaseEjec():
    def __init__(self):
            self.conexion=mysql.connector.connect(
                user='root',
                password='inacap2023',
                host='localhost',
                database='empresa',
                auth_plugin='mysql_native_password'
                )

            self.cursor=self.conexion.cursor()
        
    def cerrarBD(self):
        self.cursor.close()
        self.conexion.close()
    
    def crearTique(self, nombre):
        idTique=int(input("Ingrese ID de tique: "))
        sql1="select * from Tiques where idTique="+repr(idTique)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone()==None:
                nomCli=input("Ingrese el nombre del cliente: ")
                while len(nomCli)>20:
                    nomCli=input("Error, ingrese el nombre del cliente: ")

                rutCli=input("Ingrese RUT del cliente: ")
                while len(rutCli)>12 and len(rutCli)<12:
                    rutCli=input("Error, ingrese RUT del cliente: ")

                fono=int(input("Ingrese fono: "))
                while len(fono)>12:
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
                while len(detalleServ)>40:
                    detalleServ=input("Error, ingrese el detalle del servicio: ")
                
                areaDer=input("Ingrese el area a derivar: ")
                while len(areaDer)>15:
                    areaDer=input("Error, ingrese el area a derivar: ")
                sql2="select rutEjec from Ejecutivo where nombreEjec="+repr(nombre)

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
                    print(err)
                sql4="insert into Tiques values("+repr(idTique)+","+repr(nomCli)+","+repr(rutCli)+","+repr(fono)+","+repr(corrElec)+","+repr(tipoTique)+","+repr(criticidad)+","\
                    +repr(detalleServ)+","+repr(areaDer)+",A resolución,"+repr(rutEjec)+","+repr(rutJefe)+")"
                try:
                    self.cursor.execute(sql4)
                    self.conexion.commit()
                except Exception as err:
                    self.conexion.rollback()
                    print(err)
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
                format(prevTique[0],prevTique[1],prevTique[2],prevTique[5],prevTique[8],prevTique[9]))
    
    def tomaTique(self):
        idTique=int(input("Ingrese ID de tique: "))
        sql1="select * from Tiques where idTique="+repr(idTique)
        try:
            self.cursor.execute(sql1)
            tique=self.cursor.fetchone()
            if tique!=None:
                print(tabulate([[tique[0],tique[1],tique[2],tique[3],tique[4],tique[5],tique[6],tique[7],tique[8],tique[9],tique[10],tique[11],tique[12]]],tablefmt="github"))
                estado=input("Cambiar estado:\n\
                      Resuelto(R)\n\
                      No aplicable(N)\n\
                      : ").lower()
                