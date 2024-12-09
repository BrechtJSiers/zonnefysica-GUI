import sys

import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from scipy.optimize import curve_fit

from zonnefysica.model import fitscan, initial_scan

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class AnotherWindow(QtWidgets.QWidget):

    def __init__(self, order, periods_list, error_periods_list):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Another Window")
        vbox.addWidget(self.label)
        self.setLayout(vbox)
        self.periods_list = periods_list
        self.error_periods_list = error_periods_list
        self.order = order
        wavelength_object, _, _, _, _ = initial_scan(self.order)

        self.start_A = QtWidgets.QDoubleSpinBox()
        self.start_A.setMinimum(min(wavelength_object))
        self.start_A.setMaximum(max(wavelength_object))
        self.start_A.setSingleStep(0.01)
        self.stop_A = QtWidgets.QDoubleSpinBox()
        self.stop_A.setMinimum(min(wavelength_object))
        self.stop_A.setMaximum(max(wavelength_object))
        self.stop_A.setSingleStep(0.01)
        self.stop_A.setValue(max(wavelength_object))
        self.start_B = QtWidgets.QDoubleSpinBox()
        self.start_B.setMinimum(min(wavelength_object))
        self.start_B.setMaximum(max(wavelength_object))
        self.start_B.setSingleStep(0.01)
        self.stop_B = QtWidgets.QDoubleSpinBox()
        self.stop_B.setMinimum(min(wavelength_object))
        self.stop_B.setMaximum(max(wavelength_object))
        self.stop_B.setSingleStep(0.01)
        self.stop_B.setValue(max(wavelength_object))
        go_button = QtWidgets.QPushButton("start scan")

        vbox.addWidget(self.start_A)
        vbox.addWidget(self.stop_A)
        vbox.addWidget(self.start_B)
        vbox.addWidget(self.stop_B)
        vbox.addWidget(go_button)

        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)
        go_button.clicked.connect(self.scan_plot)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        save_button = QtWidgets.QPushButton("Save data")
        return_button = QtWidgets.QPushButton("Return")
        hbox.addWidget(return_button)
        hbox.addWidget(save_button)

        return_button.clicked.connect(self.close)
        save_button.clicked.connect(self.calculate)

    @Slot()
    def scan_plot(self):

        self.plot_widget.clear()
        self.plot_widget.addLegend()

        range_1_A = 6561.83
        range_2_A = 6563.63
        range_1_B = 6561.89
        range_2_B = 6563.68

        (
            popt_A,
            pcov_A,
            popt_B,
            pcov_B,
            fit_A_wavelength,
            fit_B_wavelength,
            normal_distribution,
        ) = fitscan(
            self.order,
            self.start_A.value(),
            self.stop_A.value(),
            self.start_B.value(),
            self.stop_B.value(),
        )
        wavelength_object, flux_object_norm_A, flux_object_norm_B, SNR_A, SNR_B = (
            initial_scan(self.order)
        )

        self.plot_widget.plot(
            wavelength_object,
            flux_object_norm_A,
            linewidth=1,
            pen="r",
            name="Dataset A",
        )
        self.plot_widget.plot(
            wavelength_object,
            flux_object_norm_B,
            linewidth=1,
            pen="b",
            name="Dataset B",
        )

        self.plot_widget.plot(
            fit_A_wavelength,
            (normal_distribution(fit_A_wavelength, popt_A[0], popt_A[1], popt_A[2])),
            name="Gaussian fitfunction A",
            pen="k",
        )
        self.plot_widget.plot(
            fit_B_wavelength,
            (normal_distribution(fit_B_wavelength, popt_B[0], popt_B[1], popt_B[2])),
            name="Gaussian fitfunction B",
            pen="g",
        )

        error_bars_A = pg.ErrorBarItem(
            x=np.array(wavelength_object),
            y=flux_object_norm_A,
            width=0,
            height=2 * flux_object_norm_A / SNR_A,
        )
        self.plot_widget.addItem(error_bars_A)
        error_bars_B = pg.ErrorBarItem(
            x=np.array(wavelength_object),
            y=flux_object_norm_B,
            width=0,
            height=2 * flux_object_norm_B / SNR_B,
        )
        self.plot_widget.addItem(error_bars_B)

        self.plot_widget.setRange(
            xRange=[self.start_A.value() - 0.5, self.stop_A.value() + 0.5]
        )
        self.plot_widget.setLabel("left", "Normalized intensity")
        self.plot_widget.setLabel("bottom", "Wavelength (Angstrom)")

    def calculate(self):
        popt_A, pcov_A, popt_B, pcov_B, _, _, _ = fitscan(
            self.order,
            self.start_A.value(),
            self.stop_A.value(),
            self.start_B.value(),
            self.stop_B.value(),
        )
        min_A = popt_A[1]
        min_B = popt_B[1]
        error_A = pcov_A[1][1]
        error_B = pcov_B[1][1]

        R = 696342000
        c = 299792458
        lambda_gem = (min_A + min_B) / 2
        delta_lambda = abs(lambda_gem - min_A)
        v = c * (delta_lambda / lambda_gem)
        T = ((2 * np.pi * R) / v) / (60 * 60 * 24)
        # print(f"{T} is de omlooptijd in dagen")

        error_T = (
            ((2 * np.pi * R / c) * ((2 * min_B * error_A) / ((min_A - min_B) ** 2)))
            ** 2
            + ((2 * np.pi * R / c) * ((2 * min_A * error_B) / ((min_B - min_A) ** 2)))
            ** 2
        ) ** (1 / 2) / (60 * 60 * 24)
        # print(f"{error_T} is de error van de omlooptijd in dagen")
        self.periods_list.append(T)
        self.error_periods_list.append(error_T)
        self.close()
        return self.periods_list, self.error_periods_list


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.periods_list = []
        self.error_periods_list = []
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

        self.select.clicked.connect(self.input)
        self.determine.clicked.connect(self.all_periods)
        self.select.clicked.connect(self.input_order)
        self.pathA.clicked.connect(self.select_pathA)
        self.pathB.clicked.connect(self.select_pathB)

    def input(self):
        self.order = int(self.choose_order.currentText())
        self.w = AnotherWindow(self.order, self.periods_list, self.error_periods_list)
        self.w.show()
        # print(order)

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

    def all_periods(self):
        self.periods_list, self.error_periods_list = self.w.calculate()
        number_of_lines = []
        for i in range(len(self.periods_list)):
            number_of_lines.append(i)
        line_list = []
        error_line = []

        def straight_line(x, p):
            return p

        popt_s, pcov_s = curve_fit(
            straight_line,
            number_of_lines,
            self.periods_list,
            p0=[25],
            sigma=self.error_periods_list,
        )
        print(popt_s[0], pcov_s[0][0])
        for i in range(len(number_of_lines)):
            line_list.append(popt_s[0])
            error_line.append(pcov_s[0][0])


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
