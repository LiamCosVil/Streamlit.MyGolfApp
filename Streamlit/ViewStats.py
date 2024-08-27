import streamlit as st
from GetDataStats import *
import pandas as pd  
import numpy as np


#------------------PAGE STRUCTURE------------------------------------------------------------


A = st.container()
st.divider()
B = st.container()
B_1, B_2 = B.columns(2, gap="large")
st.divider()
C = st.container()
C_1 = C.container()
C_2 = C.container()
C_2a, C_2b = C_2.columns([5,3], gap="large")
C_3 = C.container()
C_3b, C_3a = C_3.columns([1, 3], gap="large")
st.divider()
D = st.container()
D_1 = D.container()
D_2 = D.container()
D_2a, D_2b = D_2.columns([3,1], gap="large")
st.divider()
E = st.container()
E_1 = E.container()
E_2 = E.container()
E_2a, E_2b = E_2.columns([3,2], gap="large")


#------------------GLOBAL DEFENITIONS------------------------------------------------------------

SB_Options = {
    "Player" : "Liam",
    "Rounds" : 1,
    "Specificity" : "Overall",
    "Course" : "CGSC(Mirador)",
    "Hole" : 1
}

EX_Options = {
    "Only 18" : True,
    "Only Comps" : False
}

#------------------MAIN------------------------------------------------------------

#-SIDEBAR

with st.sidebar:

    EX_Options["Only 18"] = st.checkbox("Only 18Hole Rounds", True)
    EX_Options["Only Comps"] = st.checkbox("Only Competitions")
    st.divider()
    SB_Options["Player"] = st.selectbox(
        "Who would you like the Stats from?",
        Players.All_Names()
    )

    SB_Options["Specificity"] = st.radio(
        "How specific do you want to be?",
        ("Overall", "Course Specific", "Hole Specific")
    )

    if SB_Options["Specificity"] != "Overall":
        
        SB_Options["Course"] = st.selectbox(
            "What course would you like the Stats from?",
            Courses.All_Names()
        )
                
        if SB_Options["Specificity"] == "Hole Specific":
            
            SB_Options["Hole"] = st.number_input(
                "What hole would you like to see stats for?",
                1,
                Courses.Info(CourseName=SB_Options["Course"])[3],
                1
            )
    
    if len(Rounds.IDs(SB_Options)) > 1:
        SB_Options["Rounds"] = st.slider(
            "How many rounds back should the stats be on?",
            1, 
            len(Rounds.IDs(SB_Options)),
            len(Rounds.IDs(SB_Options))
        )
    else:
        SB_Options["Rounds"] = 1
        

    

#-TOP PAGE STATS

with A:
    
    # DEFINING THE USER OPTIONS THAT THE STATS WILL HAVE
    A_Options = EX_Options
    
    # SEPERATING THE BLOCK INTO THE 5 DIFFERENT COLUMNS
    Score_Col, GIR_Col, Fairways_Col, putts_Col, CheckBoxes_Col = st.columns(5)
    
    # ADDING THE CHECKBOXES OPTIONS
    A_Options["To Par"] = CheckBoxes_Col.checkbox("To Par")


    # CALCULATING THE AVERAGE SCORE
    Av_Score, Last_Score_Diff = Cont_A.Av_Score(SB_Options=SB_Options, EX_Options=A_Options, To_Par=A_Options["To Par"])
    
    # CALCULATING THE AVERAGE GIRs
    Av_GIR, Last_GIR_Diff = Cont_A.Av_GIR(SB_Options=SB_Options, EX_Options=A_Options)
       
    # CALCULATING THE AVERAGE FAIRWAYS HIT
    Av_Fairways, Last_Fairways_Diff = Cont_A.Av_Fairways(SB_Options=SB_Options, EX_Options=A_Options)
    
    # CALCULATING THE AVERAGE PUTTS
    Av_Putts, Last_Putts_Diff = Cont_A.Av_Putts(SB_Options=SB_Options, EX_Options=A_Options)

    # ADDING THE STATS TO THE PAGE    
    Score_Col.metric("Av Score", str(Av_Score), str(Last_Score_Diff), "inverse", "Here we compare your last 18 Hole Score to your average Score", "visible")
    GIR_Col.metric("Av GIR", str(Av_GIR)+"%", str(Last_GIR_Diff)+"%", "normal", "This is Help", "visible")
    Fairways_Col.metric("Av Fairways Hit", str(Av_Fairways)+"%", str(Last_Fairways_Diff)+"%", "normal", "This is Help", "visible")
    putts_Col.metric("Av Putts", str(Av_Putts), str(Last_Putts_Diff), "inverse", "This is Help", "visible")

