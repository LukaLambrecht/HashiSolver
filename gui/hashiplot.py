############################################
# Make a plot from a provided hashi object #
############################################


import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models import Circle
from bokeh.models import Label, LabelSet
from bokeh.models import TextInput


def makedummyplot():
    # create the figure
    fig = figure(x_range=(-0.5,0.5), y_range=(-0.5, 0.5), width=500, height=500)
    fig.xaxis.visible = False
    fig.yaxis.visible = False
    # add label
    label = Label(x=0, y=0, text='Welcome to HashiSolver!',
              text_align='center', text_baseline='middle')
    fig.add_layout(label)
    return fig


def makehashiplot(hashi, n_editable=False):
    # extract x and y ranges
    maxx = max([v.x for v in hashi.vertices])
    maxy = max([v.y for v in hashi.vertices])
    # create the figure
    fig = figure(x_range=(-0.5,maxx+0.5), y_range=(-0.5, maxy+0.5), width=500, height=500)
    fig.xaxis.visible = False
    fig.yaxis.visible = False
    # add a circle for each vertex
    x = np.array([v.x for v in hashi.vertices])
    y = np.array([v.y for v in hashi.vertices])
    r = np.ones(len(x))*0.4
    n = np.array([v.n for v in hashi.vertices])
    c = np.array([("#3288bd" if v.complete else "white") for v in hashi.vertices])
    source = ColumnDataSource(dict(x=x, y=y, r=r, n=n, c=c))
    circles = Circle(x="x", y="y", radius="r", radius_dimension='x', radius_units='data',
                line_color="#3288bd", fill_color="c", line_width=3)
    fig.add_glyph(source, circles)
    # add the expected number of connections for each vertex
    if not n_editable:
        labels = LabelSet(x='x', y='y', text='n', text_align='center', text_baseline='middle', source=source)
        fig.add_layout(labels)
    # add the expected number of connections for each vertex - editable version
    # (does not work yet)
    else: pass
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
                  [coords[0]+0.4, coords[1]-0.05, coords[2]-0.4, coords[3]-0.05],
                  [coords[0]+0.4, coords[1]+0.05, coords[2]-0.4, coords[3]+0.05]
                ]
            elif edges[1].vertical:
                coords = [
                  [coords[0]-0.05, coords[1]+0.4, coords[2]-0.05, coords[3]-0.4],
                  [coords[0]+0.05, coords[1]+0.4, coords[2]+0.05, coords[3]-0.4]
                ]
            else: raise Exception('Not yet implemented.')
        else: raise Exception('Not yet implemented.')
        # add lines
        for c in coords:
            fig.line([c[0], c[2]], [c[1], c[3]], line_width=2, line_color="#3288bd")
    return fig
