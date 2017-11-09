from classes import Gedcom_file, Individual, Family
from datetime import datetime, date
import operator
from collections import Counter
from datetime import timedelta
import re
def parse_single_individual(gedlist, index, xref):
    indiv = Individual(xref)
    date_type = None
    for gedline in gedlist[index + 1:]:
        if gedline.level == 0:
            break
        if gedline.tag == "NAME":
            indiv.name = gedline.args
        if gedline.tag == "SEX":
            indiv.sex = gedline.args[0]
        if gedline.tag == "BIRT":
            date_type = "BIRT"
        if gedline.tag == "DEAT":
            date_type = "DEAT"
        if gedline.tag == "FAMC":
            indiv.famc.append(gedline.args[0])
        if gedline.tag == "FAMS":
            indiv.fams.append(gedline.args[0])

        if gedline.tag == "DATE":
            if date_type == "BIRT":
                indiv.birthdate = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None
            elif date_type == "DEAT":
                indiv.death = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None
            else:
                print ("")
    return indiv


def parse_single_family(gedlist, index, xref):
    family = Family(xref)

    date_type = None
    for gedline in gedlist[index + 1:]:
        if gedline.level == 0:
            break
        if gedline.tag == "MARR":
            date_type = "MARR"
        if gedline.tag == "DIV":
            date_type = "DIV"

        if gedline.tag == "HUSB":
            family.husband = gedline.args[0]
        if gedline.tag == "WIFE":
            family.wife = gedline.args[0]
        if gedline.tag == "CHIL":
            family.children.append(gedline.args[0])


        if gedline.tag == "DATE":
            if date_type == "MARR":
                family.marriage = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None

            elif date_type == "DIV":
                family.divorce = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None
            else:
                print ("")

    return family
def create_gedList(lines):
    gedlist = []
    for line in lines:
        current_ged = Gedcom_file(line)
        gedlist.append(current_ged)
    return gedlist

def parse_indi(lines):
    indivi = []
    # for line in lines:
    #     current_ged = Gedcom_file(line)
    #     gedlist.append(current_ged)
    gedli = create_gedList(lines)
    for index, gedline in enumerate(gedli):
        if gedline.tag == 'INDI':
            indivi.append(parse_single_individual(gedli, index,
                                                       gedline.xref))
    return indivi
def parse_fam(lines):
    fami = []
    # for line in lines:
    #     current_ged = Gedcom_file(line)
    #     gedlist.append(current_ged)
    gedli = create_gedList(lines)
    for index, gedline in enumerate(gedli):
        if gedline.tag == 'FAM':
            fami.append(parse_single_family(gedli, index, gedline.xref))

    return fami

def create_tableFor_individuals_families(individuals, families):
    # This is used for project 3 and to display the tables
    print ('INDIVIDUALS'.center(80, ' '))
    print ('{:6s} {:20s} {:5s}  {:10s}   {:7s}  {:10s}   {:10s}' \
        .format('ID', 'Individual Name', 'Gender', 'Birthdate', 'Age', 'Alive', 'Deathdate'))
    print ('-' * 80)
    for indiv in individuals:
        age = 0
        alive = "False"
        ddate = str(indiv.death).split("-")
        bdate = str(indiv.birthdate).split("-")
        if (indiv.death is not None):
            age = int(ddate[0]) - int(bdate[0])
        else:
            alive = "True"
            if bdate is not None:
                try:
                    age = 2017 - int(bdate[0])
                except:
                    age = 0
            else:
                age = 0
        print ('{:6s} {:20s} {:5s}  {:.10s}   {:7s}  {:10s}   {:.10s}' \
            .format(indiv.uid, ' '.join(indiv.name), indiv.sex,
                    str(indiv.birthdate), str(age), alive, str(indiv.death)))

    print ('FAMILIES'.center(80, ' '))
    print ('{:6s} {:20s} {:20s} {:10.10s} {:10.10s} {}' \
        .format('ID', 'Husband', 'Wife', 'M-Date', 'D-Date',
                '# Child'))
    print ('-' * 80)
    for family in families:
        husband_name = "NA"
        wife_name = "NA"
        for indiv in individuals:
            if family.husband == indiv.uid:
                husband_name = indiv.name
            if family.wife == indiv.uid:
                wife_name = indiv.name
        print ('{:6s} {:20s} {:20s} {:10.10s} {:10.10s} {}'\
                .format(family.uid,' '.join(husband_name), ' '
                        .join(wife_name),str(family.marriage),
                        str(family.divorce),len(family.children)))
    print ("\n")



