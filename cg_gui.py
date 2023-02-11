import sys
import threading
import traceback

from PIL import ImageQt
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QColorDialog, QInputDialog
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

        # connect slots and signals
        self.ui.actionClear.triggered.connect(self.ui.canvasWidget.resetCanvas)
        self.ui.actionColor.triggered.connect(self.ui.canvasWidget.selectColor)
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
        self.ui.actionBezier.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(-1, "Curve", self.ui.canvasWidget.canvas.addCurve, "Bezier")
        )
        self.ui.actionBSpline.triggered.connect(
            lambda: self.ui.canvasWidget.drawGraphic(-1, "Curve", self.ui.canvasWidget.canvas.addCurve, "B-spline")
        )
        self.ui.actionTranslate.triggered.connect(self.ui.canvasWidget.translate)
        self.ui.actionRotate.triggered.connect(self.ui.canvasWidget.rotate)
        self.ui.actionScale.triggered.connect(self.ui.canvasWidget.scale)
        self.ui.actionCohen_Sutherland.triggered.connect(
            lambda: self.ui.canvasWidget.clip("Cohen-Sutherland")
        )
        self.ui.actionLiang_Barsky.triggered.connect(
            lambda: self.ui.canvasWidget.clip("Liang-Barsky")
        )


class CanvasWidget(QWidget):
    def __init__(self, superObject):
        super().__init__(superObject)
        self.setMouseTracking(True)
        self.waitPointsThread = None
        self.canvas = None
        self.pointList = []
        self.currentPoint = (0, 0)
        self.pointsNeeded = -1

        self.tableWidget = self.parent().parent().ui.tableWidget

        self.isGetting = False
        self.isCancelling = False

    def prepareCanvas(self):
        self.canvas = cli.Canvas(self.width(), self.height(), "./")
        self.canvas.setColor((255, 255, 255))

    def resetCanvas(self):
        self.canvas.resetCanvas(self.width(), self.height())
        self.tableWidget.setRowCount(0)
        self.update()

    def selectColor(self):
        color = QColorDialog.getColor()
        self.canvas.setColor((color.red(), color.green(), color.blue()))

    def translate(self):
        gid = self.tableWidget.currentRow()
        if gid != -1:
            dx, success = QInputDialog.getInt(self, "Translate", "dx:")
            if not success:
                return
            dy, success = QInputDialog.getInt(self, "Translate", "dy:")
            if not success:
                return
            self.canvas.translate(gid, (dx, dy))

    def rotate(self):
        gid = self.tableWidget.currentRow()
        if gid != -1:
            x, success = QInputDialog.getInt(self, "Rotate", "x:")
            if not success:
                return
            y, success = QInputDialog.getInt(self, "Rotate", "y:")
            if not success:
                return
            degree, success = QInputDialog.getInt(self, "Rotate", "degree:")
            if not success:
                return
            try:
                self.canvas.rotate(gid, (x, y), degree)
            except Exception:
                traceback.print_exc()

    def scale(self):
        gid = self.tableWidget.currentRow()
        if gid != -1:
            x, success = QInputDialog.getInt(self, "Scale", "x:")
            if not success:
                return
            y, success = QInputDialog.getInt(self, "Scale", "y:")
            if not success:
                return
            times, success = QInputDialog.getDouble(self, "Scale", "times:")
            if not success:
                return
            self.canvas.scale(gid, (x, y), times)

    def clip(self, algorithm):
        self.setWaitPointsThread(self.ClipThread(self, algorithm))
        self.waitPointsThread.start()

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
            if len(self.pointList) == self.pointsNeeded:
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

    def drawGraphic(self, pointsNeeded, graphicType, drawFunction, algorithm):
        self.pointsNeeded = pointsNeeded
        self.pointList = []
        self.setWaitPointsThread(self.DrawThread(self, graphicType, pointsNeeded, drawFunction, algorithm))
        self.waitPointsThread.start()

    def setWaitPointsThread(self, waitPointsThread):
        if self.waitPointsThread is not None:
            self.isCancelling = True
            self.waitPointsThread.notify()
            self.waitPointsThread.join()
        self.waitPointsThread = waitPointsThread

    class WaitPointsThread(threading.Thread):
        def __init__(self, canvasWidget, pointsNeeded):
            super().__init__(daemon=True)
            self.canvasWidget = canvasWidget
            self.canvasWidget.pointsNeeded = pointsNeeded
            self.canvasWidget.pointList = []
            self.condition = threading.Condition()

        def wait(self):
            self.condition.wait()

        def notify(self):
            with self.condition:
                self.condition.notify()

        def run(self):
            self.canvasWidget.isGetting = True
            self.canvasWidget.isCancelling = False
            with self.condition:
                while True:
                    if self.canvasWidget.isCancelling:
                        self.onCanceling()
                        break
                    if self.canvasWidget.isGetting:
                        self.onGetting()
                        self.wait()
                    else:
                        self.onEnding()
                        break

        def onCanceling(self):
            self.canvasWidget.isGetting = False
            self.canvasWidget.waitPointListThread = None

        def onGetting(self):
            pass

        def onEnding(self):
            self.canvasWidget.isGetting = False
            self.canvasWidget.waitPointListThread = None

    class DrawThread(WaitPointsThread):
        def __init__(self, canvasWidget, graphicType, pointsNeeded, drawFunction, algorithm):
            super().__init__(canvasWidget, pointsNeeded)
            self.drawFunction = drawFunction
            self.graphicType = graphicType
            self.algorithm = algorithm

        def onGetting(self):
            tempPointList = self.canvasWidget.pointList.copy()
            tempPointList.append(self.canvasWidget.currentPoint)
            self.drawFunction(self.algorithm, -1, tempPointList)
            self.canvasWidget.update()

        def onEnding(self):
            super().onEnding()
            graphicCount = self.canvasWidget.tableWidget.rowCount()
            if self.drawFunction(self.algorithm, graphicCount, self.canvasWidget.pointList):
                self.canvasWidget.tableWidget.insertRow(graphicCount)
                self.canvasWidget.tableWidget.setItem(graphicCount, 0, QTableWidgetItem(str(graphicCount)))
                self.canvasWidget.tableWidget.setItem(graphicCount, 1, QTableWidgetItem(self.graphicType))
                self.canvasWidget.tableWidget.setItem(graphicCount, 2, QTableWidgetItem(self.algorithm))
                self.canvasWidget.update()
            self.canvasWidget.update()

    class ClipThread(WaitPointsThread):
        def __init__(self, canvasWidget, algorithm):
            super().__init__(canvasWidget, 2)
            self.algorithm = algorithm

        def onGetting(self):
            tempPointList = self.canvasWidget.pointList.copy()
            tempPointList.append(self.canvasWidget.currentPoint)
            self.canvasWidget.canvas.addRectangle("Bresenham", -1, tempPointList)
            self.canvasWidget.update()

        def onEnding(self):
            super().onEnding()
            gid = self.canvasWidget.tableWidget.currentRow()
            try:
                self.canvasWidget.canvas.clip(self.algorithm, gid, self.canvasWidget.pointList)
            except Exception:
                traceback.print_exc()
            self.canvasWidget.update()

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())
