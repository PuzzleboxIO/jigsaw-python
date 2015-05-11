#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Puzzlebox - Jigsaw - Web Edition - Interface
#
# Copyright Puzzlebox Productions, LLC (2011-2015)

__changelog__ = """\
Last Update: 2015.03.24
"""

__todo__ = """
- Jigsaw image display on session interface
- Session failing to save and export
- "Unable to start server" error message appearing when reconnecting to ThinkGear server
- tabWidget failing to respond to mouse clicks (index 0 only)
"""

import os, sys, time
import urllib


import Puzzlebox.Jigsaw.Configuration as configuration

if configuration.ENABLE_PYSIDE:
	try:
		#import PySide as PyQt4
		from PySide import QtCore, QtGui, QtNetwork
	except Exception, e:
		print "ERROR: Exception importing PySide:",
		print e
		configuration.ENABLE_PYSIDE = False
	else:
		print "INFO: [Jigsaw:Interface] Using PySide module"

if not configuration.ENABLE_PYSIDE:
	print "INFO: [Jigsaw:Interface] Using PyQt4 module"
	from PyQt4 import QtCore, QtGui, QtNetwork


if (sys.platform == 'win32'):
	DEFAULT_IMAGE_PATH = 'images'
	import _winreg as winreg
	import itertools
	import re
	import serial
elif (sys.platform == 'darwin'):
	DEFAULT_IMAGE_PATH = 'images'
	#DEFAULT_IMAGE_PATH = '/usr/share/puzzlebox_jigsaw/images'
else:
	DEFAULT_IMAGE_PATH = '/usr/share/puzzlebox_jigsaw/images'
	import bluetooth
	#os.chdir('/usr/share/puzzlebox_jigsaw')


from Design_Interface import Ui_Form as Design

import simplejson as json

##import puzzlebox_logger
import Puzzlebox.Jigsaw.Plugin_Help as Plugin_Help
if configuration.ENABLE_PLUGIN_SESSION:
	import Puzzlebox.Jigsaw.Plugin_Session as Plugin_Session
if configuration.ENABLE_PLUGIN_EEG:
	import Puzzlebox.Jigsaw.Plugin_Eeg as Plugin_Eeg
if configuration.ENABLE_PLUGIN_WEB_BROWSER:
	import Puzzlebox.Jigsaw.Plugin_Web as Plugin_Web
if configuration.ENABLE_PLUGIN_BLOOM:
	import Puzzlebox.Bloom.Plugin_Bloom as Plugin_Bloom
if configuration.ENABLE_PLUGIN_ORBIT:
	import Puzzlebox.Orbit.Plugin_Orbit as Plugin_Orbit
if configuration.ENABLE_PLUGIN_BLENDER:
	import Puzzlebox.Jigsaw.Plugin_Blender as Plugin_Blender
if configuration.ENABLE_PLUGIN_TRENDS:
	import Puzzlebox.Jigsaw.Plugin_Trends as Plugin_Trends
if configuration.ENABLE_PLUGIN_BRAINSTORMS:
	import Puzzlebox.Jigsaw.Plugin_Brainstorms as Plugin_Brainstorms
if configuration.ENABLE_PLUGIN_ALGORITHMS:
	import Puzzlebox.Jigsaw.Plugin_Algorithms as Plugin_Algorithms
if configuration.ENABLE_PLUGIN_F1:
	import Puzzlebox.Jigsaw.Plugin_F1 as Plugin_F1


#####################################################################
# Globals
#####################################################################

DEBUG = 1

#####################################################################
# Classes
#####################################################################

