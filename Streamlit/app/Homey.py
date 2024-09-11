# streamlit_app.py

import streamlit as st
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection("myGCDB", type="sql")
connOld = st.connection("MYSG", type="sql")

# Perform query.
dfOld = connOld.query('SELECT * FROM Clubs;')
df = conn.query('SELECT * FROM Clubs;')


conn.query("CREATE TABLE TestClubs (ID , Name);")

conn.query("INSERT INTO TestClubs (ID, Name) VALUES (0, 'Driver')")

df = conn.query("'SELECT * FROM Clubs;")

for index, row in df.iterrows():
    st.write(str(row["ID"]) + str(row["Name"]))
