import unittest
from parse import parse_indi,parse_fam, birth_Before_Death_Of_Parents
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
        self.assertTrue(birth_Before_Death_Of_Parents(individuals_pass, families_pass))
        individuals_fail = parse_indi(fail_lines)
        families_fail = parse_fam(fail_lines)
        self.assertFalse(birth_Before_Death_Of_Parents(individuals_fail, families_fail))
if __name__ == '__main__':
    unittest.main()