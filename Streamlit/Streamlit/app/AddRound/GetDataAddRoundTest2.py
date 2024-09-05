import pandas as pd
import streamlit as st
from sqlalchemy.sql import text

conn = st.connection('MYSG', type='sql')

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
        with pd.ExcelWriter('data\SaveFile.xlsx') as writer:  
            New_Round_df.to_excel(writer, sheet_name="Save_Round")
            New_Holes_df.to_excel(writer, sheet_name="Save_Holes")
            New_Shots_df.to_excel(writer, sheet_name="Save_Shots")

    def Read():
        New_Round_df = pd.read_excel('data\SaveFile.xlsx', sheet_name="Save_Round")
        New_Round_df.drop(columns=New_Round_df.columns[0], axis=1, inplace=True)
        
        New_Holes_df = pd.read_excel('data\SaveFile.xlsx', sheet_name="Save_Holes")
        New_Holes_df.drop(columns=New_Holes_df.columns[0], axis=1, inplace=True)
        
        New_Shots_df = pd.read_excel('data\SaveFile.xlsx', sheet_name="Save_Shots")
        New_Shots_df.drop(columns=New_Shots_df.columns[0], axis=1, inplace=True)
        
        return New_Round_df, New_Holes_df, New_Shots_df

class AccessWrite():
    def Hole(Hole_ID, Round_ID, Hole_Number, Played_As, Hole_Par, Hole_Score, Hole_Handycap, GIR, UP_D, Fairway_OOT, Bunker_UP_D, Putts, Hole_Length):
        #Hole_ID = Holes_df.iloc[-1]["Hole Par"]+1
        with conn.session as s:
            s.execute  (text("""INSERT INTO Holes
                            ([Hole ID], [Round ID], [Hole Number], [Played As], [Hole Par], [Hole Score], [Hole Handycap], [GIR], [UP&D], [Fairway OTT], [Bunker UP&D], [Putts], [Hole Length])
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
                            ([Shot ID], [Hole ID], [Shot Number], [Distance2Hole], [Clubs], [Lie], [Desired Shot Type], [Slope], [Recovery Shot?], [Shot Type], [Distance After Shot], [In The Hole?], [Fall (Only Putt)])
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
                            ([Round ID], [Player ID], [Total Score], [Total Par], [Holes Played], [Tees Played], [Course Played], [Competition?], [Weather], [Wind], [Date], [Score2Par])
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
                            ([Course ID], [Course Name], [Course Par], [Course Holes], [Course Location])
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
        pass
                 
class New_DFs():
    def Round(RoundID = 0):
        Default = [0, 1, 76, 71, 1, "-", "-", False, "-", "-", "-", 7]
        Columns = list(DFs.Rounds_df().columns)
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]
        New_df = pd.DataFrame(Data)
        return New_df  
    def Holes(HoleID = 0, Hole_Number = 1):
        Default = [HoleID, 0, Hole_Number, 1, 4, 4, 1, False, False, False, False, 2, 300, 1]
        Columns = list(DFs.Holes_df().columns)+["Shots Played"]
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]        
        New_df = pd.DataFrame(Data)
        return New_df
    def Shots(ShotID = "0-0", HoleID = 0, Distance = 100, Club = "Driver", Lie = "Off a Tee", Shot_Num = 1, Putt_Toggle = False):
        Default = [ShotID, HoleID, Shot_Num, Distance, Club, Lie, "Straight", "Flat", False, "Straight", 1, False, "Not a Putter", Putt_Toggle]
        Columns = list(DFs.Shots_df().columns)+["Putt Toggle"]
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]        
        New_df = pd.DataFrame(Data)
        return New_df
        
class Players():
    def All_names():
        return list(DFs.Players_df()["Player Name"])

    def All_Indeses():
        return list(DFs.Players_df()["Player ID"])
    
    def ID(Name):
        return Pandas.Locate("Player ID", "Player Name", "Players", Name)[0]
    
    def Name(ID):
        return Pandas.Locate("Player Name", "Player ID", "Players", ID)[0]

class Courses():
    def All_names():
        return list(DFs.Courses_df()["Course Name"])

    def ID(Name):
        return Pandas.Locate(DFs.Courses_df(), "Course ID", "Course Name", Name)[0]
    
    def Name(ID):
        return Pandas.Locate(DFs.Courses_df(), "Course Name", "Course ID", ID)[0]

class Clubs():
    def All_names():
        return list(DFs.Clubs_df()["Club Name"])

    def ID(Name):
        return Pandas.Locate(DFs.Clubs_df(), "Club ID", "Club Name", Name)[0]
    
    def Name(ID):
        return Pandas.Locate(DFs.Clubs_df(), "Club Name", "Club ID", ID)[0]


class Pandas():
    
    def Locate(Return_Column, Search_Column, Search_Table, Search_Value):
        Single_df = conn.query('SELECT ['+str(Return_Column)+'] FROM ['+str(Search_Table)+'] WHERE ['+str(Search_Column)+'] = "'+str(Search_Value)+'"')
        Name = Single_df[str(Return_Column)].tolist()
        return Name
 
class Extras():

    def Return_Index_Of(Value, List):
        for i in range(len(List)):
            if List[i] == Value:
                return i    


    
class LeaderBoard_S():
    def Return_DF():
        Data = {"Position": ["1", "2", "T3", "", "", "T6", "", "", "", ""], 
                "Name (Date)": ["21 July 2013", "18 Jan 2020", "19 Feb 2022", "2 Oct 2014", "8 Jul 2014", "12 Mar 2014", "17 Jun 2021", "10 Nov 2019", " 9 Sep 2020", "9 Apr 2018"], 
                "Score": ["-3", "-1", "E", "E", "E", "+1", "+1", "+1", "+1", "+1"], 
                "Through": ["14", "15", "14", "16", "15", "15", "72", "16", "17", "72"]
                }
        DF = pd.DataFrame(data = Data)
        return DF

class Checks_Save():
    def CheckRoundComplete(Round_df, Holes_df, Shots_df):
        RET = True
        Errors = []
        # Round
        if Round_df.at[0, "Tees Played"] == "-":
            RET = False
            Errors.append("Tees Played")
        if Round_df.at[0, "Course Played"] == "-":
            RET = False
            Errors.append("Course Played")
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
            Hole_Score = int(row["Hole Score"])
            Round_Score += Hole_Score
            Hole_Par = int(row["Hole Par"])
            Round_Par += Hole_Par
        Holes_Played = Round_df.at[0, "Holes Played"]
        return Round_Score, Holes_Played, Round_Par