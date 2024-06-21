# external imports
import numpy as np

# local imports
from vertex import Vertex
from vertexcollection import VertexCollection
from edge import Edge


class Hashi(object):

    def __init__(self, vertexcollection):
        # default constructor
        self.vertexcollection = vertexcollection
        self.vertices = self.vertexcollection.vertices # shortcut
        self.edges = []
        self.complete = False

    def __str__(self):
        # basic printing
        infostr = 'Hashi ({} vertices, {} edges)'.format(len(self.vertices), len(self.edges))
        return infostr

    def print(self):
        # fancy printing

        # initialize grid of characters
        maxx = max([v.x for v in self.vertices])
        maxy = max([v.y for v in self.vertices])
        chars = [[' ']*(2*maxx+1)]*(2*maxy+1)
        chars = np.array(chars)

        # fill vertices
        for v in self.vertices:
            chars[len(chars)-1-2*v.y][2*v.x] = str(v.n)
                
        # fill edges
        for e in self.edges:
            xcoords = []
            ycoords = []
            if e.horizontal:
                xcoords = list(range(2*e.x1+1, 2*e.x2))
                ycoords = [len(chars)-1-2*e.y1]*len(xcoords)
                chardict = {' ': '-', '-': '='}
            elif e.vertical:
                ycoords = list(range(len(chars)-2*e.y2, len(chars)-1-2*e.y1))
                xcoords = [2*e.x1]*len(ycoords)
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
        # constructor from txt input file
        vertexcollection = VertexCollection.from_txt(txtfile)
        return Hashi(vertexcollection)

    @staticmethod
    def from_str(txt):
        # constructor from string
        vertexcollection = VertexCollection.from_str(txt)
        return Hashi(vertexcollection)

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

    def has_potential_connection(self, v1, v2):
        # first check topology (without edges)
        if not self.vertexcollection.has_potential_connection(v1, v2): return False
        # then check connections in the relevant direction
        # note: this implicitly also takes into account edges, see add_edge.
        if not v1.has_potential_connection(v2.direction(v1)): return False
        if not v2.has_potential_connection(v1.direction(v2)): return False
        return True

    def make_potential_edges(self):
        # returns a list of all currently potential edges
        # note: return type is a list of tuples of the form (edge, v1, v2)
        res = []
        for v1 in self.vertices:
            for v2 in self.vertices:
                if v2.idn<=v1.idn: continue
                if not self.has_potential_connection(v1, v2): continue
                res.append( (Edge(v1.x, v1.y, v2.x, v2.y), v1, v2) )
        return res

    def add_edge(self, v1, v2):
        if not self.has_potential_connection(v1, v2):
            raise Exception('ERROR: invalid connection.')
        # make and add the edge and connections to vertices
        edge = Edge(v1.x, v1.y, v2.x, v2.y)
        self.edges.append(edge)
        self.vertexcollection.add_connection(v1, v2)
        # close all potential connections crossing the newly added edge
        for test_edge, test_v1, test_v2 in self.make_potential_edges():
            if( test_v1.idn==v1.idn or test_v1.idn==v2.idn 
                or test_v2.idn==v1.idn or test_v2.idn==v2.idn ): continue
            if not edge.crosses( test_edge ): continue
            test_v1.close_connections(test_v2.direction(test_v1), suppress_warnings=True)
            test_v2.close_connections(test_v1.direction(test_v2), suppress_warnings=True)
        # close all potential connections to v1 and v2 if they are complete
        for vtest in [v1,v2]:
            if vtest.complete:
                for v in self.vertices:
                    if v.idn==vtest.idn: continue
                    if not self.has_potential_connection(vtest, v): continue
                    v.close_connections(vtest.direction(v))
        # check if this makes the hashi complete
        if all([v.complete for v in self.vertices]): self.complete = True
