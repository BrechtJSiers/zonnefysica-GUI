import sys

import pyqtgraph as pg
from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from zonnefysica.GUI import UserInterface


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
