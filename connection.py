from sqlalchemy import create_engine

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str)

# Attempt to connect
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
