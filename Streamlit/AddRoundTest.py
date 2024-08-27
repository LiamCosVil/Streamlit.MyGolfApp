import streamlit as st
import pandas as pd
from GetDataAddRoundTest import *

# TASk, create internal sql file, so that i can save the three dfs below upon refresh

New_Round_df, New_Holes_df, New_Shots_df = Save_File.Read()

@st.dialog("Are you sure")
def Restart_popup():
    st.write("You will loose all you round progress")
    col1, col2 = st.columns([5,2])
    Restart_N, Restart_Y = col2.columns(2)
    if Restart_Y.button("Yes"):
        New_Round_df, New_Holes_df, New_Shots_df = New_DFs.Round(), New_DFs.Holes(), New_DFs.Shots()
        Save_File.Write(New_Round_df, New_Holes_df, New_Shots_df)
        st.rerun()
    if Restart_N.button("No"):
        st.rerun()
@st.dialog("Add New Course")
def Add_course_popup():
    st.write("Please fill up all the inputs before pressing the button")
    Course_Name = st.text_input("Course Name")
    Course_Par = st.number_input("Course Par", value=72)
    Course_Holes = st.number_input("Course Holes", value=18)
    Course_Location = st.text_input("Course Location")
    
    col1, col2 = st.columns([5,2])
    if col2.button("Add course"):
        ExcelAppend.Course(Course_Name, Course_Par, Course_Holes, Course_Location)
        st.rerun()

Title_Con = st.container()
Title_Col, Restart_Col = Title_Con.columns([10,1])
Other_Con = st.container()
LeaderBoard_S_Tab, LeaderBoard_M_Tab, Round_Tab = Other_Con.tabs(["Leaderboard (Single)", "Leaderboard (Monthly)", "Round"])

Title_Col.header("Add Round")
Restart = Restart_Col.button("Delete Round")
if Restart:
    Restart_popup()


with st.sidebar:
    # PLAYER
    All_Names = Players.All_names()
    Player_Name = (st.selectbox("Who's Playing?",
                 options= All_Names,
                 index= Extras.Return_Index_Of(Players.Name(New_Round_df.at[0, "Player ID"]), All_Names)
                 ))
    New_Round_df.at[0, "Player ID"] = Players.ID(Player_Name)

    # TEES PLAYED
    All_Tees = ["Black", "White", "Yellow", "Blue", "Red", "Orange"] + ["-"]
    Tees_Played = (st.selectbox("What Tee?",
                 options= All_Tees,
                 index= Extras.Return_Index_Of(New_Round_df.at[0, "Tees Played"], All_Tees)
                 ))
    New_Round_df.at[0, "Tees Played"] = Tees_Played

    # COURSE PLAYED

    All_Courses = Courses.All_names() + ["-"]
    Course_Played = (st.selectbox("What Course?",
                 options= All_Courses,
                 index= Extras.Return_Index_Of(New_Round_df.at[0, "Course Played"], All_Courses)
                 ))
    New_Round_df.at[0, "Course Played"] = Course_Played
    
    Add_Course = st.button("Add New")
    if Add_Course:
        Add_course_popup()

with LeaderBoard_S_Tab:
    DF = LeaderBoard_S.Return_DF()
    st.dataframe(data=DF, hide_index=True, use_container_width = True, selection_mode="single-row")

with LeaderBoard_M_Tab:
    pass

with Round_Tab:
    Total_Holes = 18
    for Hole_Number in range(Total_Holes):
        with st.expander("Hole " + str(Hole_Number+1)):
            st.write("Hole " + str(Hole_Number+1))
            HI_Col1, HI_Col2, HI_Col3, HI_Col4 = st.columns(4)
            # Played As
            HI_Played_As = HI_Col1.number_input("Played As", min_value=1, value=Hole_Number+1, key="HIPlayedAs"+str(Hole_Number+1))
            # Hole Par
            HI_Hole_Par = HI_Col2.number_input("Par", min_value=1 ,value=4, key="HIPar"+str(Hole_Number+1))
            # Hole Handycap
            HI_Hole_Handycap = HI_Col3.number_input("Handycap", 1, 18, value=1, key="HIHandycap"+str(Hole_Number+1))
            # Hole Score
            HI_Hole_Score = HI_Col4.number_input("Score", min_value=1, value=HI_Hole_Par, key="HIScore"+str(Hole_Number+1))


Save_File.Write(New_Round_df, New_Holes_df, New_Shots_df)

