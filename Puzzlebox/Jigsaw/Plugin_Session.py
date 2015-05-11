#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Puzzlebox - Jigsaw - Plug-in - Session
#
# Copyright Puzzlebox Productions, LLC (2011-2015)

__changelog__ = """
Last Update: 2015.05.10
"""

__todo__ = """
- ERROR: Failing to save to Synapse format under Jigsaw (program hangs)
- Enable/Disable 
- Configure one-second timer thread if EEG is not source for data
"""

import os, sys, time
import urllib

import Puzzlebox.Jigsaw.Configuration as configuration

configuration.JSON_AVAILABLE = False

if configuration.ENABLE_PYSIDE:
	try:
		from PySide import QtCore, QtGui, QtNetwork
	except Exception, e:
		print "ERROR: Exception importing PySide:",
		print e
		configuration.ENABLE_PYSIDE = False
	else:
		print "INFO: [Jigsaw:Plugin_Session] Using PySide module"

if not configuration.ENABLE_PYSIDE:
	print "INFO: [Jigsaw:Plugin_Session] Using PyQt4 module"
	from PyQt4 import QtCore, QtGui, QtNetwork


if (sys.platform == 'win32'):
	DEFAULT_IMAGE_PATH = 'images'
	import _winreg as winreg
	import itertools
	import re
	import serial
elif (sys.platform == 'darwin'):
	DEFAULT_IMAGE_PATH = 'images'
else:
	DEFAULT_IMAGE_PATH = '/usr/share/puzzlebox_jigsaw/images'
	import bluetooth
	#os.chdir('/usr/share/puzzlebox_jigsaw')

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	_fromUtf8 = lambda s: s

from Puzzlebox.Jigsaw.Design_Plugin_Session import Ui_Form as Design

try:
	import Puzzlebox.Jigsaw.Service_JSON as service_json
except:
	print "WARN: [Jigsaw:Plugin_Session] JSON Service not available"
else:
	configuration.JSON_AVAILABLE = True


#####################################################################
# Globals
#####################################################################

DEBUG = 1

SESSION_JSON_HOST = configuration.SESSION_JSON_HOST
SESSION_JSON_PORT = configuration.SESSION_JSON_PORT

#####################################################################
# Classes
#####################################################################

