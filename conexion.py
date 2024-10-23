import psycopg2

def obtener_conexion():
    try:
        connection = None
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='123456',
            database='DBTAL',
            port='5434'
        )

        print("Conexion exitosa.")
        return connection
    except Exception as ex:
        print(ex)
        return None
        