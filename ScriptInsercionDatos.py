import pymysql.cursors
import pandas as pd
import json

#Definiendo la Tabla Producto:
class Producto:
    def __init__(self, partida, desc, marc, mod, mont):
        if(not pd.isna(partida)):
            self.partida = int(partida)
        else:
            self.partida = 0
        self.desc = desc
        self.marc = marc
        self.mod = mod
        if(pd.isna(mont)):
            self.mont=0
        else:
            self.mont = mont
    def __str__(self):
        return (f"Partida: {self.partida}\nDescripción: {self.desc}\nMarca: {self.marc}\nModelo: {self.mod}\nMonto: {self.mont}")

        

#Definiendo la Tabla Bienes.
class Bien:
    def __init__(self, inv, ser, est, localizacion, responsable, producto):     
        self.inv = inv
        self.ser = ser
        if(pd.isna(est)):
            self.est = ""
        else:
            self.est = est
        self.localizacion = localizacion
        self.responsable = responsable
        self.producto = producto
    def __str__(self):
    
       return f"Inventario: {self.inv}\nSerie: {self.ser}\nEstado: {self.est}\nResponsable: {self.responsable.nombre}\nLocalizacion: {self.localizacion.domicilio}\nProducto: {self.producto}\n\n"

#Definiendo la Tabla Adquisicion.
class Adquisicion:
    def __init__(self, folio, tipo, fecha, bien):
        if(pd.isna(folio)):
            self.folio=''
        else:
            self.folio=folio
        if(pd.isna(tipo)):
            self.tipo=''
        else:
            self.tipo=tipo
        if(pd.isna(fecha)):
            self.fecha='0000-00-00'
        else:
            self.fecha=fecha
        self.bien=bien
    def __str__(self):
        return f"\n\nFolio:{self.folio}\nTipo:{self.tipo}\nFecha:{self.fecha}\nBien:{self.bien}"

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
    def __str__(self):
        return f"Unidad Responsable:{self.unidadResp}\nUnidad Presupuestal:{self.unidadPres}\nDomicilio:{self.domicilio}"

#Definiendo la Tabla Responsable
class Responsable:
        def __init__(self, rfc, nombre, fecha, MotivoNoAsigno):
            if(pd.isna(rfc)):
                self.rfc=""
            else: 
                self.rfc = rfc
            if(pd.isna(nombre)):
                self.nombre=""
            else: 
                self.nombre = nombre
            if(pd.isna(fecha)):
                self.fecha="00-00-0000"
            else:
                self.fecha = fecha
            if(pd.isna(MotivoNoAsigno)):
                self.motivoNoAsigno = "0"
            else:
                self.motivoNoAsigno = MotivoNoAsigno
        def __str__(self):
            return f"Nombre: {self.nombre}\nRFC: {self.rfc}\nFecha: {self.fecha}\nMotivoNA: {self.motivoNoAsigno}\n"

#Abriendo el archivo de Excel.
try:
    excelFile = pd.read_excel("./PADRON DE BIENES PARAVALIDAR.xlsx",
                               header=[1], 
                               usecols="B:M",
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
registros = excelFile.iloc[:,0:11]


for index, registro in registros.iterrows():
    adquisicion=Adquisicion(registro[10],registro[9], registro[8],registro[1])
    print(index)
    print(adquisicion)
    try: 
        cursor = connection.cursor()
        sql = """ UPDATE Bienes
                SET ID_Adquisicion=(SELECT ID_Adquisicion FROM Adquisicion WHERE adq_fecha=%s AND adq_folioFiscal=%s AND adq_tipoAlta=%s
                )
                WHERE bien_inventario=%s; """
        cursor.execute(sql,(adquisicion.fecha,adquisicion.folio,adquisicion.tipo, adquisicion.bien))
    except pymysql.MySQLError as error:
        print(index)
        print("\n\n¡¡¡¡ERROR!!!!")
        print(adquisicion)
        print(error)

connection.commit()
connection.close()