class puzzlebox_jigsaw_plugin_session(QtGui.QWidget, Design):
	
	def __init__(self, log, tabIndex=None, DEBUG=DEBUG, parent=None):
		
		self.log = log
		self.DEBUG = DEBUG
		self.parent = parent
		self.tabIndex = tabIndex
		
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		
		#self.configuration = configuration
		self.configuration = self.parent.configuration
		
		self.configureSettings()
		self.connectWidgets()
		
		self.name = "Jigsaw:Plugin:Session"
		self.baseWidget = self.verticalLayoutWidget
		self.tabTitle = _fromUtf8("Session")
		
		if self.tabIndex == None:
			self.parent.tabWidget.addTab(self.baseWidget, self.tabTitle)
		else:
			self.parent.tabWidget.insertTab(self.tabIndex, self.baseWidget, self.tabTitle)
		
		self.customDataHeaders = []
		self.customData = {}
		self.protocolSupport = ['EEG']
		
		self.session_start_timestamp = time.time()
		#self.packet_count = 0
		#self.bad_packets = 0
		
		self.serviceJSON = None
	
	
	##################################################################
	
	def configureSettings(self):
		
		if (sys.platform == 'win32'):
			self.homepath = os.path.join( \
			   os.environ['HOMEDRIVE'], \
			   os.environ['HOMEPATH'], \
			   'Desktop')
		elif (sys.platform == 'darwin'):
			desktop = os.path.join(os.environ['HOME'], 'Documents')
			if os.path.exists(desktop):
				self.homepath = desktop
			else:
				self.homepath = os.environ['HOME']
		else:
			desktop = os.path.join(os.environ['HOME'], 'Desktop')
			if os.path.exists(desktop):
				self.homepath = desktop
			else:
				self.homepath = os.environ['HOME']
		
		if not os.path.exists(self.homepath):
			if self.DEBUG:
				print "DEBUG: User default path not found"
			self.homepath = os.getcwd()
		
		
		# Remove Session Time
		self.lineSessionData.setVisible(False)
		self.labelSessionProfileData.setVisible(False)
		#self.formLayoutSessionData.setVisible(False)
		self.textLabelSessionTimeTitle.setVisible(False)
		self.textLabelSessionTime.setVisible(False)
		
		
		# JSON Service
		self.lineEditJSONHost.setText(SESSION_JSON_HOST)
		self.lineEditJSONPort.setText('%i' % SESSION_JSON_PORT)
		
		self.lineEditJSONHost.setVisible(False)
		self.lineEditJSONPort.setVisible(False)
		self.textLabelJSONHost.setVisible(False)
		self.textLabelJSONPort.setVisible(False)
		self.pushButtonSessionJSON.setVisible(False)
		
		
		no_plugins_enabled = True
		
		if self.configuration.ENABLE_PLUGIN_EEG:
			no_plugins_enabled = False
		else:
			try:
				self.labelSessionPluginEEG.setVisible(False)
				self.labelSessionPluginEEGStatus.setVisible(False)
				self.formLayoutSessionPluginEEG.setVisible(False)
				self.textLabelConnectionTime.setVisible(False)
				self.textLabelConnectionTimeTitle.setVisible(False)
				self.textLabelPacketsReceived.setVisible(False)
				self.textLabelPacketsReceivedTitle.setVisible(False)
				self.textLabelPacketsDropped.setVisible(False)
				self.textLabelPacketsDroppedTitle.setVisible(False)
				self.lineSessionPluginEEG.setVisible(False)
			except:
				pass
		
		
		if self.configuration.ENABLE_PLUGIN_WEB_BROWSER:
			no_plugins_enabled = False
		else:
			self.labelSessionPluginWeb.setVisible(False)
			self.labelSessionPluginWebStatus.setVisible(False)
		
		
		if not no_plugins_enabled:
			self.labelSessionPluginNone.setVisible(False)
			self.lineSessionPluginNone.setVisible(False)
	
	
	##################################################################
	
	def connectWidgets(self):
		
		self.connect(self.pushButtonSessionSave, \
			          QtCore.SIGNAL("clicked()"), \
			          self.saveData)
		
		self.connect(self.pushButtonSessionExport, \
			          QtCore.SIGNAL("clicked()"), \
			          self.exportData)
		
		self.connect(self.pushButtonSessionReset, \
			          QtCore.SIGNAL("clicked()"), \
			          self.resetData)
		
		self.connect(self.checkBoxServiceEnableJSON, \
		             QtCore.SIGNAL("stateChanged(int)"), \
		             self.updateSessionEnableJSON)
		
		if configuration.JSON_AVAILABLE:

			self.connect(self.pushButtonSessionJSON, \
			             QtCore.SIGNAL("clicked()"), \
			             self.startJSONService)
		else:
			#self.labelSessionPluginAPI.setVisible(False)
			#self.checkBoxServiceEnableJSON.setVisible(False)
			#print dir(self.horizontalLayout_2)
			#self.horizontalLayout_2.setEnabled(False)
			#self.lineSessionPluginAPI.setVisible(False)
			
			self.checkBoxServiceEnableJSON.setEnabled(False)
	
	
	##################################################################
	
	def updateEEGProcessingGUI(self):
		
		if self.configuration.ENABLE_PLUGIN_EEG:
			
			if (self.parent.plugin_eeg.packets['rawEeg'] == [] and \
			    self.parent.plugin_eeg.packets['signals'] == [] and \
			    not self.parent.plugin_eeg.connected):
				self.pushButtonSessionSave.setEnabled(False)
				self.pushButtonSessionExport.setEnabled(False)
				self.pushButtonSessionReset.setEnabled(False)
			
			else:
				self.pushButtonSessionSave.setEnabled(True)
				self.pushButtonSessionExport.setEnabled(True)
				self.pushButtonSessionReset.setEnabled(True)
			
			
			if self.parent.plugin_eeg.connected:
				self.labelSessionPluginEEGStatus.setText('Status: Connected')
			
			else:
				self.labelSessionPluginEEGStatus.setText('Status: Disconnected')
	
	
	##################################################################
	
	def processPacketEEG(self, packet):
		
		#self.processPacketThinkGear(packet)
		#self.processPacketEmotiv(packet)
		
		if ((self.configuration.ENABLE_PLUGIN_EEG) and \
		    #(self.parent.plugin_eeg.synapseServer.protocol != None) and
		    (self.parent.tabWidget.currentIndex() == self.tabIndex)):
			
			session_time = \
			   self.parent.plugin_eeg.calculateSessionTime()
			
			
			self.textLabelSessionTime.setText(session_time)
			self.textLabelConnectionTime.setText(session_time)
		
			try:
				self.textLabelPacketsReceived.setText( "%i" % \
					#self.parent.plugin_eeg.synapseServer.protocol.packet_count)
					self.parent.plugin_eeg.getPacketCount())
			except:
				pass
			
			try:
				self.textLabelPacketsDropped.setText( "%i" % \
					#self.parent.plugin_eeg.synapseServer.protocol.bad_packets)
					self.parent.plugin_eeg.getBadPackets())
			except:
				pass
	
	
	##################################################################
	
	def processPacketThinkGear(self, packet):
		
		pass
	
	
	##################################################################
	
	def processPacketEmotiv(self, packet):
		
		pass
	
	
	##################################################################
	
	def processCustomData(self, packet):
		
		for index in self.customDataHeaders:
		#for index in self.customData.keys():
			packet['custom'][index] = self.customData[index]
		
		
		return(packet)
	
	
	##################################################################
	
	def updateCustomData(self, name, value):
		
		if name not in self.customDataHeaders:
			self.customDataHeaders.append(name)
		
		value = value.replace(',', '%2C') # escape commas
		
		self.customData[name] = value
	
	
	##################################################################
	
	def saveData(self, filename=None, use_default=False):
		if self.configuration.ENABLE_PLUGIN_EEG:
			#self.parent.plugin_eeg.synapse_interface.saveData( \
			self.parent.plugin_eeg.saveData( \
			   source=self.parent.plugin_eeg, \
			   target=self, \
			   output_file=filename, \
			   use_default=use_default)
	
	
	##################################################################
	
	def exportData(self, filename=None, use_default=False):
		
		if self.configuration.ENABLE_PLUGIN_EEG:
			#self.parent.plugin_eeg.synapse_interface.exportData( \
			self.parent.plugin_eeg.exportData( \
			   parent=self.parent, \
			   source=self.parent.plugin_eeg, \
			   #source=self.parent, \
			   target=self, \
			   output_file=filename, \
			   use_default=use_default)
	
	
	##################################################################
	
	def resetSessionStartTime(self):
		
		self.session_start_timestamp = time.time()
	
	
	##################################################################
	
	def resetData(self):
		
		if self.configuration.ENABLE_PLUGIN_EEG:
			
			self.parent.plugin_eeg.resetData()
			
			#self.parent.plugin_eeg.synapse_interface.resetData( \
			   #source=self.parent.plugin_eeg)
			   
			#self.parent.plugin_eeg.synapse_interface.updateProfileSessionStatus( \
			self.parent.plugin_eeg.updateProfileSessionStatus( \
			   source=self.parent.plugin_eeg, \
			   target=self)
			
			self.updateEEGProcessingGUI()
		
		else:
			
			# Plugin EEG would have called resetSessionStartTime()
			self.resetSessionStartTime()
	
	
	##################################################################
	
	def updateSessionEnableJSON(self):
		
		if self.checkBoxServiceEnableJSON.isChecked():
			
			self.lineEditJSONHost.setVisible(True)
			self.lineEditJSONPort.setVisible(True)
			self.textLabelJSONHost.setVisible(True)
			self.textLabelJSONPort.setVisible(True)
			self.pushButtonSessionJSON.setVisible(True)
		
		else:
			
			self.lineEditJSONHost.setVisible(False)
			self.lineEditJSONPort.setVisible(False)
			self.textLabelJSONHost.setVisible(False)
			self.textLabelJSONPort.setVisible(False)
			self.pushButtonSessionJSON.setVisible(False)
	
	
	##################################################################
	
	def startJSONService(self):
		
		server_interface = str(self.lineEditJSONHost.text())
		server_port = int(self.lineEditJSONPort.text())
		
		
		self.serviceJSON = \
			service_json.puzzlebox_jigsaw_service_json( \
				self.log, \
				server_interface=server_interface, \
				server_port=server_port, \
				DEBUG=DEBUG, \
				parent=self)
		
		#self.connect(self.thinkGearConnectServer, \
		             #QtCore.SIGNAL("sendPacket()"), \
		             #self.thinkGearConnectServer.sendPacketQueue)
		
		self.serviceJSON.start()
		
		self.pushButtonSessionJSON.setText('Stop')
		self.lineEditJSONHost.setEnabled(False)
		self.lineEditJSONPort.setEnabled(False)
		
		
		self.disconnect(self.pushButtonSessionJSON, \
		                QtCore.SIGNAL("clicked()"), \
		                self.startJSONService)
		
		self.connect(self.pushButtonSessionJSON, \
		             QtCore.SIGNAL("clicked()"), \
		             self.stopJSONService)
	
	
	##################################################################
	
	def stopJSONService(self):
		
		self.pushButtonSessionJSON.setText('Start')
		self.lineEditJSONHost.setEnabled(True)
		self.lineEditJSONPort.setEnabled(True)
		
		self.disconnect(self.pushButtonSessionJSON, \
		                QtCore.SIGNAL("clicked()"), \
		                self.stopJSONService)
		
		self.connect(self.pushButtonSessionJSON, \
		             QtCore.SIGNAL("clicked()"), \
		             self.startJSONService)
		
		try:
			self.serviceJSON.exitThread()
		except Exception, e:
			if self.DEBUG:
				print "Call failed to self.serviceJSON.exitThread():",
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

