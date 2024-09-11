# Solving methods based on disjoint subset veto.

# Note: not yet complete.

def close_connections_disjoint(hashi, verbose=False):
    # PRELIMINARY VERSION, KNOWN TO BE INCOMPLETE
    # dynamically close vertex connections,
    # based on the criterion that a connection that would create
    # a disjoint set of vertices disconnected from the rest is forbidden
    # (i.e. all vertices must be connected to each other).
    n_closed = 0
    for vidx,vertex in enumerate(hashi.vertices):
        if vertex.complete: continue
        # get the cluster of connected vertices
        cluster = hashi.get_cluster(vertex)
        # if all vertices are already connected, skip
        if len(cluster.vertices)==hashi.nvertices: continue
        # loop over potential connections
        for direction in vertex.directions_with_potential_connection():
            # get the other vertex
            other_vertex = vertex.neighbours[direction]
            if other_vertex is None: raise Exception('ERROR: something went wrong.')
            other_direction = vertex.direction(other_vertex)
            # get the cluster of the other vertex
            other_cluster = hashi.get_cluster(other_vertex)
            # if the two clusters together make up the full hashi, skip
            if len(list(set(cluster.vertices + other_cluster.vertices)))==hashi.nvertices: continue
            # if adding the connection would make both vertices complete,
            # it is not allowed and can be closed.
            if( cluster.would_make_complete((vertex, other_vertex))
                and other_cluster.would_make_complete((vertex, other_vertex)) ):
                if verbose:
                    msg = 'INFO in disjoint solver: closed connection'
                    msg += ' between {} and {}'.format(vertex, other_vertex)
                    print(msg)
                vertex.close_n_connections(direction, 1, suppress_warnings=True)
                other_vertex.close_n_connections(other_direction, 1, suppress_warnings=True)
                n_closed += 1
    return n_closed

def make_joining_connection(hashi, verbose=False):
    ### make a necessary joining connection
    # if a cluster has only one external connection that would not make it disjoint,
    # this connection has to be made necessarily
    added_edges = []
    # loop over clusters
    for cluster in hashi.clusters:
        candidate_connections = []
        # loop over external connections
        for potential_connection in cluster.get_external_connections():
            # if this connection is made towards a cluster which is made
            # complete by this connection, do not count this connection
            (intvertex, extvertex) = potential_connection
            other_cluster = hashi.get_cluster(extvertex)
            if other_cluster.would_make_complete((potential_connection)): continue
            # add the candidate
            candidate_connections.append(potential_connection)
        if len(candidate_connections)!=1: continue
        (v1, v2) = candidate_connections[0]
        hashi.add_edge(v1, v2)
        added_edges.append((v1, v2))
        if verbose:
            msg = 'INFO in disjoint solver: added connection between {} and {}'.format(v1, v2)
            print(msg)
    return added_edges
