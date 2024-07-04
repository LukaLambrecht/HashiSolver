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

def close_connections_disjoint(hashi, verbose=False):
    # dynamically close vertex connections,
    # based on the criterion that a connection that would create
    # a disjoint set of vertices disconnected from the rest is forbidden
    # (i.e. all vertices must be connected to each other).
    for vertex in hashi.vertices:
        if vertex.complete: continue
        # get the cluster of connected vertices
        cluster = hashi.get_cluster(vertex, iterative=True)
        # if all vertices are already connected, skip
        if len(cluster)==len(hashi.vertices): continue
        # loop over potential connections
        for direction in vertex.directions_with_potential_connection():
            # get the other vertex
            other_vertex = hashi.vertexcollection.find_vertex_in_direction(vertex, direction)
            if other_vertex is None: raise Exception('ERROR: something went wrong.')
            other_direction = vertex.direction(other_vertex)
            # get the cluster of the other vertex
            other_cluster = hashi.get_cluster(other_vertex, iterative=True)
            # check that both clusters are complete apart from the two given vertices
            completion = ([v.complete for v in cluster
                           if (v!=vertex and v!=other_vertex)])
            if not all(completion): continue
            other_completion = ([v.complete for v in other_cluster
                                if (v!=vertex and v!=other_vertex)])
            if not all(other_completion): continue
            # if adding the connection would make both vertices complete,
            # it is not allowed and can be closed.
            if( vertex.n_potential_connections(direction)==1
                and other_vertex.n_potential_connections(other_direction)==1 ):
                if verbose:
                    print('Closing connections because of disjointness')
                    print('Current hashi:')
                    hashi.print()
                    print('Connections closed: {}, {}'.format(vertex, direction))
                vertex.close_n_connections(direction, 1, suppress_warnings=True)
                other_vertex.close_n_connections(other_direction, 1, suppress_warnings=True)


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
        close_connections_disjoint(hashi, verbose=verbose)
