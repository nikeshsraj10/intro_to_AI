"""
Bottle states are represented by tuples (l0, l1, l2, l3,...)
lb is the number of liters currently in the bth bottle
Actions are "fill b", "dump b", and "pour b1 into b2" for each b.
Exercises:
1. Finish implementing perform_action where indicated by # TODO
"""

# Max capacity of each bottle
capacities = (5, 3)

def valid_actions(state):
    bottles = range(len(state))
    fills = ["fill %d"%b for b in bottles]
    empty = ["dump %d"%b for b in bottles]
    pours = ["pour %d into %d"%(b1,b2) for b1 in bottles for b2 in bottles]
    return fills + empty + pours

def perform_action(state, action):
    new_state = list(state)
    if action[:4] == "fill":
        b = int(action[5:]) # bottle to fill
        new_state[b] = capacities[b]
    if action[:4] == "dump":
        b = int(action[5:]) # bottle to dump
        # TODO: update new_state here
        new_state[b] = 0
    if action[:4] == "pour":
        b1, b2 = map(int, action[5:].split(" into ")) # pour b1 into b2
        # TODO: update new_state here
        b1Quantity = state[b1]
        b2Quantity = capacities[b2] - state[b2]
        new_state[b1] = new_state[b1] - min(b1Quantity, b2Quantity)
        new_state[b2] = new_state[b1] + min(b1Quantity, b2Quantity)
    return tuple(new_state)

if __name__ == "__main__":

    plan = ["fill 0", "pour 0 into 1"]
    state = (0, 0)
    print(state)
    for action in plan:
        print(action)
        state = perform_action(state, action)
        print(state)

    from graph_search import reachable_states
    states = reachable_states(
        valid_actions,
        perform_action,
        initial_state=(0,0))
    
    for i,s in enumerate(states): print("%d: %s" % (i,s))

