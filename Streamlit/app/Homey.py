# streamlit_app.py

import streamlit as st
from sqlalchemy.sql import text
import os
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')
connLoc = st.connection('MYSG', type='sql')

df = connLoc.query('SELECT * from Shots;', ttl=0)
os.write(1, f"{df}\n".encode()) 



if st.button("DO THE THING"):
    st.rerun()
