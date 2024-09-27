# streamlit_app.py

import streamlit as st
from sqlalchemy.sql import text
import os
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')

df = conn.query('SELECT * from Test_Table;', ttl=600)
os.write(1, f"{df}\n".encode()) 
for index, row in df.iterrows():
    st.write(str(row["colorID"]) + str(row["color"]))

if st.button("DO THE THING"):
    with conn.session as s:
        s.execute(text("INSERT INTO Test_Table (colorID, color) VALUES (2, 'Blue');"))
        s.commit()
