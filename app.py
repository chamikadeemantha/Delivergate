import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from datetime import datetime

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Empty password as per XAMPP config
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string
db_connection_str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str)

# Load data from the MySQL database using a connection
try:
    with engine.connect() as connection:
        customers_df = pd.read_sql('SELECT * FROM customers', con=connection)
        orders_df = pd.read_sql('SELECT * FROM orders', con=connection)
except Exception as e:
    st.error(f"Database connection error: {e}")

# Merge DataFrames for analysis
merged_df = pd.merge(orders_df, customers_df, on='customer_id')

# Streamlit app layout
st.title("Delivergate Order Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
start_date, end_date = st.sidebar.date_input("Select date range", [datetime(2023, 1, 1), datetime.now()])
filtered_orders = merged_df[(merged_df['order_date'] >= pd.to_datetime(start_date)) & 
                             (merged_df['order_date'] <= pd.to_datetime(end_date))]

# Slider for total amount spent
min_amount, max_amount = st.sidebar.slider("Total amount spent", 0.0, float(merged_df['total_amount'].max()), (0.0, float(merged_df['total_amount'].max())))
filtered_orders = filtered_orders[(filtered_orders['total_amount'] >= min_amount) & 
                                   (filtered_orders['total_amount'] <= max_amount)]

# Dropdown for filtering customers by number of orders
order_count_threshold = st.sidebar.number_input("Minimum number of orders", min_value=1, value=5)
customer_counts = filtered_orders['customer_id'].value_counts()
valid_customers = customer_counts[customer_counts > order_count_threshold].index.tolist()
filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(valid_customers)]

# Main dashboard display
st.header("Filtered Orders")
st.dataframe(filtered_orders)

# Top 10 customers by total revenue
top_customers = filtered_orders.groupby('customer_name')['total_amount'].sum().nlargest(10)
st.subheader("Top 10 Customers by Total Revenue")
st.bar_chart(top_customers)

# Total revenue over time
revenue_over_time = filtered_orders.groupby(filtered_orders['order_date'].dt.to_period('M'))['total_amount'].sum()
st.subheader("Total Revenue Over Time")
st.line_chart(revenue_over_time)

# Summary metrics
total_revenue = filtered_orders['total_amount'].sum()
unique_customers = filtered_orders['customer_id'].nunique()
number_of_orders = filtered_orders.shape[0]

st.subheader("Summary Metrics")
st.write(f"Total Revenue: ${total_revenue:.2f}")
st.write(f"Number of Unique Customers: {unique_customers}")
st.write(f"Number of Orders: {number_of_orders}")