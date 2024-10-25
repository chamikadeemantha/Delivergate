import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Fetch MySQL credentials from Streamlit secrets
db_connection_str = f"mysql+pymysql://{st.secrets['connections']['mysql']['username']}:{st.secrets['connections']['mysql']['password']}@{st.secrets['connections']['mysql']['host']}:{st.secrets['connections']['mysql']['port']}/{st.secrets['connections']['mysql']['database']}"
engine = create_engine(db_connection_str)

# Function to load data from the MySQL database
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_data():
    query = "SELECT * FROM orders"
    df = pd.read_sql(query, engine)
    return df

# Fetch and display the data
try:
    orders_df = load_data()
    st.success("Data loaded successfully!")

    # Display the fetched data in a table
    st.write("Orders Data")
    st.dataframe(orders_df)

    # Display basic analytics
    st.write("Summary Metrics")
    total_revenue = orders_df['total_amount'].sum()
    unique_customers = orders_df['customer_id'].nunique()
    total_orders = orders_df['order_id'].count()

    st.metric("Total Revenue", f"${total_revenue:,.2f}")
    st.metric("Number of Unique Customers", unique_customers)
    st.metric("Total Orders", total_orders)

    # Visualize top customers by revenue
    st.write("Top 10 Customers by Total Revenue")
    top_customers = orders_df.groupby('customer_id').sum().sort_values('total_amount', ascending=False).head(10)
    st.bar_chart(top_customers['total_amount'])

except Exception as e:
    st.error(f"Error loading data: {e}")
