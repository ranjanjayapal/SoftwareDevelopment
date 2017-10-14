import unittest
from parse import parse_indi,parse_fam
import user_stories_rj

class Test_file(unittest.TestCase):
    def test_US03_birth_before_death(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US03_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US03_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families = parse_fam(pass_lines)
        self.assertTrue(user_stories_rj.birth_before_death(individuals_pass))
        individuals_fail = parse_indi(fail_lines)
        families = parse_fam(fail_lines)
        self.assertFalse(user_stories_rj.birth_before_death(individuals_fail))
    def test_US05_marriage_before_death(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US05_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US05_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_rj.marriage_before_death(families_pass, individuals_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_rj.marriage_before_death(families_fail, individuals_fail))
    def test_US02_birth_before_marriage(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US02_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US02_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_rj.birth_before_marriage(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_rj.birth_before_marriage(individuals_fail, families_fail))
    def test_US04_marriage_before_divorce(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US04_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US04_FailFile.ged")]
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_rj.marriage_before_divorce(families_pass))
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_rj.marriage_before_divorce(families_fail))
if __name__ == '__main__':

    print "\n","*"*25,"Unit Tests of Ranjan Jayapal","*"*25,"\n"
    unittest.main()