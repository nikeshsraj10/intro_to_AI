import unittest as ut
import bottle_problem as bp

class BottleProblemTestCase(ut.TestCase):

    def test_fill(self):
        self.assertTrue((0, 3) == bp.perform_action((0, 0), "fill 1"))

    def test_dump(self):
        self.assertTrue((0, 0) == bp.perform_action((0, 2), "dump 1"))

    def test_pour(self):
        self.assertTrue((3, 0) == bp.perform_action((0, 3), "pour 1 into 0"))

    def test_perform_action(self):
        test_data = [ # state, action, new_state
            [(0, 0), "fill 0", (5, 0)],
            [(3, 0), "dump 0", (0, 0)],
            [(3, 1), "pour 0 into 1", (1, 3)],
        ]
        for state, action, new_state in test_data:
            self.assertTrue(new_state == bp.perform_action(state, action))

def do_tests():

    test_suite = ut.TestLoader().loadTestsFromTestCase(BottleProblemTestCase)
    results = ut.TextTestRunner(verbosity=2).run(test_suite)
    total, errors, fails = results.testsRun, len(results.errors), len(results.failures)
    return total, errors, fails

if __name__ == "__main__":    
    
    total, errors, fails = do_tests()
    print("Score = %d out of %d (%d errors, %d failed assertions)" % (
        total - (errors + fails), total, errors, fails))

