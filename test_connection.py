import pymysql

def conectarMySQL():
    host = "127.0.0.1"
    user = "root"
    password = "root"  # Dejar vacío si no has configurado una contraseña
    db = "restaurant_db_new"
    
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=db)
        print("Connected to MySQL database")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

if __name__ == "__main__":
    connection = conectarMySQL()
    if connection:
        connection.close()
        print("MySQL connection is closed")

