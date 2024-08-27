import pandas as pd

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

class ExcelAppend():
    def Course(Course_Name, Course_Par, Course_Holes, Course_Location):
        df = pd.DataFrame({
            "Course ID": [DFs.Courses_df().iloc[-1]["Course ID"]+1],
            "Course Name": [Course_Name],
            "Course Par": [Course_Par],
            "Course Holes": [Course_Holes],
            "Course Location": [Course_Location]
        })
        df_existing = pd.read_excel("AddRoundDFs.xlsx")
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        with pd.ExcelWriter("AddRoundDFs.xlsx", mode="a",engine="openpyxl", if_sheet_exists="replace") as writer:
            df_combined.to_excel(writer, sheet_name="Courses", index=4)
