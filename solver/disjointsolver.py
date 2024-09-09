# Solving methods based on disjoint subset veto.

# Note: not yet complete.

def close_connections_disjoint(hashi, verbose=False):
    # PRELIMINARY VERSION, KNOWN TO BE INCOMPLETE
    # dynamically close vertex connections,
    # based on the criterion that a connection that would create
    # a disjoint set of vertices disconnected from the rest is forbidden
    # (i.e. all vertices must be connected to each other).
    for vidx,vertex in enumerate(hashi.vertices):
        if vertex.complete: continue
        # get the cluster of connected vertices
        cluster_inds, cluster = hashi.get_cluster(vertex, iterative=True)
        # if all vertices are already connected, skip
        if len(cluster_inds)==hashi.nvertices: continue
        # loop over potential connections
        for direction in vertex.directions_with_potential_connection():
            # get the other vertex
            other_vertex = vertex.neighbours[direction]
            if other_vertex is None: raise Exception('ERROR: something went wrong.')
            other_direction = vertex.direction(other_vertex)
            # get the cluster of the other vertex
            other_cluster_inds, other_cluster = hashi.get_cluster(other_vertex, iterative=True)
            # if the two clusters together make up the full hashi, skip
            if len(list(set(cluster_inds+other_cluster_inds)))==hashi.nvertices: continue
            # check that both clusters are complete apart from the two given vertices
            completion = ([v.complete for v in cluster
                           if (v!=vertex and v!=other_vertex)])
            if not all(completion): continue
            other_completion = ([v.complete for v in other_cluster
                                if (v!=vertex and v!=other_vertex)])
            if not all(other_completion): continue
            # if adding the connection would make both vertices complete,
            # it is not allowed and can be closed.
            if( vertex.n_potential_connections(direction)==vertex.n_missing_connections()
                and other_vertex.n_potential_connections(other_direction)==other_vertex.n_missing_connections() ):
                if verbose:
                    print('INFO in disjoint solver: closed connections from {} in direction {}'.format(vertex, direction))
                vertex.close_n_connections(direction, 1, suppress_warnings=True)
                other_vertex.close_n_connections(other_direction, 1, suppress_warnings=True)
