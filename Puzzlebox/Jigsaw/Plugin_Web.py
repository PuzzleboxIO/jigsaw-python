#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Puzzlebox - Jigsaw - Plug-in - Web
#
# Copyright Puzzlebox Productions, LLC (2011-2012)

__changelog__ = """\
Last Update: 2012.06.22
"""

__todo__ = """
- Web status updates calling direction in plugin_session, should be via 
	plugin protocol handler (as is done for EEG packet updates)
"""

import os, sys, time
import urllib


import Puzzlebox.Jigsaw.Configuration as configuration

if configuration.ENABLE_PYSIDE:
	try:
		#import PySide as PyQt4
		from PySide import QtCore, QtGui, QtNetwork, QtWebKit
		try:
			from Puzzlebox.Jigsaw.Interface_JavaScript_PySide import puzzlebox_jigsaw_interface_javascript
		except:
			"print ERROR: [Jigsaw:Plugin_Web] Exception importing JavaScript module"
	except Exception, e:
		print "ERROR: Exception importing PySide:",
		print e
		configuration.ENABLE_PYSIDE = False
	else:
		print "INFO: [Jigsaw:Plugin_Web] Using PySide module"

if not configuration.ENABLE_PYSIDE:
	print "INFO: [Jigsaw:Plugin_Web] Using PyQt4 module"
	from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit
	try:
		from Puzzlebox.Jigsaw.Interface_JavaScript_PyQt import puzzlebox_jigsaw_interface_javascript
	except:
		"print ERROR: [Jigsaw:Plugin_Web] Exception importing JavaScript module"

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

from Puzzlebox.Jigsaw.Design_Plugin_Web import Ui_Form as Design

#import Puzzlebox.Jigsaw.Configuration as configuration
#import puzzlebox_logger


#####################################################################
# Globals
#####################################################################

DEBUG = 1

#DEFAULT_BROWSER_URL = 'http://brainstorms.puzzlebox.info'
DEFAULT_BROWSER_URL = configuration.DEFAULT_BROWSER_URL

BROWSER_JAVASCRIPT_ENABLED = configuration.BROWSER_JAVASCRIPT_ENABLED
BROWSER_PLUGINS_ENABLED = configuration.BROWSER_PLUGINS_ENABLED
BROWSER_PRIVATE_BROWSING_ENABLED = configuration.BROWSER_PRIVATE_BROWSING_ENABLED

DEFAULT_SCREENSHOT_FILE = os.path.join(os.getcwd(), "screenshot.png")


#####################################################################
# Classes
#####################################################################

