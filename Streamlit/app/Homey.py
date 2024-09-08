# streamlit_app.py

import streamlit as st
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('gcs', type='sql')

# df = conn.query("SELECT * FROM Clubs")
df = conn.read("streamlit-bucket-try/Data_Test.sql", input_format="sql")

# Print results.
for row in df.itertuples():
    st.write(row)
