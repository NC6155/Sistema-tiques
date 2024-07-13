from os import system
import mysql.connector
from tabulate import tabulate

class DatabaseJefe():
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
    
    def crearEjec(self, nombreJ):
        rutEj=input("Ingrese el rut del ejecutivo: ")
        while len(rutEj)!=12:
            rutEj=input("Error, ingrese el rut del ejecutivo: ")
        try:
            sql1="select * from Ejecutivo where rutEjec="+repr(rutEj)
            self.cursor.execute(sql1)
            if self.cursor.fetchone()==None:
                areaEj=input("Ingrese el área del ejecutivo: ")
                nombreEj=input("Ingrese el nombre del ejecutivo: ")
                contrEj=input("Ingrese la contraseña del ejecutivo: ")
                sql2="select rutJefe from JefeMesa where nombreJefe="+repr(nombreJ)
                try:
                    self.cursor.execute(sql2)
                    if self.cursor.fetchone()!=None:
                        rutJefe=self.cursor.fetchone()
                except Exception as err:
                    print(err)
                sql3="insert into Ejecutivo values("+repr(rutEj)+","+repr(areaEj)+","+repr(nombreEj)+","+repr(contrEj)+",A,"+repr(rutJefe)+");"
                try:
                    self.cursor.execute(sql3)
                    self.conexion.commit()
                except Exception as err:
                    self.conexion.rollback()
                    print(err)
        except Exception as err:      
            print(err)
        return rutJefe
    
    
    def filtradoTique(self):
        while True:
            system("cls")
            eleccion=input("Filtrar por\n\
                    Fecha de creación (F)\n\
                    Criticidad (C)\n\
                    Tipo de tique (T)\n\
                    Área (A)\n\
                    Ejecutivo que abrió el tique (AT)\n\
                    Ejecutivo que cerró el tique (CT)\n\
                    Salir (S)\n\
                    : ").upper()
            if eleccion=="F":
                filtrado=input("Ingrese fecha de creación (dd/mm/aaaa): ")
                sql2="select * from Tiques where fechaCr=str_to_date("+repr(filtrado)+",'%d/%m/%Y')"
            elif eleccion=="C":
                filtrado=input("Ingrese la criticidad de el o los tique(s): ").capitalize()
                while len(filtrado)>15:
                    filtrado=input("Error, ingrese la criticidad de el o los tique(s): ").capitalize()
                sql2="select * from Tiques where criticidad="+repr(filtrado)
            elif eleccion=="T":
                while True:
                    tipoTique=input("Elija el tipo de tique a filtrar\n\
                                    Felicitación(F)\n\
                                    Consulta(C)\n\
                                    Reclamo(R)\n\
                                    Problema(P)\n\
                                    : ").lower()
                    if tipoTique=="f":
                        filtrado="Felicitacion"
                        break
                    elif tipoTique=="c":
                        filtrado="Consulta"
                        break
                    elif tipoTique=="r":
                        filtrado="Reclamo"
                        break
                    elif tipoTique=="p":
                        filtrado="Problema"
                        break
                    else:
                        pass
                sql2="select * from Tiques where tipoTique="+repr(filtrado)
            elif eleccion=="A":
                filtrado=input("Ingrese el área de el o los tique(s): ").capitalize()
                while len(filtrado)>30:
                    filtrado=input("Error, ingrese el área de el o los tique(s): ").capitalize()
                sql2="select * from Tiques where areaDerivar="+repr(filtrado)
            elif eleccion=="AT":
                filtrado=input("Ingrese el rut del ejecutivo que abrió el o los tique(s): ")
                while len(filtrado)>12:
                    filtrado=input("Error, ingrese el rut del ejecutivo que abrió el o los tique(s): ")
                sql2="select * from Tiques where rutEjecCr="+repr(filtrado)
            elif eleccion=="CT":
                filtrado=input("Ingrese el rut del ejecutivo que cerró el o los tique(s): ")
                while len(filtrado)>12:
                    filtrado=input("Error, ingrese el rut del ejecutivo que cerró el o los tique(s): ")
                sql2="select * from Tiques where rutEjecMo="+repr(filtrado)
            elif eleccion=="S":
                break
            else:
                pass
            try:
                if sql2!=None:
                    self.cursor.execute(sql2)
                    listaFilt=self.cursor.fetchall()
                    for tiquesF in listaFilt:
                        sql3="select nombreEjec from Ejecutivo where rutEjec="+repr(tiquesF[15])
                        try:
                            self.cursor.execute(sql3)
                            if self.cursor.fetchone()!=None:
                                nomEjec=self.cursor.fetchone()
                        except Exception as err:
                            print(err)
                        print(tabulate([[tiquesF[0],tiquesF[5],tiquesF[6],tiquesF[9],tiquesF[10],nomEjec]], tablefmt="github"))
                    while True:
                        manejoTique=input("¿Desea manejar un tique en específico? (S/N)").upper()
                        if manejoTique=="S":
                            self.editarTique()
                        else:
                            break
                        
                else:
                    input("Volviendo al menú principal, presione Enter para continuar...")
            except Exception as err:
                    print(err)

    def editarTique(self):
        idTique=int(input("Ingrese el id del tique: "))
        try:
            sql1="select * from Tiques where idTique="+repr(idTique)
            self.cursor.execute(sql1)
            if self.cursor.fetchone()!=None:
                while seguir=="S":
                    system("cls")
                    eleccion=input("Elija qué editará del tique:\n\
                            Área (A)\n\
                            Tipo de tique (T)\n\
                            Criticidad (C)\n\
                            : ").upper()
                    if eleccion=="A":
                        campo="areaDerivar"
                        nuevo=input("Ingrese la nueva área: ")
                    elif eleccion=="T":
                        campo="tipoTique"
                        while True:
                            tipoTique=input("Elija el nuevo tipo del tique\n\
                                            Felicitación(F)\n\
                                            Consulta(C)\n\
                                            Reclamo(R)\n\
                                            Problema(P)\n\
                                            : ").lower()
                            if tipoTique=="f":
                                nuevo="Felicitacion"
                                break
                            elif tipoTique=="c":
                                nuevo="Consulta"
                                break
                            elif tipoTique=="r":
                                nuevo="Reclamo"
                                break
                            elif tipoTique=="p":
                                nuevo="Problema"
                                break
                            else:
                                pass
                    elif eleccion=="C":
                        campo="criticidad"
                        nuevo=input("Ingrese la nueva criticidad: ")
                    else: pass
                    sql2="update Tiques set "+repr(campo)+"="+repr(nuevo)+"where idTique="+repr(idTique)
                    try:
                        self.cursor.execute(sql2)
                        self.conexion.commit()
                    except Exception as err:
                        self.conexion.rollback()      
                        print(err)
                    seguir=input("¿Desea seguir? (S/N)\n\
                                 : ")
                    if seguir=="N":
                        break
                    elif seguir!="S" or seguir!="N":
                        print("Error de escritura")
        except Exception as err:      
            print(err)

    def restringirAcc(self):
        rutEjec=input("Ingrese el rut del ejecutivo: ")
        sql1="select * from Ejecutivo where rutEjec="+repr(rutEjec)
        try:
            self.cursor.execute(sql1)
            if self.cursor.fetchone()!=None:
                sql2="update Ejecutivo set ingreso=0 where rutEjec="+repr(rutEjec)
                try:
                    self.cursor.execute(sql2)
                    self.conexion.commit()
                    print("Acceso restringido correctamente")
                except Exception as err:
                     self.conexion.rollback()
                     print(err)
            else:
                print("Rut incorrecto/Ejecutivo no existe")
        except Exception as err:
            self.conexion.rollback()
            print(err)