# US_03 for finding birth_before_death (Ranjan Jayapal's User Story)
def birth_before_death(individuals):
    return_flag = True
    for individual in individuals:
        if individual.death != None:
            if individual.death < individual.birthdate:
                print "ERROR: INDIVIDUAL: US03: ", individual.uid, ": Birth Date: ", individual.birthdate, " is after Death Date: ", individual.death
                return_flag = False
    return return_flag
# US_05 for finding marriage_before_death (Ranjan Jayapal's User Story)
def marriage_before_death(families, individuals):
    return_flag = True
    for family in families:
        if family.marriage:
            Husband = None
            Wife = None
            for indiv in individuals:
                if indiv.uid == family.husband:
                    Husband = indiv
                elif indiv.uid == family.wife:
                    Wife = indiv
            if Husband.death is not None and family.marriage > Husband.death:
                return_flag = False
                print "ERROR: FAMILY: US05: ",family.uid,": Marriage Date: ",family.marriage," is after Husband Death: ",Husband.death
            if Wife.death is not None and family.marriage > Wife.death:
                return_flag = False
                print "ERROR: FAMILY: US05: ", family.uid, ": Marriage Date: ", family.marriage, " is after Wife Death: ", Wife.death
    return return_flag

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

    for individual in individuals:

        if len(individual.famc) > 0:
            father = None
            father_id = None
            mother = None
            mother_id = None
            fam = None

            for family in families:
                if family.uid == individual.famc[0]:
                    father_id = family.husband
                    mother_id = family.wife
                    fam = family
                    break

            for each in individuals:
                if each.uid == father_id:
                    father = each
                if each.uid == mother_id:
                    mother = each

            if father.death is not None and \
                father.death < individual.birthdate - timedelta(days = days_In_9_Months):
                print "ERROR: FAMILY: US09: ",family.uid,":child's birthdate is more than 9 months after Death of Father "
                return_flag = False

            if mother.death is not None and mother.death < individual.birthdate:
                print "ERROR: FAMILY: US09: ", family.uid, ":child's birthdate is after mother death date "
                return_flag = False
    return return_flag


# US_16 for Male last Names (Ishita Arora's User Story)
def get_lastName(male):
    match = re.search(r"/(.*)/", (" ".join(male.name)))
    surname = ""
    if match:
        surname = match.group(1)
    else:
        surname = "Not specified"
    return surname
def male_last_names(individuals, families):
    return_flag = True
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
                return_flag = False
    return return_flag
# US_08 Birth before marriage of parents (Isita Arora's User Story)
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

# US_02 Birth before marriage (Ranjan Jayapal's User Story)
def birth_before_marriage(individuals, families):
    return_flag = True
    for family in families:
        husb = family.husband
        wife = family.wife
        for individual in individuals:
            if individual.uid == husb:
                if individual.birthdate >= family.marriage:
                    print "ERROR: FAMILY: US02: ", family.uid, ": Husband's birthdate ", individual.birthdate, " is after marriage date ", family.marriage
                    return_flag = False
            if individual.uid == wife:
                if individual.birthdate >= family.marriage:
                    print "ERROR: FAMILY: US02: ", family.uid, ": Husband's birthdate ", individual.birthdate, " is after marriage date ", family.marriage
                    return_flag = False
    return return_flag

# US_04 Marriage before Divorce (Ranjan Jayapal's User Story)
def marriage_before_divorce(families):
    return_flag = True
    for family in families:
        if family.divorce is not None:
            if family.marriage > family.divorce:
                print "ERROR: FAMILY: US04: ", family.uid, ": Marriage date ", family.marriage, " is after divorce date ", family.divorce
                return_flag = False
    return return_flag


# US_01 for Dates before current date (Jitendra Purohit's User Story)
def dates_Before_Current(individuals, families):
    return_flag = True
    today = date.today()
    today = datetime(today.year, today.month, today.day)

    for individual in individuals:
        if (individual.birthdate is not None and individual.birthdate >= today):
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

#US_06 Divorce before death (Ishita Arora's User Story)
def US06_divorcebeforedeath(individuals, families):
 return_flag = False
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
             return_flag = True
             print "ERROR: FAMILY: US06: ",family.uid,": Divorce Date: ",family.marriage," is after Husband Death: ",Husband.death
         if Wife.death is not None and family.divorce > Wife.death:
             return_flag = True
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

