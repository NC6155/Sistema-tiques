import time
import mysql.connector
from tabulate import tabulate

class DatabaseJefe():
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
                sql3="insert into Ejecutivo values("+repr(rutEj)+","+repr(areaEj)+","+repr(nombreEj)+","+repr(contrEj)+","+repr(rutJefe)+");"
                try:
                    self.cursor.execute(sql3)
                    self.conexion.commit()
                except Exception as err:
                    self.conexion.rollback()
                    print(err)
        except Exception as err:      
            print(err)
        return rutJefe
    
    def generarLista(self):
        sql1="select * from Tiques"
        try:
            self.cursor.execute(sql1)
            listaTique=self.cursor.fetchall()
            if listaTique!=None:
                for tique in range(len(listaTique)):
                    sql2="select nombreEjec from Ejecutivo where rutEjec="+repr(tique[15])
                    try:
                        self.cursor.execute(sql2)
                        if self.cursor.fetchone()!=None:
                            nomEjec=self.cursor.fetchone()
                    except Exception as err:
                        print(err)
                    print(tabulate([[tique[0],tique[5],tique[6],tique[9],tique[10],nomEjec]], tablefmt="github"))
        except Exception as err:
            print(err)            