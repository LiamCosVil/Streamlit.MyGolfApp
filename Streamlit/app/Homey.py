# streamlit_app.py

import streamlit as st
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')

df = conn.query('SELECT * from mytable;', ttl=600)

for index, row in df.iterrows():
    st.write(str(row["ID"]) + str(row["Name"]))
