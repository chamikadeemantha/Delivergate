import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Replace with your password
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'

# Function to load data from the database
def load_data():
    try:
        engine = create_engine(db_connection_str)
        orders_df = pd.read_sql("SELECT * FROM orders", con=engine)
        customers_df = pd.read_sql("SELECT * FROM customers", con=engine)
        return orders_df, customers_df
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return None, None

# Load data
orders_df, customers_df = load_data()

if orders_df is not None and customers_df is not None:
    # Proceed with your Streamlit app logic...
    st.title("Order Dashboard")
    st.subheader("Filtered Orders")
