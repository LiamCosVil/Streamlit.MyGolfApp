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
if st.button("Press to do"):
    print(dfOld)
    print(df)
