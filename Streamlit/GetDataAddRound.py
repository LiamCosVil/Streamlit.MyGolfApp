import pyodbc
import pandas as pd

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\CoLi646\OneDrive\MyGolf\Streamlit\MySG-Try.accdb;')
cursor = conn.cursor()

class Get_Access():
    def CoursesInfo():
        df = pd.read_sql("SELECT * FROM Courses", conn)
        df = df.sort_values(by=['Course ID'])
        return df

    def PlayersInfo():
        df = pd.read_sql("SELECT * FROM Player", conn)
        df = df.sort_values(by=['Player ID'])
        return df

    def RoundsInfo():
        df = pd.read_sql("SELECT * FROM Rounds", conn)
        df = df.sort_values(by=['Round ID'])
        return df

    def HolesInfo():
        df = pd.read_sql("SELECT * FROM Holes", conn)
        df = df.sort_values(by=['Hole ID'])
        return df
            
    def ShotsInfo():
        df = pd.read_sql("SELECT * FROM Shots", conn)
        df = df.sort_values(by=['Shot ID'])
        return df

    def ClubsInfo():
        df = pd.read_sql("SELECT * FROM Cllubs", conn)
        df = df.sort_values(by=['ID'])
        return df

    def All(All = True):
        df_1 = Get_Access.CoursesInfo()
        df_2 = Get_Access.PlayersInfo()
        df_3 = Get_Access.RoundsInfo()
        df_4 = Get_Access.HolesInfo()
        df_5 = Get_Access.ShotsInfo()
        df_6 = Get_Access.ClubsInfo()
        with pd.ExcelWriter('AddRoundDFs.xlsx') as writer:  
            df_1.to_excel(writer, sheet_name="Courses")
            df_2.to_excel(writer, sheet_name="Players")
            df_3.to_excel(writer, sheet_name="Rounds")
            df_4.to_excel(writer, sheet_name="Holes")
            df_5.to_excel(writer, sheet_name="Shots")
            df_6.to_excel(writer, sheet_name="Cllubs")

        return True
    
class Save_File():
    def Write(New_Round_df, New_Holes_df, New_Shots_df):
        with pd.ExcelWriter('SaveFile.xlsx') as writer:  
            New_Round_df.to_excel(writer, sheet_name="Save_Round")
            New_Holes_df.to_excel(writer, sheet_name="Save_Holes")
            New_Shots_df.to_excel(writer, sheet_name="Save_Shots")

    def Read():
        New_Round_df = pd.read_excel('SaveFile.xlsx', sheet_name="Save_Round")
        New_Round_df.drop(columns=New_Round_df.columns[0], axis=1, inplace=True)
        
        New_Holes_df = pd.read_excel('SaveFile.xlsx', sheet_name="Save_Holes")
        New_Holes_df.drop(columns=New_Holes_df.columns[0], axis=1, inplace=True)
        
        New_Shots_df = pd.read_excel('SaveFile.xlsx', sheet_name="Save_Shots")
        New_Shots_df.drop(columns=New_Shots_df.columns[0], axis=1, inplace=True)
        
        return New_Round_df, New_Holes_df, New_Shots_df

