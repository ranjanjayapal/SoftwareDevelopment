import unittest
from parse import parse_indi,parse_fam
import user_stories_jp 

class test_Parent_Not_Too_Old(unittest.TestCase):
   
    def test_Parent_Not_Too_Old(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US12_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US12_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_jp.parents_Not_Too_Old(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_jp.parents_Not_Too_Old(individuals_fail, families_fail))
   
    def test_Birth_before_deathof_Parents(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US09_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US09_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_jp.birth_Before_Death_Of_Parents(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_jp.birth_Before_Death_Of_Parents(individuals_fail, families_fail))
    
    def test_Dates_Before_Current(self):
        
        pass_lines = [line.rstrip('\n\r') for line in open("US01_FailFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US01_PassFile.ged")]
       
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_jp.dates_Before_Current(individuals_pass, families_pass))

        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_jp.dates_Before_Current(individuals_fail, families_fail)) 
    
    def test_Sibling_Spacing(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US13_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US13_FailFile.ged")]
        
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_jp.sibling_Spacing(individuals_pass, families_pass))
       
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_jp.sibling_Spacing(individuals_fail, families_fail)) 
        
    def test_Multiple_Births_Less_5(self):
        
        pass_lines = [line.rstrip('\n\r') for line in open("US14_22_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US14_FailFile.ged")]
       
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_jp.multiple_Births_Less_5(individuals_pass, families_pass))

        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_jp.multiple_Births_Less_5(individuals_fail, families_fail)) 
    
    def test_Unique_Ids(self):
        
        pass_lines = [line.rstrip('\n\r') for line in open("US14_22_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US22_FailFile.ged")]
       
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_jp.unique_Ids(individuals_pass, families_pass))

        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_jp.unique_Ids(individuals_fail, families_fail)) 
    
if __name__ == '__main__':
    unittest.main()
