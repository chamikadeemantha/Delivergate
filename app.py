import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Replace with your password
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str)

# Function to load data from the database
def load_data():
    orders_df = pd.read_sql("SELECT * FROM orders", con=engine)
    customers_df = pd.read_sql("SELECT * FROM customers", con=engine)
    return orders_df, customers_df

# Load data
orders_df, customers_df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

# Date Range Filter
date_range = st.sidebar.date_input("Select date range", 
                                     [datetime.today() - timedelta(days=30), datetime.today()])
start_date, end_date = date_range

# Slider for Total Amount Filter
total_amount = st.sidebar.slider("Total Amount Spent", min_value=0, max_value=int(orders_df['total_amount'].sum()), value=(0, 1000))

# Dropdown for Customer Orders Filter
order_count_filter = st.sidebar.slider("Minimum Number of Orders", min_value=1, max_value=orders_df['customer_id'].nunique(), value=5)

# Filter Data
filtered_orders = orders_df[(orders_df['order_date'] >= pd.to_datetime(start_date)) &
                             (orders_df['order_date'] <= pd.to_datetime(end_date)) &
                             (orders_df['total_amount'] >= total_amount[0]) &
                             (orders_df['total_amount'] <= total_amount[1])]

# Get unique customer IDs who have more than the specified number of orders
customer_counts = filtered_orders['customer_id'].value_counts()
valid_customers = customer_counts[customer_counts > order_count_filter].index
filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(valid_customers)]

# Main Dashboard
st.title("Order Dashboard")

# Display the filtered data in a table
st.subheader("Filtered Orders")
st.dataframe(filtered_orders)

# Bar Chart: Top 10 Customers by Total Revenue
top_customers = filtered_orders.groupby('customer_id')['total_amount'].sum().nlargest(10)
st.subheader("Top 10 Customers by Total Revenue")
st.bar_chart(top_customers)

# Line Chart: Total Revenue Over Time
revenue_over_time = filtered_orders.resample('M', on='order_date')['total_amount'].sum()
st.subheader("Total Revenue Over Time")
st.line_chart(revenue_over_time)

# Summary Section
total_revenue = filtered_orders['total_amount'].sum()
unique_customers = filtered_orders['customer_id'].nunique()
number_of_orders = len(filtered_orders)

st.subheader("Summary Metrics")
st.write(f"Total Revenue: ${total_revenue:.2f}")
st.write(f"Number of Unique Customers: {unique_customers}")
st.write(f"Number of Orders: {number_of_orders}")
