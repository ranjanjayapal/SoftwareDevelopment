from datetime import date, datetime
from datetime import timedelta

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

# US_01 for Dates before current date (Jitendra Purohit's User Story)
def dates_Before_Current(individuals, families):
   return_flag = True
   today = date.today()
   today = datetime(today.year,today.month,today.day)

   
   for individual in individuals:
       if (individual.birthdate >= today):
          print ("ERROR: INDIVIDUAL: US01: ",individual.uid,"with BIRTH date is after today")
          return_flag = False
          
       if(individual.death is not None):
          if (individual.death >= today):
              print ("ERROR: INDIVIDUAL: US01: ",individual.uid,"with Death date is after today")
              return_flag = False
     
          
   for family in families:
       if(family.marriage >= today):
           print ("ERROR: Family: US01: ",family.uid,"with Marriage date is after today")
           return_flag = False
          
       if(family.divorce is not None):
           if(family.divorce >= today):
               print ("ERROR: Family: US01: ",family.uid,"with Divorce date is after today")
               return_flag = False
   return return_flag

# US_13 for Sibling Spacing (Jitendra Purohit's User Story)
def sibling_Spacing(individuals , families):
    return_flag = True
    family_with_children = [x for x in families if x.children is not []]
    
    for family in family_with_children:
        children_uids = family.children
        if len(children_uids) > 1:
            for child_uid in children_uids:
                child = next((x for x in individuals if x.uid == child_uid), None)
                for temp_uid in children_uids:
                    temp_child = next((x for x in individuals if x.uid == temp_uid), None)
                    if(child.birthdate - temp_child.birthdate < timedelta(weeks=22)):
                        if(child.birthdate - temp_child.birthdate > timedelta(days=2)):
                            print ("ERROR: FAMILY: US13: ", children_uids,"-", "Birth dates are either more than 2 days or less than 8 months")
                            return_flag = False
    return return_flag
