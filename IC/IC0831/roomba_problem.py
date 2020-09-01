"""
Roomba state is (r, c, p) for row, column, and power level
Actions are (dr, dc) for one step up, down, left, or right
For example, (1, 0) moves down one row and stays in the same column
Exercises:
1. Update valid_actions to include left/right motions
2. Update valid_actions and perform_action to model power loss
    a. No actions are valid when power is 0
    b. Every action reduces power by 1
    c. If roomba is at a charging station in a new state, its power is restored to max_power
3. Add code at the end of __main__ to count the reachable states where roomba's power is exactly 2
"""
import numpy as np
import matplotlib.pyplot as pt

# random grid world with wall (0), open (1), charge (2) cells
num_rows, num_cols = 4, 8 # num rows and cols
grid = np.ones((num_rows, num_cols))
walls = np.random.rand(*grid.shape) < .1 
chargers = np.random.rand(*grid.shape) < .1 
grid[walls] = 0
grid[chargers] = 2
max_power = 5

# # deterministic grid world
# num_rows, num_cols = 4, 8
# grid = np.ones((num_rows, num_cols))
# grid[-1,:int(num_cols/2)] = 0 # wall
# grid[2, 2] = 2 # charger
# max_power = 3

def showgrid(state):
    r, c, p = state
    pt.imshow(grid, cmap='gray', vmin=0, vmax=2)
    for col in range(num_cols+1): pt.plot([col-.5, col-.5], [-.5, num_rows-.5], 'k-')
    for row in range(num_rows+1): pt.plot([-.5, num_cols-.5], [row-.5, row-.5], 'k-')
    pt.text(c, r, str(p), fontsize=24)
    pt.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

def valid_actions(state):
    r, c, p = state
    actions = []
    ### TODO: add code to deal with zero power
    if p == 0: return actions
    if r > 0 and grid[r-1,c] > 0: actions.append((-1, 0))
    if r < num_rows-1 and grid[r+1,c] > 0: actions.append((1, 0))
    ### TODO: add code for column (c) boundaries
    if c > 0 and grid[r, c - 1] > 0: actions.append((0, -1))
    if c < num_cols - 1 and grid[r, c + 1] > 0: actions.append((0, 1))
    return actions

def perform_action(state, action):
    r, c, p = state
    dr, dc = action
    ### TODO: add code to deal with drainage and recharging
    p = p-1
    if(grid[r + dr][c + dc] == 2):
        p = max_power
    return (r+dr, c+dc, p)

if __name__ == "__main__":
    
    positions = list(zip(*np.nonzero(grid)))
    r, c = positions[np.random.randint(len(positions))]
    state = (r, c, max_power)

    pt.ion()
    pt.figure()
    showgrid(state)
    pt.show()
    print(state)
    for t in range(6):
        actions = valid_actions(state)
        if len(actions) == 0: break
        action = actions[np.random.randint(len(actions))]
        print(action)
        state = perform_action(state, action)
        print(state)
        pt.cla()
        showgrid(state)
        pt.pause(.5)
        pt.show()
    
    pt.ioff()
    showgrid(state)
    pt.show()

    from graph_search import reachable_states
    states = reachable_states(
        valid_actions,
        perform_action,
        initial_state=state)
    
    print(len(states))

    # ### TODO: count the reachable states with power == 2

