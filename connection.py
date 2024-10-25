import pymysql

MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Replace with your actual password
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

try:
    connection = pymysql.connect(
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DB
    )
    print("Connection successful!")
except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    if connection:
        connection.close()
