# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface/puzzlebox_jigsaw_interface_design.ui'
#
# Created: Sun May 10 18:28:33 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
	def setupUi(self, Form):
		Form.setObjectName("Form")
#Form.resize()
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
		Form.setSizePolicy(sizePolicy)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("images/puzzlebox.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		Form.setWindowIcon(icon)
		self.gridLayout_2 = QtGui.QGridLayout(Form)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setSpacing(0)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.tabWidget = QtGui.QTabWidget(Form)
		self.tabWidget.setObjectName("tabWidget")
		self.tabMain = QtGui.QWidget()
		self.tabMain.setEnabled(True)
		self.tabMain.setObjectName("tabMain")
		self.tabWidget.addTab(self.tabMain, "")
		self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

		self.retranslateUi(Form)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtGui.QApplication.translate("Form", "Puzzlebox Jigsaw", None, QtGui.QApplication.UnicodeUTF8))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), QtGui.QApplication.translate("Form", "Puzzlebox Jigsaw", None, QtGui.QApplication.UnicodeUTF8))

