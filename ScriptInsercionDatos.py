import pymysql.cursors

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
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE Bienes")
        result = cursor.fetchall()
        for row in result:
            print(row); 

except pymysql.MySQLError as e:
    print(e); 
    
