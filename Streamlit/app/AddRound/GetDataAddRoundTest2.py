import pandas as pd
import streamlit as st
from sqlalchemy.sql import text
import random
import ast

conn = st.connection('HomeDB', type='sql')

class DFs():
    def Courses_df():
        df = conn.query("SELECT * FROM Courses")
        print(df)
        return df

    def Players_df():
        df = conn.query("SELECT * FROM Players")
        return df

    def Rounds_df():
        df = conn.query("SELECT * FROM Rounds")
        return df

    def Holes_df():
        df = conn.query("SELECT * FROM Holes")
        return df
            
    def Shots_df():
        df = conn.query("SELECT * FROM Shots")
        return df

    def Clubs_df():
        df = conn.query("SELECT * FROM Clubs")
        return df
 
class Save_File():
    def Write(New_Round_df, New_Holes_df, New_Shots_df):
        with pd.ExcelWriter('Streamlit/data/SaveFile.xlsx') as writer:  
            New_Round_df.to_excel(writer, sheet_name="Save_Round")
            New_Holes_df.to_excel(writer, sheet_name="Save_Holes")
            New_Shots_df.to_excel(writer, sheet_name="Save_Shots")

    def Read():
        New_Round_df = pd.read_excel('Streamlit/data/SaveFile.xlsx', sheet_name="Save_Round")
        New_Round_df.drop(columns=New_Round_df.columns[0], axis=1, inplace=True)
        
        New_Holes_df = pd.read_excel('Streamlit/data/SaveFile.xlsx', sheet_name="Save_Holes")
        New_Holes_df.drop(columns=New_Holes_df.columns[0], axis=1, inplace=True)
        
        New_Shots_df = pd.read_excel('Streamlit/data/SaveFile.xlsx', sheet_name="Save_Shots")
        New_Shots_df.drop(columns=New_Shots_df.columns[0], axis=1, inplace=True)
        
        return New_Round_df, New_Holes_df, New_Shots_df