# US_07 less_than_150_years_old (Ranjan Jayapal's User Story)
def less_than_150_years_old(individuals):
    return_flag = True
    today = date.today()
    today = datetime(today.year, today.month, today.day)
    for individual in individuals:
        if individual.birthdate is not None:
            if individual.death is not None:
                diff = individual.death - individual.birthdate
                diff = int(str(diff).split()[0]) // 365
                if (diff) > 150:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US07: ", individual.uid, ": has died after 150 years."
            elif individual.death is None:
                diff =  today - individual.birthdate
                diff = int(str(diff).split()[0]) // 365
                if (diff) > 150:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US07: ", individual.uid, ": is still living after 150 years."
    return return_flag
# US_10 Marriage_after_14 (Ranjan Jayapal's User Story)
def marriage_after_14(individuals, families):
    return_flag = True
    for family in families:
        husb = family.husband
        wife = family.wife
        mdate = family.marriage
        for individual in individuals:
            if individual.uid == husb:
                diff = mdate - individual.birthdate
                diff = int(str(diff).split()[0]) // 365
                if diff < 14:
                    return_flag = False
                    print "ERROR: FAMILY: US10: ", family.uid, ": married when husband was less than 14 years old"
            if individual.uid == wife:
                diff = mdate - individual.birthdate
                diff = int(str(diff).split()[0]) // 365
                if diff < 14:
                    return_flag = False
                    print "ERROR: FAMILY: US10: ", family.uid, ": married when wife was less than 14 years old"
    return return_flag

#US_31 List of Living Marriage (Ishita Arora's User Story)
def US31_ListLivingSingle(individuals):
    return_flag = True
    husband_wife=[]
    people=[]
    print "*" *25
    print "List of Living Single \n"
    for individual in individuals:
        if individual.death is not None:
            if len(individual.fams) == 0:
                print individual.uid, "is living and Single"
            elif len(individual.fams) != 0:
                return_flag = False
                print "ERROR: INDIVIDUAL: US31: ", individual.uid, ": is married"
        else:
            return_flag = False
            print "ERROR: INDIVIDUAL: US31: ", individual.uid, ": is dead"
    return return_flag
#US_42 List of Living Marriage (Ishita Arora's User Story)
def US42_RejectIllegalDates(individuals,families):
    return_flag=True
    for individual in individuals:
        if individual.birthdate is None:
            return_flag=False
            print "ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid",individual.uid,"has an empty birthdate."
            continue
        if not (datetime.strptime(str(individual.birthdate).split()[0], '%Y-%m-%d')):
            print "ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid", individual.uid, \
                "has an invalid birthdate."
        bmonth = int(str(individual.birthdate).split()[0].split("-")[1])
        bday = int(str(individual.birthdate).split()[0].split("-")[2])
        if bmonth == 2 :
            if bday > 28 or bday <1:
                return_flag = False
                print "ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid",individual.uid,"february has 1 - 28 days."
        elif bmonth == 1 or bmonth == 3 or bmonth == 5 or bmonth == 7 or bmonth == 8 or bmonth == 10 or bmonth == 12:
            if bday > 31 or bday < 1:
                return_flag = False
                print "ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid", individual.uid, "thi month has 1 - 31 days."
        elif bmonth == 4 or bmonth == 6 or bmonth == 9 or bmonth == 11:
            if bday > 30 or bday < 1:
                return_flag = False
                print "ERROR: INDIVIDUAL: US42: ", individual.birthdate, ": birthdate is not valid", individual.uid, "thi month has 1 - 30 days."
        if individual.death is not None:
            dmonth = int(str(individual.death).split()[0].split("-")[1])
            dday = int(str(individual.death).split()[0].split("-")[2])
            if dmonth == 2 :
                if dday > 28 or dday <1:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US42: ", individual.death, ": deathdate is not valid",individual.uid,"february has 1 - 28 days."
            elif dmonth == 1 or dmonth == 3 or dmonth == 5 or dmonth == 7 or dmonth == 8 or dmonth == 10 or dmonth == 12:
                if dday > 31 or dday < 1:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US42: ", individual.death, ": deathdate is not valid", individual.uid, "this month has 1 - 31 days."
            elif dmonth == 4 or dmonth == 6 or dmonth == 9 or dmonth == 11:
                if dday > 30 or dday < 1:
                    return_flag = False
                    print "ERROR: INDIVIDUAL: US42: ", individual.death, ": deathdate is not valid", individual.uid, "this month has 1 - 30 days."
    for family in families:
        mmonth = int(str(family.marriage).split()[0].split("-")[1])
        mday = int(str(family.marriage).split()[0].split("-")[2])
        #divmonth = int(str(family.divorce).split()[0].split("-")[1])
        #divday = int(str(family.divorce).split()[0].split("-")[2])
        if family.marriage is not None:
            if mmonth == 2:
                if mday > 28 or mday < 1:
                    return_flag = False
                    print "ERROR: FAMILY: US42: ", family.marriage, ": marriage date is not valid", individual.uid, "february has 1 - 28 days."
            elif mmonth == 1 or mmonth == 3 or mmonth == 5 or mmonth == 7 or mmonth == 8 or mmonth == 10 or mmonth == 12:
                if mday > 31 or mday < 1:
                    return_flag = False
                    print "ERROR: FAMILY: US42: ", family.marriage, ": marriage date is not valid", individual.uid, "this month has 1 - 31 days."
            elif mmonth == 4 or mmonth == 6 or mmonth == 9 or mmonth == 11:
                if mday > 30 or mday < 1:
                    return_flag = False
                    print "ERROR: FAMILY: US42: ", family.marriage, ": birthdate is not valid", individual.uid, "this month has 1 - 30 days."
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
                print "ERROR: INDIVIDUAL: US14: ",family.uid,": More than 5 siblings born at once"
                return_flag = False

    return return_flag

