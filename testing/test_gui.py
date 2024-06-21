import os
import sys
from bokeh.io import curdoc

sys.path.append('../src')
from hashi import Hashi
sys.path.append('../solver')
import hashisolver
sys.path.append('../gui')
from gui import HashiSolverGui



doc = curdoc()
gui = HashiSolverGui(doc=doc)
