import streamlit as st
import pandas as pd
from AddRound.GetDataAddRoundTest2 import *


def Calculate_Extras():
    # Calculate Extras
    TotalPar = 0
    TotalScore = 0
    for index, row in New_Holes_df.iterrows():
        TotalPar += row["Hole_Par"]
        TotalScore += row["Hole_Score"]
    New_Round_df.at[0, "Total_Par"] = TotalPar
    New_Round_df.at[0, "Total_Score"] = TotalScore
    TotalScore2Par = TotalScore - TotalPar
    New_Round_df.at[0, "Score2Par"] = TotalScore2Par

New_Round_df, New_Holes_df, New_Shots_df = Save_File.Read()

@st.dialog("Delete Round")
def Restart_popup():
    st.write("You will loose all you round progress")
    col1, col2 = st.columns([5,2])
    Restart_N, Restart_Y = col2.columns(2)
    if Restart_Y.button("Yes"):
        New_Round_df, New_Holes_df, New_Shots_df = New_DFs.Round(), New_DFs.Holes(), New_DFs.Shots()
        
        Save_File.Write(New_Round_df, New_Holes_df, New_Shots_df)
        LeaderBoard_S.RestartExcel()
        st.rerun()
    if Restart_N.button("No"):
        st.rerun()
@st.dialog("Add New Course")
def Add_course_popup():
    st.write("Please fill up all the inputs before pressing the button")
    add_course_form = st.form("add_course_form", border=False)
    Course_Name = add_course_form.text_input("Course Name")
    Course_Par = add_course_form.number_input("Course Par", value=72)
    Course_Holes = add_course_form.number_input("Course Holes", value=18)
    Course_Location = add_course_form.text_input("Course Location")
    
    col1, col2 = st.columns([5,2])
    with col2:
        if add_course_form.form_submit_button("Add course"):
            AccessWrite.Course(Course_Name, Course_Par, Course_Holes, Course_Location)
            st.rerun()
@st.dialog("Finish & Save Round")
def Save_Round(New_Round_df, New_Holes_df, New_Shots_df):
    Check_TF, Errors = Checks_Save.CheckRoundComplete(New_Round_df, New_Holes_df, New_Shots_df)
    if Check_TF:
        st.write("Are you sure you want to finish your round now?")
        st.write("You will not be able to change anything from the round after this.")
        R_Score, R_HolesPlayed, R_Par = Checks_Save.Return_Round_Info(New_Round_df, New_Holes_df, New_Shots_df)
        st.divider()
        st.write("Holes Played: "+str(R_HolesPlayed))
        st.write("Total Par: "+str(R_Par))
        st.write("You scored: "+str(R_Score))
        st.write("To Par: "+str(R_Score-R_Par))
        st.divider()
        st.write("Make sure the info above is correct before saving")
        col1, col2 = st.columns([5,2])
        Save_N, Save_Y = col2.columns(2)
        if Save_Y.button("Yes"):
            AccessWrite.SaveCompleteRound(New_Round_df, New_Holes_df, New_Shots_df)
            New_Round_df, New_Holes_df, New_Shots_df = New_DFs.Round(), New_DFs.Holes(), New_DFs.Shots()
            Save_File.Write(New_Round_df, New_Holes_df, New_Shots_df)
            st.rerun()
        if Save_N.button("No"):
            st.rerun()
    else:
        st.write("Your Round has errors")
        st.write("Errors: " + str(Errors))
        st.write("Fiz these before saving the round")
        
Title_Con = st.container()
Title_Col, Save_Round_Col, Restart_Col = Title_Con.columns([9,1,1])
Other_Con = st.container()
Round_Tab, LeaderBoard_S_Tab  = Other_Con.tabs(["Round", "Leaderboard (Single)"])

Title_Col.header("Add Round")
Restart = Restart_Col.button("Delete Round")
if Restart:
    Restart_popup()
if Save_Round_Col.button("Finish Round"):
    New_Shots_df = New_Shots_df.sort_values(by=["Hole_ID", "Shot_Number"])
    Save_Round(New_Round_df, New_Holes_df, New_Shots_df)