class AccessWrite():
    def Hole(Hole_ID, Round_ID, Hole_Number, Played_As, Hole_Par, Hole_Score, Hole_Handycap, GIR, UP_D, Fairway_OOT, Bunker_UP_D, Putts, Hole_Length):
        #Hole_ID = Holes_df.iloc[-1]["Hole Par"]+1
        with conn.session as s:
            s.execute  (text("""INSERT INTO Holes
                            ([Hole_ID], [Round_ID], [Hole_Number], [Played_As], [Hole_Par], 
                             [Hole_Score], [Hole_Handycap], [GIR], [UP_D], [Fairway_OTT], 
                             [Bunker_UP_D], [Putts], [Hole_Length])
                            VALUES 
                            (
                                """ + str(Hole_ID) + """,
                                """ + str(Round_ID) + """,
                                """ + str(Hole_Number) + """,
                                """ + str(Played_As) + """,
                                """ + str(Hole_Par) + """,
                                """ + str(Hole_Score) + """,
                                """ + str(Hole_Handycap) + """,
                                """ + str(GIR) + """,
                                """ + str(UP_D) + """,
                                """ + str(Fairway_OOT) + """,
                                """ + str(Bunker_UP_D) + """,
                                """ + str(Putts) + """,
                                """ + str(Hole_Length) + """
                            )"""
                            ))
            s.commit()
        
    def Shot(Shot_ID, Hole_ID, Shot_Number, Distance2Hole, Club_ID, Lie, Desired_Shot, Slope, Recovery_Shot, Shot_Type, Distance_After, In_the_Hole, Fall):
        #Shot_ID = Shots_df.iloc[-1]["Shot ID"]+1
        with conn.session as s:
            s.execute  (text("""INSERT INTO Shots
                            ([Shot_ID], [Hole_ID], [Shot_Number], [Distance_2_Hole], [Club_ID], 
                             [Lie], [Desired_Shot_Type], [Slope], [Recovery_Shot], 
                             [Shot_Type], [Distance_After], [In_The_Hole], 
                             [Fall_Putt])
                            VALUES 
                            (
                                """ + str(Shot_ID) + """,
                                """ + str(Hole_ID) + """,
                                """ + str(Shot_Number) + """,
                                """ + str(Distance2Hole) + """,
                                """ + str(Club_ID) + """,
                                '""" + str(Lie) + """',
                                '""" + str(Desired_Shot) + """',
                                '""" + str(Slope) + """',
                                """ + str(Recovery_Shot) + """,
                                '""" + str(Shot_Type) + """',
                                """ + str(Distance_After) + """,
                                """ + str(In_the_Hole) + """,
                                '""" + str(Fall) + """'
                            )"""
                            ))
            s.commit()
        
    def Round(Round_ID, Player_ID, Total_Score, Total_Par, Holes_Played, Tees_Played, Course_Played_ID, Competition_Bool, Weather, Wind, Date, Score2Par):
        #Round_ID = Rounds_df.iloc[-1]["Round ID"]+1
        with conn.session as s:
            s.execute  (text("""INSERT INTO Rounds
                            ([Round_ID], [Player_ID], [Total_Score], [Total_Par], 
                             [Holes_Played], [Tees_Played], [Course_ID], 
                             [Competition], [Weather], [Wind], [Date], [Score2Par])
                            VALUES 
                            (
                                """ + str(Round_ID) + """,
                                """ + str(Player_ID) + """,
                                """ + str(Total_Score) + """,
                                """ + str(Total_Par) + """,
                                """ + str(Holes_Played) + """,
                                '""" + str(Tees_Played) + """',
                                """ + str(Course_Played_ID) + """,
                                """ + str(Competition_Bool) + """,
                                '""" + str(Weather) + """',
                                '""" + str(Wind) + """',
                                '""" + str(Date) + """',
                                """ + str(Score2Par) + """
                            )"""
                            ))
            s.commit()
        
    def Course(Course_Name, Course_Par, Course_Holes, Course_Location):    
        Course_ID = int(DFs.Courses_df().iloc[-1]["Course ID"])+1 
        with conn.session as s:
            s.execute  (text("""INSERT INTO Courses
                            ([Course_ID], [Course_Name], [Course_Par], [Course_Holes], 
                             [Course_Location])
                            VALUES 
                            (
                                """ + str(Course_ID) + """,
                                '""" + str(Course_Name) + """',
                                """ + str(Course_Par) + """,
                                """ + str(Course_Holes) + """,
                                '""" + str(Course_Location) + """'
                            )"""
                            ))
            s.commit()
      
    def SaveCompleteRound(DF_Round, DF_Holes, DF_Shots):
        # Save Round
        Round_ID = conn.query("SELECT MAX([Round_ID]+0) as [NUM] FROM Rounds;").values[0][0]+1
        Score2Par = DF_Round["Total_Score"][0]-DF_Round["Total_Par"][0]
        AccessWrite.Round(Round_ID, 
                          DF_Round["Player_ID"][0], 
                          DF_Round["Total_Score"][0], 
                          DF_Round["Total_Par"][0], 
                          DF_Round["Holes_Played"][0], 
                          DF_Round["Tees_Played"][0], 
                          Courses.ID(DF_Round["Course_ID"][0]), 
                          DF_Round["Competition"][0], 
                          DF_Round["Weather"][0], 
                          DF_Round["Wind"][0], 
                          DF_Round["Date"][0],
                          Score2Par)
        # Save Holes
        Hole_1_ID = conn.query("SELECT MAX([Hole_ID]+0) as [NUM] FROM Holes;").values[0][0]+1
        for index, row in DF_Holes.iterrows():
            Hole_ID = Hole_1_ID+row["Hole_ID"]
            AccessWrite.Hole(Hole_ID, 
                             Round_ID, 
                             row["Hole_Number"], 
                             row["Played_As"], 
                             row["Hole_Par"], 
                             row["Hole_Score"], 
                             row["Hole_Handycap"], 
                             row["GIR"], 
                             row["UP_D"], 
                             row["Fairway_OTT"], 
                             row["Bunker_UP_D"], 
                             row["Putts"], 
                             row["Hole_Length"])
        # Save Shots
        Shot_1_ID = conn.query("SELECT MAX([Shot_ID]+0) as [NUM] FROM Shots;").values[0][0]+1
        for index, row in DF_Shots.iterrows():
            Shot_ID = Shot_1_ID+index
            Hole_ID = Hole_1_ID+row["Hole_ID"]
            AccessWrite.Shot(Shot_ID, 
                             Hole_ID, 
                             row["Shot_Number"], 
                             row["Distance_2_Hole"], 
                             Clubs.ID(row["Clubs"]), 
                             row["Lie"], 
                             row["Desired_Shot_Type"], 
                             row["Slope"], 
                             row["Recovery_Shot"], 
                             row["Shot_Type"], 
                             row["Distance_After"], 
                             row["In_The_Hole"], 
                             row["Fall_Putt"])
             
