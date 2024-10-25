import pymysql

try:
    conn = pymysql.connect(host='localhost', user='root', password='root', db='delivergatedb')
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version:", data)
    conn.close()
except pymysql.MySQLError as e:
    print(f"Error: {e}")
