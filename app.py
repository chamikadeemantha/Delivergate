import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql

# Initialize connection using the connection details in secrets.toml
db_connection_str = f"mysql+pymysql://{st.secrets['connections']['mysql']['username']}:{st.secrets['connections']['mysql']['password']}@{st.secrets['connections']['mysql']['host']}:{st.secrets['connections']['mysql']['port']}/{st.secrets['connections']['mysql']['database']}"
engine = create_engine(db_connection_str)

# Load data from the MySQL database
@st.cache_data(ttl=600)  # Cache the result for 10 minutes
def load_data():
    query = "SELECT * FROM orders;"
    df = pd.read_sql(query, engine)
    return df

# Get the data
orders_df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

# Date range filter
min_date = pd.to_datetime(orders_df['order_date']).min()
max_date = pd.to_datetime(orders_df['order_date']).max()
date_range = st.sidebar.date_input("Select date range", [min_date, max_date])

# Filter by total amount spent
amount_spent = st.sidebar.slider("Filter by total amount spent", 
                                 min_value=float(orders_df['total_amount'].min()), 
                                 max_value=float(orders_df['total_amount'].max()), 
                                 value=float(orders_df['total_amount'].min()))

# Filter by number of orders
customer_orders_count = orders_df.groupby('customer_id').size()
order_count = st.sidebar.selectbox("Filter by number of orders", 
                                   options=[5, 10, 20, 50], index=0)

# Apply filters
filtered_orders = orders_df[
    (pd.to_datetime(orders_df['order_date']) >= pd.to_datetime(date_range[0])) &
    (pd.to_datetime(orders_df['order_date']) <= pd.to_datetime(date_range[1])) &
    (orders_df['total_amount'] >= amount_spent)
]

# Filter customers with more than selected number of orders
filtered_customers = customer_orders_count[customer_orders_count > order_count].index
filtered_orders = filtered_orders[filtered_orders['customer_id'].isin(filtered_customers)]

# Main Dashboard
st.header("Dashboard")

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_orders)

# Bar Chart: Top 10 customers by total revenue
st.subheader("Top 10 Customers by Total Revenue")
top_customers = filtered_orders.groupby('customer_id').sum().sort_values('total_amount', ascending=False).head(10)
st.bar_chart(top_customers['total_amount'])

# Line Chart: Total revenue over time (grouped by week or month)
st.subheader("Revenue Over Time")
filtered_orders['order_date'] = pd.to_datetime(filtered_orders['order_date'])
revenue_over_time = filtered_orders.resample('W', on='order_date').sum()  # Grouped by week
st.line_chart(revenue_over_time['total_amount'])

# Summary Section
st.subheader("Summary")
total_revenue = filtered_orders['total_amount'].sum()
unique_customers = filtered_orders['customer_id'].nunique()
total_orders = filtered_orders['order_id'].count()

st.metric("Total Revenue", f"${total_revenue:,.2f}")
st.metric("Number of Unique Customers", unique_customers)
st.metric("Total Number of Orders", total_orders)
