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

# Streamlit App
st.title("Customer Table Display")

def load_customer_data():
    # Query the customers table
    query = "SELECT * FROM customers"
    # Load the data into a DataFrame
    df = pd.read_sql(query, con=engine)
    return df

# Display the customers table in Streamlit
st.subheader("Customers Data")
customers_df = load_customer_data()
st.write(customers_df)

st.success("Customer data loaded successfully!")
