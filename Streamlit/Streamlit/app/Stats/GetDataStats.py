import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\CoLi646\Documents\Other\Golf\MySG-Try.accdb;')
cursor = conn.cursor()

#------------------GLOBAL DEFENITIONS------------------------------------------------------------



## LONG ##

class Get():
    def CoursesInfo():
        CoursesInfo = []
        cursor.execute('SELECT * FROM Courses')
        for row in cursor.fetchall():
            CoursesInfo.append(row)
        return CoursesInfo

    def PlayersInfo():
        PlayersInfo = []
        cursor.execute('SELECT * FROM Player')
        for row in cursor.fetchall():
            PlayersInfo.append(row)
        return PlayersInfo

    def RoundsInfo():
        RoundsInfo = []
        cursor.execute('SELECT * FROM Rounds')
        for row in cursor.fetchall():
            RoundsInfo.append(row)
        return RoundsInfo

    def HolesInfo():
        HolesInfo = []
        cursor.execute('SELECT * FROM Holes')
        for row in cursor.fetchall():
            HolesInfo.append(row)
        return HolesInfo
        
    def ShotsInfo():
        ShotsInfo = []
        cursor.execute('SELECT * FROM Shots')
        for row in cursor.fetchall():
            ShotsInfo.append(row)
        return ShotsInfo

    def ClubsInfo():
        ClubsInfo = []
        cursor.execute('SELECT * FROM Cllubs')
        for row in cursor.fetchall():
            ClubsInfo.append(row)
        return ClubsInfo

    def All(All = True):
        Courses_Info = Get.CoursesInfo()
        #print(Courses_Info)
        Players_Info = Get.PlayersInfo()
        #print(Players_Info)
        Rounds_Info = Get.RoundsInfo()
        #print(Rounds_Info)
        Holes_Info = Get.HolesInfo()
        #print(Holes_Info)
        Shots_Info = Get.ShotsInfo()
        #print(Shots_Info)
        Clubs_Info = Get.ClubsInfo()
        #print(Clubs_Info)
        print("PRITED ALL")
        return True, Courses_Info, Players_Info, Rounds_Info, Holes_Info, Shots_Info, Clubs_Info
    
