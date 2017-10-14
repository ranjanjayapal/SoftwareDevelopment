
def birth_before_death(individuals):
    return_flag = True
    for individual in individuals:
        if individual.death != None:
            if individual.death < individual.birthdate:
                print "ERROR: FAMILY: US03: ", individual.uid, ": Birth Date: ", individual.birthdate, " is after Death Date: ", individual.death
                return_flag = False
    return return_flag

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

def marriage_before_divorce(families):
    return_flag = True
    for family in families:
        if family.divorce is not None:
            if family.marriage > family.divorce:
                print "ERROR: FAMILY: US04: ", family.uid, ": Marriage date ", family.marriage, " is after divorce date ", family.divorce
                return_flag = False
    return return_flag
