# external imports
import numpy as np

# local imports
import vertexsolver


def close_connections(hashi):
    # dynamically close vertex connections,
    # based on available number of endpoints
    n_closed = 0
    for vertex in hashi.vertices:
        for direction in vertex.directions_with_potential_connection():
            n_potential_direction = vertex.n_potential_connections(direction)
            other_vertex = hashi.vertexcollection.find_vertex_in_direction(vertex, direction)
            if other_vertex is None: raise Exception('ERROR: something went wrong.')
            max_endpoints = min(
                    other_vertex.multiplicity,
                    other_vertex.n - np.sum(other_vertex.connections==1)
            )
            if max_endpoints < n_potential_direction:
                n_close = n_potential_direction - max_endpoints
                vertex.close_n_connections(direction, n_close)
                n_closed += n_close
    return n_closed

def solve(hashi):
    ### main solving method

    # vertex solver
    added_edges = ['dummy']
    close_connections(hashi)
    while len(added_edges)>0:
        added_edges = []
        for vertex in hashi.vertices:
            added_edges += vertexsolver.fill_vertex(hashi, vertex, repeat=True)
        close_connections(hashi)
