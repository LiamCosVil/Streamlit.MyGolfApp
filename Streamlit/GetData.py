import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\CoLi646\Documents\Other\Golf\MySG-Try.accdb;')
cursor = conn.cursor()

## LONG ##

def Return_CoursesInfo_L():
    CoursesInfo = []
    cursor.execute('SELECT * FROM Courses')
    for row in cursor.fetchall():
        CoursesInfo.append(row)
    return CoursesInfo

def Return_PlayersInfo_L():
    PlayersInfo = []
    cursor.execute('SELECT * FROM Player')
    for row in cursor.fetchall():
        PlayersInfo.append(row)
    return PlayersInfo

def Return_RoundsInfo_L():
    RoundsInfo = []
    cursor.execute('SELECT * FROM Rounds')
    for row in cursor.fetchall():
        RoundsInfo.append(row)
    return RoundsInfo

def Return_HolesInfo_L():
    HolesInfo = []
    cursor.execute('SELECT * FROM Holes')
    for row in cursor.fetchall():
        HolesInfo.append(row)
    return HolesInfo
    

## RETURN ALL NAMES ##

def Return_Courses():
    Courses = []
    for course in Courses_Info:
        Courses.append(course[1])
    return Courses

def Return_Players():
    Players = []
    for player in Players_Info:
        Players.append(player[1])
    return Players


## RETURN SINGLE INFO ##

def Return_CourseInfo(Course):
    for course in Courses_Info:
        if course[1] == Course:
            return course

def Return_RoundInfo(RoundID):
    for round in Rounds_Info:
        if round[0] == RoundID:
            return round

def Return_PlayerInfo(Player):
    for player in Players_Info:
        if player[1] == Player:
            return player
        
## RETURN SPECIFIC INFO ##

def Reurn_RoundsScores(SB_Options, Only18, OnlyComps):
    Scores = []
    Scores2Par = []
    for round in Rounds_Info:
        if SB_Check(SB_Options, Round=round):
            if Other_Checks(Round=round, CHKS_OnlyComps=OnlyComps, CHKS_Only18=Only18):
                if round[4] == 18:
                    Scores.append(round[2]*(18/round[4]))
                    Scores2Par.append(round[-1]*(18/round[4]))
    return Scores, Scores2Par

def Return_HolesStats(SB_Options, Only18, OnlyComps):
    GIR = []
    Fairways = []
    Putts = []
    AmountofNonPar3LastRound = 1
    #UPD = []
    #BUPD = []
    for hole in Holes_Info:
        if SB_Check(SB_Options, Hole=hole):
            if Other_Checks(Hole=hole, CHKS_OnlyComps=OnlyComps, CHKS_Only18=Only18):
                GIR.append(hole[7])
                Putts.append(hole[-2])
                if hole[4] != 3:
                    Fairways.append(hole[9])
                    if Return_LastRoundInfo(SB_Options, Only18, OnlyComps)[0] == hole[1]:
                        AmountofNonPar3LastRound += 1
    return GIR, Fairways, Putts, AmountofNonPar3LastRound
                
def Return_LastRoundInfo(SB_Options, Only18, OnlyComps):    
    for round in Rounds_Info[::-1]:
        if SB_Check(SB_Options, Round=round):
            if Other_Checks(round, CHKS_OnlyComps=OnlyComps, CHKS_Only18=Only18):
                    return round


## CHECKS ##

def SB_Check(SB_Options, Round = None, Hole = None):
    if Round != None:
        if Round[1] == Return_PlayerInfo(SB_Options[0])[0]:
            if SB_Options[1] == "Overall":
                return True
            else:
                if Round[6] == Return_CourseInfo(SB_Options[2])[0]:
                    return True
        return False
    elif Hole != None:
        if Return_RoundInfo(Hole[1])[1] == Return_PlayerInfo(SB_Options[0])[0]:
            if SB_Options[1] == "Overall":
                return True
            else:
                if Return_RoundInfo(Hole[1])[6] == Return_CourseInfo(SB_Options[2])[0]:
                    if SB_Options[1] == "Course Specific":
                        return True
                    else:
                        if Hole[2] == SB_Options[3]:
                            return True
        return False
                    
def Other_Checks(Round = None, Hole = None, CHKS_OnlyComps = None, CHKS_Only18 = None):
    if Round != None:
        CHKD_Round = Round
    elif Hole != None:
        CHKD_Round = Return_RoundInfo(Hole[1])
        
    if Round != None:
        if CHKS_OnlyComps and (not CHKD_Round[7]):
            return False
        elif (CHKS_OnlyComps == False) and (CHKD_Round[7]):
            return False
        
        if CHKS_Only18 and (not CHKD_Round[4]):
            return False
        elif (CHKS_Only18 == False) and (CHKD_Round[4]):
            return False
    
    return True        
            

Courses_Info = Return_CoursesInfo_L()
Rounds_Info = Return_RoundsInfo_L()
Holes_Info = Return_HolesInfo_L()
Players_Info = Return_PlayersInfo_L()

print("Course_Info")
print(Courses_Info)
print("Rounds_Info")
print(Rounds_Info)
print("Holes_Info")
print(Holes_Info)
print("Players_Info")
print(Players_Info)
