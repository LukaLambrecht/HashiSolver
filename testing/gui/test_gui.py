import os
import sys
from bokeh.io import curdoc

sys.path.append('../../gui-bokeh')
from gui import HashiSolverGui



doc = curdoc()
gui = HashiSolverGui(doc=doc)
