import unittest
from agile_3rd import parse_indi,parse_fam
import user_stories

class Test_file(unittest.TestCase):
    def test_US03_birth_before_death(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US03_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US03_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families = parse_fam(pass_lines)
        self.assertTrue(user_stories.birth_before_death(individuals_pass))
        individuals_fail = parse_indi(fail_lines)
        families = parse_fam(fail_lines)
        self.assertFalse(user_stories.birth_before_death(individuals_fail))
    def test_US05_marriage_before_death(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US05_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US05_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories.marriage_before_death(families_pass,individuals_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertTrue(user_stories.marriage_before_death(families_fail,individuals_fail))
if __name__ == '__main__':
    unittest.main()