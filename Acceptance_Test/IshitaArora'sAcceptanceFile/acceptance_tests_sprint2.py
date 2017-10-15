import unittest
from parse import parse_indi,parse_fam
import user_stories_sprint2

class test_user_stories(unittest.TestCase):
    def test_divorce_before_death(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US06_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US06_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_sprint2.US06_divorcebeforedeath(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertTrue(user_stories_sprint2.US06_divorcebeforedeath(individuals_fail,families_fail))

    def test_list_living_married(self):
        pass_lines = [line.rstrip('\n\r') for line in open("US30_PassFile.ged")]
        fail_lines = [line.rstrip('\n\r') for line in open("US30_FailFile.ged")]
        individuals_pass = parse_indi(pass_lines)
        families_pass = parse_fam(pass_lines)
        self.assertTrue(user_stories_sprint2.US30_list_living_married(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(user_stories_sprint2.US30_list_living_married(individuals_fail, families_fail))

if __name__ == '__main__':
    unittest.main()