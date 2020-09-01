"""
2x2x2 rubiks cube
state is a 2x2x2x3 char array
first 3 dimensions are positions on the cube
last dimension is the colors in each of the 3 spatial directions
spatial directions are 0:x, 1:y, 2:z
"""
import numpy as np
import matplotlib.pyplot as pt
from matplotlib.patches import Polygon

R, G, B, W, Y, O = range(6)
colors = {
    R: (1.,0.,0.), # red
    G: (0.,1.,0.), # green
    B: (0.,0.,1.), # blue
    W: (1.,1.,1.), # white
    Y: (1.,1.,0.), # yellow
    O: (1.,.64,0.), # orange
}

def unhash(state):
    return np.frombuffer(state, dtype=np.byte).reshape((2,2,2,3))
def rehash(state):
    return state.tobytes()

def showcube(state):
    state = unhash(state)
    ax = pt.gca()
    angles = -np.arange(3) * np.pi * 2 / 3
    axes = np.array([np.cos(angles), np.sin(angles)])
    for d in range(3):
        for a, b in [(0,0),(0,1),(1,0),(1,1)]:
            xy = [a*axes[:,d] + b*axes[:,(d+1) % 3],
                (a+1)*axes[:,d] + b*axes[:,(d+1) % 3],
                (a+1)*axes[:,d] + (b+1)*axes[:,(d+1) % 3],
                a*axes[:,d] + (b+1)*axes[:,(d+1) % 3]]
            c = colors[state[tuple(np.roll((a,b,0),d))+((d+2) % 3,)]]
            ax.add_patch(Polygon(xy, facecolor=c, edgecolor='k'))
    pt.xlim(2*axes[0,:].min(), 2*axes[0,:].max())
    pt.ylim(2*axes[1,:].min(), 2*axes[1,:].max())
    ax.axis('equal')
    ax.axis('off')

def valid_actions(state):
    return [0, 1, 2] # which spatial direction to spin

def perform_action(state, action):
    new_state = unhash(state).copy()
    # rotate cubie positions
    index = [slice(None)]*4
    index[action] = 1
    new_state[tuple(index)] = np.rot90(new_state[tuple(index)], axes=(0,1))
    # rotate cubies
    swap = [d for d in range(3) if d != action]
    new_state[tuple(index[:3])+(swap,)] = new_state[tuple(index[:3])+(swap[::-1],)]
    return rehash(new_state)

if __name__ == "__main__":
    
    solved = np.zeros((2,2,2,3),dtype=np.byte)
    solved[0,:,:,0] = R
    solved[1,:,:,0] = O
    solved[:,0,:,1] = W
    solved[:,1,:,1] = Y
    solved[:,:,1,2] = G
    solved[:,:,0,2] = B
    print(solved)
    solved = rehash(solved)
    
    pt.subplot(1,3,1)
    showcube(solved)
    
    state = solved
    plan = [0, 1, 2]
    for action in plan:
        state = perform_action(state, action)
    pt.subplot(1,3,2)
    showcube(state)

    for action in np.repeat(plan[::-1], 3):
        state = perform_action(state, action)
    pt.subplot(1,3,3)
    showcube(state)
    pt.show()
    
    from graph_search import reachable_states
    states = reachable_states(valid_actions, perform_action, solved)
    print(len(states))

