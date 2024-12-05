import pymysql.cursors
import pandas as pd
import json

#Definiendo la Tabla Bienes.
class Bien:
    def __init__(self, partida, inv, desc, marc, mod, ser, mont, est):
        self.partida = int(partida)
        self.inv = inv
        self.desc = desc
        self.marc = marc
        self.mod = mod
        self.ser = ser
        self.mont = mont
        self.est = est

    def __str__(self):
       return f"Partida: {self.partida}\nInventario: {self.inv}\nDescripcion: {self.desc}\nMarca: {self.marc}\nModelo: {self.mod}\nSerie: {self.ser}\nMonto: {self.mont}\nEstado: {self.est}\n\n"
    
#Definiendo la Tabla Localizacion
class Localizacion:
    def __init__(self, unidadResp, unidadPres, domicilio):
        if(pd.isna(unidadResp)):
            self.unidadResp=""
        else:
            self.unidadResp=unidadResp
        if(pd.isna(unidadPres)):
            self.unidadPres=""
        else: 
            self.unidadPres=unidadPres
        if(pd.isna(domicilio)):
            self.domicilio=""
        else:
            self.domicilio=domicilio

#Definiendo la Tabla Responsable
class Responsable:
        def __init__(self, rfc, nombre, fecha, MotivoNoAsigno):
            if(pd.isna(rfc)):
                self.rfc=""
            else: 
                self.rfc = rfc
            self.nombre = nombre
            self.fecha = fecha
            self.motivoNoAsigno = MotivoNoAsigno
        def __str__(self):
            return f"Nombre: {self.nombre}\nRFC: {self.rfc}\nFecha: {self.fecha}\nMotivoNA: {self.motivoNoAsigno}\n"
                    
#Abriendo el archivo de Excel.
try:
    excelFile = pd.read_excel("./PADRON DE BIENES PARAVALIDAR.xlsx",
                               header=[1], 
                               usecols="P:S",
                               dtype={"NÚMERO DE UNIDAD RESPONSABLE": str, 
                                      "NÚMERO UNIDAD PRESUPUESTAL" : str}
                               )
    print("Se abrió el archivo correctamente")

except EnvironmentError as error: 
    print(error)

#Estableciendo la Conexión a la Base de Datos.
try: 
    connection = pymysql.connect(
            host="localhost",
            user="root",
            port=3307,
            database="InventarioInnovacionSistemas",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    print("Conexion Exitosa"); 

except pymysql.MySQLError as e:
    print(e); 


#Obteniendo los primeros 10 elementos.
registros = excelFile.iloc[:,0:4]


for index, registro in registros.iterrows():
    responsable = Responsable(registro[0], registro[1], registro[2], registro[3])
    print(responsable) 
    try: 
        cursor = connection.cursor()
        sql = f"INSERT INTO responsable (res_rfc, res_nombre, res_fechaResguardo, res_motivoNoAsigno) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, (responsable.rfc, responsable.nombre, responsable.fecha, responsable.motivoNoAsigno))
    except pymysql.MySQLError as error:
        print(error)
    print(f"Analicé {index}")

connection.commit()
connection.close()

