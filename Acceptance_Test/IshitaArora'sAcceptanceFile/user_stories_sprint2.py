import re
from datetime import timedelta

list_living_marriages = []

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
             print ("ERROR: FAMILY: US06: ",family.uid,": Divorce Date: ",family.marriage," is after Husband Death: ",Husband.death)
         if Wife.death is not None and family.divorce > Wife.death:
             return_flag = True
             print ("ERROR: FAMILY: US06: ", family.uid, ": Divorce Date: ", family.marriage, " is after Wife Death: ", Wife.death)
 return return_flag

def US30_listlivingmarried(individuals,families):
        return_flag=True
        for individual in individuals:
            if len(individual.fam)>0:
                for family in families:
                    if family.uid==individual.famc[0]:
                        if "marriage" in family and family["marriage"] is not None:
                            marriage_date=datetime.strptime(family["marriage"],"%Y-%m-%d %H:%M:%S")
                        if "husband" in family and "wife" in family:
                            result_husband=individual(family["husband"])
                            result_wife=individual(family["wife"])
                            husband_alive=True
                            wife_alive=True
                            for hus in result_husband:
                                if "death" in hus:
                                    husband_alive=False
                            for wif in result_wife:
                                if "death" in wif:
                                    wife_alive=False
                            if wife_alive!=True and husband_alive!=True:
                                list_living_marriages.append(family["FAMID"])
        unique_marr=list(set(list_living_marriages))
        for i in unique_marr:
            for fami in families:
                print ("ERROR: FAMILY: US30: ", family.uid, ": Living marriage")