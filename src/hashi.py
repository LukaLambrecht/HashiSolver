# external imports
import numpy as np

# local imports
from vertex import Vertex
from cluster import Cluster
from edge import Edge


class Hashi(object):

    def __init__(self, vertices):
        # default constructor from list of vertices
        # set basic attributes
        self.vertices = vertices
        self.nvertices = len(vertices)
        self.edges = []
        self.complete = False
        # determine correct neighbours
        # (i.e. topologically connected vertices)
        for vertex in self.vertices:
            for direction in [0,1,2,3]:
                # find neighbour in list of provided vertices
                neighbour = vertex.find_closest(vertices, direction)
                vertex.neighbours[direction] = neighbour
        # initialize clusters
        # note: initally, none of the vertices have a connection,
        #       so each vertex represents its own cluster;
        #       they will be gradually merged into only one cluster
        #       when fully solved.
        self.clusters = [Cluster(vertices=[v]) for v in vertices]
        self.cluster_lookup_table = {}
        for idx in range(len(vertices)): self.cluster_lookup_table[idx] = self.clusters[idx]
        # initialize topology
        # note: this needs to be done after setting the neighbours,
        #       since the topology matrix is defined based on those neighbours
        self.topology = -np.ones((self.nvertices, self.nvertices))
        self.make_topology()

    def __str__(self):
        # basic printing
        infostr = 'Hashi ({} vertices, {} edges)'.format(self.nvertices, len(self.edges))
        return infostr

    def print(self):
        # fancy printing

        # initialize grid of characters
        offsetx = min([v.x for v in self.vertices])
        offsety = min([v.y for v in self.vertices])
        maxx = max([v.x for v in self.vertices]) - offsetx
        maxy = max([v.y for v in self.vertices]) - offsety
        chars = [[' ']*(2*maxx+1)]*(2*maxy+1)
        chars = np.array(chars)

        # fill vertices
        for v in self.vertices:
            chars[len(chars)-1-2*(v.y-offsety)][2*(v.x-offsetx)] = str(v.n)
                
        # fill edges
        for e in self.edges:
            xcoords = []
            ycoords = []
            if e.horizontal:
                xcoords = list(range(2*(e.x1-offsetx)+1, 2*(e.x2-offsetx)))
                ycoords = [len(chars)-1-2*(e.y1-offsety)]*len(xcoords)
                chardict = {' ': '-', '-': '='}
            elif e.vertical:
                ycoords = list(range(len(chars)-2*(e.y2-offsety), len(chars)-1-2*(e.y1-offsety)))
                xcoords = [2*(e.x1-offsetx)]*len(ycoords)
                chardict = {' ': '|', '|': '"'}
            for xcoord,ycoord in zip(xcoords, ycoords):
                chars[ycoord][xcoord] = chardict[chars[ycoord][xcoord]]

        # group characters in lines
        lines = [''.join(linechars) for linechars in chars]

        # add boundary lines
        lines = ['|'+line+'|' for line in lines]
        horizontal = '-'*len(lines[0])
        lines = [horizontal] + lines + [horizontal]

        # append lines in a single string
        txt = '\n'.join(lines)
        print(txt)

    @staticmethod
    def from_txt(txtfile):
        # static constructor from txt input file
        with open(txtfile, 'r') as f: txt = f.read()
        return Hashi.from_str(txt)

    @staticmethod
    def from_str(txt):
        # format lines
        lines = [line.strip(' \t\n') for line in txt.split('\n')]
        lines = [line for line in lines if len(line)!=0]
        # make collection of vertices
        vertices = []
        for y,line in enumerate(lines[::-1]):
            for x,char in enumerate(line):
                if char=='-': continue
                try: n = int(char)
                except: raise Exception('ERROR: unrecognized character: {}'.format(char))
                v = Vertex(x, y, n)
                vertices.append(v)
        # return a Hashi object
        return Hashi(vertices)

    @staticmethod
    def from_dict(vdict):
        # constructor from a dict of the form {(x,y): n, ...}
        vertices = []
        for (x,y),n in vdict.items():
            vertex = Vertex(x, y, n)
            vertices.append(vertex)
        return Hashi(vertices)

    def to_str(self):
        # reverse operation with respect to from_str,
        # i.e. make string representation suitable for writing to file
        # (note: edges are ignored, mostly used for empty hashis)
        offsetx = min([v.x for v in self.vertices])
        offsety = min([v.y for v in self.vertices])
        maxx = max([v.x for v in self.vertices]) - offsetx
        maxy = max([v.y for v in self.vertices]) - offsety
        chars = [['-']*(maxx+1)]*(maxy+1)
        chars = np.array(chars)
        for v in self.vertices:
            chars[len(chars)-1-(v.y-offsety)][v.x-offsetx] = str(v.n)
        lines = [''.join(linechars) for linechars in chars]
        txt = '\n'.join(lines)
        return txt

    def make_topology(self):
        # make the topology for the provided list of vertices
        # note: this function is primarily meant to run on a list of vertices
        #       where all vertex connections are still in open/potential state
        #       (right after initialization).
        #       it will raise an error if a closed or established connection is found
        #       (maybe to revisit later if the need arises).

        # loop over vertices
        for vidx, vertex in enumerate(self.vertices):
            # check if some connections were already closed or established
            if -1 in vertex.connections: raise Exception('ERROR: found already closed connection.') 
            if 1 in vertex.connections: raise Exception('ERROR: found already established connection.')
            # loop over the directions
            for direction in [0,1,2,3]:
                # neighbour in the given direction
                neighbour = vertex.neighbours[direction]
                # if none, close the corresponding connections and continue
                if neighbour is None:
                    vertex.close_connections(direction)
                    continue
                # set the topological connection as allowed
                nidx = self.vertices.index(neighbour)
                self.topology[vidx, nidx] = 0
                self.topology[nidx, vidx] = 0
    
    def get(self, v):
        # auxiliary function for vertex/index conversion
        if isinstance(v, int):
            vidx = v
            v = self.vertices[vidx]
        elif isinstance(v, Vertex):
            vidx = self.vertices.index(v)
        else: raise Exception('ERROR: unrecognized type for vertex: {}'.format(type(v)))
        return (vidx, v)
    
    def get_vertex_at_coordinate(self, x, y):
        for vidx, v in self.vertices:
            if( v.x==x and v.y==y ): return (vidx, v)
        return None

    def get_edges(self):
        # get edges grouped by whether they connect the same vertices.
        # returns a dict with keys of the form (x1, y1, x2, y2)
        # and values which are lists of corresponding edges.
        res = {}
        for e in self.edges:
            key = (e.x1, e.y1, e.x2, e.y2)
            if key in res.keys(): res[key].append(e)
            else: res[key] = [e]
        return res

    def get_cluster(self, v):
        ### get the cluster of vertices that are connected to the given vertex
        vidx, v = self.get(v)
        cluster_ids = []
        cluster = self.cluster_lookup_table[vidx]
        return cluster

    def has_potential_connection(self, v1, v2):
        ### check if a connection between v1 and v2 could be made
        v1idx, v1 = self.get(v1)
        v2idx, v2 = self.get(v2)
        return v1.can_connect_with(v2)

    def make_potential_edges(self):
        # returns a list of all currently potential edges
        # note: return type is a list of tuples of the form (edge, v1, v2)
        res = []
        for v1idx, v1 in enumerate(self.vertices):
            for v2idx, v2 in enumerate(self.vertices):
                if v2idx<=v1idx: continue
                if not self.has_potential_connection(v1, v2): continue
                res.append( (Edge(v1.x, v1.y, v2.x, v2.y), v1idx, v1, v2idx, v2) )
        return res

    def add_edge(self, v1, v2):
        v1idx, v1 = self.get(v1)
        v2idx, v2 = self.get(v2)
        # check if connection is allowed
        if not self.has_potential_connection(v1, v2):
            print('ERROR: invalid connection:')
            print('Trying to make a connection between:')
            print('  - {}'.format(v1))
            print('  - {}'.format(v2))
            raise Exception('ERROR: invalid connection.')
        # make and add the edge
        edge = Edge(v1.x, v1.y, v2.x, v2.y)
        self.edges.append(edge)
        # modify topology matrix
        self.topology[v1idx, v2idx] += 1
        self.topology[v2idx, v1idx] += 1
        # modify vertex connections
        v1.add_connection(v2.direction(v1))
        v2.add_connection(v1.direction(v2))
        # merge clusters
        c1 = self.cluster_lookup_table[v1idx]
        c2 = self.cluster_lookup_table[v2idx]
        if c1 != c2:
            c1.add_cluster(c2)
            for vidx in range(len(self.vertices)):
                if self.cluster_lookup_table[vidx] == c2:
                    self.cluster_lookup_table[vidx] = c1
            self.clusters.remove(c2)
        # close all potential connections crossing the newly added edge
        for test_edge, test_v1idx, test_v1, test_v2idx, test_v2 in self.make_potential_edges():
            if( test_v1idx==v1idx or test_v1idx==v2idx 
                or test_v2idx==v1idx or test_v2idx==v2idx ): continue
            if not edge.crosses( test_edge ): continue
            test_v1.close_connections(test_v2.direction(test_v1), suppress_warnings=True)
            test_v2.close_connections(test_v1.direction(test_v2), suppress_warnings=True)
        # close all potential connections to v1 and v2 if they are complete
        for vtestidx, vtest in zip([v1idx, v2idx], [v1,v2]):
            if vtest.complete:
                for vidx, v in enumerate(self.vertices):
                    if vidx==vtestidx: continue
                    if not self.has_potential_connection(vtest, v): continue
                    v.close_connections(vtest.direction(v))
        # check if this makes the hashi complete
        if all([v.complete for v in self.vertices]): self.complete = True
