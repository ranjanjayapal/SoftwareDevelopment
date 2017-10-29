import re
from datetime import timedelta
from datetime import datetime

def get_lastName(male):
    match = re.search(r"/(.*)/", (" ".join(male.name)))
    surname = ""
    if match:
        surname = match.group(1)
    else:
        surname = "Not specified"
    return surname
def male_last_names(individuals, families):
    return_flag = False
    for family in families:
        males = []
        for individual in individuals:
            if individual.sex is "M" and (
                family.uid in individual.famc or
                family.uid in individual.fams):
                males.append(individual)
        for male in males[1:]:
            # match = re.search(r"/(.*)/", (" ".join(male.name)))
            # surname = ""
            # if match:
            #     surname = match.group(1)
            # else:
            #     surname = "Not specified"
            if get_lastName(male) != get_lastName(males[0]):
                print "ERROR: FAMILY: US16: ", family.uid, ": do not some males with the last name of ",get_lastName(males[0])
                return_flag = True
    return return_flag
def birth_before_marriage_of_parents(individuals, families):
    days_In_9_Months = 266
    return_flag = True
    for individual in individuals:
        if len(individual.famc) > 0:
            for family in families:
                if family.uid == individual.famc[0]:
                    if family.marriage:
                        if family.marriage > individual.birthdate:
                            print "ERROR: FAMILY: US08: ", family.uid, ": child's birthdate ",individual.birthdate," is before parents marriage date ",family.marriage
                            return_flag = False
                    if family.marriage and family.divorce:
                        if family.divorce < individual.birthdate - timedelta(days=days_In_9_Months):
                            print "ERROR: FAMILY: US08: ", family.uid, ": child's birthdate ", individual.birthdate, " is more that 9 months after parents divorce date ", family.divorce
                            return_flag = False
    return return_flag

#US_06 Divorce before death (Ishita Arora's User Story)
def US06_divorcebeforedeath(individuals, families):
 return_flag = True
 for family in families:
     if family.divorce:
         Husband = None
         Wife = None
         for individual in individuals:
             if individual.uid == family.husband:
                 Husband = individual
             elif individual.uid == family.wife:
                 Wife = individual
         if Husband.death is not None and family.divorce > Husband.death:
             return_flag = False
             print "ERROR: FAMILY: US06: ",family.uid,": Divorce Date: ",family.marriage," is after Husband Death: ",Husband.death
         if Wife.death is not None and family.divorce > Wife.death:
             return_flag = False
             print "ERROR: FAMILY: US06: ", family.uid, ": Divorce Date: ", family.marriage, " is after Wife Death: ", Wife.death
 return return_flag

#US_30 List of Living Marriage (Ishita Arora's User Story)
def US30_listlivingmarried(individuals,families):
        return_flag=True
        for family in families:
            if family.divorce is None and family.marriage is not None:
                husb = family.husband
                wife = family.wife
                for individual in individuals:
                    if individual.uid == husb:
                        if individual.death is not None:
                            return_flag = False
                            print "ERROR: FAMILY: US30: ", family.uid, ": has a dead husband", individual.death, "Hence living married condition failed"
                    if individual.uid == wife:
                        if individual.death is not None:
                            return_flag = False
                            print "ERROR: FAMILY: US30: ", family.uid, ": has a dead wife", individual.death, "Hence living married condition failed"
            elif family.divorce is not None:
                return_flag = False
                print "ERROR: FAMILY: US30: ", family.uid, ": has a divorse date", family.divorce," and are not married anymore. Hence living married condition failed"
        return  return_flag

def US31_ListLivingSingle(individuals):
    return_flag = True
    husband_wife=[]
    people=[]
    print ("*" *25)
    print ("List of Living Single \n")
    for individual in individuals:
        if individual.death is not None:
            if len(individual.fams) == 0:
                print (individual.uid, "is living and Single")
            elif len(individual.fams) != 0:
                return_flag = False
                print ("ERROR: INDIVIDUAL: US31: ", individual.uid, ": is married")
        else:
            return_flag = False
            print ("ERROR: INDIVIDUAL: US31: ", individual.uid, ": is dead")
    return return_flag



