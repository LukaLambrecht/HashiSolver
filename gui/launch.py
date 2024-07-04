# import external modules
import os
import sys
from bokeh.io import curdoc

# import local modules
sys.path.append('../src')
from hashi import Hashi
sys.path.append('../solver')
import hashisolver

# import GUI class
from gui import HashiSolverGui

# launch the GUI
doc = curdoc()
gui = HashiSolverGui(doc=doc)