with st.sidebar:
    Round_Form = st.form("round_form", border=False)
    # PLAYER
    All_Names = Players.All_names()
    Player_Name = (Round_Form.selectbox("Who's Playing?",
                 options= All_Names,
                 index= Extras.Return_Index_Of(Players.Name(New_Round_df.at[0, "Player_ID"]), All_Names)
                 ))
    New_Round_df.at[0, "Player_ID"] = Players.ID(Player_Name)

    # TEES PLAYED
    All_Tees = ["Black", "White", "Yellow", "Blue", "Red", "Orange"] + ["-"]
    Tees_Played = (Round_Form.selectbox("What Tee?",
                 options= All_Tees,
                 #index=3
                 index= Extras.Return_Index_Of(New_Round_df.at[0, "Tees_Played"], All_Tees),
                 
                 ))
    New_Round_df.at[0, "Tees_Played"] = Tees_Played

    # COURSE PLAYED
    All_Courses = Courses.All_names() + ["-"]
    Course_Played = (Round_Form.selectbox("What Course?",
                 options= All_Courses,
                 index= Extras.Return_Index_Of(New_Round_df.at[0, "Course_ID"], All_Courses)
                 ))
    New_Round_df.at[0, "Course_ID"] = Course_Played
    
    #Add_Course = st.button("Add New")
    #if Add_Course:
    #    Add_course_popup()
    
    # IS COMPETITION
    Is_Competition = Round_Form.checkbox("Competition?")
    New_Round_df.at[0, "Competition"] = Is_Competition
    
    # WEATHER
    All_Weather = ["Very Hot & Sunny", "Sunny", "Some Clouds", "Cloudy", "Small Showers", "Rainy", "Heavy Rain", "-"]
    Weather = (Round_Form.selectbox("How was the weather?",
                 options= All_Weather,
                 index= Extras.Return_Index_Of(New_Round_df.at[0, "Weather"], All_Weather)
                 ))
    New_Round_df.at[0, "Weather"] = Weather
    
    # WIND
    All_Wind = ["No Wind", "Some Wind", "Decent Amount", "Crazy strong Wind", "-"]
    Wind = (Round_Form.selectbox("How was the wind?",
                 options= All_Wind,
                 index= Extras.Return_Index_Of(New_Round_df.at[0, "Wind"], All_Wind)
                 ))
    New_Round_df.at[0, "Wind"] = Wind
    
    
    # DATE
    Date = Round_Form.date_input("Date", value=pd.to_datetime("today"), key="Date")
    New_Round_df.at[0, "Date"] = Date

    
    if Round_Form.form_submit_button("Save"):
        LeaderBoard_S.Save_Rounds_4_Leadrerboard()
        

with LeaderBoard_S_Tab:
    try:
        DF = LeaderBoard_S.Return_DF(New_Round_df.at[0, "Holes_Played"], New_Round_df.at[0, "Score2Par"])
        st.dataframe(data=DF, 
                    hide_index=True, 
                    use_container_width = True, 
                    selection_mode="single-row", 
                    column_config={"Position":st.column_config.Column(width="small"),
                                    "Name (Date)":st.column_config.Column(width="medium"),
                                    "Score":st.column_config.Column(width="small"),
                                    "Through":st.column_config.Column(width="small")
                                    })
    except IndexError:
        st.header("Save the Sidebar Options before viewing leaderboard")



