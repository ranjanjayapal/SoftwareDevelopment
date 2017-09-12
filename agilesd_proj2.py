key_words = ['INDI','NAME','SEX','BIRT','DEAT','FAMC','FAMS','FAM','MARR','HUSB','WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE']
text_file = open('RanjanJayapal_FamilyGEDCOM.ged', 'r')
for line in text_file:
    print "-->",line.strip()
    words = line.split()
    if len(words) > 2:
        if words[2] == 'INDI' or words[2] == 'FAM':
            print "<--", words[0], "|", words[2], "|Y|", words[1], "|", ' '.join(words[3:])
            continue
    if words[1].strip() not in key_words:
        if len(words) > 2:
            if words[2] != 'INDI' and words[2] != 'FAM':
                print "<--",words[0],"|", words[1],"|N|",' '.join(words[2:])
        else:
            print "<--",words[0],"|",words[1],"|N|"
    else:
        if (words[1] == 'NAME' and words[0] == '2') or (words[1] == 'DATE' and words[0] == '1'):
            print "<--", words[0], "|", words[1], "|N|", ' '.join(words[2:])
            continue
        elif (words[1] == "FAM" or words[1] == "HEAD" or words[1] == "INDI" or words[1] == "NOTE"  or words[1] == "TRLR") and ( words[0] == "0"):
            print "<--",words[0],"|",words[1],"|Y|",' '.join(words[2:])
        elif (words[1] == "BIRT" or words[1] == "CHIL" or words[1] == "DEAT" or words[1] == "DIV"  or words[1] == "FAMC" or words[1] == "FAMS" or words[1] == "HUSB" or words[1] == "MARR" or words[1] == "NAME" or words[1] == "SEX" or words[1] == "WIFE") and (words[0] == "1"):
            print "<--", words[0], "|", words[1], "|Y|", ' '.join(words[2:])
        else:
            print "<--",words[0],"|",words[1],"|N|",' '.join(words[2:])