import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Use a simple connection string pointing to your MySQL database
engine = create_engine('mysql+pymysql://root:@localhost:3306/delivergatedb')

@st.cache
def load_data():
    # Load the data from MySQL tables
    customers_df = pd.read_sql('SELECT * FROM customers', con=engine)
    orders_df = pd.read_sql('SELECT * FROM orders', con=engine)
    return customers_df, orders_df

customers_df, orders_df = load_data()

# You can now proceed with any data processing and visualization as previously outlined
st.header("Customer Orders Dashboard")

# Example: Display the data
st.subheader("Customers Data")
st.dataframe(customers_df)

st.subheader("Orders Data")
st.dataframe(orders_df)

# Further dashboard setup and analysis can be added here