class Rounds():
    def Info(RoundID, ReverseSearch = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        for Round in Rounds_Info[::Reverse_Index]:
            if Round[0] == RoundID:
                return Round
    
    def IDs(SB_Options = None, EX_Options = None, ReverseSearch = True, RoundsBack = None):
        
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
            
        Round_IDs = []
        for Round in Rounds_Info[::Reverse_Index]:
            if Rounds.SB_Checks(SB_Options, Round):
                if Rounds.EX_Checks(EX_Options, Round):
                    Round_IDs.append(Round[0])
        
        if RoundsBack is not None:
            Round_IDs = Round_IDs[:RoundsBack]
            
        return Round_IDs
    
    def Return_All(SB_Options = None, EX_Options = None, ReverseSearch = True, RoundsBack = None):
        
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
            
        All_Rounds = []
        for Round in Rounds_Info[::Reverse_Index]:
            if Rounds.SB_Checks(SB_Options, Round):
                if Rounds.EX_Checks(EX_Options, Round):
                    All_Rounds.append(Round)
                    
        if RoundsBack is not None:
            All_Rounds = All_Rounds[:RoundsBack]
            
        return All_Rounds
    
    def SB_Checks(SB_Options, Round):
        # CHECK THAT SB_OPTIONS IN NOT NULL (IN CASE IT IS, MEANS THAT WE DO NOT WANT CHECKS, SO RETURN TRUE)
        if SB_Options != None:
            
            # CHECK THAT THE ROUND HAS BEEN PLAYED BY THE PLAYER, ELSE RET FALSE
            if SB_Options["Player"] == Players.Info(Round[1])[1]:

                # IF SPECIFICITY IS OVERALL, RETURN TRUE
                if SB_Options["Specificity"] == "Overall":

                    return True
                
                # IF SPECIFICITY IS NOT OVERALL
                else:

                    # CHECK THAT THE COURSE PLAYED IS THE SAME ONE, IN CASE RET TRUE, ELSE RET FALSE
                    if SB_Options["Course"] == Courses.Info(CourseID=Round[6])[1]:
                        return True
                    
                    else:
                        return False
            else:
                return False
        else:
            return True
    
    def EX_Checks(EX_Options, Round):
        
        # CHECK THAT EX_OPTIONS IN NOT NULL (IN CASE IT IS, MEANS THAT WE DO NOT WANT CHECKS, SO RETURN TRUE)
        if EX_Options != None:
            
            # ITERATE OVER ALL VALUES IN EX_OPTIONS DICCTIONARY
            for Option in EX_Options.keys():
                
                # MATCH KEY WITH ITSELF
                match Option:
                    
                    # IF ONLY18, AND ROUND IS NOT 18, THEN RETURN FALSE
                    case "Only 18":
                        if EX_Options[Option] == True:
                            if Round[4] != 18:
                                return False
                            
                    # IF ONLY COMPS, AND ROUND IS NOT A COMP, THEN RETURN FALSE
                    case "Only Comps":
                        if EX_Options[Option] == True:
                            if not Round[7]:
                                return False
        
        # IF NONE HAE A SUCCESSFULL FALSE RETURN, THEN RETURN TRUE
        return True
        
class Players():
    def Info(PlayerID):
        for Player in Players_Info:
            if Player[0] == PlayerID:
                return Player
    
    def IDs():
        pass
    
    def Return_All():
        pass
    
    def All_Names():
        Names = []
        for player in Players_Info:
            Names.append(player[1])
        return Names

class Courses():
    def Info(CourseID = None, CourseName = None):
        if CourseID != None:
            for course in Courses_Info:
                if course[0] == CourseID:
                    return course
                
        elif CourseName != None:
            for course in Courses_Info:
                if course[1] == CourseName:
                    return course
    
    def IDs():
        pass
    
    def Return_All():
        pass
    
    def All_Names():
        Names = []
        for course in Courses_Info:
            Names.append(course[1])
        return Names
    
class Holes():
    def Info(HoleID, ReverseSearch = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[0] == HoleID:
                return Hole
    
    def IDs(SB_Options = None, EX_Options = None):
        pass
    
    def Return_All(SB_Options = None, EX_Options = None, ReverseSearch = True, RoundsBack = None):
        pass
    
    def Return_All_GIRs_From_Round_Ids(Round_Ids_List, Hole_Num = None, ReverseSearch = True ):
        
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        Holes_GIR = []
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[1] in Round_Ids_List:
                if Hole_Num == None:
                    Holes_GIR.append(Hole[7])
                elif Hole_Num == Hole[2]:
                    Holes_GIR.append(Hole[7])
         
        return Holes_GIR
    
    def Return_All_Scores_From_Round_Ids(Round_Ids_List, Hole_Num = None, ReverseSearch = True):
        
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
                    
        Holes_Scores = []
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[1] in Round_Ids_List:
                if Hole_Num == None:
                    Holes_Scores.append(Hole[5])
                elif Hole_Num == Hole[2]:
                    Holes_Scores.append(Hole[5])
         
        return Holes_Scores
            
    def Return_All_Fairwyas_From_Round_Ids(Round_Ids_List, Include_Par3 = False, Hole_Num = None, ReverseSearch = True):
        
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        Last_Round_Holes = 0
        
        Holes_Fairways = []
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[1] in Round_Ids_List:
                if (Hole[4] != 3) or (Include_Par3):
                    if Hole[1] == Round_Ids_List[0]:
                        Last_Round_Holes += 1
                    if Hole_Num == None:
                        Holes_Fairways.append(Hole[9])
                    elif Hole_Num == Hole[2]:
                        Holes_Fairways.append(Hole[9])
         
        return Holes_Fairways, Last_Round_Holes
    
    def Return_All_Putts_From_Round_Ids(Round_Ids_List, Hole_Num = None, ReverseSearch = True):
        
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
                    
        Holes_Putts = []
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[1] in Round_Ids_List:
                if Hole_Num == None:
                    Holes_Putts.append(Hole[11])
                elif Hole_Num == Hole[2]:
                    Holes_Putts.append(Hole[11])
         
        return Holes_Putts    
    
    def Return_All_Scores_From_Round_Ids_Sperated_By_Par(Round_Ids_List, ReverseSearch = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
                    
        Scores_Par3 = []
        Scores_Par4 = []
        Scores_Par5 = []
        
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[1] in Round_Ids_List:
                if Hole[4] == 3:
                    Scores_Par3.append(Hole[5])
                elif Hole[4] == 4:
                    Scores_Par4.append(Hole[5])
                elif Hole[4] == 5:
                    Scores_Par5.append(Hole[5])
        return Scores_Par3, Scores_Par4, Scores_Par5   
   
    def All_Hole_IDs_From_Round_IDs(Rounds_Ids_List, No_Par5s = False, No_Par3s = False, Specific_Hole_Number = None,  ReverseSearch = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        All_Holes = []
        
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[1] in Rounds_Ids_List:
                if (Hole[4] != 3) or (not No_Par3s):
                    if (Hole[4] != 5) or (not No_Par5s):
                        if Specific_Hole_Number != None:
                            if Hole[2] == Specific_Hole_Number:
                                All_Holes.append(Hole[0])
                        else:
                            All_Holes.append(Hole[0])
        return All_Holes

    def All_Hole_IDs_and_Scores_From_Round_IDs(Rounds_Ids_List, No_Par5s = False, No_Par3s = False, Specific_Hole_Number = None,  ReverseSearch = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        All_Holes = []
        
        for Hole in Holes_Info[::Reverse_Index]:
            if Hole[1] in Rounds_Ids_List:
                if (Hole[4] != 3) or (not No_Par3s):
                    if (Hole[4] != 5) or (not No_Par5s):
                        if Specific_Hole_Number != None:
                            if Hole[2] == Specific_Hole_Number:
                                All_Holes.append([Hole[0], Hole[5]])
                        else:
                            All_Holes.append([Hole[0], Hole[5]])
        return All_Holes


class Clubs():
    def Return_Club_Name(ClubId):
        for Club in Clubs_Info:
            if Club[0] == ClubId:
                return Club[1]

    def Return_All_Club_Names():
        All_Clubs = []
        for Club in Clubs_Info:
            All_Clubs.append(Club[1])
        return All_Clubs
        
        
class Shots():
    
    def Return_All_Shots_With_a_Specific_Shot_Number_From_Hole_IDs(Hole_IDs, Shot_Number, ReverseSearch = True, To_Par = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        D_Scores = []
        W_Scores = []
        I_Scores = []
        
        for Shot in Shots_Info[::Reverse_Index]:
            if Shot[2] == Shot_Number:
                if Shot[1] in Hole_IDs:
                    
                    if Clubs.Return_Club_Name(Shot[4]) == "Driver":
                        
                        D_Scores.append(Holes.Info(Shot[1])[5]-Holes.Info(Shot[1])[4])
                        
                    elif Clubs.Return_Club_Name(Shot[4]) == ("3W" or "5W"):
                        
                        W_Scores.append(Holes.Info(Shot[1])[5]-Holes.Info(Shot[1])[4])
                        
                    elif Clubs.Return_Club_Name(Shot[4]) != "Putter":
                        
                        I_Scores.append(Holes.Info(Shot[1])[5]-Holes.Info(Shot[1])[4])
                        
        return D_Scores, W_Scores, I_Scores
    
    def Return_All_Shots_From_a_List_of_Clubs_From_Their_Hole_IDs_and_Clubs(Hole_IDs, Clubs_Dicc, ReverseSearch = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        for Shot in Shots_Info[::Reverse_Index]:
            if Shot[1] in Hole_IDs:
                if Clubs.Return_Club_Name(Shot[4]) in Clubs_Dicc:
                    Dists = [str(Shot[3]),str(Shot[10])]
                    Dists[0] = Dists[0].replace("Decimal('", "")
                    Dists[0] = float(Dists[0].replace("')", ""))
                    Dists[1] = Dists[1].replace("Decimal('", "")
                    Dists[1] = float(Dists[1].replace("')", ""))
                    Clubs_Dicc[Clubs.Return_Club_Name(Shot[4])].append(Dists)
        return Clubs_Dicc
    
    def Return_All_Shots_Scores_From_a_List_of_Clubs_From_Their_Hole_IDs_S_and_Clubs(Hole_IDs_S, Clubs_Dicc, ReverseSearch = True):
        if not ReverseSearch:
            Reverse_Index = 1
        else:
            Reverse_Index = -1
        
        for Shot in Shots_Info[::Reverse_Index]:
            for Holes_Index in range(len(Hole_IDs_S)):
                if Shot[1] == Hole_IDs_S[Holes_Index][0]:
                    if Clubs.Return_Club_Name(Shot[4]) in Clubs_Dicc:
                        Dists = [str(Shot[3]), Hole_IDs_S[Holes_Index][1]+1-Shot[2]]
                        Dists[0] = Dists[0].replace("Decimal('", "")
                        Dists[0] = float(Dists[0].replace("')", ""))
                        Clubs_Dicc[Clubs.Return_Club_Name(Shot[4])].append(Dists)
                    break
        return Clubs_Dicc
    
    
    
class Cont_A():
    def Av_Score(SB_Options = None, EX_Options = None, To_Par = False):
        
        # DEFINE A LIST WHERE ALL THE SCORE WILL GO 
        All_Scores = []
        
        # CHANGE A IDENX VALUE DEPENDING ON IF TO PAR OR NOT (FOR LATER)
        if To_Par:
            I = -1
        else:
            I = 2
        
        if SB_Options["Specificity"] != "Hole Specific":
            # LOOP OVER ALL ROUNDS THAT PASS THE CHECKS
            for Round in (Rounds.Return_All(SB_Options = SB_Options, EX_Options = EX_Options, ReverseSearch = True, RoundsBack = SB_Options["Rounds"])):
                
                # ADD THE ROUND TO A LIST, NORMALIZING THE SCORE TO A 18 HOLE SCORE
                Normallized_Score = Round[I]*(18/Round[4])
                All_Scores.append(Normallized_Score)
        
        else:
            IDs = (Rounds.IDs(SB_Options=SB_Options, EX_Options=EX_Options, ReverseSearch = True, RoundsBack = SB_Options["Rounds"]))
            All_Scores = Holes.Return_All_Scores_From_Round_Ids(IDs, Hole_Num=SB_Options["Hole"])
            
        # CALCULATE THE AVERAGE OF THE LIST, IF /0, RETURN NA
        try:
            Av_Score = round(sum(All_Scores)/len(All_Scores),1)
            I = len(All_Scores)-1
            Last_Score_Diff = round((sum(All_Scores)/len(All_Scores))-(sum(All_Scores[-I:])/len(All_Scores[-I:])),1)

        except ZeroDivisionError:
            Av_Score = "NA"
            Last_Score_Diff = "NA"
        
        return Av_Score, Last_Score_Diff

    def Av_GIR(SB_Options = None, EX_Options = None, ReverseSearch = True):
        
        IDs = Rounds.IDs(SB_Options = SB_Options, EX_Options = EX_Options, ReverseSearch = ReverseSearch, RoundsBack = SB_Options["Rounds"])
        if SB_Options["Specificity"] != "Hole Specific":
            GIRs = Holes.Return_All_GIRs_From_Round_Ids(IDs)
            try:
                Last_Round_Holes = Rounds.Info(IDs[0])[4]
            except IndexError:
                Last_Round_Holes = 0
            
        else:
            GIRs = Holes.Return_All_GIRs_From_Round_Ids(IDs, Hole_Num=SB_Options["Hole"])
            Last_Round_Holes = 1

        
        
        try:
            Av_GIRs = round((sum(GIRs)/len(GIRs))*100)
            I = len(GIRs)-Last_Round_Holes
            Last_GIRs_Diff = round(((sum(GIRs)/len(GIRs))-(sum(GIRs[-I:])/len(GIRs[-I:])))*100)

        except ZeroDivisionError:
            Av_GIRs = "NA"
            Last_GIRs_Diff = "NA"
            
        return Av_GIRs, Last_GIRs_Diff
        
    def Av_Fairways(SB_Options = None, EX_Options = None, ReverseSearch = True):
        
        IDs = Rounds.IDs(SB_Options = SB_Options, EX_Options = EX_Options, ReverseSearch = ReverseSearch, RoundsBack = SB_Options["Rounds"])
        if SB_Options["Specificity"] != "Hole Specific":
            Fairways, Last_Round_Holes = Holes.Return_All_Fairwyas_From_Round_Ids(IDs)
        else:
            Fairways, Last_Round_Holes = Holes.Return_All_Fairwyas_From_Round_Ids(IDs, Hole_Num=SB_Options["Hole"])
            Last_Round_Holes = 1
        
        try:
            Av_Fairways = round((sum(Fairways)/len(Fairways))*100)
            I = len(Fairways)-Last_Round_Holes
            Last_Fairways_Diff = round(((sum(Fairways)/len(Fairways))-(sum(Fairways[-I:])/len(Fairways[-I:])))*100)
        except ZeroDivisionError:
            Av_Fairways = "NA"
            Last_Fairways_Diff = "NA"
            
        return Av_Fairways, Last_Fairways_Diff
        
    def Av_Putts(SB_Options = None, EX_Options = None, ReverseSearch = True):
        
        IDs = Rounds.IDs(SB_Options = SB_Options, EX_Options = EX_Options, ReverseSearch = ReverseSearch, RoundsBack = SB_Options["Rounds"])
        if SB_Options["Specificity"] != "Hole Specific":
            Putts = Holes.Return_All_Putts_From_Round_Ids(IDs)
            try:
                Last_Round_Holes = Rounds.Info(IDs[0])[4]
            except IndexError:
                Last_Round_Holes = 0
        else:
            Putts = Holes.Return_All_Putts_From_Round_Ids(IDs, Hole_Num=SB_Options["Hole"])
            Last_Round_Holes = 1
        
        try:
            Av_Putts = round((sum(Putts)/len(Putts)),2)
            I = len(Putts)-Last_Round_Holes
            Last_Putts_Diff = round(((sum(Putts)/len(Putts))-(sum(Putts[-I:])/len(Putts[-I:]))),2)
  
        except ZeroDivisionError:
            Av_Putts = "NA"
            Last_Putts_Diff = "NA"
            
        return Av_Putts, Last_Putts_Diff

class Cont_B():
    
    def Av_ParX_Score(SB_Options, EX_Options):
        # RETURN THE LAST X ROUNDS IDS WITH THE CORRECT CRITERIA AND SB CRITERIA
        OP_IDs = Rounds.IDs(SB_Options=SB_Options, EX_Options=EX_Options, ReverseSearch=True, RoundsBack = SB_Options["Rounds"])
        
        # RETURN THE LAST X ROUNDS IDS WITH THE CORRECT CRITERIA
        IDs = Rounds.IDs(EX_Options=EX_Options, ReverseSearch=True)
        
        # FROM THE IDS, RETURN ALL THE HOLES SCORES FOR BOTH OF THE ABOVE AND GROUP THEM IN DIFFERENT LISTS DPENDING ON PAR (6 TOTAL LISTS)
        OP_Scores_3s, OP_Scores_4s, OP_Scores_5s = Holes.Return_All_Scores_From_Round_Ids_Sperated_By_Par(OP_IDs)
        Scores_3s, Scores_4s, Scores_5s = Holes.Return_All_Scores_From_Round_Ids_Sperated_By_Par(IDs)
        
        # AVERAGE THEM ALL
        LIST_THEM = [OP_Scores_3s, OP_Scores_4s, OP_Scores_5s, Scores_3s, Scores_4s, Scores_5s]
        AV_LIST_THEM = []
        for i in LIST_THEM:
            try:
                AV_LIST_THEM.append(round(sum(i)/len(i),2))
            except ZeroDivisionError:
                AV_LIST_THEM.append(0)
                
        
        # RETURN THEM
        return AV_LIST_THEM[3], AV_LIST_THEM[0], AV_LIST_THEM[4], AV_LIST_THEM[1], AV_LIST_THEM[5], AV_LIST_THEM[2]
        
    def AV_Club_OTT_Score(SB_Options, EX_Options, No_Par5s):
        
        # RETURN THE LAST X ROUNDS IDS WITH THE CORRECT CRITERIA AND SB CRITERIA
        R_OP_IDs = Rounds.IDs(SB_Options=SB_Options, EX_Options=EX_Options, ReverseSearch=True, RoundsBack = SB_Options["Rounds"])
        
        # RETURN THE LAST X ROUNDS IDS WITH THE CORRECT CRITERIA
        R_IDs = Rounds.IDs(EX_Options=EX_Options, ReverseSearch=True)
        
        # FOR THE ABOVE ROUNDS, RETURN EVERY HOLE THAT CRITERIA SAYS (NO PAR 3S, AND IF HOLE SPECIFICITY, THEN ONLY THAT HOLE)
        if SB_Options["Specificity"] == "Hole Specific":
            H_OP_IDs = Holes.All_Hole_IDs_From_Round_IDs(R_OP_IDs, No_Par5s=No_Par5s, No_Par3s=True, Specific_Hole_Number =  SB_Options["Hole"])
            H_IDs = Holes.All_Hole_IDs_From_Round_IDs(R_IDs, No_Par5s=No_Par5s, No_Par3s=True)

            
        else:
            H_OP_IDs = Holes.All_Hole_IDs_From_Round_IDs(R_OP_IDs, No_Par5s=No_Par5s, No_Par3s=True)
            H_IDs = Holes.All_Hole_IDs_From_Round_IDs(R_IDs, No_Par5s=No_Par5s, No_Par3s=True)        

        # FOR THE ABOVE HOLES IDS, RETURN EVERY TEE SHOT IN A LIST OF ALL INFO
        D_Scores, W_Scores, I_Scores = Shots.Return_All_Shots_With_a_Specific_Shot_Number_From_Hole_IDs(H_IDs, 1)
        D_Scores_O, W_Scores_O, I_Scores_O = Shots.Return_All_Shots_With_a_Specific_Shot_Number_From_Hole_IDs(H_OP_IDs, 1)
        
        # AVERAGE THEM OUT
        LIST_THEM = [D_Scores, W_Scores, I_Scores, D_Scores_O, W_Scores_O, I_Scores_O]


        AV_LIST_THEM = []
        for i in LIST_THEM:
            try:
                AV_LIST_THEM.append(round(sum(i)/len(i),2))
            except ZeroDivisionError:
                AV_LIST_THEM.append(0)        
        
        # RETURN
        return AV_LIST_THEM[0], AV_LIST_THEM[3], AV_LIST_THEM[1], AV_LIST_THEM[4], AV_LIST_THEM[2], AV_LIST_THEM[5]

class Cont_C():
    def Return_Shots_Proximity_Diccionary(SB_Options, EX_Options, Clubs_2do):
        # RETURN THE LAST X ROUNDS IDS WITH THE CORRECT CRITERIA AND SB CRITERIA
        R_IDs = Rounds.IDs(SB_Options=SB_Options, EX_Options=EX_Options, ReverseSearch=True, RoundsBack = SB_Options["Rounds"])    
        
        # RETURN ALL THE HOLES ID THAT ARE PART OF THESE LAST X ROUNDS
        if SB_Options["Specificity"] == "Hole Specific":
            H_IDs = Holes.All_Hole_IDs_From_Round_IDs(R_IDs, Specific_Hole_Number =  SB_Options["Hole"])
        else:
            H_IDs = Holes.All_Hole_IDs_From_Round_IDs(R_IDs)

        # CREATE A DICC WITH ALL THE CLUBS
        Clubs_Dicc = {}
        for club in Clubs_2do:
            Clubs_Dicc[club] = []
        
        # FOR ALL THE SHOTS IN THE HOLES ABOVE, ADD THEM TO THEIR CORRESPONDING PLACE IN THE DICC
        Clubs_Dicc = Shots.Return_All_Shots_From_a_List_of_Clubs_From_Their_Hole_IDs_and_Clubs(H_IDs, Clubs_Dicc)
        
        
        # RETURN THE DICCIONARY
        return Clubs_Dicc
        
class Cont_D():
    pass       

class Cont_E():
    
    def Return_Shots_Score_2_Proximity_Diccionary(SB_Options, EX_Options, Clubs_2do):
        # RETURN THE LAST X ROUNDS IDS WITH THE CORRECT CRITERIA AND SB CRITERIA
        R_IDs = Rounds.IDs(SB_Options=SB_Options, EX_Options=EX_Options, ReverseSearch=True, RoundsBack = SB_Options["Rounds"])    
        
        # RETURN ALL THE HOLES ID THAT ARE PART OF THESE LAST X ROUNDS
        if SB_Options["Specificity"] == "Hole Specific":
            H_IDs_S = Holes.All_Hole_IDs_and_Scores_From_Round_IDs(R_IDs, Specific_Hole_Number =  SB_Options["Hole"])
        else:
            H_IDs_S = Holes.All_Hole_IDs_and_Scores_From_Round_IDs(R_IDs)

        # CREATE A DICC WITH ALL THE CLUBS
        Clubs_Dicc = {}
        for club in Clubs_2do:
            Clubs_Dicc[club] = []
        
        # FOR ALL THE SHOTS IN THE HOLES ABOVE, ADD THEM TO THEIR CORRESPONDING PLACE IN THE DICC
        Clubs_Dicc = Shots.Return_All_Shots_Scores_From_a_List_of_Clubs_From_Their_Hole_IDs_S_and_Clubs(H_IDs_S, Clubs_Dicc)
        
        
        # RETURN THE DICCIONARY
        return Clubs_Dicc
  

X, Courses_Info, Players_Info, Rounds_Info, Holes_Info, Shots_Info, Clubs_Info = Get.All()