# Solving methods based on individual vertices.

# These methods focus on a single vertex in a hashi,
# and try to establish connections based solely on the
# pattern of closed, potential and established connections for that vertex.

# They are intended to be run in a loop over all vertices in a hashi
# (or potentially on some specific vertex if there is a special reason to believe
# a connection could be established for that vertex).

# external imports
import numpy as np


def find_directions_to_connect(vertex):
    # helper function to fill_vertex.
    # find connections that can be made (if any),
    # based only on vertex connection properties.

    # compare number of potential connections with target number of connections
    n_established = np.sum(vertex.connections==1)
    n_needed = vertex.n - n_established
    n_potential = np.sum(vertex.connections==0)
    res = []

    # simplest case where all connections can be trivially filled,
    # since the number of potential connections equals the number of missing connections.
    if n_potential == n_needed:
        for direction in vertex.directions_with_potential_connection():
            n_potential_direction = vertex.n_potential_connections(direction)
            res += [direction]*n_potential_direction
        return res

    # non-trivial case:
    # check for each direction separately if all other directions
    # could potentially absorb all missing connections.
    for direction in vertex.directions_with_potential_connection():
        # calculate number of potential connections in other directions than this one
        n_potential_other_directions = sum([vertex.n_potential_connections(d) for d in [0,1,2,3] if d!=direction])
        # at least the overflow must be filled in this direction
        overflow = n_needed - n_potential_other_directions
        if overflow>0:
            if vertex.n_potential_connections(direction)<overflow:
                msg = 'ERROR: something went wrong'
                raise Exception(msg)
            res += [direction]*overflow
    return res

def fill_vertex(hashi, vertex, repeat=False, verbose=False):
    # function to add edges to a hashi by filling up vertex connections.
    # example:
    #  - vertex.n = 2
    #  - vertex.connections = [0, 0, -1, -1, -1, -1, -1, -1]
    #  -> add two upward edges
    # example:
    #  - vertex.n = 5
    #  - vertex.connections = [-1, -1, 0, 0, 0, 0, 0, 0]
    #  -> add an edge to the left, right, and downwards.
    
    # initializations and first checks
    added_edges = []
    if vertex.complete: return added_edges

    # find directions in which a connection can be made
    directions = find_directions_to_connect(vertex)

    # check early return condition
    if len(directions)==0: return added_edges

    # make the connections
    for direction in directions:
        other_vertex = vertex.neighbours[direction]
        if other_vertex is None: raise Exception('ERROR: something went wrong')
        hashi.add_edge(vertex, other_vertex)
        added_edges.append((vertex, other_vertex))
        if verbose:
            msg = 'INFO in vertex solver: added connection from {} in direction {}'.format(vertex, direction)
            print(msg)

    # repeat if required
    if repeat: added_edges += fill_vertex(hashi, vertex, repeat=True)

    # return added edges
    return added_edges
