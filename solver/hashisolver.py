# external imports
import numpy as np

# local imports
import vertexsolver
import disjointsolver


def close_connections(hashi, verbose=False):
    # dynamically close vertex connections,
    # based on available number of endpoints.
    # note: 
    n_closed = 0
    for vertex in hashi.vertices:
        for direction in vertex.directions_with_potential_connection():
            n_potential_direction = vertex.n_potential_connections(direction)
            other_vertex = hashi.find_vertex_in_direction(vertex, direction)
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


def solve(hashi, verbose=False):
    ### main solving method

    # vertex solver
    added_edges = ['dummy']
    close_connections(hashi)
    while len(added_edges)>0:
        added_edges = []
        for vertex in hashi.vertices:
            added_edges += vertexsolver.fill_vertex(hashi, vertex, repeat=True)
        close_connections(hashi)
        disjointsolver.close_connections_disjoint(hashi, verbose=verbose)
    for vertex in hashi.vertices: vertexsolver.fill_vertex(hashi, vertex, repeat=True)