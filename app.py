import streamlit as st

conn = st.experimental_connection('mysql', type='sql')
df = conn.query('SELECT * from customers;', ttl=600)
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")