import os
import sys
from base64 import b64decode
from bokeh.io import show
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import Button
from bokeh.models.widgets import FileInput

sys.path.append('../src')
from hashi import Hashi
import hashisolver

from hashiplot import makedummyplot
from hashiplot import makehashiplot


class HashiSolverGui(object):
    
    def __init__(self, doc=None):
        # copy provided attributes
        if doc is None: self.doc = curdoc()
        else: self.doc = doc
        # get empty dummy figure
        p = makedummyplot()
        # create buttons
        self.load_button = Button(label="Load", button_type="primary")
        self.load_button.on_click(self.open_file_input)
        self.solve_button = Button(label="Solve", button_type="success")
        self.solve_button.on_click(self.solve)
        # create layout
        self.layout = self.make_default_layout(p, self.doc)
        # set dummy attributes initialized later
        self.hashi = None

    def make_layout(self, elements, doc):
        rows = [row(*els) for els in elements]
        layout = column(*rows)
        if len(doc.roots)==0: doc.add_root(layout)
        else: doc.roots[0].children = [layout]
        return layout

    def make_default_layout(self, hashifig, doc):
        elements = [[hashifig], [self.load_button, self.solve_button]]
        self.make_layout(elements, doc)

    def open_file_input(self):
        self.file_input = FileInput(accept=".txt")
        self.file_input.on_change("value", self.open_file)
        layout = column(row(self.file_input))
        curdoc().roots[0].children = [layout]

    def open_file(self, attr, old, new):
        # note: because of security restrictions,
        #       the FileInput widget cannot return
        #       a full path, but only the file basename.
        #       therefore, instead of returning the file path,
        #       its contents are returned (or rather 'uploaded')
        #       as a base64 encoded string.
        b64encoded = self.file_input.value
        bts = b64decode(b64encoded)
        txt = bts.decode('utf-8')
        # load the hashi
        self.hashi = Hashi.from_str(txt)
        self.hashi.print()
        # update the layout
        p = makehashiplot(self.hashi)
        self.make_default_layout(p, self.doc)

    def solve(self):
        # check if hashi was loaded
        if self.hashi is None: return
        # solve the hashi
        hashisolver.solve(self.hashi)
        self.hashi.print()
        print('Complete: {}'.format(self.hashi.complete))
        # update the layout
        p = makehashiplot(self.hashi)
        self.make_default_layout(p, self.doc)
