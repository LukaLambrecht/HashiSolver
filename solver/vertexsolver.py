# external imports
import numpy as np


def find_directions_to_connect(vertex):
    # helper function to fill_vertex.
    # find connections that can be made (if any),
    # based only on vertex properties.

    # compare number of potential connections with target number of connections
    n_established = np.sum(vertex.connections==1)
    n_needed = vertex.n - n_established
    n_potential = np.sum(vertex.connections==0)
    res = []

    # simplest case where all connections can be trivially filled
    if n_potential == n_needed:
        for direction in vertex.directions_with_potential_connection():
            n_potential_direction = vertex.n_potential_connections(direction)
            res += [direction]*n_potential_direction
        return res

    # non-trivial case
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

def fill_vertex(hashi, vertex, repeat=False):
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
        other_vertex = hashi.vertexcollection.find_vertex_in_direction(vertex, direction)
        if other_vertex is None: raise Exception('ERROR: something went wrong')
        hashi.add_edge(vertex, other_vertex)
        added_edges.append((vertex, other_vertex))

    # repeat if required
    if repeat: added_edges += fill_vertex(hashi, vertex, repeat=True)

    # return added edges
    return added_edges
