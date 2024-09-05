import pandas as pd
import streamlit as st
#from app.AddRound.GetDataAddRoundTest2 import *

conn = st.connection('MYSG', type='sql')
#Save_File.Write(New_DFs.Round(), New_DFs.Holes(), New_DFs.Shots())
#with conn.session as s:
#    s.execute(text('DELETE FROM Courses WHERE [Course ID] = 4;'))
#    s.commit()


df = conn.query("SELECT MAX([Hole ID]+0) as [NUM] FROM Holes;")
print(df)
#df = DFs.Courses_df()
#print(df)