with Round_Tab:
    Holes_Cont_Empty = st.empty()
    Add_Hole_Col, Del_Hole_Col,Save_Round_Col = st.columns([2,15,2])
    if Add_Hole_Col.button("Add Hole"):
        New_Round_df.at[0, "Holes_Played"] += 1
        New_Holes_df = pd.concat([New_Holes_df, New_DFs.Holes(
            Hole_Number=New_Round_df.at[0, "Holes_Played"],
            HoleID=New_Round_df.at[0, "Holes_Played"]-1
            )], ignore_index=True)
        New_Shots_df = pd.concat([New_Shots_df, New_DFs.Shots(
            ShotID=str(New_Round_df.at[0, "Holes_Played"]-1)+"-"+"0",
            HoleID=New_Round_df.at[0, "Holes_Played"]-1,
                )], ignore_index=True)
    if New_Round_df.at[0, "Holes_Played"] > 1:
        if Del_Hole_Col.button("Delete Hole"):
            New_Holes_df = New_Holes_df.drop(New_Round_df.at[0, "Holes_Played"]-1)
            
            for index, row in New_Shots_df.iterrows():

                if int(New_Round_df.at[0, "Holes_Played"]-1) == int(row["Shot_ID"][0]):
                    New_Shots_df = New_Shots_df.drop(index)
            New_Round_df.at[0, "Holes_Played"] -= 1

    
        
    Holes_Cont = Holes_Cont_Empty.container()
    for Hole_Number in range(New_Round_df.at[0, "Holes_Played"]):
        with Holes_Cont.expander("Hole " + str(Hole_Number+1)):
            st.write("Hole " + str(Hole_Number+1))
            Hole_Form_Early = st.form("Form Hole Early"+str(Hole_Number), border=True)
            Shots_Cont_Empty = st.empty()  
            Hole_Form_Late = st.form("Form Hole Late"+str(Hole_Number), border=True)
            
            # SHOTS
            
            Shots_Cont = Shots_Cont_Empty.container()
            Tabs_Col, Add_Shot_Col, Rem_Shot_Col = Shots_Cont.columns([11,1,1])
            if Add_Shot_Col.button("Add", key="AddShot"+str(Hole_Number+1)):
                New_Holes_df.at[Hole_Number, "Shots_Played"] += 1
                New_DF_Lie = "Green"
                New_DF_PT = True
                if (New_Holes_df.at[Hole_Number, "Hole_Par"] == 4) and (New_Holes_df.at[Hole_Number, "Shots_Played"] == 2):
                    New_DF_Lie = "Fairway"
                    New_DF_PT = False
                elif (New_Holes_df.at[Hole_Number, "Hole_Par"] == 5) and ((New_Holes_df.at[Hole_Number, "Shots_Played"] == 3)or(New_Holes_df.at[Hole_Number, "Shots_Played"] == 2)):
                    New_DF_Lie = "Fairway"
                    New_DF_PT = False
                New_Shots_df = pd.concat([New_Shots_df, New_DFs.Shots(
                    ShotID=str(Hole_Number)+"-"+str(New_Holes_df.at[Hole_Number, "Shots_Played"]-1),
                    HoleID=Hole_Number,
                    Shot_Num=New_Holes_df.at[Hole_Number, "Shots_Played"],
                    Distance = 100.0,
                    #DO IF PAR 3 THEN GREEN, PAR 4 THEN FW THEN GREEN...
                    Lie=New_DF_Lie,
                    Putt_Toggle=New_DF_PT
                    
                     )], ignore_index=True)
                
            if New_Holes_df.at[Hole_Number, "Shots_Played"] > 1:
                if Rem_Shot_Col.button("Rmv", key="RemShot"+str(Hole_Number+1)):
                    # DELETE SHOTS FROM THAT HOLE
                    
                    for index, row in New_Shots_df.iterrows():
                        if int(Hole_Number) == int(row["Shot_ID"][0]):
                            if int(New_Holes_df.at[Hole_Number, "Shots_Played"]-1) == int(row["Shot_ID"][2]):
                                New_Shots_df = New_Shots_df.drop(index)
                    # DONT LET IT GO DOWN TO 0, SAME WIOTH HOLES
                    New_Holes_df.at[Hole_Number, "Shots_Played"] -= 1
                    
                    
                                    
                                
                                
            Tabs_ID_List = []
            for Shot_Num in range(New_Holes_df.at[Hole_Number, "Shots_Played"]):
                Tabs_ID_List.append("Shot "+str(Shot_Num+1))
                
            Tabs_List = Tabs_Col.tabs(Tabs_ID_List)
            for Shot_Num in range(len(Tabs_List)):
                with Tabs_List[Shot_Num]:
                    
                    Shot_ID = str(Hole_Number)+"-"+str(Shot_Num)
                    DF_Shot_ID = list(New_Shots_df.loc[New_Shots_df['Shot_ID'] == Shot_ID].index)[0]
                    IS_Putt = st.toggle("Putt?", value=New_Shots_df.at[DF_Shot_ID, "Putt_Toggle"] ,key="ISPUTT"+Shot_ID)
                    New_Shots_df.at[DF_Shot_ID, "Putt_Toggle"] = bool(IS_Putt)
                    
                    Shot_Form = st.form("Shot Form"+str(Hole_Number)+str(Shot_Num), border=True)
                    # SHOT ID
                    SI_Shot_ID = Shot_ID
                    #New_Shots_df.at[Hole_Number+Shot_Num, "Hole Number"] = HI_Hole_Num
                    # HOLE ID
                    SI_Hole_ID = Hole_Number
                    
                    if IS_Putt:
                        COL_Shotnum, COL_Dist = Shot_Form.columns(2)
                        COL_Lie, COL_Slope = Shot_Form.columns(2)
                        COL_Fall, COL_In = Shot_Form.columns(2)
                    else:
                        COL_Shotnum, COL_Dist, COL_Club= Shot_Form.columns(3)
                        COL_Lie, COL_Slope, COL_Recov = Shot_Form.columns(3)
                        COL_Desired, COL_Outcome, COL_In = Shot_Form.columns(3)
                    
                    # SHOT NUMBER
                    SI_Shot_Number = COL_Shotnum.number_input("Shot_Number",
                                                            min_value=1,
                                                            value=New_Shots_df.at[DF_Shot_ID, "Shot_Number"],
                                                            key="SIShotID"+str(Hole_Number+1)+str(Shot_Num+1))
                    New_Shots_df.at[DF_Shot_ID, "Shot_Number"] = SI_Shot_Number
                    # Distance2Hole
                    if SI_Shot_Number != 1:

                        SI_Shot_Distance = float(COL_Dist.number_input("Distance",
                                                                min_value=0.0,
                                                                value=float(New_Shots_df.at[DF_Shot_ID, "Distance_2_Hole"]),
                                                                step = 0.1,
                                                                key="SIDistance2Hole"+str(Hole_Number+1)+str(Shot_Num+1)))
                        New_Shots_df.at[DF_Shot_ID, "Distance_2_Hole"] = SI_Shot_Distance
                    # Club
                    if not IS_Putt:
                        All_Clubs = Clubs.All_names()
                        SI_Club = COL_Club.selectbox("Club Used",
                                                  All_Clubs,
                                                  index=Extras.Return_Index_Of(New_Shots_df.at[DF_Shot_ID, "Club_ID"],All_Clubs),
                                                  key="SIClub"+str(Hole_Number+1)+str(Shot_Num+1))
                        New_Shots_df.at[DF_Shot_ID, "Club_ID"] = SI_Club
                    else:
                        New_Shots_df.at[DF_Shot_ID, "Club_ID"] = "Putter"
                    # Lie
                    All_Lies = ["Fairway", "Fairway (Bad Lie)", "Green", "Bunker (Soft)", "Bunker (Hard)", "Semi Rough", "Rough", "Heavy Rough", "Bushes & Tall Grass", "Off a Tee"]
                    SI_Lie = COL_Lie.selectbox("How was the Lie?",
                                                  options= All_Lies,
                                                  index=Extras.Return_Index_Of(New_Shots_df.at[DF_Shot_ID, "Lie"],All_Lies),
                                                  key="SILie"+str(Hole_Number+1)+str(Shot_Num+1))
                    New_Shots_df.at[DF_Shot_ID, "Lie"] = SI_Lie
                    # Desired Shot
                    if not IS_Putt:
                        All_Shot_Types_Des = ["Straight", "Punch StraigSht", "High Fade", "Punch Fade", "High Draw", "Punch Draw", "Half Swing", "Recovery Straight", "Recovery Fade", "Recovery Draw", "Flop (Full)", "Flop (Half)", "Chip (Runner)", "Chip (Spinny)", "Bunker (Runner)", "Bunker (Spinny)", "Putt"]
                        SI_Des_Shot = COL_Desired.selectbox("Desired Shot",
                                                        options=All_Shot_Types_Des,
                                                        index=Extras.Return_Index_Of(New_Shots_df.at[DF_Shot_ID, "Desired_Shot_Type"], All_Shot_Types_Des),
                                                        key="SIDesShot"+str(Hole_Number+1)+str(Shot_Num+1))
                    else:
                        SI_Des_Shot = "Putt"
                    New_Shots_df.at[DF_Shot_ID, "Desired_Shot_Type"] = SI_Des_Shot
                    # Slope
                    All_Slopes = ["Flat", "Uphill", "Downhill", "Wind With", "Wind Against"]
                    SI_Slope = COL_Slope.selectbox("Slope",
                                                   options=All_Slopes,
                                                   index=Extras.Return_Index_Of(New_Shots_df.at[DF_Shot_ID, "Slope"],All_Slopes),
                                                   key="SISlope"+str(Hole_Number+1)+str(Shot_Num+1))
                    New_Shots_df.at[DF_Shot_ID, "Slope"] = SI_Slope
                    # Recovery Shot
                    if not IS_Putt:
                        SI_Recovery = COL_Recov.checkbox("Recovery?",
                                                        key="SIRecovery"+str(Hole_Number+1)+str(Shot_Num+1))
                    else:
                        SI_Recovery = False
                    New_Shots_df.at[DF_Shot_ID, "Recovery_Shot"] = SI_Recovery
                    # Shot Type
                    if not IS_Putt:
                        All_Shot_Types = ["Straight", "Long", "Short", "High Fade", "Low Fade", "High Draw", "Low Draw", "Slice", "Pull", "Duff", "Sky", "Shank", "Air Ball", "Top", "Hit a Tree", "Putt", "Flop Good", "Flop Long", "Flop Short", "Chip Good", "Chip Long", "Chip Short", "Bunker Good", "Bunker Long", "Bunker Short"]
                        SI_Shot_Type = COL_Outcome.selectbox("Shot Outcome",
                                                        options=All_Shot_Types,
                                                        index=Extras.Return_Index_Of(New_Shots_df.at[DF_Shot_ID, "Shot_Type"] , All_Shot_Types),
                                                        key="SIShotType"+str(Hole_Number+1)+str(Shot_Num+1))
                    else:
                        SI_Shot_Type = "Putt"
                    New_Shots_df.at[DF_Shot_ID, "Shot_Type"] = SI_Shot_Type

                    # In The Hole
                    SI_In_The_Hole = COL_In.checkbox("Did the shot go in?",
                                                        value=New_Shots_df.at[DF_Shot_ID, "In_The_Hole"],
                                                         key="HIInTheHole"+str(Hole_Number+1)+str(Shot_Num+1))
                    New_Shots_df.at[DF_Shot_ID, "In_The_Hole"] = SI_In_The_Hole
                    # Distance After Shot
                    if New_Shots_df.at[DF_Shot_ID, "Shot_Number"] != 1:
                        New_Shots_df.at[list(New_Shots_df.loc[New_Shots_df['Shot_ID'] == (str(Hole_Number)+"-"+str(Shot_Num-1))].index)[0], "Distance_After"] = New_Shots_df.at[DF_Shot_ID, "Distance_2_Hole"]
                    # Calculate After, if in the hole then 0,
                    if SI_In_The_Hole:
                        New_Shots_df.at[DF_Shot_ID, "Distance_After"] = 0
                    # Fall (Only putt)
                    # if Putt:
                    if IS_Putt:
                        All_Putt_Types = ["Left 2 Right", "Right 2 Left", "Both", "Straight", "Not a Putter"]
                        SI_Putt_Fall = COL_Fall.selectbox("Fall of the Putt",
                                                        options=All_Putt_Types,
                                                        index=Extras.Return_Index_Of(New_Shots_df.at[DF_Shot_ID, "Fall_Putt"], All_Putt_Types),
                                                        key="HIPuttFall"+str(Hole_Number+1)+str(Shot_Num+1))
                    else:
                        SI_Putt_Fall = "Not a Putter"
                    New_Shots_df.at[DF_Shot_ID, "Fall_Putt"] = SI_Putt_Fall
                    Shot_Form.form_submit_button("Save Hole")
                    
 
            # HOLE
            HI_Col1, HI_Col2, HI_Col3, HI_Col4 = Hole_Form_Early.columns(4)
            # Hole ID
            HI_Hole_ID = Hole_Number
            New_Holes_df.at[Hole_Number, "Hole_ID"] = HI_Hole_ID
            # Hole Number
            HI_Hole_Num = HI_Col1.number_input("Hole Number", 
                                                min_value=1, 
                                                value=New_Holes_df.at[Hole_Number, "Hole_Number"], 
                                                key="HIHoleNum"+str(Hole_Number+1))
            New_Holes_df.at[Hole_Number, "Hole_Number"] = HI_Hole_Num
            # Played As
            HI_Played_As = Hole_Number+1
            New_Holes_df.at[Hole_Number, "Played_As"] = HI_Played_As
            # Hole Par
            HI_Hole_Par = HI_Col2.number_input("Par", 
                                               min_value=1,
                                               value=New_Holes_df.at[Hole_Number, "Hole_Par"],
                                               key="HIPar"+str(Hole_Number+1))
            New_Holes_df.at[Hole_Number, "Hole_Par"] = HI_Hole_Par
            # Hole Handycap
            HI_Hole_Handycap = HI_Col3.number_input("Handycap", 
                                                    1, 
                                                    18, 
                                                    value=New_Holes_df.at[Hole_Number, "Hole_Handycap"],
                                                    key="HIHandycap"+str(Hole_Number+1))
            New_Holes_df.at[Hole_Number, "Hole_Handycap"] = HI_Hole_Handycap
            # Hole Length
            HI_Hole_Len = HI_Col4.number_input("Hole Length",
                                               min_value=0,
                                               value=New_Holes_df.at[Hole_Number, "Hole_Length"],
                                               key="HILen"+str(Hole_Number+1))            
            New_Holes_df.at[Hole_Number, "Hole_Length"] = HI_Hole_Len
            
            # Update 1st shot

            Shot_ID = str(Hole_Number)+"-0"
            DF_Shot_ID = list(New_Shots_df.loc[New_Shots_df['Shot_ID'] == Shot_ID].index)[0]
            New_Shots_df.at[DF_Shot_ID, "Distance_2_Hole"] = HI_Hole_Len

            
            Hole_Form_Early.form_submit_button("Save Hole Info")
                   
            HI_Col1, HI_Col2, HI_Col3, HI_Col4 = Hole_Form_Late.columns(4)
            # GIR
            HI_GIR = HI_Col1.checkbox("GIR",
                                      value=New_Holes_df.at[Hole_Number, "GIR"],
                                      key="HIGIR"+str(Hole_Number+1),)
            New_Holes_df.at[Hole_Number, "GIR"] = HI_GIR
            # UP&D
            HI_UP_D = HI_Col2.checkbox("UP&D",
                                       value=New_Holes_df.at[Hole_Number, "Up_D"],
                                      key="HIUP&D"+str(Hole_Number+1),)
            New_Holes_df.at[Hole_Number, "Up_D"] = HI_UP_D
            # Fairway
            HI_Fairway = HI_Col3.checkbox("Fairway OTT",
                                          value=New_Holes_df.at[Hole_Number, "Fairway_OTT"], 
                                      key="HIFairway"+str(Hole_Number+1),)
            New_Holes_df.at[Hole_Number, "Fairway_OTT"] = HI_Fairway
            # Bunker UP&D
            HI_Bunker_UP_D = HI_Col4.checkbox("Bunker Up&D",
                                              value=New_Holes_df.at[Hole_Number, "Bunker_Up_D"], 
                                      key="HIBunkerUP&D"+str(Hole_Number+1),)
            New_Holes_df.at[Hole_Number, "Bunker_Up_D"] = HI_Bunker_UP_D
            HI_Col1, HI_Col2, HI_Col3, HI_Col4 = Hole_Form_Late.columns(4)
            # Putts
            HI_Putts = HI_Col1.number_input("Putts", 
                                                min_value=0, 
                                                value=New_Holes_df.at[Hole_Number, "Putts"], 
                                                key="HIPutts"+str(Hole_Number+1))
            New_Holes_df.at[Hole_Number, "Putts"] = HI_Putts
            # Hole Score
            HI_Hole_Score = HI_Col2.number_input("Score", 
                                                 min_value=1, 
                                                 value=New_Holes_df.at[Hole_Number, "Hole_Score"], 
                                                 key="HIScore"+str(Hole_Number+1))
            New_Holes_df.at[Hole_Number, "Hole_Score"] = HI_Hole_Score
            
            Hole_Form_Late.form_submit_button("Save Hole")
            

Calculate_Extras()

Save_File.Write(New_Round_df, New_Holes_df, New_Shots_df)
