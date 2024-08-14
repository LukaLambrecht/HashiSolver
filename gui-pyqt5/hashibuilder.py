import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLabel, QLineEdit

sys.path.append(os.path.abspath('../src'))
from hashi import Hashi
sys.path.append(os.path.abspath('../reader'))
from reader import HashiImageReader


class PickSizeWindow(QWidget):

    def __init__(self):
        super(PickSizeWindow, self).__init__()

        # todo: maybe replace QLineEdit with more dedicated
        #       widgets for choosing numbers in reasonable range.
        size_layout = QGridLayout()
        nrows_label = QLabel("Number of rows")
        size_layout.addWidget(nrows_label, 0, 0)
        self.nrows_edit = QLineEdit("5")
        size_layout.addWidget(self.nrows_edit, 0, 1)
        ncols_label = QLabel("Number of columns")
        size_layout.addWidget(ncols_label, 1, 0)
        self.ncols_edit = QLineEdit("5")
        size_layout.addWidget(self.ncols_edit, 1, 1)

        buttons_layout = QGridLayout()
        self.ok_button = QPushButton('Ok')
        buttons_layout.addWidget(self.ok_button, 0, 0)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.cancel)
        buttons_layout.addWidget(self.cancel_button, 0, 1)

        self.main_layout = QGridLayout()
        self.main_layout.addLayout(size_layout, 0, 0)
        self.main_layout.addLayout(buttons_layout, 1, 0)

        self.setLayout(self.main_layout)

    def cancel(self, event):
        self.close()


class HashiBuilderWindow(QWidget):
    
    def __init__(self):
        super(HashiBuilderWindow, self).__init__()

        (self.dgrid, self.dgrid_layout) = self.make_digit_grid()

        buttons_layout = QGridLayout()
        self.ok_button = QPushButton('Ok')
        buttons_layout.addWidget(self.ok_button, 0, 0)
        self.size_button = QPushButton('Change size')
        self.size_button.clicked.connect(self.open_change_size_window)
        buttons_layout.addWidget(self.size_button, 0, 1)
        self.image_button = QPushButton('Load from image')
        self.image_button.clicked.connect(self.choose_image)
        buttons_layout.addWidget(self.image_button, 0, 2)
        
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(self.dgrid_layout, 0, 0)
        self.main_layout.addLayout(buttons_layout, 1, 0)
        
        self.setLayout(self.main_layout)

    def make_digit_grid(self, nrows=7, ncols=7):
        dgrid_layout = QGridLayout()
        dgrid = []
        for i in range(nrows):
            dgrid.append([])
            for j in range(ncols):
                textbox = QLineEdit()
                dgrid[i].append(textbox)
                dgrid_layout.addWidget(textbox, i, j)
        return (dgrid, dgrid_layout)

    def closeEvent(self, event):
        event.accept()

    def make_hashi(self):
        hashistr = ''
        for i in range(len(self.dgrid)):
            for j in range(len(self.dgrid[i])):
                txt = self.dgrid[i][j].text()
                if( txt=='' or txt==' ' or txt=='\t' or txt=='-' ): hashistr += '-'
                else: hashistr += str(int(txt))
            hashistr += '\n'
        hashistr = hashistr.strip(' \t\n')
        hashi = Hashi.from_str(hashistr)
        return hashi

    def open_change_size_window(self, event):
        self.picksizewindow = PickSizeWindow()
        self.picksizewindow.ok_button.clicked.connect(self.get_size_params)
        self.picksizewindow.show()

    def get_size_params(self, event):
        nrows = int(self.picksizewindow.nrows_edit.text())
        ncols = int(self.picksizewindow.ncols_edit.text())
        self.picksizewindow.close()
        del self.picksizewindow
        self.change_size(nrows=nrows, ncols=ncols)

    def change_size(self, nrows=7, ncols=7):
        self.main_layout.removeItem(self.dgrid_layout)
        self.dgrid_layout.deleteLater()
        del self.dgrid_layout
        (self.dgrid, self.dgrid_layout) = self.make_digit_grid(nrows=nrows, ncols=ncols)
        self.main_layout.addLayout(self.dgrid_layout, 0, 0)
        self.main_layout.update()
        
    def choose_image(self, event):
        # choose file
        inputfile, _ = QFileDialog.getOpenFileName(self, 'Choose image', '../fls', '')
        if inputfile == '': return
        # read file into hashi vertices
        HIR = HashiImageReader()
        HIR.loadimage(inputfile)
        HIR.nrows = 11 # to make automatic / interactive
        HIR.ncols = 11 # to make automatic / interactive
        vertices = HIR.hashidict()
        # update interactive display
        self.change_size(nrows=HIR.nrows, ncols=HIR.ncols)
        for (xcoord,ycoord),n in vertices.items():
            xidx = HIR.nrows-1-ycoord
            yidx = xcoord
            self.dgrid[xidx][yidx].setText(str(n))
