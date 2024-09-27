# streamlit_app.py

import streamlit as st
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')

df = conn.query('SELECT * from Test_Table;', ttl=600)

for index, row in df.iterrows():
    st.write(str(row["colorID"]) + str(row["color"]))

if st.button("DO THING"):
    df = conn.query("INSERT INTO Test_Table (colorID, color) VALUES (2, 'Blue');", ttl=600)