# US_22 Unique ID's (Jitendra Purohit's User Story)
def unique_Ids(individuals, families):
    return_flag = True

    individual_list = []
    family_list = []

    for individual in individuals:
        if individual.uid in individual_list:
            print "ERROR: INDIVIDUAL: US22: ",individual.uid,":Individual ID already exists"
            return_flag = False
        else:
            individual_list.append(individual.uid)
    for family in families:
        if family.uid in family_list:
            print "ERROR: INDIVIDUAL: US22: ",family.uid,":Family ID already exists"
            return_flag = False
        else:
            family_list.append(family.uid)
    return return_flag

# US_36 Ranjan Jayapal's User Story
def list_recent_deaths(individuals):
    return_flag = True
    today = date.today()
    today = datetime(today.year, today.month, today.day)
    print "List of Recent Deaths:"
    print "*"*50
    for individual in individuals:
        if individual.death is not None:
            diff = today - individual.death
            diff = int(str(diff).split()[0])
            if diff < 30:
                print individual.uid ,"died only ",diff," days ago"
            else:
                return_flag = False
                print "ERROR: INDIVIDUAL: US36: ",individual.uid," died more than 30 days ago"
    return return_flag

# US_29 Ranjan Jayapal's User Story
def list_deceased(individuals):
    return_flag = True
    print "\nList of Deceased Individuals:"
    print "*"*50
    for individual in individuals:
        if individual.death is not None:
            print individual.uid," is Deceased"
        else:
            return_flag = False
            print "ERROR: INDIVIDUAL: US29: ",individual.uid," is not deceased"
    return return_flag

individuals = []
families = []
lines = [line.rstrip('\n\r') for line in open("RanjanJayapal_FamilyGEDCOM.ged")]
individuals = parse_indi(lines)
families = parse_fam(lines)
individuals.sort(key=operator.attrgetter('int_id'))
families.sort(key=operator.attrgetter('int_id'))
# required to create the entire table with all the
create_tableFor_individuals_families(individuals,families)


print "*"*25,"Sprint 1", "*"*25,"\n"
# Calling US_03 birth_before_death
US_03 = birth_before_death(individuals)
# Calling US_05 marriage_before_death
US_05 = marriage_before_death(families,individuals)

US_12 = parents_Not_Too_Old(individuals,families)
US_09 = birth_Before_Death_Of_Parents(individuals,families)
US_16 = male_last_names(individuals,families)
US_08 = birth_before_marriage_of_parents(individuals,families)
print "\n"
print "*"*25,"Sprint 2", "*"*25,"\n"
US_02 = birth_before_marriage(individuals,families)
US_04 = marriage_before_divorce(families)

US_06= US06_divorcebeforedeath(individuals,families)
US_30= US30_listlivingmarried(individuals,families)

US_01= dates_Before_Current(individuals,families)
US_13 = sibling_Spacing(individuals,families)
print "\n"
print "*"*25,"Sprint 3", "*"*25,"\n"
US_07 = less_than_150_years_old(individuals)
US_10 = marriage_after_14(individuals, families)
US_31 = US31_ListLivingSingle(individuals)
US_42 = US42_RejectIllegalDates(individuals, families)
US_14 = multiple_Births_Less_5(individuals, families)
US_22 = unique_Ids(individuals, families)
print "\n"
print "*"*25,"Sprint 4", "*"*25,"\n"
US_36 = list_recent_deaths(individuals)
US_29 = list_deceased(individuals)
