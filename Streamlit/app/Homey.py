# streamlit_app.py

import streamlit as st
from sqlalchemy.sql import text
import os
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('MyGolf', type='sql')
connLoc = st.connection('MYSG', type='sql')

df = connLoc.query('SELECT * from Clubs;', ttl=0)
os.write(1, f"{df}\n".encode()) 



if st.button("DO THE THING"):
    for index, row in df.iterrows():
        with conn.session as s:
            s.execute(text("INSERT INTO Clubs (Club_ID, Club_Name) VALUES ("+str(row["Club ID"])+", '"+str(row["Club Name"])+"');"))
            s.commit()
    st.rerun()
