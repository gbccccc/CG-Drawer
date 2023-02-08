# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from cg_gui import CanvasWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(530, 0, 271, 541))
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 541))
        self.tableWidget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(90)
        self.tableWidget.verticalHeader().setVisible(False)
        self.canvasWidget = CanvasWidget(self.centralwidget)
        self.canvasWidget.setGeometry(QtCore.QRect(-1, -1, 531, 541))
        self.canvasWidget.setObjectName("canvasWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuGraphic = QtWidgets.QMenu(self.menubar)
        self.menuGraphic.setObjectName("menuGraphic")
        self.menuLine = QtWidgets.QMenu(self.menuGraphic)
        self.menuLine.setObjectName("menuLine")
        self.menuPolygon = QtWidgets.QMenu(self.menuGraphic)
        self.menuPolygon.setObjectName("menuPolygon")
        self.menuEllipse = QtWidgets.QMenu(self.menuGraphic)
        self.menuEllipse.setObjectName("menuEllipse")
        self.menuCurve = QtWidgets.QMenu(self.menuGraphic)
        self.menuCurve.setObjectName("menuCurve")
        self.menuTransform = QtWidgets.QMenu(self.menubar)
        self.menuTransform.setObjectName("menuTransform")
        self.menuClip = QtWidgets.QMenu(self.menuTransform)
        self.menuClip.setObjectName("menuClip")
        self.menuDrawer = QtWidgets.QMenu(self.menubar)
        self.menuDrawer.setObjectName("menuDrawer")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionDDA = QtWidgets.QAction(MainWindow)
        self.actionDDA.setObjectName("actionDDA")
        self.actionBresenham = QtWidgets.QAction(MainWindow)
        self.actionBresenham.setObjectName("actionBresenham")
        self.actionPolyDDA = QtWidgets.QAction(MainWindow)
        self.actionPolyDDA.setObjectName("actionPolyDDA")
        self.actionPolyBresenham = QtWidgets.QAction(MainWindow)
        self.actionPolyBresenham.setObjectName("actionPolyBresenham")
        self.actionMidpoint = QtWidgets.QAction(MainWindow)
        self.actionMidpoint.setObjectName("actionMidpoint")
        self.actionBezier = QtWidgets.QAction(MainWindow)
        self.actionBezier.setObjectName("actionBezier")
        self.actionBSpline = QtWidgets.QAction(MainWindow)
        self.actionBSpline.setObjectName("actionBSpline")
        self.actionTranslate = QtWidgets.QAction(MainWindow)
        self.actionTranslate.setObjectName("actionTranslate")
        self.actionRotate = QtWidgets.QAction(MainWindow)
        self.actionRotate.setObjectName("actionRotate")
        self.actionScale = QtWidgets.QAction(MainWindow)
        self.actionScale.setObjectName("actionScale")
        self.actionLiang_Barsky = QtWidgets.QAction(MainWindow)
        self.actionLiang_Barsky.setObjectName("actionLiang_Barsky")
        self.actionCohen_Sutherland = QtWidgets.QAction(MainWindow)
        self.actionCohen_Sutherland.setObjectName("actionCohen_Sutherland")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.menuLine.addAction(self.actionDDA)
        self.menuLine.addAction(self.actionBresenham)
        self.menuPolygon.addAction(self.actionPolyDDA)
        self.menuPolygon.addAction(self.actionPolyBresenham)
        self.menuEllipse.addAction(self.actionMidpoint)
        self.menuCurve.addAction(self.actionBezier)
        self.menuCurve.addAction(self.actionBSpline)
        self.menuGraphic.addAction(self.menuLine.menuAction())
        self.menuGraphic.addAction(self.menuPolygon.menuAction())
        self.menuGraphic.addAction(self.menuEllipse.menuAction())
        self.menuGraphic.addAction(self.menuCurve.menuAction())
        self.menuClip.addAction(self.actionLiang_Barsky)
        self.menuClip.addAction(self.actionCohen_Sutherland)
        self.menuTransform.addAction(self.actionTranslate)
        self.menuTransform.addAction(self.actionRotate)
        self.menuTransform.addAction(self.actionScale)
        self.menuTransform.addAction(self.menuClip.menuAction())
        self.menuDrawer.addAction(self.actionClear)
        self.menubar.addAction(self.menuDrawer.menuAction())
        self.menubar.addAction(self.menuGraphic.menuAction())
        self.menubar.addAction(self.menuTransform.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Algorithm"))
        self.menuGraphic.setTitle(_translate("MainWindow", "Graphic"))
        self.menuLine.setTitle(_translate("MainWindow", "Line"))
        self.menuPolygon.setTitle(_translate("MainWindow", "Polygon"))
        self.menuEllipse.setTitle(_translate("MainWindow", "Ellipse"))
        self.menuCurve.setTitle(_translate("MainWindow", "Curve"))
        self.menuTransform.setTitle(_translate("MainWindow", "Transform"))
        self.menuClip.setTitle(_translate("MainWindow", "Clip"))
        self.menuDrawer.setTitle(_translate("MainWindow", "Drawer"))
        self.actionDDA.setText(_translate("MainWindow", "DDA"))
        self.actionBresenham.setText(_translate("MainWindow", "Bresenham"))
        self.actionPolyDDA.setText(_translate("MainWindow", "DDA"))
        self.actionPolyBresenham.setText(_translate("MainWindow", "Bresenham"))
        self.actionMidpoint.setText(_translate("MainWindow", "Midpoint"))
        self.actionBezier.setText(_translate("MainWindow", "Bezier"))
        self.actionBSpline.setText(_translate("MainWindow", "BSpline"))
        self.actionTranslate.setText(_translate("MainWindow", "Translate"))
        self.actionRotate.setText(_translate("MainWindow", "Rotate"))
        self.actionScale.setText(_translate("MainWindow", "Scale"))
        self.actionLiang_Barsky.setText(_translate("MainWindow", "Cohen-Sutherland"))
        self.actionCohen_Sutherland.setText(_translate("MainWindow", "Liang-Barsky"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
