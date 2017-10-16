import unittest
from parse import parse_indi,parse_fam, birth_Before_Death_Of_Parents
import user_stories_ia

class test_user_stories(unittest.TestCase):
    def test_male_last_names(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US16_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US16_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertFalse(user_stories_ia.male_last_names(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertTrue(user_stories_ia.male_last_names(individuals_fail,families_fail))
    def test_birth_before_marriage_of_parents(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US08_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US08_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_ia.birth_before_marriage_of_parents(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_ia.birth_before_marriage_of_parents(individuals_fail, families_fail))

    def test_divorce_before_death(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US06_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US06_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_ia.US06_divorcebeforedeath(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_ia.US06_divorcebeforedeath(individuals_fail, families_fail))

    def test_list_living_married(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US30_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US30_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_ia.US30_listlivingmarried(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_ia.US30_listlivingmarried(individuals_fail, families_fail))

if __name__ == '__main__':
    unittest.main()