class puzzlebox_jigsaw_interface(QtGui.QWidget, Design):
	
	def __init__(self, log, server=None, DEBUG=DEBUG, parent=None):
		
		self.log = log
		self.DEBUG = DEBUG
		
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.icon = None
		
		self.configuration = configuration
		
		self.configureSettings()
		self.connectWidgets()
		
		self.name = "Jigsaw:Interface"
		
		self.activePlugins = []
		self.configurePlugins()
		
		self.customDataHeaders = []
	
	
	##################################################################
	
	def configureSettings(self):
		
		# Jigsaw Interface
		
		image_path = "puzzlebox.ico"
		if not os.path.exists(image_path):
			image_path = os.path.join(DEFAULT_IMAGE_PATH, image_path)
		
		if os.path.exists(image_path):
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(image_path), \
				            QtGui.QIcon.Normal, \
				            QtGui.QIcon.Off)
			self.icon = icon
			self.setWindowIcon(icon)
		
		
		#Resize window to minimum size
		if self.configuration.INTERFACE_WINDOW_SHRINK:
			self.resize(0,0)
		
		if self.configuration.INTERFACE_WINDOW_POSITION != None:
			self.move(self.configuration.INTERFACE_WINDOW_POSITION[0], \
			          self.configuration.INTERFACE_WINDOW_POSITION[1])
	
	
	##################################################################
	
	def connectWidgets(self):
		
		# Keyboard Shortcuts
		
		#action = QtGui.QAction(self)
		#action.setShortcut(QtGui.QKeySequence("Home"))
		#self.connect(action, QtCore.SIGNAL("activated()"), self.loadWebBrowserHome)
		#self.addAction(action)
		
		#action = QtGui.QAction(self)
		#action.setShortcut(QtGui.QKeySequence("Up"))
		#self.connect(action, QtCore.SIGNAL("activated()"), self.pushButtonControlForwards, QtCore.SLOT("animateClick()"))
		#self.addAction(action)
		
		#action = QtGui.QAction(self)
		#action.setShortcut(QtGui.QKeySequence("Down"))
		#self.connect(action, QtCore.SIGNAL("activated()"), self.pushButtonControlBackwards, QtCore.SLOT("animateClick()"))
		#self.addAction(action)
		
		#action = QtGui.QAction(self)
		#action.setShortcut(QtGui.QKeySequence("Left"))
		#self.connect(action, QtCore.SIGNAL("activated()"), self.pushButtonControlLeft, QtCore.SLOT("animateClick()"))
		#self.addAction(action)
		
		#action = QtGui.QAction(self)
		#action.setShortcut(QtGui.QKeySequence("Right"))
		#self.connect(action, QtCore.SIGNAL("activated()"), self.pushButtonControlRight, QtCore.SLOT("animateClick()"))
		#self.addAction(action)
		
		#action = QtGui.QAction(self)
		#action.setShortcut(QtGui.QKeySequence("End"))
		#self.connect(action, QtCore.SIGNAL("activated()"), self.pushButtonControlMagnetOff, QtCore.SLOT("animateClick()"))
		#self.addAction(action)
		
		
		# Debug
		#self.pushButtonControlForwards.setAutoRepeat(False)
		#self.pushButtonControlForwards.setAutoRepeatDelay(0)
		#self.pushButtonControlForwards.setAutoRepeatInterval(0)
		
		
		pass
	
	
	##################################################################
	
	def configurePlugins(self):
		
		
		if self.configuration.ENABLE_PLUGIN_SESSION:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_session = Plugin_Session.puzzlebox_jigsaw_plugin_session( \
			                     self.log, \
			                     tabIndex=tabIndex, \
			                     DEBUG=self.DEBUG, \
			                     parent=self)
			
			self.activePlugins.append(self.plugin_session)
		
		
		if self.configuration.ENABLE_PLUGIN_EEG:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_eeg = Plugin_Eeg.puzzlebox_jigsaw_plugin_eeg( \
			                     self.log, \
			                     tabIndex=tabIndex, \
			                     DEBUG=self.DEBUG, \
			                     parent=self)
			
			self.activePlugins.append(self.plugin_eeg)
		
		
		if self.configuration.ENABLE_PLUGIN_ORBIT:
			
			# Re-import in order to work around namespace issue
			import Puzzlebox.Orbit.Plugin_Orbit as Plugin_Orbit
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_orbit = Plugin_Orbit.puzzlebox_jigsaw_plugin_orbit( \
			                         self.log, \
			                         tabIndex=tabIndex, \
			                         DEBUG=self.DEBUG, \
			                         parent=self)
			
			self.activePlugins.append(self.plugin_orbit)
		
		
		if self.configuration.ENABLE_PLUGIN_BLOOM:
			
			# Re-import in order to work around namespace issue
			import Puzzlebox.Bloom.Plugin_Bloom as Plugin_Bloom
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_bloom = Plugin_Bloom.puzzlebox_jigsaw_plugin_bloom( \
			                         self.log, \
			                         tabIndex=tabIndex, \
			                         DEBUG=self.DEBUG, \
			                         parent=self)
			
			self.activePlugins.append(self.plugin_bloom)
		
		
		if self.configuration.ENABLE_PLUGIN_BRAINSTORMS:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_brainstorms = Plugin_Brainstorms.puzzlebox_jigsaw_plugin_brainstorms( \
			                         self.log, \
			                         tabIndex=tabIndex, \
			                         DEBUG=self.DEBUG, \
			                         parent=self)
			
			self.activePlugins.append(self.plugin_brainstorms)
		
		
		if self.configuration.ENABLE_PLUGIN_WEB_BROWSER:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_web = Plugin_Web.puzzlebox_jigsaw_plugin_web( \
			                     self.log, \
			                     tabIndex=tabIndex, \
			                     DEBUG=self.DEBUG, \
			                     parent=self)
			
			self.activePlugins.append(self.plugin_web)
		
		
		if self.configuration.ENABLE_PLUGIN_BLENDER:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_blender = Plugin_Blender.puzzlebox_jigsaw_plugin_blender( \
			                         self.log, \
			                         tabIndex=tabIndex, \
			                         DEBUG=self.DEBUG, \
			                         parent=self)
			
			self.activePlugins.append(self.plugin_blender)
		
		
		if self.configuration.ENABLE_PLUGIN_TRENDS:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_trends = Plugin_Trends.puzzlebox_jigsaw_plugin_trends( \
			                         self.log, \
			                         tabIndex=tabIndex, \
			                         DEBUG=self.DEBUG, \
			                         parent=self)
			
			self.activePlugins.append(self.plugin_trends)
		
		
		if self.configuration.ENABLE_PLUGIN_ALGORITHMS:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_algorithms = Plugin_Algorithms.puzzlebox_jigsaw_plugin_algorithms( \
			                         self.log, \
			                         tabIndex=tabIndex, \
			                         DEBUG=self.DEBUG, \
			                         parent=self)
			
			self.activePlugins.append(self.plugin_algorithms)
		
		
		if self.configuration.ENABLE_PLUGIN_F1:
			
			tabIndex = len(self.activePlugins) + 1
			
			self.plugin_f1 = Plugin_F1.puzzlebox_jigsaw_plugin_f1( \
			                         self.log, \
			                         tabIndex=tabIndex, \
			                         DEBUG=self.DEBUG, \
			                         parent=self)
			
			self.activePlugins.append(self.plugin_f1)
		
		
		if self.configuration.ENABLE_PLUGIN_HELP:
			
			tabIndex = len(self.activePlugins) + 1
			#tabIndex = None
			
			self.plugin_help = Plugin_Help.puzzlebox_jigsaw_plugin_help( \
			                     self.log, \
			                     tabIndex=tabIndex, \
			                     DEBUG=self.DEBUG, \
			                     parent=self)
			
			self.activePlugins.append(self.plugin_help)
		
		
		if self.configuration.ENABLE_PLUGIN_SESSION:
			
			# Session Plugin was already created and added to the interface
			# but we re-append it to the list of plugins last so that custom
			# data which is collected through it end up last when exported
			# to CSV
			self.activePlugins.remove(self.plugin_session)
			self.activePlugins.append(self.plugin_session)
		
		
		if self.configuration.ENABLE_PLUGIN_ORBIT:
			
			# Orbit Plugin was already created and added to interface
			# but we want to update certain other portions of the interface
			# which are loaded later (such as the Help page)
			self.plugin_orbit.updateOrbitInterface()
		
		
		if self.configuration.ENABLE_PLUGIN_BLOOM:
			
			# Bloom Plugin was already created and added to interface
			# but we want to update certain other portions of the interface
			# which are loaded later (such as the Help page)
			self.plugin_bloom.updateBloomInterface()

		
		self.tabWidget.setTabEnabled(0, False)
		self.tabWidget.setCurrentIndex(1)
	
	
	##################################################################
	
	def setProgressBarColor(self, progressBar, color):
		
		progressBar.setStyleSheet(" QProgressBar {\n"
		"     border: 1px solid grey;\n"
		"     border-radius: 2px;\n"
		"     text-align: center;\n"
		" } \n"
		"QProgressBar::chunk {\n"
		"     background-color: #%s;\n"
		" }" % color)
	
	
	###################################################################
	
	def stop(self):
		
		for plugin in self.activePlugins:
			try:
				plugin.stop()
			except Exception, e:
				if self.DEBUG:
					print "ERROR: [Jigsaw:Interface] Exception calling %s.stop():" % plugin.name,
					print e
	
	
	##################################################################
	
	def closeEvent(self, event):
		
		quit_message = "Are you sure you want to exit the program?"
		
		reply = QtGui.QMessageBox.question( \
		           self, \
		          'Quit Puzzlebox Jigsaw', \
		           quit_message, \
		           QtGui.QMessageBox.Yes, \
		           QtGui.QMessageBox.No)
		
		if reply == QtGui.QMessageBox.Yes:
			
			self.stop()
			
			event.accept()
		
		else:
			event.ignore()


#####################################################################
# Functions
#####################################################################

#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
	
	#log = puzzlebox_logger.puzzlebox_logger(logfile='client_interface')
	log = None
	
	app = QtGui.QApplication(sys.argv)
	
	window = puzzlebox_jigsaw_interface(log, DEBUG)
	window.show()
	
	sys.exit(app.exec_())

