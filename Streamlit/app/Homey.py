# streamlit_app.py

import streamlit as st
from sqlalchemy.sql import text
import os
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')
connLoc = st.connection('MYSG', type='sql')

df = connLoc.query('SELECT * from Courses;', ttl=0)
os.write(1, f"{df}\n".encode()) 



if st.button("DO THE THING"):
    for index, row in df.iterrows():
        with conn.session as s:
            s.execute(text("""INSERT INTO Courses
                            (Course_ID, Course_Name, Course_Par, Course_Holes, Course_Location) 
                            VALUES 
                            ("""+str(row["Course ID"])+""", 
                            '"""+str(row["Course Name"])+"""', 
                            """+str(row["Course Par"])+""", 
                            """+str(row["Course Holes"])+""", 
                            '"""+str(row["Course Location"])+"""')
                            ;"""))
            s.commit()
    st.rerun()
