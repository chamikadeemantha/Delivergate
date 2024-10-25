import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='delivergatedb'
    )
    print("Connection successful!")
    connection.close()
except pymysql.MySQLError as e:
    print(f"Error: {e}")
