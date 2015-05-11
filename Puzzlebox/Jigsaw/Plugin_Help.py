#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Puzzlebox - Jigsaw - Plug-in - Help
#
# Copyright Puzzlebox Productions, LLC (2011-2012)

__changelog__ = """\
Last Update: 2012.04.01
"""

__todo__ = """
"""

import os, sys, time
import urllib


import Puzzlebox.Jigsaw.Configuration as configuration

if configuration.ENABLE_PYSIDE:
	try:
		#import PySide as PyQt4
		from PySide import QtCore, QtGui, QtNetwork, QtWebKit
	except Exception, e:
		print "ERROR: Exception importing PySide:",
		print e
		configuration.ENABLE_PYSIDE = False
	else:
		print "INFO: [Jigsaw:Plugin_Help] Using PySide module"

if not configuration.ENABLE_PYSIDE:
	print "INFO: [Jigsaw:Plugin_Help] Using PyQt4 module"
	from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit


if (sys.platform == 'win32'):
	DEFAULT_IMAGE_PATH = 'images'
elif (sys.platform == 'darwin'):
	DEFAULT_IMAGE_PATH = 'images'
else:
	DEFAULT_IMAGE_PATH = '/usr/share/puzzlebox_jigsaw/images'

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	_fromUtf8 = lambda s: s

from Puzzlebox.Jigsaw.Design_Plugin_Help import Ui_Form as Design

#import Puzzlebox.Jigsaw.Configuration as configuration
#import puzzlebox_logger


#####################################################################
# Globals
#####################################################################

DEBUG = 1

PUZZLEBOX_FEEDBACK_URL = configuration.PUZZLEBOX_FEEDBACK_URL

DEFAULT_HELP_URL = configuration.DEFAULT_HELP_URL

#####################################################################
# Classes
#####################################################################

class puzzlebox_jigsaw_plugin_help(QtGui.QWidget, Design):
	
	def __init__(self, log, tabIndex=None, DEBUG=DEBUG, parent=None):
		
		self.log = log
		self.DEBUG = DEBUG
		self.parent = parent
		self.tabIndex = tabIndex
		
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		
		self.configuration = configuration
		
		self.configureSettings()
		self.connectWidgets()
		
		self.name = "Jigsaw-Plugin-Help"
		self.baseWidget = self.verticalLayoutWidget
		self.tabTitle = _fromUtf8("Help")
		
		if self.tabIndex == None:
			self.parent.tabWidget.addTab(self.baseWidget, self.tabTitle)
		else:
			self.parent.tabWidget.insertTab(self.tabIndex, self.baseWidget, self.tabTitle)
		
		self.customDataHeaders = []
		self.protocolSupport = []
		
		self.firstLoad = True
	
	
	##################################################################
	
	def configureSettings(self):
		
		self.loadWebURL(DEFAULT_HELP_URL)
		
		self.parent.setProgressBarColor( \
		   self.progressBarWebProgress, 'CFCDCB') # Grey
	
	
	##################################################################
	
	def connectWidgets(self):
		
		self.connect(self.pushButtonSendFeedback, \
		             QtCore.SIGNAL("clicked()"), \
		             self.sendFeedback)
		
		
		self.connect(self.webViewWebBrowser, \
		             QtCore.SIGNAL("loadStarted(int)"), \
		             self.updateWebBrowserProgress)
		
		self.connect(self.webViewWebBrowser, \
		             QtCore.SIGNAL("loadProgress(int)"), \
		             self.updateWebBrowserProgress)
	
	
	##################################################################
	
	#def updateEEGProcessingGUI(self):
		#pass
	
	##def processPacketThinkGear(self, packet):
		##pass
	#def processPacketEEG(self, packet):
		#pass
	
	#def disconnectFromThinkGearHost(self):
		#pass
	
	
	##################################################################
	
	def processCustomData(self, packet):
		
		#if 'URL' in self.customDataHeaders:
			#url = self.webViewWebBrowser.url()
			#url = str(url.toString())
			#url = url.replace(',', '%2C') # escape commas
			#packet['custom']['URL'] = url
		
		
		return(packet)
	
	
	##################################################################
	
	def sendFeedback(self):
		
		values = {}
		
		values['name'] = str(self.lineEditFeedbackName.text())
		values['email'] = str(self.lineEditFeedbackEmail.text())
		values['comment'] = str(self.textEditFeedback.toPlainText())
		
		values['subject'] = '[jigsaw feedback]'
		values['capcha_contact'] = 'brainstorms'
		
		
		url_data = urllib.urlencode(values)
		
		try:
			page = urllib.urlopen(PUZZLEBOX_FEEDBACK_URL, url_data)
			
			reply = QtGui.QMessageBox.information( \
		              self.parent, \
		              u'Feedback Sent', \
		              u'Thank you for your feedback', \
		              QtGui.QMessageBox.Ok)
			
			self.lineEditFeedbackName.setText('')
			self.lineEditFeedbackEmail.setText('')
			self.textEditFeedback.setText('')
		
		except:
			reply = QtGui.QMessageBox.information( \
		              self.parent, \
		              u'Feedback Error', \
		              u'We\'re sorry but there was an error submitting your feedback.\nPlease email contact@puzzlebox.info instead.', \
		              QtGui.QMessageBox.Ok)
	
	
	##################################################################
	
	def loadWebURL(self, url=None):
		
		if url == None:
			url = self.lineEditWebLocation.text()
		
		url = str(url)
		
		if url == '':
			url = DEFAULT_BROWSER_URL
		
		if (url.startswith('path://')):
			url = "file://" + os.path.join( os.getcwd(), url.split('path://')[1] )
		
		if (not url.startswith('http://') and \
		    not url.startswith('https://') and \
		    not url.startswith('file://')):
			url = "http://%s" % url
		
		if (sys.platform == 'win32'):
			url = url.replace('file://', '')
		
		
		self.progressBarWebProgress.setEnabled(True)
		self.updateWebBrowserProgress(progress=0)
		
		
		if self.DEBUG:
			print "[Jigsaw:Plugin_Help] loadWebURL:",
			print url
		
		self.webViewWebBrowser.load( QtCore.QUrl(url) )
	
	
	##################################################################
	
	def updateWebBrowserProgress(self, progress=0):
		
		self.progressBarWebProgress.setValue(progress)
		
		if progress == 100:
			status = 'Online Help: Ready'
			
			if self.firstLoad:
				# Make sure browser scrolls to top of first page when app is first launched
				scrollPoint = QtCore.QPoint(0,0)
				try:
					self.webViewWebBrowser.page().mainFrame().setScrollPosition(scrollPoint)
				except Exception, e:
					if self.DEBUG:
						print "ERROR: Unable to setScrollPosition:"
						print e
				self.firstLoad = False
		
		elif progress == 0:
			status = 'Online Help: Connecting'
		
		else:
			status = 'Online Help: Loading'
		
		
		try:
			self.lineEditWebStatus.setText(status)
		except Exception, e:
			if self.DEBUG:
				print "ERROR: Unable to lineEditWebStatus.setText:"
				print e
	
	
	##################################################################
	
	def stop(self):
		
		pass


#####################################################################
# Functions
#####################################################################

#####################################################################
# Main
#####################################################################

#if __name__ == '__main__':
	
	#pass

