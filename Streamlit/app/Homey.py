# streamlit_app.py

import streamlit as st
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection("myGCDB", type="sql")
connOld = st.connection("MYSG", type="sql")

# Perform query.
conn.query("CREATE TABLE ClubsTest ("Club ID" SERIAL PRIMARY KEY,"Club Name" VARCHAR(100));")
