import os
import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
plt.ioff()
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog

from hashiplot import makedummyplot, makehashiplot
from hashibuilder import HashiBuilderWindow
sys.path.append(os.path.abspath('../src'))
from hashi import Hashi
sys.path.append(os.path.abspath('../solver'))
import hashisolver


class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, hashi=None):
        if hashi is None: self.fig, self.ax = makedummyplot()
        else: self.fig, self.ax = makehashiplot(hashi)
        super(MplCanvas, self).__init__(self.fig)


class HashiSolverGui(QMainWindow):
    
    def __init__(self, parent=None):
        super(HashiSolverGui, self).__init__(parent)
        central = QWidget()
        
        self.hashi = None
        
        buttons_layout = QGridLayout()
        self.load_button = QPushButton('Load')
        self.load_button.clicked.connect(self.load)
        buttons_layout.addWidget(self.load_button, 0, 0)
        self.build_button = QPushButton('Build')
        self.build_button.clicked.connect(self.open_build_window)
        buttons_layout.addWidget(self.build_button, 0, 1)
        self.solve_button = QPushButton('Solve')
        self.solve_button.clicked.connect(self.solve)
        buttons_layout.addWidget(self.solve_button, 0, 2)
        
        self.mplcanvas = MplCanvas()
        
        main_layout = QGridLayout(central)
        main_layout.addWidget(self.mplcanvas, 0, 0)
        main_layout.addLayout(buttons_layout, 1, 0)
        
        self.setCentralWidget(central)

    def closeEvent(self, event):
        event.accept()
        
    def load(self, event):
        inputfile, _ = QFileDialog.getOpenFileName(self, 'some text', '../fls', '(*.txt)')
        if inputfile == '': return
        self.hashi = Hashi.from_txt(inputfile)
        self.redraw()

    def open_build_window(self, event):
        # note: buildwindow must be an attribute of self
        #       for the showing of the second window to work
        self.buildwindow = HashiBuilderWindow()
        self.buildwindow.ok_button.clicked.connect(self.build_hashi)
        self.buildwindow.show()

    def build_hashi(self, event):
        self.hashi = self.buildwindow.make_hashi()
        self.buildwindow.close()
        del self.buildwindow
        self.redraw()
        
    def solve(self, event):
        if self.hashi is None: return
        hashisolver.solve(self.hashi)
        self.redraw()
        
    def redraw(self):
        if self.hashi is None: return
        self.mplcanvas.ax.cla()
        _ = makehashiplot(self.hashi, fig=self.mplcanvas.fig, ax=self.mplcanvas.ax)
        self.mplcanvas.draw()
      
def main():
   app = QApplication(sys.argv)
   app.setQuitOnLastWindowClosed(True)
   window = HashiSolverGui()
   window.show()
   sys.exit(app.exec())
   
if __name__ == '__main__':
   main()