class AccessWrite():
    def Hole(Hole_ID, Round_ID, Hole_Number, Played_As, Hole_Par, Hole_Score, Hole_Handycap, GIR, UP_D, Fairway_OOT, Bunker_UP_D, Putts, Hole_Length):
        #Hole_ID = Holes_df.iloc[-1]["Hole Par"]+1
            
        cursor.execute  ("""INSERT INTO Holes
                        ([Hole ID], [Round ID], [Hole Number], [Played As], [Hole Par], [Hole Score], [Hole Hanycap], [GIR], [UP&D], [Fairway OOT], [Bunker UP&d], [Putts], [Hole Length])
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
                        )
        conn.commit()
        
    def Shot(Shot_ID, Hole_ID, Shot_Number, Distance2Hole, Club_ID, Lie, Desired_Shot, Slope, Recovery_Shot, Shot_Type, Distance_After, In_the_Hole, Fall):
        #Shot_ID = Shots_df.iloc[-1]["Shot ID"]+1
            
        cursor.execute  ("""INSERT INTO Shots
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
                        )
        conn.commit()
        
    def Round(Round_ID, Player_ID, Total_Score, Total_Par, Holes_Played, Tees_Played, Course_Played_ID, Competition_Bool, Weather, Wind, Date, Score2Par):
        #Round_ID = Rounds_df.iloc[-1]["Round ID"]+1
            
        cursor.execute  ("""INSERT INTO Rounds
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
                        )
        conn.commit()
        
    def Course(Course_Name, Course_Par, Course_Holes, Course_Location):    
        Course_ID = DFs.Courses_df().iloc[-1]["Course ID"]+1            
        cursor.execute  ("""INSERT INTO Courses
                        ([Course ID], [Course Name], [Course Par], [Course Holes], [Course Location])
                        VALUES 
                        (
                            """ + str(Course_ID) + """,
                            '""" + str(Course_Name) + """',
                            """ + str(Course_Par) + """,
                            """ + str(Course_Holes) + """,
                            '""" + str(Course_Location) + """'
                        )"""
                        )
        conn.commit()
        
class DFs():
    def Courses_df():
        Courses_df = pd.read_excel('AddRoundDFs.xlsx', sheet_name="Courses")
        Courses_df.drop(columns=Courses_df.columns[0], axis=1, inplace=True)
        return Courses_df
        
    def Players_df():
        Players_df = pd.read_excel('AddRoundDFs.xlsx', sheet_name="Players")
        Players_df.drop(columns=Players_df.columns[0], axis=1, inplace=True)
        return Players_df

    def Rounds_df():
        Rounds_df = pd.read_excel('AddRoundDFs.xlsx', sheet_name="Rounds")
        Rounds_df.drop(columns=Rounds_df.columns[0], axis=1, inplace=True)
        return Rounds_df

    def Holes_df():
        Holes_df = pd.read_excel('AddRoundDFs.xlsx', sheet_name="Holes")
        Holes_df.drop(columns=Holes_df.columns[0], axis=1, inplace=True)
        return Holes_df
            
    def Shots_df():
        Shots_df = pd.read_excel('AddRoundDFs.xlsx', sheet_name="Shots")
        Shots_df.drop(columns=Shots_df.columns[0], axis=1, inplace=True)
        return Shots_df

    def Clubs_df():
        Clubs_df = pd.read_excel('AddRoundDFs.xlsx', sheet_name="Clubs")
        Clubs_df.drop(columns=Clubs_df.columns[0], axis=1, inplace=True)
        return Clubs_df
              
class New_DFs():
    def Round():
        Default = [0, 1, 76, 71, 18, "-", "-", False, "Hot", "None", "Today", 7]
        Columns = list(DFs.Rounds_df().columns)
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]
        New_df = pd.DataFrame(Data)
        return New_df  
    def Holes():
        Default = [0, 0, 1, 1, 4, 4, 1, False, False, False, False, 2, 300]
        Columns = list(DFs.Holes_df().columns)
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]        
        New_df = pd.DataFrame(Data)
        return New_df
    def Shots():
        Default = [0, 0, 1, 100, "None", "None", "Straight", "Flat", False, "Straight", 1, False, "Not a Putter"]
        Columns = list(DFs.Shots_df().columns)
        Data = {}
        for Col, Def in zip(Columns, Default):
            Data[Col] = [Def]        
        New_df = pd.DataFrame(Data)
        return New_df
        
class Players():
    def All_names():
        return list(DFs.Players_df()["Player Name"])

    def ID(Name):
        return Pandas.Locate(DFs.Players_df(), "Player ID", "Player Name", Name)[0]
    
    def Name(ID):
        return Pandas.Locate(DFs.Players_df(), "Player Name", "Player ID", ID)[0]

class Courses():
    def All_names():
        return list(DFs.Courses_df()["Course Name"])

    def ID(Name):
        return Pandas.Locate(DFs.Courses_df(), "Course ID", "Course Name", Name)[0]
    
    def Name(ID):
        return Pandas.Locate(DFs.Courses_df(), "Course Name", "Course ID", ID)[0]


class Pandas():
    def Locate(DataFrame, Return_Column, Search_Column, Search_Value):
        # Find all values(IDs)(Return_column) where (Search_Column) is (Search_Value)
        DF_ = DataFrame.loc[DataFrame[Search_Column] == Search_Value]
        return list(DF_[Return_Column])
 
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


DONE_BOOL = Get_Access.All()
