import sys
import threading

from PIL import ImageQt
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem
from pyqt5_plugins.examplebutton import QtWidgets
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

        self.ui.actionDDA.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(2, "Line", self.ui.canvasWidget.canvas.addLine, "DDA")
        )
        self.ui.actionBresenham.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(2, "Line", self.ui.canvasWidget.canvas.addLine, "Bresenham")
        )
        self.ui.actionPolyDDA.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(-1, "Polygon", self.ui.canvasWidget.canvas.addPolygon, "DDA")
        )
        self.ui.actionPolyBresenham.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(-1, "Polygon", self.ui.canvasWidget.canvas.addPolygon, "Bresenham")
        )
        self.ui.actionMidpoint.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(2, "Ellipse", self.ui.canvasWidget.canvas.addEllipse, "Midpoint")
        )
        self.ui.actionMidpoint.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(-1, "Curve", self.ui.canvasWidget.canvas.addCurve, "Bezier")
        )
        self.ui.actionMidpoint.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(-1, "Curve", self.ui.canvasWidget.canvas.addCurve, "B-spline")
        )
        self.ui.actionClear.triggered.connect(self.ui.canvasWidget.resetCanvas)


class CanvasWidget(QWidget):
    def __init__(self, superObject):
        super().__init__(superObject)
        self.setMouseTracking(True)
        self.waitPointsThread = None
        self.canvas = None
        self.pointList = []
        self.currentPoint = (0, 0)
        self.pointsLimit = -1

        self.tableWidget = self.parent().parent().ui.tableWidget

        self.isGetting = False
        self.isCancelling = False

    def prepareCanvas(self):
        self.canvas = cli.Canvas(self.width(), self.height(), "./")
        self.canvas.setColor((105, 200, 200))

    def resetCanvas(self):
        self.canvas.resetCanvas(self.width(), self.height())
        self.tableWidget.setRowCount(0)
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent):
        if self.canvas is None:
            return
        painter = QPainter(self)
        painter.drawImage(0, 0, ImageQt.toqimage(self.canvas.getImage()))

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if not self.isGetting:
            return
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self.pointList.append((e.x(), e.y()))
            self.currentPoint = (e.x(), e.y())
            if len(self.pointList) == self.pointsLimit:
                self.endGettingPoints()
            else:
                # notify waiting thread
                self.waitPointsThread.notify()
        elif e.button() == QtCore.Qt.MouseButton.RightButton:
            self.endGettingPoints()

    def endGettingPoints(self):
        self.isGetting = False
        # notify waiting thread
        self.waitPointsThread.notify()

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if not self.isGetting:
            return

        self.currentPoint = (e.x(), e.y())
        # notify waiting thread
        self.waitPointsThread.notify()

    def notifyWaitPointListThread(self):
        while not self.waitPointsThread.isAlive():
            self.waitPointsThread.notify()

    def drawGraphic(self, pointsLimit, graphicType, drawFunction, algorithm):
        self.pointsLimit = pointsLimit
        self.pointList = []
        self.isGetting = True
        self.isCancelling = False
        self.waitPointsThread = self.DrawThread(self, graphicType, drawFunction, algorithm)
        self.waitPointsThread.start()

    class DrawThread(threading.Thread):
        def __init__(self, canvasWidget, graphicType, drawFunction, algorithm):
            super().__init__(daemon=True)
            self.canvasWidget = canvasWidget
            self.drawFunction = drawFunction
            self.graphicType = graphicType
            self.algorithm = algorithm
            self.condition = threading.Condition()

        def wait(self):
            self.condition.wait()

        def notify(self):
            with self.condition:
                self.condition.notify()

        def run(self):
            with self.condition:
                while True:
                    if self.canvasWidget.isCancelling:
                        self.canvasWidget.isGetting = False
                        self.canvasWidget.waitPointListThread = None
                        break
                    if self.canvasWidget.isGetting:
                        tempPointList = self.canvasWidget.pointList.copy()
                        tempPointList.append(self.canvasWidget.currentPoint)
                        self.drawFunction(self.algorithm, -1, tempPointList)
                        self.canvasWidget.update()
                        self.wait()
                    else:
                        graphicCount = self.canvasWidget.tableWidget.rowCount()
                        self.drawFunction(self.algorithm, graphicCount,
                                          self.canvasWidget.pointList)
                        self.canvasWidget.tableWidget.insertRow(graphicCount)
                        self.canvasWidget.tableWidget.setItem(graphicCount, 0, QTableWidgetItem(str(graphicCount)))
                        self.canvasWidget.tableWidget.setItem(graphicCount, 1, QTableWidgetItem(self.graphicType))
                        self.canvasWidget.tableWidget.setItem(graphicCount, 2, QTableWidgetItem(self.algorithm))
                        self.canvasWidget.update()
                        self.canvasWidget.isGetting = False
                        self.canvasWidget.waitPointListThread = None
                        break

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())