class puzzlebox_jigsaw_plugin_web(QtGui.QWidget, Design):
	
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
		
		self.name = "Jigsaw-Plugin-Web"
		self.baseWidget = self.verticalLayoutWidget
		self.tabTitle = _fromUtf8("Web Browser")
		
		if self.tabIndex == None:
			self.parent.tabWidget.addTab(self.baseWidget, self.tabTitle)
		else:
			self.parent.tabWidget.insertTab(self.tabIndex, self.baseWidget, self.tabTitle)
		
		self.customDataHeaders = ['URL']
		self.protocolSupport = ['EEG']
		
		try:
			self.jigsawJavaScript = \
			   puzzlebox_jigsaw_interface_javascript( \
				   DEBUG=DEBUG, \
				   parent=self.parent)
		except:
			self.jigsawJavaScript = None
			print "JavaScript module not available"		
		
		self.firstLoad = True
	
	
	##################################################################
	
	def configureSettings(self):
		
		# Web Browser
		
		try:
			self.webViewWebBrowser.settings().globalSettings().setAttribute( \
			   QtWebKit.QWebSettings.WebAttribute.JavascriptEnabled, BROWSER_JAVASCRIPT_ENABLED)
		except Exception, e:
			if self.DEBUG:
				print "ERROR: Unable to set browser JavascriptEnabled attribute:"
				print e
		
		try:
			self.webViewWebBrowser.settings().globalSettings().setAttribute( \
			   QtWebKit.QWebSettings.WebAttribute.PluginsEnabled, BROWSER_PLUGINS_ENABLED)
		except Exception, e:
			if self.DEBUG:
				print "ERROR: Unable to set browser PluginsEnabled attribute:"
				print e
		
		try:
			self.webViewWebBrowser.settings().globalSettings().setAttribute( \
			   QtWebKit.QWebSettings.WebAttribute.PrivateBrowsingEnabled, BROWSER_PRIVATE_BROWSING_ENABLED)
		except Exception, e:
			if self.DEBUG:
				print "ERROR: Unable to set browser PrivateBrowsingEnabled attribute:"
				print e
		
		self.loadWebBrowserHome()
		
		self.parent.setProgressBarColor( \
			self.progressBarWebProgress, 'CFCDCB') # Grey
		
		#self.webViewWebBrowser.setMinimumSize(1024, 768)
		#self.webViewWebBrowser.setMaximumSize(1024, 768)
	
	
	##################################################################
	
	def connectWidgets(self):
		
		#self.connectWebControls()
		
		# Web Browser
		
		self.connect(self.pushButtonWebBack, \
		             QtCore.SIGNAL("clicked()"), \
		             self.webViewWebBrowser.back)
		self.connect(self.pushButtonWebForward, \
		             QtCore.SIGNAL("clicked()"), \
		             self.webViewWebBrowser.forward)
		self.connect(self.pushButtonWebStop, \
		             QtCore.SIGNAL("clicked()"), \
		             self.webViewWebBrowser.stop)
		self.connect(self.pushButtonWebReload, \
		             QtCore.SIGNAL("clicked()"), \
		             self.webViewWebBrowser.reload)
		
		self.connect(self.webViewWebBrowser, \
		             QtCore.SIGNAL("urlChanged(QUrl)"), \
		             self.urlChanged)
		
		self.connect(self.lineEditWebLocation, \
		             QtCore.SIGNAL("returnPressed()"), \
		             self.loadWebURL)
		
		self.connect(self.webViewWebBrowser, \
		             QtCore.SIGNAL("loadStarted(int)"), \
		             self.updateWebBrowserProgress)
		
		self.connect(self.webViewWebBrowser, \
		             QtCore.SIGNAL("loadProgress(int)"), \
		             self.updateWebBrowserProgress)
	
	
	##################################################################
	
	def updateEEGProcessingGUI(self):
		pass
	
	##def processPacketThinkGear(self, packet):
		##pass
	
	def processPacketEEG(self, packet):
		pass
	
	
	##################################################################
	
	def processCustomData(self, packet):
		
		if 'URL' in self.customDataHeaders:
			url = self.webViewWebBrowser.url()
			url = str(url.toString())
			url = url.replace(',', '%2C') # escape commas
			packet['custom']['URL'] = url
		
		
		return(packet)
	
	
	##################################################################
	
	def processPacketForExport(self, packet={}, output={}):
		
		return(output)
	
	
	##################################################################
	
	def loadWebURL(self, url=None):
		
		if url == None:
			url = self.lineEditWebLocation.text()
		
		url = str(url)
		
		if url == '':
			url = DEFAULT_BROWSER_URL
		
		if (not url.startswith('http://') and \
		    not url.startswith('https://') and \
		    not url.startswith('file://')):
			url = "http://%s" % url
		
		self.lineEditWebLocation.setText(url)
		
		#self.progressBarWebProgress.setEnabled(True)
		#self.setProgressBarColor( \
			#self.progressBarWebProgress, 'CFCDCB') # Grey
		self.updateWebBrowserProgress(progress=0)
		
		self.webViewWebBrowser.load( QtCore.QUrl(url) )
	
	
	##################################################################
	
	def loadWebBrowserHome(self):
		
		self.lineEditWebLocation.setText(DEFAULT_BROWSER_URL)
		#self.lineEditWebStatus.setText('Status: Connecting')
		self.loadWebURL(DEFAULT_BROWSER_URL)
	
	
	##################################################################
	
	def updateWebBrowserProgress(self, progress=0):
		
		self.progressBarWebProgress.setValue(progress)
		
		if progress == 100:
			#self.saveWebBrowserScreenshot()
			
			status = 'Status: Complete'
			#self.progressBarWebProgress.setEnabled(False)
			
			self.connectWebControls()
			
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
			status = 'Status: Connecting'
		
		else:
			status = 'Status: Loading'
		
		self.lineEditWebStatus.setText(status)
		if self.configuration.ENABLE_PLUGIN_SESSION:
			try:
				self.parent.plugin_session.labelSessionPluginWebStatus.setText(status)
			except Exception, e:
				if self.DEBUG:
					print "ERROR: Unable to labelSessionPluginWebStatus.setText:"
					print e
	
	
	##################################################################
	
	def connectWebControls(self):
		
		# Note: Example gathered from 
		#       http://stackoverflow.com/questions/6447011/pyqt-pyside-webkit-and-exposing-methods-from-to-javascript
		
		try:
			self.webViewWebBrowser.page().mainFrame().addToJavaScriptWindowObject( \
			   'jigsawJavaScript', \
			   self.jigsawJavaScript)
		except Exception, e:
			if self.DEBUG:
				print "ERROR: Unable to addToJavaScriptWindowObject inconnectWebControls:"
				print e
	
	
	##################################################################
	
	def urlChanged(self):
		
		url = self.webViewWebBrowser.url()
		url = url.toString()
		
		self.lineEditWebLocation.setText(url)
	
	
	##################################################################
	
	def saveWebBrowserScreenshot(self):
		
		pageSize = self.webViewWebBrowser.page().mainFrame().contentsSize()
		
		if self.DEBUG > 1:
			print pageSize
		
		# Paint this frame into an image
		screenshot = QtGui.QImage(pageSize, \
		                          QtGui.QImage.Format_ARGB32)
		painter = QtGui.QPainter(screenshot)
		self.webViewWebBrowser.page().mainFrame().render(painter)
		painter.end()
		
		
		if self.DEBUG:
			print "Saving screenshot: %s" % DEFAULT_SCREENSHOT_FILE
		
		screenshot.save(DEFAULT_SCREENSHOT_FILE)
	
	
	##################################################################
	
	def stop(self):
		
		pass


#####################################################################
#####################################################################

#class ConsolePrinter(QtCore.QObject):
	#def __init__(self, parent=None):
		#super(ConsolePrinter, self).__init__(parent)
	
	#@QtCore.pyqtSlot(str)
	#def text(self, message):
		#print message
	
	#@QtCore.Slot(str)
	#def text(self, message):
		#print message


#####################################################################
# Functions
#####################################################################

#####################################################################
# Main
#####################################################################

#if __name__ == '__main__':
	
	#pass

