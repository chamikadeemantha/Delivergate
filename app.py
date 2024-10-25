import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str)

# Load data from MySQL
@st.cache_data
def load_data():
    customers = pd.read_sql('SELECT * FROM customers', con=engine)
    orders = pd.read_sql('SELECT * FROM orders', con=engine)
    return customers, orders

# Load data
customers_df, orders_df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# Date Range Filter
min_date = orders_df['order_date'].min()
max_date = orders_df['order_date'].max()
date_range = st.sidebar.date_input("Select Order Date Range:", [min_date, max_date])
filtered_orders_df = orders_df[(orders_df['order_date'] >= pd.Timestamp(date_range[0])) & (orders_df['order_date'] <= pd.Timestamp(date_range[1]))]

# Total Amount Slider Filter
min_amount, max_amount = int(filtered_orders_df['total_amount'].min()), int(filtered_orders_df['total_amount'].max())
total_amount_filter = st.sidebar.slider("Filter by Total Amount Spent:", min_amount, max_amount, min_amount)
filtered_orders_df = filtered_orders_df[filtered_orders_df['total_amount'] >= total_amount_filter]

# Filter by Number of Orders
customer_order_counts = filtered_orders_df['customer_id'].value_counts()
customer_min_orders = st.sidebar.slider("Customers with Minimum Number of Orders:", 1, 10, 1)
filtered_customers = customer_order_counts[customer_order_counts >= customer_min_orders].index
filtered_orders_df = filtered_orders_df[filtered_orders_df['customer_id'].isin(filtered_customers)]

# Main Dashboard
st.title("Delivergate Orders Dashboard")

# Display filtered data
st.subheader("Filtered Orders")
st.dataframe(filtered_orders_df)

# Aggregate Data for Summary
total_revenue = filtered_orders_df['total_amount'].sum()
unique_customers = filtered_orders_df['customer_id'].nunique()
total_orders = filtered_orders_df['order_id'].nunique()

# Summary Section
st.subheader("Summary")
st.write(f"Total Revenue: ${total_revenue:,.2f}")
st.write(f"Number of Unique Customers: {unique_customers}")
st.write(f"Number of Orders: {total_orders}")

# Top 10 Customers by Revenue
top_customers = (
    filtered_orders_df.groupby('customer_id')['total_amount']
    .sum()
    .nlargest(10)
    .reset_index()
    .merge(customers_df, on='customer_id')
)
st.subheader("Top 10 Customers by Total Revenue")
st.bar_chart(data=top_customers, x='customer_name', y='total_amount')

# Revenue Over Time (Line Chart)
st.subheader("Revenue Over Time")
filtered_orders_df['order_date'] = pd.to_datetime(filtered_orders_df['order_date'])
revenue_over_time = filtered_orders_df.set_index('order_date').resample('W')['total_amount'].sum()
st.line_chart(revenue_over_time)
