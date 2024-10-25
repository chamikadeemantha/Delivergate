import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Function to establish MySQL connection
def create_connection():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["username"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"]["port"]
        )
        if conn.is_connected():
            st.write("Successfully connected to the database")
        return conn
    except Error as e:
        st.error(f"Error: '{e}'")
        return None

# Function to get data from the database
def get_data(conn):
    query = 'SELECT * FROM customers;'
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(result)

# Main Streamlit app logic
def main():
    st.title('Customer Data Viewer')

    conn = create_connection()
    if conn:
        df = get_data(conn)
        if not df.empty:
            for row in df.itertuples():
                st.write(f"{row.name} has a :{row.pet}:")
        else:
            st.write("No data found.")
    else:
        st.write("Could not establish a connection to the database.")

if __name__ == "__main__":
    main()