def US42_RejectIllegalDates(individuals,families):
    return_flag=True
    for individual in individuals:
        if individual.birthdate is None:
            return_flag=False
            print ("ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid",individual.uid,"has an empty birthdate.")
        if not (datetime.strptime(str(individual.birthdate).split()[0], '%Y-%m-%d')):
            print ("ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid", individual.uid, \
                "has an invalid birthdate.")
        bmonth = int(str(individual.birthdate).split()[0].split("-")[1])
        bday = int(str(individual.birthdate).split()[0].split("-")[2])
        if bmonth == 2 :
            if bday > 28 or bday <1:
                return_flag = False
                print ("ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid",individual.uid,"february has 1 - 28 days.")
        elif bmonth == 1 or bmonth == 3 or bmonth == 5 or bmonth == 7 or bmonth == 8 or bmonth == 10 or bmonth == 12:
            if bday > 31 or bday < 1:
                return_flag = False
                print ("ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid", individual.uid, "thi month has 1 - 31 days.")
        elif bmonth == 4 or bmonth == 6 or bmonth == 9 or bmonth == 11:
            if bday > 30 or bday < 1:
                return_flag = False
                print ("ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid", individual.uid, "thi month has 1 - 30 days.")
        if individual.death is not None:
            dmonth = int(str(individual.death).split()[0].split("-")[1])
            dday = int(str(individual.death).split()[0].split("-")[2])
            if dmonth == 2 :
                if dday > 28 or dday <1:
                    return_flag = False
                    print ("ERROR: INDIVIDUAL: US42: ", individual.death, ": deathdate is not valid",individual.uid,"february has 1 - 28 days.")
            elif dmonth == 1 or dmonth == 3 or dmonth == 5 or dmonth == 7 or dmonth == 8 or dmonth == 10 or dmonth == 12:
                if dday > 31 or dday < 1:
                    return_flag = False
                    print ("ERROR: INDIVIDUAL: US42: ", individual.death, ": deathdate is not valid", individual.uid, "this month has 1 - 31 days.")
            elif dmonth == 4 or dmonth == 6 or dmonth == 9 or dmonth == 11:
                if dday > 30 or dday < 1:
                    return_flag = False
                    print ("ERROR: INDIVIDUAL: US42: ", individual.death, ": deathdate is not valid", individual.uid, "this month has 1 - 30 days.")
    for family in families:
        mmonth = int(str(family.marriage).split()[0].split("-")[1])
        mday = int(str(family.marriage).split()[0].split("-")[2])
        #divmonth = int(str(family.divorce).split()[0].split("-")[1])
        #divday = int(str(family.divorce).split()[0].split("-")[2])
        if family.marriage is not None:
            if mmonth == 2:
                if mday > 28 or mday < 1:
                    return_flag = False
                    print ("ERROR: FAMILY: US42: ", family.marriage, ": marriage date is not valid", individual.uid, "february has 1 - 28 days.")
            elif mmonth == 1 or mmonth == 3 or mmonth == 5 or mmonth == 7 or mmonth == 8 or mmonth == 10 or mmonth == 12:
                if mday > 31 or mday < 1:
                    return_flag = False
                    print ("ERROR: FAMILY: US42: ", family.marriage, ": marriage date is not valid", individual.uid, "this month has 1 - 31 days.")
            elif mmonth == 4 or mmonth == 6 or mmonth == 9 or mmonth == 11:
                if mday > 30 or mday < 1:
                    return_flag = False
                    print ("ERROR: FAMILY: US42: ", family.marriage, ": birthdate is not valid", individual.uid, "this month has 1 - 30 days.")
    return return_flag