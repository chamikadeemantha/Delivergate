import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Empty password as per XAMPP config
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str)

# Streamlit app
st.title("Delivergate Pvt Ltd Database Viewer")

# Function to load data from MySQL
@st.cache_data
def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df

# Display Customers table
st.header("Customers Table")
customers_df = load_data('customers')
st.write(customers_df)

# Display Orders table
st.header("Orders Table")
orders_df = load_data('orders')
st.write(orders_df)

# Add more features to your app as needed
