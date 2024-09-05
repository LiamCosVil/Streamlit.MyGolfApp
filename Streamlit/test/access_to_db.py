import pandas as pd
import streamlit as st
from to_delete.GetDataAddRound import *
from sqlalchemy.sql import text

conn = st.connection('MYSG', type='sql')

df = Get_Access.ShotsInfo()

print(df)

#for i in df.index:

with conn.session as s:
    
    for i in df.index:
        s.execute(text(
            "INSERT INTO Shots ([Shot ID], [Hole ID], [Shot Number], [Distance2Hole], [Clubs], [Lie], [Desired Shot Type], [Slope], [Recovery Shot?], [Shot Type], [Distance After Shot], [In The Hole?], [Fall (Only Putt)]) VALUES ('"
            +str(df['Shot ID'][i])+"', '"
            +str(df['Hole ID'][i])+"', '"
            +str(df['Shot Number'][i])+"', '"
            +str(df['Distance2Hole'][i])+"', '"
            +str(df['Clubs'][i])+"', '"
            +str(df['Lie'][i])+"', '"
            +str(df['Desired Shot Type'][i])+"', '"
            +str(df['Slope'][i])+"', '"
            +str(df['Recovery Shot?'][i])+"', '"
            +str(df['Shot Type'][i])+"', '"
            +str(df['Distance After Shot'][i])+"', '"            
            +str(df['In The Hole?'][i])+"', '"
            +str(df['Fall (Only Putt)'][i])+"');")
        )
    s.commit()



with conn.session as s:
    
    s.execute(text('DROP TABLE pet_owners;'))
    #s.execute(text('CREATE TABLE IF NOT EXISTS Holes ([Hole ID], [Round ID], [Hole Number], [Played As], [Hole Par], [Hole Score], [Hole Handycap], [GIR], [UP&D], [Fairway OTT], [Bunker UP&D], [Putts], [Hole Length]);'))
    #s.execute(text('DELETE FROM Clubs;'))
    #s.execute(text('ALTER TABLE Clubs DROP ROWID;'))
    s.commit()