with B:

    with B_1:

        # DEFINING THE USER OPTIONS THAT THE STATS WILL HAVE
        B_1_Options = EX_Options

        B_1a = st.container()
        # SEPERATING THE TOP BLOCK INTO THE 2 DIFFERENT COLUMNS
        B_1a_Text, B_1a_Checkbox = B_1a.columns([3,2], vertical_alignment="center")
        
        # ADDING THE CHECKBOX OPTIONS
        B_1_Options["To Par"] = B_1a_Checkbox.checkbox("See Par Stats relative to Par")
        B_1a_Text.subheader("Scores By Par", 
                    help="Here we split your average scores by the par of the hole that that score was on, and compare the overall average to whatever you specifiy your options to be.",
                    divider=True
                    )
        
        # RETURN THE AVERAGE SCORE ON PAR 3S, 4S, AND 5S
        if B_1_Options["To Par"]:
            Par3, Par4, Par5 = -3,-4,-5
        else:
            Par3, Par4, Par5 = 0,0,0
            
        Av_Par3_Score, Av_Par3_Score_Options, Av_Par4_Score, Av_Par4_Score_Options, Av_Par5_Score, Av_Par5_Score_Options = Cont_B.Av_ParX_Score(SB_Options=SB_Options, EX_Options=B_1_Options)
        
        data = {
        "Overall": [Av_Par3_Score+Par3, Av_Par4_Score+Par4, Av_Par5_Score+Par5],
        "Specific": [Av_Par3_Score_Options+Par3, Av_Par4_Score_Options+Par4, Av_Par5_Score_Options+Par5]
        }

        df = pd.DataFrame(data, index = ["Par 3s", "Par 4s", "Par 5s"])
        st.bar_chart(df, y_label = "Av. Score", stack=False)
        
    with B_2:
        # DEFINING THE USER OPTIONS THAT THE STATS WILL HAVE
        B_2_Options = EX_Options

        B_2a = st.container()
        # SEPERATING THE TOP BLOCK INTO THE 2 DIFFERENT COLUMNS
        B_2a_Text, B_2a_Checkbox = B_2a.columns([3,2], vertical_alignment="center")
        
        # ADDING THE CHECKBOX OPTIONS
        B_2_Options["Not Include Par 5s"] = B_2a_Checkbox.checkbox("Check to not Include Par 5s")
        B_2a_Text.subheader("Scores By Tee Club", 
                            help="Here we split your average scores by the club used off the tee, and compare the overall average to whatever you specifiy your options to be. Does not include par 3s.",
                            divider=True
                            )
        
        # RETURN THE AVERAGE SCORE ON PAR 3S, 4S, AND 5S        
        Av_D_Score, Av_D_Score_O, Av_W_Score, Av_W_Score_O, Av_I_Score, Av_I_Score_O = Cont_B.AV_Club_OTT_Score(SB_Options=SB_Options, EX_Options=B_2_Options, No_Par5s=B_2_Options["Not Include Par 5s"])
        
        data = {
        "Overall": [Av_D_Score, Av_W_Score, Av_I_Score],
        "Specific": [Av_D_Score_O, Av_W_Score_O, Av_I_Score_O]
        }

        df = pd.DataFrame(data, index = ["Driver", "Wood", "Iron"])
        st.bar_chart(df,y_label = "Av. Score", stack=False, )

