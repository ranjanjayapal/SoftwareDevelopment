from classes import Gedcom_file, Individual, Family
from datetime import datetime
from prettytable import PrettyTable
import operator
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

        # This assumes the following date tag corresponds to prev tag
        if gedline.tag == "DATE":
            if date_type == "BIRT":
                # Store birthdate as datetime object
                indiv.birthdate = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None
            elif date_type == "DEAT":
                # Store death as datetime object
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
                # Store divorce date as datetime
                family.divorce = datetime(
                    int(gedline.args[2]),
                    datetime.strptime(gedline.args[1], '%b').month,
                    int(gedline.args[0]))
                date_type = None
            else:
                print ""

    return family

individuals = []
families = []
gedlist = []
individualTable = PrettyTable()
individualTable.field_names = ["ID", "Name", "Gender", "Birthday", "Death"]
familyTable = PrettyTable()
familyTable.field_names = ["ID", "Husband Name", "Wife Name", "Marriage Date", "Divorse Date"
                           "Children"]

lines = [line.rstrip('\n\r') for line in open("RanjanJayapal_FamilyGEDCOM.ged")]
for line in lines:
    current_ged = Gedcom_file(line)
    gedlist.append(current_ged)

# Parsing of 0 level tags
for index, gedline in enumerate(gedlist):
    if gedline.tag == 'INDI':
        individuals.append(parse_single_individual(gedlist, index,
                                                       gedline.xref))
    if gedline.tag == 'FAM':
        families.append(parse_single_family(gedlist, index, gedline.xref))
# individualTable.add_row(individuals)
# familyTable.add_row(families)
individuals.sort(key=operator.attrgetter('int_id'))
families.sort(key=operator.attrgetter('int_id'))
# print individualTable
# print familyTable
print "\n"
print 'INDIVIDUALS'.center(80, ' ')
print "\n"
print '{:6s} {:20s} {:5s} {:10s}     {:10s}'\
    .format('ID', 'Individual Name', 'Gender', 'Birthdate', 'Deathdate')
print '-' * 80
for indiv in individuals:
    print '{:6s} {:20s} {:5s} {:.10s}     {:.10s}'\
        .format(indiv.uid, ' '.join(indiv.name), indiv.sex,
                str(indiv.birthdate), str(indiv.death))

print "\n\n"
print 'FAMILIES'.center(80, ' ')
print "\n"
print '{:6s} {:20s} {:20s} {:10.10s} {:10.10s} {}'\
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
        .format(family.uid, ' '.join(husband_name), ' '.join(wife_name),
                str(family.marriage), str(family.divorce),
                len(family.children))
print "\n\n"


