import sys
import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import matplotlib.pyplot as plt 
from zonnefysica.model import fitscan
import numpy as np
from zonnefysica.GUI import UserInterface

# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        vbox = QtWidgets.QVBoxLayout(central_widget)

        start_A = QtWidgets.QDoubleSpinBox()
        stop_A = QtWidgets.QDoubleSpinBox()
        start_B = QtWidgets.QDoubleSpinBox()
        stop_B = QtWidgets.QDoubleSpinBox()
        go_button = QtWidgets.QPushButton('start scan')

        vbox.addWidget(start_A)
        vbox.addWidget(stop_A)
        vbox.addWidget(start_B)
        vbox.addWidget(stop_B)
        vbox.addWidget(go_button)
        
        self.plot_widget=pg.PlotWidget()
        vbox.addWidget(self.plot_widget)
        go_button.clicked.connect(self.scan_plot)

    @Slot()
    def scan_plot(self):

        self.plot_widget.clear()
        self.plot_widget.addLegend()

        range_1_A = 6561.83 
        range_2_A = 6563.63
        range_1_B = 6561.89 
        range_2_B = 6563.68 

        popt_A, pcov_A, popt_B, pcov_B, wavelength_object, flux_object_norm_A, flux_object_norm_B, SNR_A, SNR_B, fit_A_wavelength, fit_B_wavelength, normal_distribution = fitscan(order, range_1_A, range_2_A, range_1_B, range_2_B)
        self.plot_widget.plot(wavelength_object, flux_object_norm_A, linewidth=1, pen= 'r', name="Dataset A")
        self.plot_widget.plot(wavelength_object, flux_object_norm_B, linewidth=1, pen = 'b', name="Dataset B")


        self.plot_widget.plot(fit_A_wavelength, (normal_distribution(fit_A_wavelength, popt_A[0], popt_A[1], popt_A[2])), name='Gaussian fitfunction A', pen = 'k')
        self.plot_widget.plot(fit_B_wavelength, (normal_distribution(fit_B_wavelength, popt_B[0], popt_B[1], popt_B[2])), name='Gaussian fitfunction B', pen = 'g')

        error_bars_A = pg.ErrorBarItem(x=np.array(wavelength_object), y=flux_object_norm_A, width = 0, height=2 * flux_object_norm_A/SNR_A)
        self.plot_widget.addItem(error_bars_A)
        error_bars_B = pg.ErrorBarItem(x=np.array(wavelength_object), y=flux_object_norm_B, width = 0, height=2 * flux_object_norm_B/SNR_B)
        self.plot_widget.addItem(error_bars_B)

        self.plot_widget.setRange(xRange=[range_1_A - 0.5, range_2_A + 0.5])
        self.plot_widget.setLabel("left", "Normalized intensity")
        self.plot_widget.setLabel("bottom", "Wavelength (Angstrom)")






def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


order = UserInterface()
waarde = order.input()
print(int(waarde))


if __name__ == "__main__":
    main()
