from classes import Gedcom_file, Individual, Family
from datetime import datetime
import operator
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
                print ""
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
                print ""

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
    print 'INDIVIDUALS'.center(80, ' ')
    print '{:6s} {:20s} {:5s}  {:10s}   {:7s}  {:10s}   {:10s}' \
        .format('ID', 'Individual Name', 'Gender', 'Birthdate', 'Age', 'Alive', 'Deathdate')
    print '-' * 80
    for indiv in individuals:
        age = 0
        alive = "False"
        ddate = str(indiv.death).split("-")
        bdate = str(indiv.birthdate).split("-")
        if (indiv.death is not None):
            age = int(ddate[0]) - int(bdate[0])
        else:
            alive = "True"
            age = 2017 - int(bdate[0])
        print '{:6s} {:20s} {:5s}  {:.10s}   {:7s}  {:10s}   {:.10s}' \
            .format(indiv.uid, ' '.join(indiv.name), indiv.sex,
                    str(indiv.birthdate), str(age), alive, str(indiv.death))

    print 'FAMILIES'.center(80, ' ')
    print '{:6s} {:20s} {:20s} {:10.10s} {:10.10s} {}' \
        .format('ID', 'Husband', 'Wife', 'M-Date', 'D-Date',
                '# Child')
    print '-' * 80
    for family in families:
        husband_name = "NA"
        wife_name = "NA"
        for indiv in individuals:
            if family.husband == indiv.uid:
                husband_name = indiv.name
            if family.wife == indiv.uid:
                wife_name = indiv.name
        print '{:6s} {:20s} {:20s} {:10.10s} {:10.10s} {}'\
                .format(family.uid,' '.join(husband_name), ' '
                        .join(wife_name),str(family.marriage),
                        str(family.divorce),len(family.children))
    print "\n"



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

print "\n"