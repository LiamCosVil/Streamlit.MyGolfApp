# streamlit_app.py

import streamlit as st
from sqlalchemy.sql import text
import os
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')
connLoc = st.connection('MYSG', type='sql')

df = connLoc.query('SELECT * from Holes;', ttl=0)
os.write(1, f"{df}\n".encode()) 



if st.button("DO THE THING"):
    for index, row in df.iterrows():
        with conn.session as s:
            s.execute(text("""INSERT INTO Holes
                            (Hole_ID, Round_ID, Hole_Number, Played_As, Hole_Par, Hole_Score, Hole_Handycap, GIR,
                            Up_D, Fairway_OOT, Bunker_Up_D, Putts, Hole_Length) 
                            VALUES 
                            ("""+str(row["Hole ID"])+""", 
                            """+str(row["Round ID"])+""", 
                            """+str(row["Hole Number"])+""", 
                            """+str(row["Played As"])+""", 
                            """+str(row["Hole Par"])+""",
                            """+str(row["Hole Score"])+""",
                            """+str(row["Hole Handycap"])+""",
                            """+str(row["GIR"])+""",
                            """+str(row["UP&D"])+""",
                            """+str(row["Fairway OTT"])+""",
                            """+str(row["Bunker UP&D"])+""",
                            """+str(row["Hole Length"])+""",
                            """+str(row["Putts"])+"""
                            );"""))
            s.commit()
            os.write(1, f"{index}\n".encode()) 
    st.rerun()