class Rounds():
    
    def Return_Random_20(Only18 = False, Course = None, OnlyComp = False):
        if Only18 & (Course == None) & (not OnlyComp):
            return list(conn.query("SELECT * FROM Rounds WHERE [Holes_Played] == 18 ORDER BY RANDOM() LIMIT 20;")["Round_ID"])
        elif (not Only18) & (Course == None) & (not OnlyComp):
            return list(conn.query("SELECT * FROM Rounds ORDER BY RANDOM() LIMIT 20;")["Round_ID"]) 
        
        
    def All_IDs(Only18 = False, Course = None, OnlyComp = False):
        if Only18 & (Course == None) & (not OnlyComp):
            return list(conn.query("SELECT * FROM Rounds WHERE [Holes_Played] == 18")["Round_ID"])
        elif (not Only18) & (Course == None) & (not OnlyComp):
            return list(conn.query("SELECT * FROM Rounds")["Round_ID"]) 
                
    def Date(ID):
        return Pandas.Locate("Date", "Round_ID", "Rounds", ID)[0]
                 
class New_DFs():
    def Round(RoundID = 0):
        Default = [0, 1, 76, 71, 1, "-", "-", False, "-", "-", "-", 0]
        Columns = list(DFs.Rounds_df().columns)
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]
        New_df = pd.DataFrame(Data)
        return New_df  
    def Holes(HoleID = 0, Hole_Number = 1):
        Default = [HoleID, 0, Hole_Number, 1, 4, 4, 1, False, False, False, False, 2, 300, 1]
        Columns = list(DFs.Holes_df().columns)+["Shots_Played"]
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]        
        New_df = pd.DataFrame(Data)
        return New_df
    def Shots(ShotID = "0-0", HoleID = 0, Distance = 100, Club = "Driver", Lie = "Off a Tee", Shot_Num = 1, Putt_Toggle = False):
        Default = [ShotID, HoleID, Shot_Num, Distance, Club, Lie, "Straight", "Flat", False, "Straight", 1, False, "Not a Putter", Putt_Toggle]
        Columns = list(DFs.Shots_df().columns)+["Putt_Toggle"]
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]        
        New_df = pd.DataFrame(Data)
        return New_df
        
class Players():
    def All_names():
        return list(DFs.Players_df()["Player_Name"])

    def All_Indeses():
        return list(DFs.Players_df()["Player_ID"])
    
    def ID(Name):
        return Pandas.Locate("Player_ID", "Player_Name", "Players", Name)[0]
    
    def Name(ID):
        return Pandas.Locate("Player_Name", "Player_ID", "Players", ID)[0]

class Courses():
    def All_names():
        return list(DFs.Courses_df()["Course_Name"])

    def ID(Name):
        return Pandas.Locate("Course_ID", "Course_Name", "Courses", Name)[0]
    
    def Name(ID):
        return Pandas.Locate("Course_Name", "Course_ID", "Courses", ID)[0]

class Clubs():
    def All_names():
        return list(DFs.Clubs_df()["Club_Name"])

    def ID(Name):
        return Pandas.Locate("Club_ID", "Club_Name", "Clubs", Name)[0]
    
    def Name(ID):
        return Pandas.Locate("Club_Name", "Club_ID", "Clubs", ID)[0]


class Pandas():
    
    def Locate(Return_Column, Search_Column, Search_Table, Search_Value):
        Single_df = conn.query('SELECT ['+str(Return_Column)+'] FROM ['+str(Search_Table)+'] WHERE ['+str(Search_Column)+'] = '+str(Search_Value)+';')
        Name = Single_df[str(Return_Column)].tolist()
        return Name
 
class Extras():

    def Return_Index_Of(Value, List):
        for i in range(len(List)):
            if List[i] == Value:
                return i    
    
