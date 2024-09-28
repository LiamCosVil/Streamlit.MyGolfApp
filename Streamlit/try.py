import pandas as pd
import streamlit as st
from sqlalchemy.sql import text
from app.AddRound.GetDataAddRoundTest2 import *

conn = st.connection('HomeDB', type='sql')

df = conn.query('SELECT * from mytable;', ttl=600)
print(df)

#LeaderBoard_S.Save_Rounds_4_Leadrerboard()


#conn = st.connection('MYSG', type='sql')
#Save_File.Write(New_DFs.Round(), New_DFs.Holes(), New_DFs.Shots())
#with conn.session as s:
#    s.execute(text('DELETE FROM Rounds WHERE [Round ID] = "10";'))
#    s.commit()


#df = conn.query("SELECT MAX([Hole ID]+0) as [NUM] FROM Holes;").values[0][0]
#print(df)
#df = DFs.Courses_df()
#print(df)


#with conn.session as s:
#    s.execute(text('''INSERT INTO Clubs ([Club ID], [Club Name]) VALUES('19','jh ffd')'''))
#    s.commit()


#print(Players.All_Indeses())


# Define connection parameters
#conn = st.connection('myGCDB', type='sql')

#print("OK")
#df = conn.query('SELECT * FROM home;', ttl="1m")

# Print results.
#for row in df.itertuples():
#    print(f"{row.name} has a :{row.pet}:")