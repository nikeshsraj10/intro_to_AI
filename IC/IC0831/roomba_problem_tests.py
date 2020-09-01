import numpy as np
import unittest as ut
import roomba_problem as rp

class RoombaProblemTestCase(ut.TestCase):

    def test_upper_left(self):
        if rp.grid[0, 0] == 0: return
        actions = set()
        if rp.grid[0,1] > 0: actions.add((0, 1))
        if rp.grid[1,0] > 0: actions.add((1, 0))
        self.assertTrue(actions == set(rp.valid_actions((0, 0, rp.max_power))))

    def test_middle_left(self):
        if rp.grid[1, 0] == 0: return
        actions = set()
        if rp.grid[0,0] > 0: actions.add((-1, 0))
        if rp.grid[2,0] > 0: actions.add((+1, 0))
        if rp.grid[2,1] > 0: actions.add(( 0, 1))
        self.assertTrue(actions == set(rp.valid_actions((1, 0, rp.max_power))))

    def test_drainage_valid(self):
        self.assertTrue(set() == set(rp.valid_actions((1, 1, 0))))
    
    def test_drainage_loss(self):
        actions = set()
        if rp.grid[0,0] > 0:
            self.assertTrue(
                (0, 0, rp.max_power-1) == rp.perform_action((1, 0, rp.max_power), (-1, 0)))
        if rp.grid[2,0] > 0:
            self.assertTrue(
                (2, 0, rp.max_power-1) == rp.perform_action((1, 0, rp.max_power), (+1, 0)))
        if rp.grid[1,1] > 0:
            self.assertTrue(
                (1, 1, rp.max_power-1) == rp.perform_action((1, 0, rp.max_power), (0, 1)))

    def test_drainage_restore(self):
        chargers = list(zip(*np.nonzero(rp.grid == 2)))
        for r, c in chargers:
            state = (r, c, rp.max_power - 1)
            actions = rp.valid_actions(state)
            if len(actions) == 0: continue
            dr, dc = actions[0]
            next_state = rp.perform_action(state, (dr, dc))
            restore_state = rp.perform_action(next_state, (-dr, -dc))
            self.assertTrue(restore_state[-1] == rp.max_power)

def do_tests():

    test_suite = ut.TestLoader().loadTestsFromTestCase(RoombaProblemTestCase)
    results = ut.TextTestRunner(verbosity=2).run(test_suite)
    total, errors, fails = results.testsRun, len(results.errors), len(results.failures)
    return total, errors, fails

if __name__ == "__main__":    
    
    total, errors, fails = do_tests()
    print("Score = %d out of %d (%d errors, %d failed assertions)" % (
        total - (errors + fails), total, errors, fails))


