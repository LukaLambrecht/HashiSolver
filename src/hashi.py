# external imports
import numpy as np

# local imports
from vertex import Vertex
from edge import Edge


class Hashi(object):

    def __init__(self, vertices, do_make_topology=True):
        # default constructor from list of vertices
        # set basic attributes
        self.vertices = vertices
        self.nvertices = len(vertices)
        self.edges = []
        self.complete = False
        # initialize topology
        self.topology = -np.ones((self.nvertices,self.nvertices))
        if do_make_topology: self.make_topology()

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
        for vidx, v in enumerate(self.vertices):
            # check if some connections were already closed or established
            if -1 in v.connections: raise Exception('ERROR: found already closed connection.') 
            if 1 in v.connections: raise Exception('ERROR: found already established connection.')
            # for this vertex, make collection of all other vertices in the collection
            otherids = [idx for idx in range(len(self.vertices)) if idx!=vidx]
            othervertices = [self.vertices[idx] for idx in otherids]
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
                self.topology[self.vertices.index(v), self.vertices.index(closest)] = 0
                self.topology[self.vertices.index(closest), self.vertices.index(v)] = 0
    
    def subset(self, vids):
        # make a new Hashi that is a subset of the current one
        # (including potential partial solving so far)
        
        # define subset of vertices and make a new hashi with those
        vertices = [self.vertices[vidx].copy() for vidx in vids]
        sub = Hashi(vertices, do_make_topology=False)
        # set topology
        topology = self.topology
        topology = topology[:,vids]
        topology = topology[vids,:]
        sub.topology = topology
        # copy all edges that are fully within the subset of vertices
        # (not the ones that connect vertices outside the subset)
        for edge in self.edges:
            if edge.connects([self.vertices[vidx] for vidx in vids]):
                sub.edges.append(edge.copy())
        return sub
    
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

    def get_cluster(self, v, iterative=False, cluster=None):
        # get a list of vertices that are connected to the given vertex
        vidx, v = self.get(v)
        if cluster is None: cluster = [v]
        new = []
        for direction in v.directions_with_established_connection():
            other = self.find_vertex_in_direction(v, direction)
            if other not in cluster:
                cluster.append(other)
                new.append(other)
        if iterative:
            for v2 in new: self.get_cluster(v2, iterative=True, cluster=cluster)
        cluster_ids = [self.vertices.index(v2) for v2 in cluster]
        return (cluster_ids, cluster)

    def has_potential_connection(self, v1, v2):
        v1idx, v1 = self.get(v1)
        v2idx, v2 = self.get(v2)
        # first check potential connection in topology
        if self.topology[v1idx, v2idx]==-1: return False
        # then check connections in the relevant direction
        # note: this implicitly also takes into account edges, see add_edge.
        if not v1.has_potential_connection(v2.direction(v1)): return False
        if not v2.has_potential_connection(v1.direction(v2)): return False
        return True

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
        # make and add the edge and connections to vertices
        edge = Edge(v1.x, v1.y, v2.x, v2.y)
        self.edges.append(edge)
        self.topology[v1idx, v2idx] += 1
        self.topology[v2idx, v1idx] += 1
        v1.add_connection(v2.direction(v1))
        v2.add_connection(v1.direction(v2))
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
        
    def find_vertex_in_direction(self, v, direction):
        # find a vertex in a given direction from a given vertex
        # note: returns None if no vertex was found in the given direction
        # note: only topology is taken into account, i.e. no check is done
        #       on the status of the connection(s).
        vidx, v = self.get(v)
        candidate_indices = np.nonzero(self.topology[vidx,:]!=-1)[0]
        candidates = [self.vertices[idx] for idx in candidate_indices]
        for candidate in candidates:
            if candidate.is_in_direction(v, direction): return candidate
        return None
