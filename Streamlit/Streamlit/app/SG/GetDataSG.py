import pyodbc
import pandas as pd

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\CoLi646\Documents\Other\Golf\MySG-Try.accdb;')
cursor = conn.cursor()

#------------------GLOBAL DEFENITIONS------------------------------------------------------------

## LONG ##

class Get_Access():
    def CoursesInfo():
        df = pd.read_sql("SELECT * FROM Courses", conn)
        return df

    def PlayersInfo():
        df = pd.read_sql("SELECT * FROM Player", conn)
        return df

    def RoundsInfo():
        df = pd.read_sql("SELECT * FROM Rounds", conn)
        return df

    def HolesInfo():
        df = pd.read_sql("SELECT * FROM Holes", conn)
        return df
            
    def ShotsInfo():
        df = pd.read_sql("SELECT * FROM Shots", conn)
        return df

    def ClubsInfo():
        df = pd.read_sql("SELECT * FROM Cllubs", conn)
        return df

    def All(All = True):
        Courses_df = Get_Access.CoursesInfo()
        #print(Courses_df)
        Players_df = Get_Access.PlayersInfo()
        #print(Players_df)
        Rounds_df = Get_Access.RoundsInfo()
        #print(Rounds_df)
        Holes_df = Get_Access.HolesInfo()
        #print(Holes_df)
        Shots_df = Get_Access.ShotsInfo()
        #print(Shots_df)
        Clubs_df = Get_Access.ClubsInfo()
        #print(Clubs_df)
        print("PRITED ALL")
        return True, Courses_df, Players_df, Rounds_df, Holes_df, Shots_df, Clubs_df
    
class Get_PGA_Baseline():
    def Putting():
        df = pd.read_excel('PGA_Pro_Baseline.xlsx', sheet_name="Putt")
        return df

    def Shots():
        df = pd.read_excel('PGA_Pro_Baseline.xlsx', sheet_name="Shot")
        return df


print(Get_Access.CoursesInfo())

#cursor.execute("""INSERT INTO Courses
#                    ([Course ID], [Course Name], [Course Par], [Course Holes], [Course Location])
#                    VALUES 
#                    (9, 'CGSC(Mirador)', 72, 18, 'Tarragona')"""
#                    )

#conn.commit()

print(Get_Access.CoursesInfo())

#BL_Pro_Putting_df = Get_PGA_Baseline.Putting()
#BL_Pro_Shots_df = Get_PGA_Baseline.Shots()
#DONE_BOOL, Courses_df, Players_df, Rounds_df, Holes_df, Shots_df, Clubs_df = Get_Access.All()

conn.close()

