import pymysql

def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="memo",
        password="memo123.",  
        db="juegos"
    )
