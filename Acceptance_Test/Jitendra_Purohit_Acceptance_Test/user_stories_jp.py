from datetime import timedelta, date,datetime
from collections import Counter
# US_12 for Parents not too old (Jitendra Purohit's User Story)
def parents_Not_Too_Old(individuals, families):
    return_flag = True
    days_In_60_Years = 21900
    days_In_80_Years = 29200

    family_with_children = [x for x in families if x.children is not []]

    for family in family_with_children:

        mother = next((x for x in individuals if x.uid == family.wife), None)
        father = next((x for x in individuals if x.uid == family.husband), None)

        children_uids = family.children

        for child_uid in children_uids:
            child = next((x for x in individuals if x.uid == child_uid), None)

            if mother and child:
                if (child.birthdate - mother.birthdate) > timedelta(days_In_60_Years):
                    print "ERROR: FAMILY: US12: ",family.uid,": Mother",mother.uid," is 60 years greater than child ",child.uid
                    return_flag = False

            if father and child:
                if (child.birthdate - father.birthdate) > timedelta(days=days_In_80_Years):
                    print "ERROR: FAMILY: US12: ", family.uid, ": Father", father.uid, " is 80 years greater than child ", child.uid
                    return_flag = False
    return return_flag

# US_09 for Birth Before Death of Parents (Jitendra Purohit's User Story)
def birth_Before_Death_Of_Parents(individuals, families):
    return_flag = True
    days_In_9_Months = 266

    for family in families:
        husb = family.husband
        wife = family.wife
        children = family.children
        husb_dday = None
        wife_dday = None
        for individual in individuals:
            if individual.uid == husb:
                husb_dday = individual.death
            elif individual.uid == wife:
                wife_dday = individual.death
        for individual in individuals:
            if individual.uid in children:
                if husb_dday is not None and (individual.birthdate - husb_dday) < timedelta(days = days_In_9_Months):
                    print "ERROR: FAMILY: US09: ", individual.uid, " was born after death of father"
                    return_flag = False
                elif wife_dday is not None and (individual.birthdate - wife_dday) < timedelta(days = days_In_9_Months):
                    print "ERROR: FAMILY: US09: ", individual.uid, " was born after death of mother"
                    return_flag = False

    return return_flag


# US_01 for Dates before current date (Jitendra Purohit's User Story)
def dates_Before_Current(individuals, families):
    return_flag = True
    today = date.today()
    today = datetime(today.year, today.month, today.day)

    for individual in individuals:
        if (individual.birthdate >= today):
            print "ERROR: INDIVIDUAL: US01: ", individual.uid, "with BIRTH date",individual.birthdate," is after today",today
            return_flag = False

        if (individual.death is not None):
            if (individual.death >= today):
                print "ERROR: INDIVIDUAL: US01: ", individual.uid, "with Death date",individual.death," is after today",today
                return_flag = False

    for family in families:
        if (family.marriage >= today):
            print "ERROR: Family: US01: ", family.uid, "with Marriage date", family.marriage," is after today",today
            return_flag = False

        if (family.divorce is not None):
            if (family.divorce >= today):
                print "ERROR: Family: US01: ", family.uid, "with Divorce date", family.divorce," is after today",today
                return_flag = False
    return return_flag

# US_14 for Multiple Births less than 5 (Jitendra Purohit's User Story)
def multiple_Births_Less_5(individuals,families):
    return_flag = True

    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)
        sib_birthdays = []
        for sibling in siblings:
            sib_birthdays.append(sibling.birthdate)
        result = Counter(sib_birthdays).most_common(1)
        for (a,b) in result:
            if b > 5:
                print ("ERROR: INDIVIDUAL: US14: ",family.uid,": More than 5 siblings born at once")
                return_flag = False

    return return_flag

# US_22 Unique ID's (Jitendra Purohit's User Story)
def unique_Ids(individuals, families):
    return_flag = True

    individual_list = []
    family_list = []

    for individual in individuals:
        if individual.uid in individual_list:
            print ("ERROR: INDIVIDUAL: US22: ",individual.uid,":Individual ID already exists")
            return_flag = False
        else:
            individual_list.append(individual.uid)
    for family in families:
        if family.uid in family_list:
            print ("ERROR: INDIVIDUAL: US22: ",family.uid,":Family ID already exists")
            return_flag = False
        else:
            family_list.append(family.uid)
    return return_flag

# US_13 for Sibling Spacing (Jitendra Purohit's User Story)
def sibling_Spacing(individuals, families):
    return_flag = True
    for family in families:
        sibling_uids = family.children
        siblings = list(x for x in individuals if x.uid in sibling_uids)
        sib_birthdays = sorted(siblings, key=lambda ind: ind.birthdate, reverse=False)
        i = 0
        count = len(sib_birthdays)
        while i < count - 1:
            diff = sib_birthdays[i + 1].birthdate - sib_birthdays[i].birthdate
            if (diff > timedelta(days=2) and diff < timedelta(days=243)):
                print "ERROR: FAMILY: US13: ", sib_birthdays[i].uid, "and", sib_birthdays[i + 1].uid, "Birth dates are either more than 2 days or less than 8 months"
                return_flag = False
            i += 1
    return return_flag
# US_17 No marriage to descendents (Jitendra Purohit's User Story)
def no_Marriage_To_Decendants(individuals, families):
    return_flag = True
    print "\n"
    for family in families:
        husb = family.husband
        wife = family.wife
        decendants = family.children
        for individual in individuals:
            if individual.uid in decendants:
                if husb in individual.fams:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US17: ",husb," was married to a decendent"
                elif wife in individual.fams:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US17: ",wife," was married to a decendent"
    return return_flag

# US_18 Siblings should not marry (Jitendra Purohit's User Story)
def no_Sibling_Marriage(individuals, families):
    return_flag = True
    for family in families:
        children = family.children
        for individual in individuals:
            if individual.uid in children:
                if len(individual.fams)>0 and individual.fams[0] in children:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US18:",individual.uid," siblings are married"
    return return_flag