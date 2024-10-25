from sqlalchemy import create_engine, text

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Empty password as per XAMPP config
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str)

# Try connecting to the database and running a test query
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))  # Use text() to handle raw SQL
        for row in result:
            print("Connection successful. Query result:", row)
except Exception as e:
    print("Error occurred:", str(e))
