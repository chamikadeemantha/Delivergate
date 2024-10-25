import streamlit as st
# streamlit_app.py

import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from customers;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.customer_id } has a :{row.customer_name}:")import streamlit as st
import mysql.connector
from mysql.connector import Error

# Initialize connection to MySQL
def init_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",   # Or your remote database host
            user="root",        # MySQL username
            password="",        # MySQL password
            database="delivergatedb"  # Database name
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error while connecting to MySQL: {str(e)}")
        return None

# Perform query
def run_query(conn, query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    return cursor.fetchall()

# Streamlit application interface
st.title("Customer Data from MySQL Database")

# Initialize connection
conn = init_connection()

if conn:
    # Perform query
    query = 'SELECT * FROM customers;'  # Adjust the query as per your database
    data = run_query(conn, query)

    # Print results
    for row in data:
        st.write(f"Customer ID: {row['customer_id']}, Customer Name: {row['customer_name']}")

    # Close connection after use
    conn.close()
else:
    st.error("Failed to connect to the database.")
import streamlit as st
import mysql.connector
from mysql.connector import Error

# Initialize connection to MySQL
def init_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",   # Or your remote database host
            user="root",        # MySQL username
            password="",        # MySQL password
            database="delivergatedb"  # Database name
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error while connecting to MySQL: {str(e)}")
        return None

# Perform query
def run_query(conn, query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    return cursor.fetchall()

# Streamlit application interface
st.title("Customer Data from MySQL Database")

# Initialize connection
conn = init_connection()

if conn:
    # Perform query
    query = 'SELECT * FROM customers;'  # Adjust the query as per your database
    data = run_query(conn, query)

    # Print results
    for row in data:
        st.write(f"Customer ID: {row['customer_id']}, Customer Name: {row['customer_name']}")

    # Close connection after use
    conn.close()
else:
    st.error("Failed to connect to the database.")
