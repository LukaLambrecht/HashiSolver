# external imports
import numpy as np

# local imports
from vertex import Vertex


class VertexCollection(object):

    def __init__(self, vertices):
        # default constructor
        # set basic attributes
        self.vertices = vertices
        self.nvertices = len(vertices)
        # initialize topology
        self.topology = -np.ones((self.nvertices,self.nvertices))
        # make topology
        self.make_topology()

    def __str__(self):
        # basic printing
        infostr = 'VertexCollection\n  Vertices:\n'
        for v in self.vertices: infostr += '    - {}\n'.format(v)
        infostr += '  Topology:\n'
        infostr += '{}'.format(self.topology)
        return infostr

    @staticmethod
    def from_txt(txtfile):
        # static constructor from txt input file

        # read lines from txt file
        with open(txtfile, 'r') as f:
            lines = f.readlines()
        lines = [line.strip(' \t\n') for line in lines]

        # make collection of vertices
        idn = 0
        vertices = []
        for y,line in enumerate(lines[::-1]):
            for x,char in enumerate(line):
                if char=='-': continue
                try: n = int(char)
                except: raise Exception('ERROR: unrecognized character: {}'.format(char))
                v = Vertex(idn, x, y, n)
                vertices.append(v)
                idn += 1

        # return a VertexCollection object
        return VertexCollection(vertices)

    def make_topology(self):
        # make the topology for the provided list of vertices
        # note: this function is primarily meant to run on a list of vertices
        #       where all vertex connections are still in open/potential state
        #       (right after initialization).
        #       it will raise an error if a closed or established connection is found
        #       (maybe to revisit later if the need arises).

        # loop over vertices
        for v in self.vertices:
            # check if some connections were already closed or established
            if -1 in v.connections: raise Exception('ERROR: found already closed connection.') 
            if 1 in v.connections: raise Exception('ERROR: found already established connection.')
            # for this vertex, make collection of all other vertices in the collection
            othervertices = [v2 for v2 in self.vertices if v.idn != v2.idn]
            # loop over the directions
            for direction in [0,1,2,3]:
                # find other vertices in the given direction
                candidates = [v2 for v2 in othervertices if v2.is_in_direction(v, direction)]
                # if none, close the corresponding connections and continue
                if len(candidates)==0:
                    v.close_connections(direction)
                    continue
                # if one or multiple, find the closest one
                closest = v.find_closest(candidates, direction)
                # set the topological connection as allowed
                self.topology[v.idn, closest.idn] = 0
                self.topology[closest.idn, v.idn] = 0

    def has_potential_connection(self, v1, v2):
        if isinstance(v1, int): v1 = self.vertices[v1]
        if isinstance(v2, int): v2 = self.vertices[v2]
        # first check potential connection in topology
        if self.topology[v1.idn, v2.idn]==-1: return False
        # then check open connections in vertices
        if not v1.has_potential_connection(v2.direction(v1)): return False
        if not v2.has_potential_connection(v1.direction(v2)): return False
        return True

    def add_connection(self, v1, v2):
        if isinstance(v1, int): v1 = self.vertices[v1]
        if isinstance(v2, int): v2 = self.vertices[v2]
        if not self.has_potential_connection(v1, v2):
            raise Exception('ERROR: connection not allowed.')
        self.topology[v1.idn, v2.idn] += 1
        self.topology[v2.idn, v1.idn] += 1
        v1.add_connection(v2.direction(v1))
        v2.add_connection(v1.direction(v2))

    def find_vertex_in_direction(self, v, direction):
        # find a vertex in a given direction from a given vertex
        # note: returns None if no vertex was found in the given direction
        # note: only topology is taken into account, i.e. no check is done
        #       on the status of the connection(s).
        candidate_indices = np.nonzero(self.topology[v.idn,:]!=-1)[0]
        candidates = [self.vertices[idx] for idx in candidate_indices]
        for candidate in candidates:
            if candidate.is_in_direction(v, direction): return candidate
        return None
