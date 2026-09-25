import unittest
from auth_triage import triage, EVENTS
class TriageTests(unittest.TestCase):
    def test_baseline(self): self.assertEqual(triage(EVENTS), [('trainee-a',3)])
    def test_empty(self): self.assertEqual(triage([]), [])
    def test_boundary_exclusion(self): self.assertEqual(triage([EVENTS[0],EVENTS[-1]],threshold=1), [])
    def test_success_not_failure(self): self.assertEqual(triage([EVENTS[4]],threshold=1), [])
    def test_accounts_separate(self): self.assertEqual(triage(EVENTS,threshold=1), [('trainee-a',3),('trainee-b',1)])
    def test_threshold(self): self.assertEqual(triage(EVENTS,threshold=4), [])
    def test_input_order(self): self.assertEqual(triage(list(reversed(EVENTS))), [('trainee-a',3)])
    def test_invalid_window(self):
        with self.assertRaises(ValueError): triage([],start='z',end='a')
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError): triage([],threshold=0)
if __name__ == '__main__': unittest.main()
