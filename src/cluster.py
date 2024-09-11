# import external modules
import numpy as np

# import local modules
from vertex import Vertex


class Cluster(object):
    # implementation of a cluster of connected vertices.

    def __init__(self, vertices=None):
        ### initializer
        self.vertices = vertices if vertices is not None else []

    def __str__(self):
        infostr = 'Cluster with following vertices ({}):\n'.format(len(self.vertices))
        for vertex in self.vertices: infostr += '{}\n'.format(vertex)
        return infostr
    
    def copy(self):
        return Cluster(vertices = [v.copy() for v in self.vertices])

    def add_vertex(self, vertex, check_connection=True):
        ### add a vertex to the cluster
        # note: this does not modify any of the vertex connections;
        #       that cannot be done in this function, since there might be ambiguity
        #       in which connection to make exactly.
        # note: make the vertex connection first, then add it to the cluster
        #       (since an error will be raised if trying to add a vertex to a cluster
        #       to which it is not already connected).
        canadd = True
        if check_connection:
            # check if a connection is already made
            # between the vertex and this cluster
            canadd = False
            if len(self.vertices)==0: canadd = True
            for othervertex in self.vertices:
                if vertex.is_connected_with(othervertex):
                    canadd = True
                    break
        if canadd: self.vertices.append(vertex)
        else: raise Exception('ERROR: cannot add vertex to cluster.')

    def add_cluster(self, other, check_connection=True):
        ### add all vertices of another cluster to this cluster
        # note: just as with add_vertex, make the connection first,
        #       then merge the clusters, else an error will be raised.
        # first check if both clusters can be connected
        canadd = True
        if check_connection:
            # check if a connection is already made
            # between any of the vertices in the other cluster
            # and any of the vertices in this cluster
            canadd = False
            for vertex in self.vertices:
                for othervertex in other.vertices:
                    if vertex.is_connected_with(othervertex):
                        canadd = True
                        break
                if canadd: break
        if canadd:
            for vertex in other.vertices: self.add_vertex(vertex, check_connection=False)
        else: raise Exception('ERROR: cannot add clusters to each other.')

    def get_connections(self, only_internal=False, only_external=False):
        ### get a list of all potential connections for this cluster
        # - only_internal: if set to True, keep only connections that do not cross the cluster boundary
        # - only_external: if set to True, keep only connections that cross the cluster boundary
        res = []
        for vertex in self.vertices:
            # shortcut: skip vertices that are complete
            if vertex.complete: continue
            # loop over neighbours
            for neighbour in vertex.neighbours:
                # skip non-existing neighbours
                if neighbour is None: continue
                # skip neighbours that could not be connected
                if not vertex.can_connect_with(neighbour): continue
                # optional filtering
                if only_internal:
                    # skip neighbours that are outside the cluster
                    if neighbour not in self.vertices: continue
                if only_external:
                    # skip neighbours that belong to the cluster
                    if neighbour in self.vertices: continue
                # add potential connection to list
                res.append((vertex, neighbour))
        return res

    def get_internal_connections(self):
        ### get a list of all potential connections that do not cross the cluster boundary
        return self.get_connections(only_internal=True)

    def get_external_connections(self):
        ### get a list of all potential connections that cross the cluster boundary
        return self.get_connections(only_external=True)

    def would_make_complete(self, connection):
        ### check if a given connection would make a cluster complete
        (v1, v2) = connection
        if not v1.can_connect_with(v2):
            raise Exception('ERROR: something went wrong.')
        # check if all other vertices in this cluster are complete
        completion = [v.complete for v in self.vertices if (v!=v1 and v!=v2)]
        if not all(completion): return False
        # check if v1 and v2 are complete except in each others direction
        for v in [v1, v2]:
            if v not in self.vertices: continue
            direction = v2.direction(v1) if v==v1 else v1.direction(v2)
            if v.n_missing_connections() > v.n_potential_connections(direction): return False
        return True
