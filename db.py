# instalar pymysql -> pip install pymysql
# importar pymysql / SQLachemy / dbmysql
import pymysql

# conectar con el servidro MySQL
def conectarMySQL():
 
    host="127.0.0.1"
    user="root"
    clave="root"
    db="restaurant_db_new"
   
       
    return pymysql.connect(host=host,user=user,password=clave,database=db)
   