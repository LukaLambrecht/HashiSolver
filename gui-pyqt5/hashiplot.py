import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def makedummyplot():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.text(0.5, 0.5, 'Welcome to HashiSolver!', ha='center', va='center', transform=ax.transAxes,
            fontsize=15)
    return (fig, ax)

def makehashiplot(hashi, fig=None, ax=None):
    # extract x and y ranges
    maxx = max([v.x for v in hashi.vertices])
    maxy = max([v.y for v in hashi.vertices])
    # create the figure
    if fig is None or ax is None: fig, ax = plt.subplots()
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.set_xlim((-0.5, maxx+0.5))
    ax.set_ylim((-0.5, maxy+0.5))
    ax.set_aspect('equal')
    # add a circle for each vertex
    for vertex in hashi.vertices:
        facecolor = 'lightskyblue' if vertex.complete else 'white'
        c = plt.Circle((vertex.x, vertex.y), radius=0.4, edgecolor='b', facecolor=facecolor)
        ax.add_artist(c)
    # add the expected number of connections for each vertex
    for vertex in hashi.vertices:
        ax.text(vertex.x, vertex.y, str(vertex.n), ha='center', va='center')
    # add lines for all edges
    for coords, edges in hashi.get_edges().items():
        # get correct coordinates
        if len(edges)==1:
            if edges[0].horizontal:
                coords = [[coords[0]+0.4, coords[1], coords[2]-0.4, coords[3]]]
            elif edges[0].vertical:
                coords = [[coords[0], coords[1]+0.4, coords[2], coords[3]-0.4]]
            else: raise Exception('Not yet implemented.')
        elif len(edges)==2:
            if edges[0].horizontal:
                coords = [
                  [coords[0]+0.4, coords[1]-0.07, coords[2]-0.4, coords[3]-0.07],
                  [coords[0]+0.4, coords[1]+0.07, coords[2]-0.4, coords[3]+0.07]
                ]
            elif edges[1].vertical:
                coords = [
                  [coords[0]-0.07, coords[1]+0.4, coords[2]-0.07, coords[3]-0.4],
                  [coords[0]+0.07, coords[1]+0.4, coords[2]+0.07, coords[3]-0.4]
                ]
            else: raise Exception('Not yet implemented.')
        else: raise Exception('Not yet implemented.')
        # add lines
        for c in coords:
            ax.plot([c[0], c[2]], [c[1], c[3]], linewidth=2, color='b')
    return (fig,ax)
