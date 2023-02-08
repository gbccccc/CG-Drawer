import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from pyqt5_plugins.examplebuttonplugin import QtGui

import cg_cli as cli


class MainWindow(QMainWindow):
    def __init__(self):
        from ui.MainWindow import Ui_MainWindow
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.horizontalHeader().setFixedHeight(40)
        self.ui.canvasWidget.prepareCanvas()


class CanvasWidget(QWidget):
    def __init__(self, superObject):
        super().__init__(superObject)
        self.canvas = None

    def prepareCanvas(self):
        self.canvas = cli.Canvas(self.width(), self.height(), "./")

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        ...

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        ...


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
