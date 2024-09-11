# external imports
import numpy as np

# local imports
import vertexsolver
import disjointsolver


def close_connections(hashi, verbose=False):
    # dynamically close vertex connections,
    # based on available number of endpoints.
    n_closed = 0
    # loop over vertices and directions for each vertex
    for vertex in hashi.vertices:
        for direction in vertex.directions_with_potential_connection():
            # find number of potential connections and other vertex in this direction
            n_potential_direction = vertex.n_potential_connections(direction)
            other_vertex = vertex.neighbours[direction]
            if other_vertex is None: raise Exception('ERROR: something went wrong.')
            # determine maximum number of endpoints
            # (baseline is just the multiplicity of the other vertex,
            #  but could be constrained if the other vertex already has established connections)
            max_endpoints = min(
                    other_vertex.multiplicity,
                    other_vertex.n - np.sum(other_vertex.connections==1)
            )
            # close the appropriate number of connections
            # so that the number of potential connections does not exceed
            # the number of availabe endpoints
            if max_endpoints < n_potential_direction:
                n_close = n_potential_direction - max_endpoints
                vertex.close_n_connections(direction, n_close)
                n_closed += n_close
    return n_closed


def solve(hashi, verbose=False):
    ### main solving method

    # vertex solver
    added_edges = ['dummy']
    n_closed_connections = 1 # dummy
    while len(added_edges)>0 or n_closed_connections>0:
        added_edges = []
        n_closed_connections = 0
        n_closed_connections += close_connections(hashi)
        for vertex in hashi.vertices:
            added_edges += vertexsolver.fill_vertex(hashi, vertex, repeat=True, verbose=verbose)
        n_closed_connections += close_connections(hashi)
        n_closed_connections += disjointsolver.close_connections_disjoint(hashi, verbose=verbose)
        added_edges += disjointsolver.make_joining_connection(hashi, verbose=verbose)
