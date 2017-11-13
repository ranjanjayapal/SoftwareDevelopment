import re
from datetime import timedelta, date, datetime
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
# US_38 Ishita Arora's User Story
def list_upcoming_birthdays(individuals):
    return_flag = True
    print "\nList of Upcoming Birthdays:"
    print "*" * 50
    today = date.today()
    today = datetime(today.year, today.month, today.day)
    for individual in individuals:
        if individual.birthdate is not None:
            str_month = str(individual.birthdate).split()[0].split("-")[1]
            # print str_month
            str_day = str(individual.birthdate).split()[0].split("-")[2]
            # print str_day
            bday = "2017-"+str_month+"-"+str_day
            # print datetime.strptime(bday, "%Y-%m-%d")
            # print today
            diff = today - datetime.strptime(bday, "%Y-%m-%d")
            # print diff, individual.uid
            diff = int(str(diff).split()[0])
            if diff<30:
                print individual.uid, " has an upcoming birthday within 30 days"
            else:
                return_flag = False
                print "ERROR: INDIVIDUAL: US38: ",individual.uid," does not have an upcoming birthday within 30 days"
    return return_flag
# US_35 Ishita Arora's User Story
def list_recent_births(individuals):
    return_flag = True
    print "\nList of recent Births:"
    print "*" * 50
    today = date.today()
    today = datetime(today.year, today.month, today.day)
    for individual in individuals:
        if individual.birthdate is not None:
            diff = today - individual.birthdate
            diff = int(str(diff).split()[0])
            if diff < 30:
                print individual.uid, "was born within 30 days"
            else:
                return_flag = False
                print "ERROR: INDIVIDUAL: US35: ",individual.uid," was not born within 30 days"
    return  return_flag
