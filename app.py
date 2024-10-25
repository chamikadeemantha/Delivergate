import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# MySQL Database Connection Parameters
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_HOST = '127.0.0.1'  # Use 127.0.0.1 instead of localhost
MYSQL_PORT = 3306
MYSQL_DB = 'delivergatedb'

# Create a connection string and engine with connection pool settings
db_connection_str = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
engine = create_engine(db_connection_str, pool_size=5, max_overflow=2)

# Verify direct MySQL connection using mysql-connector-python
try:
    conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version:", data)
    conn.close()
    st.success("Successfully connected to the database!")
except mysql.connector.Error as e:
    st.error(f"Direct connection failed: {e}")

# Load data with error handling and cache
@st.cache_data
def load_data():
    try:
        customers_query = "SELECT * FROM customers"
        orders_query = "SELECT * FROM orders"
        customers_df = pd.read_sql(customers_query, con=engine)
        orders_df = pd.read_sql(orders_query, con=engine)
        return customers_df, orders_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()  # Return empty DataFrames if connection fails

# Load data
customers_df, orders_df = load_data()

# Sidebar Filters
st.sidebar.header('Filters')

# Date range filter
if not orders_df.empty:
    min_date = orders_df['order_date'].min()
    max_date = orders_df['order_date'].max()
    date_range = st.sidebar.date_input('Order Date Range', [min_date, max_date])
    # Filter orders based on the selected date range
    filtered_orders = orders_df[(orders_df['order_date'] >= pd.to_datetime(date_range[0])) & 
                                (orders_df['order_date'] <= pd.to_datetime(date_range[1]))]
else:
    st.warning("Orders data could not be loaded.")
    filtered_orders = pd.DataFrame()

# Slider to filter customers by total amount spent
if not filtered_orders.empty:
    total_spent = filtered_orders.groupby('customer_id')['total_amount'].sum().reset_index()
    spent_slider = st.sidebar.slider('Total Amount Spent (greater than)', 0, int(total_spent['total_amount'].max()), 1000)
    filtered_customers = total_spent[total_spent['total_amount'] > spent_slider]

    # Dropdown to filter customers by number of orders
    order_count = filtered_orders['customer_id'].value_counts().reset_index()
    order_count.columns = ['customer_id', 'num_orders']
    customer_order_filter = st.sidebar.selectbox('Customers with more than X orders', [1, 5, 10])
    filtered_order_count = order_count[order_count['num_orders'] > customer_order_filter]

    # Merge filtered data
    filtered_customers = pd.merge(filtered_customers, filtered_order_count, on='customer_id')
    final_filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(filtered_customers['customer_id'])]
else:
    st.warning("Filtered orders data is empty.")
    final_filtered_orders = pd.DataFrame()

# Main Dashboard
st.write("### Filtered Orders")
st.dataframe(final_filtered_orders)

# Bar chart for top 10 customers by total revenue
if not total_spent.empty:
    st.write("### Top 10 Customers by Total Revenue")
    top_customers = total_spent.sort_values(by='total_amount', ascending=False).head(10)
    fig, ax = plt.subplots()
    ax.barh(top_customers['customer_id'].astype(str), top_customers['total_amount'])
    ax.set_xlabel('Total Revenue')
    ax.set_ylabel('Customer ID')
    st.pyplot(fig)

# Line chart for total revenue over time
if not filtered_orders.empty:
    st.write("### Total Revenue Over Time")
    filtered_orders['order_date'] = pd.to_datetime(filtered_orders['order_date'])
    revenue_over_time = filtered_orders.resample('M', on='order_date')['total_amount'].sum()
    fig, ax = plt.subplots()
    ax.plot(revenue_over_time.index, revenue_over_time.values)
    ax.set_xlabel('Order Date')
    ax.set_ylabel('Total Revenue')
    st.pyplot(fig)

# Summary section showing key metrics
if not final_filtered_orders.empty:
    st.write("### Summary")
    total_revenue = final_filtered_orders['total_amount'].sum()
    unique_customers = final_filtered_orders['customer_id'].nunique()
    total_orders = final_filtered_orders['order_id'].nunique()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")
    st.metric("Unique Customers", unique_customers)
    st.metric("Total Orders", total_orders)
else:
    st.warning("No data available for the summary metrics.")
