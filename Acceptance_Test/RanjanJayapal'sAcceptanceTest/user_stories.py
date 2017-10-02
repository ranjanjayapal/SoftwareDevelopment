def birth_before_death(individuals):
    return_flag = True
    for individual in individuals:
        if individual.death != None:
            if individual.death < individual.birthdate:
                print "ERROR: FAMILY: US05: ", individual.uid, ": Birth Date: ", individual.birthdate, " is after Death Date: ", individual.death
                return_flag = False
    return return_flag
def marriage_before_death(families, individuals):
    return_flag = False
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
                return_flag = True
                print "ERROR: FAMILY: US05: ",family.uid,": Marriage Date: ",family.marriage," is after Husband Death: ",Husband.death
            if Wife.death is not None and family.marriage > Wife.death:
                return_flag = True
                print "ERROR: FAMILY: US05: ", family.uid, ": Marriage Date: ", family.marriage, " is after Wife Death: ", Wife.death
    return return_flag