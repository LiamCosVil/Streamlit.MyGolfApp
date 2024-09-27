# streamlit_app.py

import streamlit as st
from sqlalchemy.sql import text
import os
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')
connLoc = st.connection('MYSG', type='sql')

df = connLoc.query('SELECT * from Rounds;', ttl=0)
os.write(1, f"{df}\n".encode()) 



if st.button("DO THE THING"):
    for index, row in df.iterrows():
        with conn.session as s:
            s.execute(text("""INSERT INTO Rounds
                            (Round_ID, Player_ID, Total_Score, Total_Par, Holes_Played, Tees_Played, Course_ID, Competition,
                            Weather, Wind, Date, Score2Par) 
                            VALUES 
                            ("""+str(row["Round ID"])+""", 
                            """+str(row["Player ID"])+""", 
                            """+str(row["Total Score"])+""", 
                            """+str(row["Total Par"])+""", 
                            """+str(row["Holes Played"])+"""
                            '"""+str(row["Tees Played"])+"""'
                            """+str(row["Course Played"])+"""
                            """+str(row["Competition?"])+"""
                            '"""+str(row["Weather"])+"""'
                            '"""+str(row["Wind"])+"""'
                            '"""+str(row["Date"])+"""'
                            '"""+str(row["Score2Par"])+"""'
                            );"""))
            s.commit()
            os.write(1, f"{index}\n".encode()) 
    st.rerun()
