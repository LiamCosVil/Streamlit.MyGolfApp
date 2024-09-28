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
    for index, row in df.iterrows():
        with conn.session as s:
            s.execute(text("""INSERT INTO Shots
                            (Shot_ID, Hole_ID, Shot_Number, Distance_2_hole, Club_ID, Lie,
                            Desired_Shot_Type, Slope, Recovery_Shot, Shot_Type, 
                            Distance_After, In_The_Hole, Fall_Putt) 
                            VALUES 
                            ("""+str(row["Shot ID"])+""", 
                            """+str(row["Hole ID"])+""", 
                            """+str(row["Shot Number"])+""", 
                            """+str(row["Distance2Hole"])+""", 
                            """+str(row["Clubs"])+""",
                            '"""+str(row["Lie"])+"""',
                            '"""+str(row["Desired Shot Type"])+"""',
                            '"""+str(row["Slope"])+"""',
                            """+str(row["Recovery Shot?"])+""",
                            '"""+str(row["Shot Type"])+"""',
                            """+str(row["Distance After Shot"])+""",
                            """+str(row["In The Hole?"])+""",
                            '"""+str(row["Fall (Only Putt)"])+"""'
                            );"""))
            s.commit()
            os.write(1, f"{index}\n".encode()) 
    st.rerun()