class LeaderBoard_S():
    
    def Save_Rounds_4_Leadrerboard():
        IDS_20_RAND = Rounds.Return_Random_20(Only18=True)
        
        Players_20 = [
                      "WOODS",
                      "McILROY",
                      "SCHEFFLER",
                      "SPIETH",
                      "RAHM",
                      "KOEPKA",
                      "DeCHAMBEAU",
                      "SCHAUFFELE",
                      "NICKLAUS",
                      "PALMER",
                      "HOGAN",
                      "PLAYER",
                      "BALLESTEROS",
                      "SCOTT",
                      "MICKELSON",
                      "THOMAS",
                      "FOWLER",
                      "OLAZABAL",
                      "ELS",
                      "JOHNSON D."
                      ]
        
        random.shuffle(Players_20)
        
        Data = {
            "Name": Players_20[:len(IDS_20_RAND)],
            "Code_Value": [],
            "Scores": []
        }
        
        for RoundID in IDS_20_RAND:
            # Return all holes from that Round (Only HoleNum Par and Score)
            TheDB = conn.query("SELECT `Hole_Number`, `Hole_Par`, `Hole_Score` FROM Holes WHERE `Round_ID` = "+str(RoundID)+";")
            # Order the holes by Hole Num
            for index, row in TheDB.iterrows():
                Val_Int = int(row['Hole_Par'])
                row['Hole_Par'] = Val_Int
                Val_Int = int(row['Hole_Score'])
                row['Hole_Score'] = Val_Int
                Val_Int = int(row['Hole _Number'])
                row['Hole_Number'] = Val_Int
                
            TheDB = TheDB.sort_values(by=['Hole_Number'])
            # Create a list of the Pregressive Score
            ScoreList = []
            for index, row in TheDB.iterrows():
                ScoreList.append(row["Hole_Score"]-row["Hole_Par"])
            ProgScoreList = [0]
            for Score in ScoreList:
                CurrScore = ProgScoreList[-1]+Score
                ProgScoreList.append(CurrScore)

            # Append Date of Round and pregressive scores list
            Data["Code_Value"].append(random.randint(0,6))
            Data["Scores"].append(ProgScoreList)
        
        
        ScoresDF = pd.DataFrame(data = Data)
        with pd.ExcelWriter('Streamlit/data/leaderboard_S.xlsx') as writer: 
            ScoresDF.to_excel(writer)
        print(ScoresDF)
        
    def RestartExcel():
        Data = {
        }
        ScoresDF = pd.DataFrame(data = Data)
        with pd.ExcelWriter('Streamlit/data/leaderboard_S.xlsx') as writer: 
            ScoresDF.to_excel(writer)

    def Return_DF(Holes_Played, Player_Score):
        
        DF_LB = pd.read_excel('Streamlit/data/leaderboard_S.xlsx')
        DF_LB.drop(columns=DF_LB.columns[0], axis=1, inplace=True)
        
        
        Through = []
        Curr_Score = []
        for index, row in DF_LB.iterrows():
            if row["Code_Value"]+Holes_Played > 17:
                Through.append("F")
                Curr_Score.append(ast.literal_eval(row["Scores"])[18])
            else:
                Through.append(row["Code_Value"]+Holes_Played)
                Curr_Score.append(ast.literal_eval(row["Scores"])[row["Code_Value"]+Holes_Played])
        
        DF_LB["Current_Score"] = Curr_Score
        DF_LB["Through"] = Through
        
        My_DF_LB = {"Name": "Current Round", "Code_Value": 0, "Scores": [], "Current_Score": Player_Score, "Through": Holes_Played}
        
        DF_LB = DF_LB._append(My_DF_LB, ignore_index=True)
        
        DF_LB = DF_LB.sort_values(by=['Current_Score'], ignore_index= True)
        
        
        
        # Generate Position Lists
        
        Positions = []
        for index, row in DF_LB.iterrows():
            if index != 0:
                if row["Current_Score"] == LB_Itt_Score:
                    Positions.append(Positions[-1])
                else:
                    Positions.append(Positions[-1]+1)
                LB_Itt_Score = row["Current_Score"]
            else:
                Positions.append(1)
                LB_Itt_Score = row["Current_Score"]
        
        
        LB_Itt_Pos = 0
        Positions_text = []
        for p in range(len(Positions)):
            if LB_Itt_Pos == Positions[p]:
                Positions_text.append("")
            else:
                try:
                    if Positions[p] == Positions[p+1]:
                        Positions_text.append("T"+str(Positions[p]))
                    else:
                        Positions_text.append(str(Positions[p]))
                except IndexError:
                    Positions_text.append(str(Positions[p]))
                LB_Itt_Pos = Positions[p]
            
                
        DF_LB["Positions"] = Positions_text
        
    
        
        Data = {"Position": list(DF_LB["Positions"]), 
                "Name (Date)": list(DF_LB["Name"]), 
                "Score": list(DF_LB["Current_Score"]), 
                "Through": list(DF_LB["Through"]), 
                }
        DF = pd.DataFrame(data = Data)
        return DF

class Checks_Save():
    def CheckRoundComplete(Round_df, Holes_df, Shots_df):
        RET = True
        Errors = []
        # Round
        if Round_df.at[0, "Tees_Played"] == "-":
            RET = False
            Errors.append("Tees_Played")
        if Round_df.at[0, "Course_ID"] == "-":
            RET = False
            Errors.append("Course_ID")
        if Round_df.at[0, "Weather"] == "-":
            RET = False
            Errors.append("Weather")
        if Round_df.at[0, "Wind"] == "-":
            RET = False
            Errors.append("Wind")

        return RET, Errors
    
    def Return_Round_Info(Round_df, Holes_df, Shots_df):
        Round_Score = 0
        Round_Par = 0
        for index, row in Holes_df.iterrows():
            Hole_Score = int(row["Hole_Score"])
            Round_Score += Hole_Score
            Hole_Par = int(row["Hole_Par"])
            Round_Par += Hole_Par
        Holes_Played = Round_df.at[0, "Holes_Played"]
        return Round_Score, Holes_Played, Round_Par
