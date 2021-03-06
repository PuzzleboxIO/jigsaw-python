# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface/puzzlebox_jigsaw_interface_design-plugin_help.ui'
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
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
		Form.setSizePolicy(sizePolicy)
		Form.setFocusPolicy(QtCore.Qt.NoFocus)
		#self.verticalLayoutWidget = QtGui.QWidget(Form)
		self.verticalLayoutWidget = QtGui.QWidget()
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 641, 474))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setSpacing(0)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem)
		self.verticalLayoutFeedback = QtGui.QVBoxLayout()
		self.verticalLayoutFeedback.setContentsMargins(-1, -1, 6, -1)
		self.verticalLayoutFeedback.setObjectName("verticalLayoutFeedback")
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem1)
		self.labelPuzzleboxControlPanel = QtGui.QLabel(self.verticalLayoutWidget)
		self.labelPuzzleboxControlPanel.setText("")
		self.labelPuzzleboxControlPanel.setPixmap(QtGui.QPixmap("images/puzzlebox_logo.png"))
		self.labelPuzzleboxControlPanel.setScaledContents(False)
		self.labelPuzzleboxControlPanel.setAlignment(QtCore.Qt.AlignCenter)
		self.labelPuzzleboxControlPanel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
		self.labelPuzzleboxControlPanel.setObjectName("labelPuzzleboxControlPanel")
		self.horizontalLayout.addWidget(self.labelPuzzleboxControlPanel)
		self.textLabelTitlePuzzleboxJigsaw = QtGui.QLabel(self.verticalLayoutWidget)
		font = QtGui.QFont()
		font.setPointSize(14)
		self.textLabelTitlePuzzleboxJigsaw.setFont(font)
		self.textLabelTitlePuzzleboxJigsaw.setTextFormat(QtCore.Qt.AutoText)
		self.textLabelTitlePuzzleboxJigsaw.setWordWrap(False)
		self.textLabelTitlePuzzleboxJigsaw.setOpenExternalLinks(True)
		self.textLabelTitlePuzzleboxJigsaw.setObjectName("textLabelTitlePuzzleboxJigsaw")
		self.horizontalLayout.addWidget(self.textLabelTitlePuzzleboxJigsaw)
		spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem2)
		self.verticalLayoutFeedback.addLayout(self.horizontalLayout)
		self.labelWebsiteInformation = QtGui.QLabel(self.verticalLayoutWidget)
		self.labelWebsiteInformation.setObjectName("labelWebsiteInformation")
		self.verticalLayoutFeedback.addWidget(self.labelWebsiteInformation)
		self.labelWebsiteAddress = QtGui.QLabel(self.verticalLayoutWidget)
		self.labelWebsiteAddress.setAlignment(QtCore.Qt.AlignCenter)
		self.labelWebsiteAddress.setObjectName("labelWebsiteAddress")
		self.verticalLayoutFeedback.addWidget(self.labelWebsiteAddress)
		spacerItem3 = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		self.verticalLayoutFeedback.addItem(spacerItem3)
		self.line_4 = QtGui.QFrame(self.verticalLayoutWidget)
		self.line_4.setFrameShape(QtGui.QFrame.HLine)
		self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
		self.line_4.setObjectName("line_4")
		self.verticalLayoutFeedback.addWidget(self.line_4)
		spacerItem4 = QtGui.QSpacerItem(15, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		self.verticalLayoutFeedback.addItem(spacerItem4)
		self.labelSubmitFeedback = QtGui.QLabel(self.verticalLayoutWidget)
		self.labelSubmitFeedback.setAlignment(QtCore.Qt.AlignCenter)
		self.labelSubmitFeedback.setObjectName("labelSubmitFeedback")
		self.verticalLayoutFeedback.addWidget(self.labelSubmitFeedback)
		self.labelFeedbackDescription = QtGui.QLabel(self.verticalLayoutWidget)
		self.labelFeedbackDescription.setObjectName("labelFeedbackDescription")
		self.verticalLayoutFeedback.addWidget(self.labelFeedbackDescription)
		self.formLayout_3 = QtGui.QFormLayout()
		self.formLayout_3.setContentsMargins(-1, 6, -1, 6)
		self.formLayout_3.setVerticalSpacing(6)
		self.formLayout_3.setObjectName("formLayout_3")
		self.labelFeedbackName = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.labelFeedbackName.sizePolicy().hasHeightForWidth())
		self.labelFeedbackName.setSizePolicy(sizePolicy)
		self.labelFeedbackName.setAlignment(QtCore.Qt.AlignCenter)
		self.labelFeedbackName.setObjectName("labelFeedbackName")
		self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelFeedbackName)
		self.lineEditFeedbackName = QtGui.QLineEdit(self.verticalLayoutWidget)
		self.lineEditFeedbackName.setEnabled(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lineEditFeedbackName.sizePolicy().hasHeightForWidth())
		self.lineEditFeedbackName.setSizePolicy(sizePolicy)
		self.lineEditFeedbackName.setObjectName("lineEditFeedbackName")
		self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditFeedbackName)
		self.labelFeedbackEmail = QtGui.QLabel(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.labelFeedbackEmail.sizePolicy().hasHeightForWidth())
		self.labelFeedbackEmail.setSizePolicy(sizePolicy)
		self.labelFeedbackEmail.setAlignment(QtCore.Qt.AlignCenter)
		self.labelFeedbackEmail.setObjectName("labelFeedbackEmail")
		self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelFeedbackEmail)
		self.lineEditFeedbackEmail = QtGui.QLineEdit(self.verticalLayoutWidget)
		self.lineEditFeedbackEmail.setEnabled(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lineEditFeedbackEmail.sizePolicy().hasHeightForWidth())
		self.lineEditFeedbackEmail.setSizePolicy(sizePolicy)
		self.lineEditFeedbackEmail.setObjectName("lineEditFeedbackEmail")
		self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEditFeedbackEmail)
		self.verticalLayoutFeedback.addLayout(self.formLayout_3)
		self.textEditFeedback = QtGui.QTextEdit(self.verticalLayoutWidget)
		self.textEditFeedback.setEnabled(True)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.textEditFeedback.sizePolicy().hasHeightForWidth())
		self.textEditFeedback.setSizePolicy(sizePolicy)
		self.textEditFeedback.setObjectName("textEditFeedback")
		self.verticalLayoutFeedback.addWidget(self.textEditFeedback)
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setContentsMargins(-1, 6, -1, -1)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem5)
		self.pushButtonSendFeedback = QtGui.QPushButton(self.verticalLayoutWidget)
		self.pushButtonSendFeedback.setEnabled(True)
		self.pushButtonSendFeedback.setObjectName("pushButtonSendFeedback")
		self.horizontalLayout_2.addWidget(self.pushButtonSendFeedback)
		spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem6)
		self.verticalLayoutFeedback.addLayout(self.horizontalLayout_2)
		spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayoutFeedback.addItem(spacerItem7)
		self.horizontalLayout_3.addLayout(self.verticalLayoutFeedback)
		spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem8)
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setSpacing(6)
		self.verticalLayout_2.setContentsMargins(6, -1, 0, -1)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.webViewWebBrowser = QtWebKit.QWebView(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.webViewWebBrowser.sizePolicy().hasHeightForWidth())
		self.webViewWebBrowser.setSizePolicy(sizePolicy)
		self.webViewWebBrowser.setObjectName("webViewWebBrowser")
		self.verticalLayout_2.addWidget(self.webViewWebBrowser)
		self.horizontalLayoutStatusBar = QtGui.QHBoxLayout()
		self.horizontalLayoutStatusBar.setSpacing(6)
		self.horizontalLayoutStatusBar.setContentsMargins(0, -1, -1, -1)
		self.horizontalLayoutStatusBar.setObjectName("horizontalLayoutStatusBar")
		self.lineEditWebStatus = QtGui.QLineEdit(self.verticalLayoutWidget)
		self.lineEditWebStatus.setEnabled(False)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lineEditWebStatus.sizePolicy().hasHeightForWidth())
		self.lineEditWebStatus.setSizePolicy(sizePolicy)
		self.lineEditWebStatus.setObjectName("lineEditWebStatus")
		self.horizontalLayoutStatusBar.addWidget(self.lineEditWebStatus)
		self.progressBarWebProgress = QtGui.QProgressBar(self.verticalLayoutWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.progressBarWebProgress.sizePolicy().hasHeightForWidth())
		self.progressBarWebProgress.setSizePolicy(sizePolicy)
		self.progressBarWebProgress.setProperty("value", 0)
		self.progressBarWebProgress.setTextVisible(True)
		self.progressBarWebProgress.setObjectName("progressBarWebProgress")
		self.horizontalLayoutStatusBar.addWidget(self.progressBarWebProgress)
		self.verticalLayout_2.addLayout(self.horizontalLayoutStatusBar)
		self.horizontalLayout_3.addLayout(self.verticalLayout_2)
		self.verticalLayout.addLayout(self.horizontalLayout_3)

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
		self.textLabelTitlePuzzleboxJigsaw.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://jigsaw.puzzlebox.info\"><span style=\" font-size:11pt; font-weight:600; text-decoration: none; color:#000000;\">Puzzlebox<br />Jigsaw</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.labelWebsiteInformation.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For information and updates on</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">this software please visit:</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.labelWebsiteAddress.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://jigsaw.puzzlebox.info\"><span style=\"text-decoration: none; color:#000000;; color:#0000ff;\">http://jigsaw.puzzlebox.info</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.labelSubmitFeedback.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Submit Feedback</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.labelFeedbackDescription.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please use this form to submit your</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">comments, bug reports, and feature requests</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.labelFeedbackName.setText(QtGui.QApplication.translate("Form", "Name ", None, QtGui.QApplication.UnicodeUTF8))
		self.labelFeedbackEmail.setText(QtGui.QApplication.translate("Form", "Email ", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButtonSendFeedback.setText(QtGui.QApplication.translate("Form", "Send", None, QtGui.QApplication.UnicodeUTF8))
		self.lineEditWebStatus.setText(QtGui.QApplication.translate("Form", "Status: N/A", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