with C:
    C_Options = EX_Options

    with C_1:
        C_1.subheader("Proximity to hole, by distance to hole", 
                    help="Here we blablablabal",
                    divider=True
                    )

    with C_2:
        with C_2b:
            
            Clubs_List = Clubs.Return_All_Club_Names()
            
            Clubs_List.remove("Putter")
            
            C_2ba, C_2bb = C_2b.columns(2)
            
            options_all = C_2ba.checkbox("Include all Clubs", True)
            By_GIR = C_2bb.checkbox("Divide by GIR")
                                   
            C_Clubs = C_2b.multiselect(
                                    "What are your favorite colors",
                                    Clubs_List if (not options_all) else ["all"],
                                    default = ["all"] if options_all else [],
                                    disabled  = options_all
                                    )
            if C_Clubs == ["all"]:
                C_Clubs = Clubs_List
                
            
        with C_2a:
            
            # WHAT I WANT : {"DRIVER" : [[100,45],[400,250],[367,45]], "3W" : [[45...]]}
            Club_Shot_Distances_Dicc = Cont_C.Return_Shots_Proximity_Diccionary(SB_Options, C_Options, C_Clubs)
            
            
            Data = []
            for Club in Club_Shot_Distances_Dicc:
                for Dist_Pair in Club_Shot_Distances_Dicc[Club]:
                    Data.append([Dist_Pair[0], Dist_Pair[1], Club])
            
            
            chart_data = pd.DataFrame(
                Data, columns=["col1", "col2", "col3"]
            )
            
            
            
            
            st.scatter_chart(
                chart_data,
                x="col1",
                y="col2",
                color="col3",
            )

    with C_3:
        with C_3b:
            
            
            st.write("")
            
            
        with C_3a:
            
            # WHAT I WANT : {"DRIVER" : [[100,45],[400,250],[367,45]], "3W" : [[45...]]}
            Club_Shot_Distances_Dicc = Cont_C.Return_Shots_Proximity_Diccionary(SB_Options, C_Options, ["Putter"])
            
            
            Data = []
            for Club in Club_Shot_Distances_Dicc:
                for Dist_Pair in Club_Shot_Distances_Dicc[Club]:
                    Data.append([Dist_Pair[0], Dist_Pair[1], Club])
            
            
            chart_data = pd.DataFrame(
                Data, columns=["col1", "col2", "col3"]
            )
            
            
            
            
            st.scatter_chart(
                chart_data,
                x="col1",
                y="col2",
                color="col3",
            )

with D:
    D_Options = EX_Options

    with D_1:
        D_1.subheader("Tee chot distance & probably something else", 
                    help="Here we blablablabal",
                    divider=True
                    )

    with D_2:
        with D_2a:
            pass                
            
        with D_2b:
            D_Options["Clubs"] = D_2b.selectbox(
                "What club do you want the stats for?",
                Clubs.Return_All_Club_Names()
            )
            
            D_Options["Only Fairway"] = D_2b.checkbox(
                "Do you want to Include tee shots that hit the fairway",
                True
            )
   
with E:
    E_Options = EX_Options

    with E_1:
        E_1.subheader("Av. Score by distance to Hole", 
                    help="Here we blablablabal",
                    divider=True
                    )

    with E_2:
        with E_2b:
            Clubs_List = Clubs.Return_All_Club_Names()
            
            Clubs_List.remove("Putter")
                        
            options_all = E_2b.checkbox("Include_all Clubs", True)
                                   
            E_Clubs = E_2b.multiselect(
                                    "What_are your favorite colors",
                                    Clubs_List if (not options_all) else ["all"],
                                    default = ["all"] if options_all else [],
                                    disabled  = options_all
                                    )
            if E_Clubs == ["all"]:
                E_Clubs = Clubs_List
                        
        with E_2a:
            # WHAT I WANT : {"DRIVER" : [[100,45],[400,250],[367,45]], "3W" : [[45...]]}
            Club_Shot_Distances_Dicc = Cont_E.Return_Shots_Score_2_Proximity_Diccionary(SB_Options, E_Options, E_Clubs)
            
            
            Data = []
            for Club in Club_Shot_Distances_Dicc:
                for Dist_Pair in Club_Shot_Distances_Dicc[Club]:
                    Data.append([Dist_Pair[0], Dist_Pair[1], Club])
            
            
            chart_data = pd.DataFrame(
                Data, columns=["col1", "col2", "col3"]
            )
            
            
            
            
            E_2a.scatter_chart(
                chart_data,
                x="col1",
                y="col2",
                color="col3",
            )


