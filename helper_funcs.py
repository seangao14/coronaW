# functions to be ran once per frame rather than per objects

from scipy.spatial.distance import pdist
import numpy as np

def get_distance(people):
    locs = []
    distances = {}
    for i in people:
        locs.append([i.x_pos, i.y_pos])
    d = np.array(pdist(locs))
    index = 0
    for i in range(len(people)):
        for j in range(i+1, len(people)):
            distances[i, j] = d[index]
            index += 1

    # output format: {(0, 1): d, (0, 2): d, (0, 3): d, (1, 2): d, (1, 3): d, (2, 3): d}
    return distances