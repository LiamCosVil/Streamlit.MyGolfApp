# streamlit_app.py

import streamlit as st
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection("myGCDB", type="sql")

# Perform query.
df = conn.query('SELECT * FROM Clubs;', ttl="10m")

print(df)
# Print results.
for row in df.itertuples():
    st.write(row)
