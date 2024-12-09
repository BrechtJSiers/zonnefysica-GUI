import sys

import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class AnotherWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        vbox = QtWidgets.QVBoxLayout(central_widget)

        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        hbox4 = QtWidgets.QHBoxLayout()
        hbox5 = QtWidgets.QHBoxLayout()
        hbox6 = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)

        self.pathA = QtWidgets.QPushButton("Choose pathA")
        self.pathB = QtWidgets.QPushButton("Choose pathB")
        self.choose_order = QtWidgets.QComboBox()
        self.choose_order.addItems(["3", "7", "13"])
        self.select = QtWidgets.QPushButton("Select")
        hbox1.addWidget(self.pathA)
        hbox1.addWidget(self.pathB)
        hbox1.addWidget(self.choose_order)
        hbox1.addWidget(self.select)

        self.saved = QtWidgets.QLabel("Saved")
        hbox2.addWidget(self.saved)

        self.determine = QtWidgets.QPushButton("Determine rotationperiod")
        hbox3.addWidget(self.determine)

        self.graph_rot = pg.PlotWidget()
        hbox4.addWidget(self.graph_rot)

        # self.value_1_line = QtWidgets.QPushButton("Calculated periods per line")
        # # give list with added points and values
        # hbox5.addWidget(self.value_1_line)

        self.give_answer = QtWidgets.QLabel("Mean value")
        hbox6.addWidget(self.give_answer)

        self.select.clicked.connect(self.input_order)
        self.pathA.clicked.connect(self.select_pathA)
        self.pathB.clicked.connect(self.select_pathB)

    def input_order(self):
        self.w = AnotherWindow()
        self.w.show()
        # pathA = self.filenameA
        # pathB = self.filenameB

    def select_pathA(self):
        self.filenameA = QtWidgets.QFileDialog.getExistingDirectory()
        print(self.filenameA)

    def select_pathB(self):
        self.filenameB = QtWidgets.QFileDialog.getExistingDirectory()
        print(self.filenameB)

    @Slot()
    def select_abs_line(self, order):
        print(order)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
