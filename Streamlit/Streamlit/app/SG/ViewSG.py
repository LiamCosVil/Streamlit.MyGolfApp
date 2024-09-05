import streamlit as st
from app.SG.GetDataSG import *
import pandas as pd  
import numpy as np

TotalRounds = 68

st.title("View Shots Gained")

# Using "with" notation
with st.sidebar:
    
    Relative2_radio = st.radio(
        "Specificity of Stats",
        ("Myself", "TourPro")
    )    
    
    SGFromRounds_slider = st.slider(
        "How many rounds back should the stats be on?",
        1, 
        TotalRounds,
        1
    )

    if Relative2_radio == "Myself":

        SGToRounds_slider = st.slider(
            "hhh",
            1, 
            TotalRounds,
            1
        )

        Course_Selectbox = st.selectbox(
            "Is there any course you want the Shots Gained from?",
            ("Overall", "Sant Cugat Golf", "Camiral Golf", "Golf Costa Brava", "El Prat")
        )

    
        if Course_Selectbox != "Overall":
            
            Amount_of_Holes = 18

            if Course_Selectbox == "Sant Cugat Golf":
                Amount_of_Holes = 19
            elif Course_Selectbox == "El Prat":
                Amount_of_Holes = 27
            
            HoleNumber = st.number_input(
                "Which hole would you like to see stats for?",
                1,
                Amount_of_Holes,
                1
            )            

