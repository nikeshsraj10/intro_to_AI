"""
Exercises:
Add code to return the size of the frontier at each iteration of the while loop
"""
def reachable_states(valid_actions, perform_action, initial_state):
    frontier = set([initial_state])
    explored = set()
    while len(frontier) > 0:
        state = frontier.pop()
        explored.add(state)
        for action in valid_actions(state):
            new_state = perform_action(state, action)
            if new_state not in explored and new_state not in frontier:
                frontier.add(new_state)
    return explored

