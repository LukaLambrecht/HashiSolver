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
        #       that needs to be done separately;
        #       it cannot be done here, since there might be ambiguity
        #       in which connection to make.
        canadd = True
        if check_connection:
            # check if a connection can be or is already made
            # between the vertex and this cluster
            canadd = False
            if len(self.vertices)==0: canadd = True
            for othervertex in self.vertices:
                if( vertex.can_connect_with(othervertex)
                    or vertex.is_connected_with(othervertex) ):
                    canadd = True
                    break
        if canadd: self.vertices.append(vertex)
        else: raise Exception('ERROR: cannot add vertex to cluster.')

    def add_cluster(self, other, check_connection=True):
        ### add all vertices of another cluster to this cluster
        # first check if both clusters can be connected
        canadd = True
        if check_connection:
            # check if a connection can be or is already made
            # between any of the vertices in the other cluster
            # and any of the vertices in this cluster
            canadd = False
            for vertex in self.vertices:
                for othervertex in other.vertices:
                    if( vertex.can_connect_with(othervertex)
                        or vertex.is_connected_with(othervertex) ):
                        canadd = True
                        break
                if canadd: break
        if canadd:
            for vertex in other.vertices: self.add_vertex(vertex, check_connection=False)
        else: raise Exception('ERROR: cannot add clusters to each other.')

    def get_external_connections(self):
        ### get a list of all potential connections that cross the cluster boundary
        res = []
        for vertex in self.vertices:
            # shortcut: skip vertices that are complete
            if vertex.complete: continue
            # loop over neighbours
            for neighbour in vertex.neighbours:
                # skip non-existing neighbours
                if neighbour is None: continue
                # skip neighbours that are already in the cluster
                if neighbour in self.vertices: continue
                # skip neighbours that could not be connected
                if not vertex.can_connect_with(neighbour): continue
                # add potential connection to list
                res.append((vertex, neighbour))
        return res
