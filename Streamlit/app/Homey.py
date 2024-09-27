# streamlit_app.py

import streamlit as st
from sqlalchemy.sql import text
import os
# from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('HomeDB', type='sql')
connLoc = st.connection('MYSG', type='sql')

df = connLoc.query('SELECT * from Players;', ttl=0)
os.write(1, f"{df}\n".encode()) 



if st.button("DO THE THING"):
    for index, row in df.iterrows():
        with conn.session as s:
            s.execute(text("""INSERT INTO Players
                            (Player_ID, Player_Name, Player_Surename, Player_Handycap, Player_Gender) 
                            VALUES 
                            ("""+str(row["Player ID"])+""", 
                            '"""+str(row["Player Name"])+"""', 
                            '"""+str(row["Player Surename"])+"""', 
                            """+str(row["Player Handycap"])+""", 
                            '"""+str(row["Player Gender"])+"""')
                            ;"""))
            s.commit()
            os.write(1, f"{index}\n".encode()) 
    st.rerun()
