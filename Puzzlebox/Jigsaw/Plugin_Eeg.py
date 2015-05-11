#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Puzzlebox - Jigsaw - Plug-in - Eeg
#
# Copyright Puzzlebox Productions, LLC (2011-2015)

__changelog__ = """\
Last Update: 2015.01.17
"""

__todo__ = """
- Independently track Cognitiv actions
- Set Cognitiv legend to match current action
- Can't re-connect to Emotiv once disconnected
- Server not stopping properly when using Stop/Start repeatedly
"""

import os, sys, time

import Puzzlebox.Jigsaw.Configuration as configuration

if configuration.ENABLE_PYSIDE:
	try:
		from PySide import QtCore, QtGui, QtNetwork
	except Exception, e:
		print "ERROR: [Jigsaw:Plugin_Eeg] Exception importing PySide:",
		print e
		configuration.ENABLE_PYSIDE = False
	else:
		print "INFO: [Jigsaw:Plugin_Eeg] Using PySide module"

if not configuration.ENABLE_PYSIDE:
	print "INFO: [Jigsaw:Plugin_Eeg] Using PyQt4 module"
	from PyQt4 import QtCore, QtGui, QtNetwork


try:
	from Puzzlebox.Jigsaw.Interface_Plot import *
	MATPLOTLIB_AVAILABLE = True
except Exception, e:
	print "ERROR: [Jigsaw:Plugin_Eeg] Exception importing Puzzlebox.Jigsaw.Interface_Plot:",
	print e
	MATPLOTLIB_AVAILABLE = False


if (sys.platform == 'win32'):
	import _winreg as winreg
	import itertools
	import re
	import serial
	DEFAULT_IMAGE_PATH = 'images'
elif (sys.platform == 'darwin'):
	DEFAULT_IMAGE_PATH = 'images'
else:
	import bluetooth
	DEFAULT_IMAGE_PATH = '/usr/share/puzzlebox_jigsaw/images'


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	_fromUtf8 = lambda s: s


from Puzzlebox.Jigsaw.Design_Plugin_Eeg import Ui_Form as Design

import Puzzlebox.Synapse.Device as synapse_device
import Puzzlebox.Synapse.Session as synapse_session
import Puzzlebox.Synapse.Client as synapse_client
import Puzzlebox.Synapse.ThinkGear.Server as thinkgear_server
import Puzzlebox.Synapse.Emotiv.Server as emotiv_server
import Puzzlebox.Synapse.Muse.Server as muse_server

try:
	import Puzzlebox.Synapse.Emotiv.Protocol as synapse_emotiv_protocol
except Exception, e:
	print "ERROR: [Synapse:Emotiv:Client] Exception importing Emotiv.Protocol:",
	print e
	synapse_emotiv_protocol = None

try:
	import Puzzlebox.Synapse.Muse.Protocol as synapse_muse_protocol
except Exception, e:
	print "ERROR: [Synapse:Muse:Client] Exception importing Muse.Protocol:",
	print e
	synapse_muse_protocol = None

#####################################################################
# Globals
#####################################################################

DEBUG = 1

SYNAPSE_SERVER_HOST = configuration.SYNAPSE_SERVER_HOST
SYNAPSE_SERVER_PORT = configuration.SYNAPSE_SERVER_PORT

THINKGEAR_SERVER_HOST = configuration.THINKGEAR_SERVER_HOST
THINKGEAR_SERVER_PORT = configuration.THINKGEAR_SERVER_PORT

EMULATE_THINKGEAR_FOR_EMOTIV = configuration.EMULATE_THINKGEAR_FOR_EMOTIV
EMULATE_THINKGEAR_FOR_MUSE = configuration.EMULATE_THINKGEAR_FOR_MUSE

EEG_PRESERVE_RAW_DATA = configuration.EEG_PRESERVE_RAW_DATA

DEVICE_PATH = '/dev'
PATH_TO_HCITOOL = '/usr/bin/hcitool'

BLINK_VALID_RANGE = 2 # 2 seconds


TEMPLATE_LABEL = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>
<head>
<meta name="qrichtext" content="1" />
<style type="text/css">
p, li { white-space: pre-wrap; }
</style>
</head>
<body style=" font-family:'Sans'; font-size:10pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">__TEMPLATE_LABEL__</span>
</p>
</body>
</html>'''

#####################################################################
# Classes
#####################################################################

class puzzlebox_jigsaw_plugin_eeg(synapse_device.puzzlebox_synapse_device, \
                                  synapse_session.puzzlebox_synapse_session, \
                                  Design):
	
	def __init__(self, log, \
	             tabIndex=None, \
	             DEBUG=DEBUG, \
	             parent=None, \
	             embedded_mode=False):
		
		self.log = log
		self.DEBUG = DEBUG
		self.parent = parent
		self.tabIndex = tabIndex
		
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		
		self.configuration = configuration
		
		self.configureSettings()
		self.connectWidgets()
		
		self.name = "Jigsaw:Plugin:Eeg"
		self.baseWidget = self.verticalLayoutWidget_2
		#self.baseWidget = self.verticalLayoutWidget
		self.tabTitle = _fromUtf8("EEG")
		
		if self.tabIndex == None:
			self.parent.tabWidget.addTab(self.baseWidget, self.tabTitle)
		else:
			self.parent.tabWidget.insertTab(self.tabIndex, self.baseWidget, self.tabTitle)
		
		self.warnings = []
		
		self.customDataHeaders = []
		self.protocolSupport = []
		
		self.synapseServer = None
		self.synapseClient = None
		
		self.packets = {}
		self.packets['rawEeg'] = []
		self.packets['signals'] = []
		#self.packets['custom'] = {}
		
		self.packet_count = 0
		self.bad_packets = 0
		
		
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
		
		
		self.connected = False
	
	
	##################################################################
	
	def configureSettings(self):
		
		# Eeg
		
		self.configureControlPanelSynapseServer()
		self.updateControlPanelEEGSource()
		self.updateControlPanelEEGModel()
		
		
		# Hide Emulate ThinkGear by default
		self.checkBoxControlEmulateThinkGear.setVisible(False)
		
		# Display Host for Synapse Socket Server
		#self.lineEditSynapseHost.setText(THINKGEAR_SERVER_HOST)
		self.lineEditSynapseHost.setText(SYNAPSE_SERVER_HOST)
		
		# Display Port for Synapse Socket Server
		#self.lineEditSynapsePort.setText('%i' % THINKGEAR_SERVER_PORT)
		self.lineEditSynapsePort.setText('%i' % SYNAPSE_SERVER_PORT)
		
		
		self.parent.setProgressBarColor( \
			self.progressBarControlConcentration, 'FF0000') # Red
		self.parent.setProgressBarColor( \
			self.progressBarControlRelaxation, '0000FF') # Blue
		self.parent.setProgressBarColor( \
			self.progressBarControlConnectionLevel, '00FF00') # Green
		
		self.pushButtonControlConcentrationEnable.setVisible(False)
		self.pushButtonControlRelaxationEnable.setVisible(False)
		
		if MATPLOTLIB_AVAILABLE:
			#windowBackgroundRGB = (self.palette().window().color().red() / 255.0, \
			                            #self.palette().window().color().green() / 255.0, \
			                            #self.palette().window().color().blue() / 255.0)
			
			self.windowBackgroundRGB = (self.palette().window().color().red() / 255.0, \
			                            self.palette().window().color().green() / 255.0, \
			                            self.palette().window().color().blue() / 255.0)
			
			self.rawEEGMatplot = rawEEGMatplotlibCanvas( \
			                        parent=self.widgetPlotRawEEG, \
			                        width=self.widgetPlotRawEEG.width(), \
			                        height=self.widgetPlotRawEEG.height(), \
			                        title=None, \
			                        axes_top_text='1.0s', \
			                        axes_bottom_text='0.5s', \
			                        facecolor=self.windowBackgroundRGB)
			
			self.historyEEGThinkGear = historyEEGMatplotlibCanvas( \
			                            parent=self.widgetPlotHistoryThinkGear, \
			                            width=self.widgetPlotHistoryThinkGear.width(), \
			                            height=self.widgetPlotHistoryThinkGear.height(), \
			                            title=None, \
			                            axes_right_text='percent', \
			                            facecolor=self.windowBackgroundRGB)
			
			self.historyEEGEmotivCognitiv = historyEEGEmotivCognitiv( \
			                            parent=self.widgetPlotHistoryEmotivCognitiv, \
			                            width=self.widgetPlotHistoryEmotivCognitiv.width(), \
			                            height=self.widgetPlotHistoryEmotivCognitiv.height(), \
			                            title=None, \
			                            axes_right_text='percent', \
			                            legend_values=['Cognitiv'], \
			                            facecolor=self.windowBackgroundRGB)
			
			self.historyEEGEmotivAffectiv = historyEEGEmotivAffectiv( \
			                            parent=self.widgetPlotHistoryEmotivAffectiv, \
			                            width=self.widgetPlotHistoryEmotivAffectiv.width(), \
			                            height=self.widgetPlotHistoryEmotivAffectiv.height(), \
			                            title=None, \
			                            axes_right_text='percent', \
			                            facecolor=self.windowBackgroundRGB)
			
			
			self.setTemplateLabel(self.labelChartTop, 'Raw EEG Waves')
			self.widgetPlotRawEEG.setVisible(True)
			self.widgetPlotHistoryEmotivCognitiv.setVisible(False)
			
			self.setTemplateLabel(self.labelChartBottom, 'Brain Signals History')
			self.widgetPlotHistoryEmotivAffectiv.setVisible(False)
			self.widgetPlotHistoryThinkGear.setVisible(True)
			
			
			# Help
			#url = self.configuration.DEFAULT_EEG_HELP_URL
			url = self.parent.configuration.DEFAULT_EEG_HELP_URL
			if (url.startswith('path://')):
				url = "file://" + os.path.join( os.getcwd(), url.split('path://')[1] )
			if (sys.platform == 'win32'):
				url = url.replace('file://', '')
			
			if self.DEBUG:
				print "[Jigsaw:Plugin_EEG] loadWebURL:",
				print url
			
			self.webViewEEG.load( QtCore.QUrl(url) )
	
	
	##################################################################
	
	def connectWidgets(self):
		
		# Eeg
		
		self.connect(self.comboBoxEEGHeadsetModel, \
		             QtCore.SIGNAL("activated(int)"), \
		             self.updateControlPanelEEGModel)
		
		self.connect(self.comboBoxEEGSource, \
		             QtCore.SIGNAL("activated(int)"), \
		             self.updateControlPanelEEGSource)
		
		self.connect(self.comboBoxDeviceSelect, \
		             QtCore.SIGNAL("activated(int)"), \
		             self.updateControlPanelEEGDevice)
		
		self.connect(self.checkBoxControlEnableServer, \
		             QtCore.SIGNAL("stateChanged(int)"), \
		             self.updateControlPanelEnableServer)
		
		self.connect(self.pushButtonControlSearch, \
		             QtCore.SIGNAL("clicked()"), \
		             self.updateControlPanelEEGSource)
		
		self.connect(self.pushButtonSynapseServer, \
		             QtCore.SIGNAL("clicked()"), \
		             self.startEEGProcessing)
	
	
	##################################################################
	
	def setTemplateLabel(self, widget, label):
		
		label = TEMPLATE_LABEL.replace('__TEMPLATE_LABEL__', label)
		
		widget.setText(label)
	
	
	##################################################################
	
	#def processCustomData(self, packet):
		
		##if 'URL' in self.customDataHeaders:
			##url = self.webViewWebBrowser.url()
			##url = str(url.toString())
			##url = url.replace(',', '%2C') # escape commas
			##packet['custom']['URL'] = url
		
		
		#return(packet)
	
	
	##################################################################
	
	def updateDevices(self):
		
		self.comboBoxDeviceSelect.clear()
		
		devices = self.searchForDevices()
		
		if devices == []:
			devices = ['No Devices Found']
			self.comboBoxDeviceSelect.setEnabled(False)
		else:
			self.comboBoxDeviceSelect.setEnabled(True)
			self.pushButtonSynapseServer.setEnabled(True)
		
		for device in devices:
			self.comboBoxDeviceSelect.addItem(device)
	
	
	################################################################
	
	def updateControlPanelEEGModel(self, index=None):
		
		model = self.comboBoxEEGHeadsetModel.currentText()
		
		self.comboBoxEEGSource.clear()
		
		sources = []
		
		if (model == 'Emotiv EPOC'):
			
			sources.append('Emotiv Control Panel')
			sources.append('EmoComposer')
			
			if self.parent.configuration.EMULATE_THINKGEAR_FOR_EMOTIV:
				self.checkBoxControlEmulateThinkGear.setVisible(True)
			
			self.setTemplateLabel(self.labelChartTop, 'Emotiv Cognitiv History')
			self.widgetPlotRawEEG.setVisible(False)
			self.widgetPlotHistoryEmotivCognitiv.setVisible(True)
			
			self.setTemplateLabel(self.labelChartBottom, 'Emotiv Affectiv History')
			self.widgetPlotHistoryEmotivAffectiv.setVisible(True)
			self.widgetPlotHistoryThinkGear.setVisible(False)
			
			emotiv_error_message = "Warning: Emotiv driver failed to load."
			
			if (sys.platform == 'win32'):
				emotiv_error_message = "Warning: Emotiv driver failed to load. Please check that edk.dll edk_utils.dll are installed at %s" % \
				os.path.join( os.getcwd() )
				#os.path.join( os.getcwd(), "Puzzlebox", "Synapse", "Emotiv")
			
			if ((synapse_emotiv_protocol == None) and \
			    ('emotiv_driver' not in self.warnings)):
				QtGui.QMessageBox.information(self, \
				                             'Warning', \
				                             emotiv_error_message)
				self.warnings.append('emotiv_driver')
		            
		            
		elif (model == 'InterAxon Muse'):
			
			#sources.append('Emotiv Control Panel')
			sources.append('MuseIO')
			if self.parent.configuration.SPACEBREW_ENABLE:
				sources.append('Spacebrew')
			
			if self.parent.configuration.EMULATE_THINKGEAR_FOR_MUSE:
				self.checkBoxControlEmulateThinkGear.setVisible(True)
			
			#self.setTemplateLabel(self.labelChartTop, 'Emotiv Cognitiv History')
			#self.widgetPlotRawEEG.setVisible(False)
			#self.widgetPlotHistoryEmotivCognitiv.setVisible(True)
			
			#self.setTemplateLabel(self.labelChartBottom, 'Emotiv Affectiv History')
			#self.widgetPlotHistoryEmotivAffectiv.setVisible(True)
			#self.widgetPlotHistoryThinkGear.setVisible(False)
			
			#emotiv_error_message = "Warning: Emotiv driver failed to load."
			
			#if (sys.platform == 'win32'):
				#emotiv_error_message = "Warning: Emotiv driver failed to load. Please check that edk.dll edk_utils.dll are installed at %s" % \
				#os.path.join( os.getcwd() )
				##os.path.join( os.getcwd(), "Puzzlebox", "Synapse", "Emotiv")
			
			#if ((synapse_muse_protocol == None) and \
			    #('muse_driver' not in self.warnings)):
				#QtGui.QMessageBox.information(self, \
				                             #'Warning', \
				                             #muse_error_message)
				#self.warnings.append('muse_driver')
		
		else:
			
			if (sys.platform == 'win32'):
				sources.append('ThinkGear Connect')
				sources.append('Puzzlebox Synapse')
				sources.append('ThinkGear Emulator')
				sources.append('Hardware Device')
			elif (sys.platform == 'darwin'):
				sources.append('ThinkGear Connect')
				sources.append('Puzzlebox Synapse')
				sources.append('ThinkGear Emulator')
				sources.append('Hardware Device')
			else:
				sources.append('Hardware Device')
				sources.append('ThinkGear Emulator')
				sources.append('Puzzlebox Synapse')
				sources.append('ThinkGear Connect')
			
			self.checkBoxControlEmulateThinkGear.setVisible(False)
			
			self.setTemplateLabel(self.labelChartTop, 'Raw EEG Waves')
			self.widgetPlotRawEEG.setVisible(True)
			self.widgetPlotHistoryEmotivCognitiv.setVisible(False)
			
			self.setTemplateLabel(self.labelChartBottom, 'Brain Signals History')
			self.widgetPlotHistoryEmotivAffectiv.setVisible(False)
			self.widgetPlotHistoryThinkGear.setVisible(True)
		
		
		for source in sources:
			self.comboBoxEEGSource.addItem(source)
		
		
		self.updateControlPanelEEGSource()
	
	
	################################################################
	
	def updateControlPanelEEGSource(self, index=None):
		
		source = self.comboBoxEEGSource.currentText()
		
		if source in ['Puzzlebox Synapse', 'ThinkGear Connect']:
			
			self.configureControlPanelSynapseClient()
			self.pushButtonSynapseServer.setEnabled(True)
		
		elif source == 'ThinkGear Emulator':
			
			self.configureControlPanelSynapseServer()
			self.comboBoxDeviceSelect.setVisible(False)
			self.pushButtonControlSearch.setVisible(False)
			self.pushButtonSynapseServer.setEnabled(True)
		
		elif source == 'Hardware Device':
			
			self.updateDevices()
			if self.comboBoxDeviceSelect.currentText() == 'No Devices Found':
				self.pushButtonSynapseServer.setEnabled(False)
			else:
				self.pushButtonSynapseServer.setEnabled(True)
			
			self.comboBoxDeviceSelect.setVisible(True)
			self.pushButtonControlSearch.setVisible(True)
			self.configureControlPanelSynapseServer()
		
		elif source in ['Emotiv Control Panel', 'EmoComposer']:
			
			self.configureControlPanelSynapseServer()
			self.comboBoxDeviceSelect.setVisible(False)
			self.pushButtonControlSearch.setVisible(False)
			self.pushButtonSynapseServer.setEnabled(True)
			
		elif source in ['MuseIO', 'Spacebrew']:
			
			self.configureControlPanelSynapseServer()
			self.comboBoxDeviceSelect.setVisible(False)
			self.pushButtonControlSearch.setVisible(False)
			self.pushButtonSynapseServer.setEnabled(True)
	
	
	################################################################
	
	def updateControlPanelEEGDevice(self, index=None):
		
		if self.DEBUG > 2:
			print "DEBUG: [Jigsaw:Plugin_Eeg] updateControlPanelEEGDevice called -",
			print index
	
	
	################################################################
	
	def configureControlPanelSynapseServer(self):
		
		#self.updateDevices()
		
		self.checkBoxControlEnableServer.setVisible(True)
		self.updateControlPanelEnableServer(None)
		
		self.pushButtonControlSearch.setVisible(True)
		
		self.lineControlSourceServer.setVisible(True)
		
		self.pushButtonSynapseServer.setText('Start')
	
	
	################################################################
	
	def configureControlPanelSynapseClient(self):
		
		self.comboBoxDeviceSelect.setVisible(False)
		
		self.checkBoxControlEnableServer.setVisible(False)
		self.checkBoxControlEnableServer.setCheckState(QtCore.Qt.Checked)
		self.updateControlPanelEnableServer(None)
		
		self.pushButtonControlSearch.setVisible(False)
		
		self.lineControlSourceServer.setVisible(False)
		
		self.pushButtonSynapseServer.setText('Connect')
	
	
	################################################################
	
	def updateControlPanelEnableServer(self, arg):
		
		if self.checkBoxControlEnableServer.isChecked():
			
			self.lineEditSynapseHost.setVisible(True)
			self.lineEditSynapsePort.setVisible(True)
			self.textLabelSynapseHost.setVisible(True)
			self.textLabelSynapsePort.setVisible(True)
		
		else:
			
			self.lineEditSynapseHost.setVisible(False)
			self.lineEditSynapsePort.setVisible(False)
			self.textLabelSynapseHost.setVisible(False)
			self.textLabelSynapsePort.setVisible(False)
	
	
	##################################################################
	
	def startEEGProcessing(self):
		
		if self.connected:
			return
		
		selection = self.comboBoxEEGSource.currentText()
		
		if selection in ['Puzzlebox Synapse', 'ThinkGear Connect']:
			
			self.connectToSynapseHost()
		
		
		elif selection == 'ThinkGear Emulator':
			
			self.startSynapseServer()
		
		
		elif selection == 'Hardware Device':
			
			self.startSynapseServer()
		
		
		elif selection in ['Emotiv Control Panel', 'EmoComposer']:
			
			self.startSynapseServer()
		
		
		elif selection in ['MuseIO', 'Spacebrew']:
			
			self.startSynapseServer()
		
		
		self.connected = True
		
		
		# Handle GUI Elements
		self.updateEEGProcessingGUI()
	
	
	##################################################################
	
	def stopEEGProcessing(self):
		
		if not self.connected:
			return
		
		selection = self.comboBoxEEGSource.currentText()
		
		if selection in ['Puzzlebox Synapse', 'ThinkGear Connect']:
			
			self.disconnectFromSynapseHost()
		
		
		elif selection == 'ThinkGear Emulator':
			
			self.stopSynapseServer()
		
		
		elif selection == 'Hardware Device':
			
			self.stopSynapseServer()
		
		
		elif selection in ['Emotiv Control Panel', 'EmoComposer']:
			
			self.stopSynapseServer()
		
		
		elif selection in ['MuseIO', 'Spacebrew']:
			
			self.stopSynapseServer()
		
		
		self.connected = False
		
		# Handle GUI Elements
		self.updateEEGProcessingGUI()
	
	
	##################################################################
	
	def collectCustomDataHeadersFromSynapseServer(self):
		
		# Clear previous data when re-starting
		for header in self.synapseServer.customDataHeaders:
			if header in self.customDataHeaders:
				del(self.customDataHeaders[ self.customDataHeaders.index(header) ])
		
		
		for header in self.synapseServer.customDataHeaders:
			if header not in self.customDataHeaders:
				self.customDataHeaders.append(header)
		
		
		#print "EEG:",
		#print self.customDataHeaders
	
	
	##################################################################
	
	def connectToSynapseHost(self):
		
		if self.DEBUG:
			print "INFO: [Jigsaw:Plugin_Eeg] Connecting to Synapse Host"
		
		server_host = str(self.lineEditSynapseHost.text())
		server_port = int(self.lineEditSynapsePort.text())
		
		self.synapseClient = \
		   synapse_client.puzzlebox_synapse_client( \
			   self.log, \
			   server_host=server_host, \
			   server_port=server_port, \
			   DEBUG=0, \
			   parent=self)
		
		#self.synapseServer = \
		   #thinkgear_server.puzzlebox_synapse_server_thinkgear( \
		      #self.log, \
		      ##server_interface=server_interface, \
		      ##server_port=server_port, \
		      ##device_model=eeg_headset_model, \
		      ##device_address=device_address, \
		      ##emulate_headset_data=emulate_headset_data, \
		      #DEBUG=DEBUG, \
		      #parent=self)
		
		self.synapseServer = \
		   thinkgear_server.puzzlebox_synapse_server_thinkgear( \
		      self.log, \
		      server_interface=None, \
		      #server_port=server_port, \
		      #device_model=eeg_headset_model, \
		      #device_address=device_address, \
		      #emulate_headset_data=emulate_headset_data, \
		      DEBUG=DEBUG, \
		      parent=self)

		
		if (self.synapseClient.socket.state() != QtNetwork.QAbstractSocket.ConnectedState):
			QtGui.QMessageBox.information(self, \
			                            self.synapseClient.socket.name, \
			              "Failed to connect to remote service %s:%i" % \
			               (server_host, server_port))
			              #"Failed to connect to Synapse socket server")
		
		else:
			
			self.disconnect(self.pushButtonSynapseServer, \
			                QtCore.SIGNAL("clicked()"), \
			                self.startEEGProcessing)
			
			self.connect(self.pushButtonSynapseServer, \
			             QtCore.SIGNAL("clicked()"), \
			             self.stopEEGProcessing)
			
			self.pushButtonSynapseServer.setText('Disconnect')
			
			self.comboBoxEEGHeadsetModel.setEnabled(False)
			self.comboBoxEEGSource.setEnabled(False)
			self.lineEditSynapseHost.setEnabled(False)
			self.lineEditSynapsePort.setEnabled(False)
		
		
		self.collectCustomDataHeadersFromSynapseServer()
	
	
	##################################################################
	
	def disconnectFromSynapseHost(self):
		
		if self.DEBUG:
			print "INFO: [Jigsaw:Plugin_Eeg] Disconnecting from Synapse Host"
		
		self.synapseClient.disconnectFromHost()
		
		self.disconnect(self.pushButtonSynapseServer, \
			          QtCore.SIGNAL("clicked()"), \
			          self.stopEEGProcessing)
		
		self.connect(self.pushButtonSynapseServer, \
			          QtCore.SIGNAL("clicked()"), \
			          self.startEEGProcessing)
		
		#self.pushButtonControlForwards.emit(QtCore.SIGNAL("released()"))
		
		self.pushButtonSynapseServer.setText('Connect')
		
		#self.textLabelEEGStatus.setText('Disconnected')
		
		self.comboBoxEEGHeadsetModel.setEnabled(True)
		self.comboBoxEEGSource.setEnabled(True)
		self.lineEditSynapseHost.setEnabled(True)
		self.lineEditSynapsePort.setEnabled(True)
		
		self.progressBarControlConcentration.setValue(0)
		self.progressBarControlRelaxation.setValue(0)
		self.progressBarControlConnectionLevel.setValue(0)
		
	
	
	##################################################################
	
	def updateEEGProcessingGUI(self):
		
		if self.connected:
			
			self.comboBoxEEGHeadsetModel.setEnabled(False)
			self.comboBoxEEGSource.setEnabled(False)
			self.comboBoxDeviceSelect.setEnabled(False)
			self.pushButtonControlSearch.setEnabled(False)
			self.checkBoxControlEnableServer.setEnabled(False)
			self.lineEditSynapseHost.setEnabled(False)
			self.lineEditSynapsePort.setEnabled(False)
			
			#self.pushButtonSessionSave.setEnabled(True)
			#self.pushButtonSessionExport.setEnabled(True)
			#self.pushButtonSessionReset.setEnabled(True)
			
			self.pushButtonSynapseServer.setText('Stop')
			
			self.disconnect(self.pushButtonSynapseServer, \
			                QtCore.SIGNAL("clicked()"), \
			                self.startEEGProcessing)
			
			self.connect(self.pushButtonSynapseServer, \
			             QtCore.SIGNAL("clicked()"), \
			             self.stopEEGProcessing)
		
		else:
			
			self.comboBoxEEGHeadsetModel.setEnabled(True)
			self.comboBoxEEGSource.setEnabled(True)
			self.comboBoxDeviceSelect.setEnabled(True)
			self.pushButtonControlSearch.setEnabled(True)
			self.checkBoxControlEnableServer.setEnabled(True)
			self.lineEditSynapseHost.setEnabled(True)
			self.lineEditSynapsePort.setEnabled(True)
			
			#if self.packets['rawEeg'] == [] and self.packets['signals'] == []:
				#self.pushButtonSessionSave.setEnabled(False)
				#self.pushButtonSessionExport.setEnabled(False)
				#self.pushButtonSessionReset.setEnabled(False)
			
			self.progressBarControlConcentration.setValue(0)
			self.progressBarControlRelaxation.setValue(0)
			self.progressBarControlConnectionLevel.setValue(0)
			
			self.pushButtonSynapseServer.setText('Start')
			
			## In case the user connects to a MindSet, then disconnects
			## and re-connects to a MindSet Emulator,
			## we need to reset the max power values
			#
			#self.maxEEGPower = THINKGEAR_EMULATION_MAX_EEG_POWER_VALUE
			#
			#self.progressBarEEGDelta.setMaximum(self.maxEEGPower)
			#self.progressBarEEGTheta.setMaximum(self.maxEEGPower)
			#self.progressBarEEGLowAlpha.setMaximum(self.maxEEGPower)
			#self.progressBarEEGHighAlpha.setMaximum(self.maxEEGPower)
			#self.progressBarEEGLowBeta.setMaximum(self.maxEEGPower)
			#self.progressBarEEGHighBeta.setMaximum(self.maxEEGPower)
			#self.progressBarEEGLowGamma.setMaximum(self.maxEEGPower)
			#self.progressBarEEGMidGamma.setMaximum(self.maxEEGPower)
			
			
			self.disconnect(self.pushButtonSynapseServer, \
			                QtCore.SIGNAL("clicked()"), \
			                self.stopEEGProcessing)
			
			self.connect(self.pushButtonSynapseServer, \
			             QtCore.SIGNAL("clicked()"), \
			             self.startEEGProcessing)
		
		
		for plugin in self.parent.activePlugins:
			if 'EEG' in plugin.protocolSupport:
				try:
					plugin.updateEEGProcessingGUI()
				except Exception, e:
					if self.DEBUG:
						print "ERROR: [Jigsaw:Plugin_Eeg] Exception calling %s updateEEGProcessingGUI():" % plugin.name,
						print e
	
	
	##################################################################
	
	def startSynapseServer(self):
		
		eeg_headset_model = str(self.comboBoxEEGHeadsetModel.currentText())
		source = self.comboBoxEEGSource.currentText()
		server_interface = str(self.lineEditSynapseHost.text())
		server_port = int(self.lineEditSynapsePort.text())
		
		if ((eeg_headset_model == 'NeuroSky MindWave Mobile') or \
		    (eeg_headset_model == 'NeuroSky MindWave') or \
		    (eeg_headset_model == 'NeuroSky MindSet')):
			
			self.startThinkGearConnectService()
		
		elif (eeg_headset_model == 'Emotiv EPOC'):
			
			self.startEmotivService()
		
		elif (eeg_headset_model == 'InterAxon Muse'):
			
			if (source == 'MuseIO'):
				self.startMuseService()
			elif (source == 'Spacebrew'):
				self.startSpacebrewService()
		
		
		self.synapseClient = \
		   synapse_client.puzzlebox_synapse_client( \
		      self.log, \
		      server_host=server_interface, \
		      server_port=server_port, \
		      DEBUG=0, \
		      parent=self)
		
		self.synapseClient.start()
	
	
	##################################################################
	
	def stopSynapseServer(self):
		
		eeg_headset_model = str(self.comboBoxEEGHeadsetModel.currentText())
		
		if ((eeg_headset_model == 'NeuroSky MindWave Mobile') or \
		    (eeg_headset_model == 'NeuroSky MindWave') or \
		    (eeg_headset_model == 'NeuroSky MindSet')):
			
			self.stopThinkGearConnectService()
		
		elif (eeg_headset_model == 'Emotiv EPOC'):
			
			self.stopEmotivService()
			
		elif (eeg_headset_model == 'InterAxon Muse'):
			
			self.stopMuseService()
		
		
		try:
			self.synapseClient.exitThread()
		except Exception, e:
			if self.DEBUG:
				print "ERROR: [Jigsaw:Plugin_Eeg] Call failed to self.synapseClient.exitThread():",
				print e
		
		try:
			self.synapseServer.exitThread()
		except Exception, e:
			if self.DEBUG:
				print "ERROR: [Jigsaw:Plugin_Eeg] Call failed to self.synapseServer.exitThread():",
				print e
		
		
		# Handle GUI Elements
		self.updateEEGProcessingGUI()
	
	
	##################################################################
	
	def startThinkGearConnectService(self):
		
		eeg_headset_model = str(self.comboBoxEEGHeadsetModel.currentText())
		device_source = str(self.comboBoxEEGSource.currentText())
		device_address = str(self.comboBoxDeviceSelect.currentText())
		server_interface = str(self.lineEditSynapseHost.text())
		server_port = int(self.lineEditSynapsePort.text())
		emulate_headset_data = (device_source == 'ThinkGear Emulator')
		
		self.synapseServer = \
		   thinkgear_server.puzzlebox_synapse_server_thinkgear( \
		      self.log, \
		      server_interface=server_interface, \
		      server_port=server_port, \
		      device_model=eeg_headset_model, \
		      device_address=device_address, \
		      emulate_headset_data=emulate_headset_data, \
		      DEBUG=DEBUG, \
		      parent=self)
		
		
		## Clear previous data when re-starting
		#for header in self.synapseServer.customDataHeaders:
			#if header in self.customDataHeaders:
				#del(self.customDataHeaders[ self.customDataHeaders.index(header) ])
		
		
		#for header in self.synapseServer.customDataHeaders:
			#if header not in self.customDataHeaders:
				#self.customDataHeaders.append(header)
		
		
		self.collectCustomDataHeadersFromSynapseServer()
		
		
		self.synapseServer.start()
	
	
	##################################################################
	
	def stopThinkGearConnectService(self):
		
		#for header in self.synapseServer.customDataHeaders:
			#if header in self.customDataHeaders:
				#del(self.customDataHeaders[ self.customDataHeaders.index(header) ])
		
		# Allow collected EEG data to persist after service has been stopped
		pass
	
	
	##################################################################
	
	def startEmotivService(self):
		
		device_address = str(self.comboBoxEEGSource.currentText())
		
		if device_address == 'Emotiv Control Panel':
			device_address = configuration.EMOTIV_SERVER_PORT_CONTROL_PANEL
		else:
			device_address = configuration.EMOTIV_SERVER_PORT_EMOCOMPOSER
		
		
		server_interface = str(self.lineEditSynapseHost.text())
		server_port = int(self.lineEditSynapsePort.text())
		eeg_headset_model = str(self.comboBoxEEGHeadsetModel.currentText())
		emulate_headset_data = (device_address == 'ThinkGear Emulator')
		
		emulate_thinkgear = (self.checkBoxControlEmulateThinkGear.isChecked())
		
		self.synapseServer = \
		   emotiv_server.puzzlebox_synapse_server_emotiv( \
		      self.log, \
		      server_interface=server_interface, \
		      server_port=server_port, \
		      device_model=eeg_headset_model, \
		      device_address=device_address, \
		      emulate_headset_data=emulate_headset_data, \
		      emulate_thinkgear=emulate_thinkgear, \
		      DEBUG=DEBUG, \
		      parent=self)
		
		for header in self.synapseServer.customDataHeaders:
			if header not in self.customDataHeaders:
				self.customDataHeaders.append(header)
		
		self.synapseServer.start()
	
	
	##################################################################
	
	def stopEmotivService(self):
		
		for header in self.synapseServer.customDataHeaders:
			if header in self.customDataHeaders:
				del(self.customDataHeaders[ self.customDataHeaders.index(header) ])
	
	
	##################################################################
	
	def startMuseService(self):
		
		device_address = str(self.comboBoxEEGSource.currentText())
		
		if device_address == 'MuseIO':
			device_address = configuration.MUSE_SERVER_PORT
		#else:
			#device_address = configuration.EMOTIV_SERVER_PORT_EMOCOMPOSER
		
		
		server_interface = str(self.lineEditSynapseHost.text())
		server_port = int(self.lineEditSynapsePort.text())
		eeg_headset_model = str(self.comboBoxEEGHeadsetModel.currentText())
		emulate_headset_data = (device_address == 'ThinkGear Emulator')
		
		emulate_thinkgear = (self.checkBoxControlEmulateThinkGear.isChecked())
		
		self.synapseServer = \
		   muse_server.puzzlebox_synapse_server_muse( \
		      self.log, \
		      server_interface=server_interface, \
		      server_port=server_port, \
		      device_model=eeg_headset_model, \
		      device_address=device_address, \
		      emulate_headset_data=emulate_headset_data, \
		      emulate_thinkgear=emulate_thinkgear, \
		      DEBUG=DEBUG, \
		      parent=self)
		
		for header in self.synapseServer.customDataHeaders:
			if header not in self.customDataHeaders:
				self.customDataHeaders.append(header)
		
		self.synapseServer.start()
	
	
	##################################################################
	
	def startSpacebrewService(self):
		
		device_address = str(self.comboBoxEEGSource.currentText())
		
		#if device_address == 'MuseIO':
			#device_address = configuration.MUSE_SERVER_PORT
		##else:
			##device_address = configuration.EMOTIV_SERVER_PORT_EMOCOMPOSER
		
		device_address = configuration.SPACEBREW_HOST
		
		
		server_interface = str(self.lineEditSynapseHost.text())
		server_port = int(self.lineEditSynapsePort.text())
		eeg_headset_model = str(self.comboBoxEEGHeadsetModel.currentText())
		emulate_headset_data = (device_address == 'ThinkGear Emulator')
		
		emulate_thinkgear = (self.checkBoxControlEmulateThinkGear.isChecked())
		
		self.synapseServer = \
		   spacebrew_server.puzzlebox_synapse_server_spacebrew( \
		      self.log, \
		      server_interface=server_interface, \
		      server_port=server_port, \
		      device_model=eeg_headset_model, \
		      device_address=device_address, \
		      emulate_headset_data=emulate_headset_data, \
		      emulate_thinkgear=emulate_thinkgear, \
		      DEBUG=DEBUG, \
		      parent=self)
		
		for header in self.synapseServer.customDataHeaders:
			if header not in self.customDataHeaders:
				self.customDataHeaders.append(header)
		
		self.synapseServer.start()
	
	
	##################################################################
	
	def stopMuseService(self):
		
		#self.muse_server.protocol.keep_running = False
		#self.muse_server.exitThread()
		self.synapseServer.exitThread()
		
		#for header in self.synapseServer.customDataHeaders:
			#if header in self.customDataHeaders:
				#del(self.customDataHeaders[ self.customDataHeaders.index(header) ])
	
	
	##################################################################
	
	def stopSpacebrewService(self):
		
		#self.muse_server.protocol.keep_running = False
		self.spacebrew_server.exitThread()
		
		#for header in self.synapseServer.customDataHeaders:
			#if header in self.customDataHeaders:
				#del(self.customDataHeaders[ self.customDataHeaders.index(header) ])
	
	
	##################################################################
	
	def processPacketEEG(self, packet):
		
		eeg_headset_model = str(self.comboBoxEEGHeadsetModel.currentText())
		
		if (eeg_headset_model == 'Emotiv EPOC'):
			self.processPacketEmotiv(packet)
		elif (eeg_headset_model == 'InterAxon Muse'):
			self.processPacketMuse(packet)
		else:
			self.processPacketThinkGear(packet)
		
		for plugin in self.parent.activePlugins:
			if 'EEG' in plugin.protocolSupport:
				try:
					plugin.processPacketEEG(packet)
				except Exception, e:
					if self.DEBUG:
						print "ERROR: [Jigsaw:Plugin_Eeg] Exception calling %s processPacketEEG():" % plugin.name,
						print e
		
		
		if (self.parent.tabWidget.currentIndex() == \
		    self.tabIndex):
			
			self.updateProfileSessionStatus()
	
	
	##################################################################
	
	def processPacketThinkGear(self, packet):
		
		tabVisible = (self.parent.tabWidget.currentIndex() == \
		              self.tabIndex)
		
		# Raw EEG
		if ('rawEeg' in packet.keys()):
			
			if configuration.EEG_PRESERVE_RAW_DATA:
				#self.packets['rawEeg'].append(packet['rawEeg'])
				self.packets['rawEeg'].append(packet)
			
			if MATPLOTLIB_AVAILABLE:
				if self.parent.tabWidget.currentIndex() == self.tabIndex:
					self.rawEEGMatplot.updateValues(packet['rawEeg'])
					
					return
		
		else:
			self.packets['signals'].append(packet)
		
		
		if ('eSense' in packet.keys()):
			
			if self.DEBUG > 2:
				print packet
			
			#self.processEyeBlinks()
			
			if ('attention' in packet['eSense'].keys()):
				if self.pushButtonControlConcentrationEnable.isChecked():
					
					# Record URL against timestamps for eSense "attention"
					packet = self.processCustomData(packet)
					
					if tabVisible:
						self.progressBarControlConcentration.setValue(packet['eSense']['attention'])
			
			
			if ('meditation' in packet['eSense'].keys()) and tabVisible:
				if self.pushButtonControlRelaxationEnable.isChecked():
					self.progressBarControlRelaxation.setValue(packet['eSense']['meditation'])
		
		
			if MATPLOTLIB_AVAILABLE:
				self.historyEEGThinkGear.updateValues('eSense', packet['eSense'])
				if (self.parent.tabWidget.currentIndex() == self.tabIndex):
					self.historyEEGThinkGear.updateFigure('eSense', packet['eSense'])
		
		#self.updateControlPower()
		#self.updateProgressBarColors()
		
		
		if ('poorSignalLevel' in packet.keys()) and tabVisible:
			
			if self.DEBUG > 2:
				print packet
			
			if packet['poorSignalLevel'] == 200:
				value = 0
				self.textLabelControlConnectionLevel.setText('No Contact')
			elif packet['poorSignalLevel'] == 0:
				value = 100
				self.textLabelControlConnectionLevel.setText('Connected')
			else:
				value = int(100 - ((packet['poorSignalLevel'] / 200.0) * 100))
			self.textLabelControlConnectionLevel.setText('Connection Level')
			self.progressBarControlConnectionLevel.setValue(value)
		
		
		## Eye Blinks
		#if ('blinkStrength' in packet.keys()):
			
			#if self.DEBUG:
				#print packet
			
			#self.blinks[time.time()] = packet
			##self.processEyeBlinks()
	
	
	##################################################################
	
	def processPacketEmotiv(self, packet):
		
		if self.DEBUG > 2:
			print "INFO: [Jigsaw:Plugin_Eeg] Emotiv packet received:"
			print packet
		
		tabVisible = (self.parent.tabWidget.currentIndex() == \
		              self.tabIndex)
		
		self.packets['signals'].append(packet)
		
		
		# Record URL against timestamps
		packet = self.processCustomData(packet)
		
		
		if ('emotivStatus' in packet.keys()):
			
			if ('contactNumberOfQualityChannels' in packet['emotivStatus']):
				
				signalLevel =  \
				   (packet['emotivStatus']['contactNumberOfQualityChannels'] / 18.0) * 200
				signalLevel = 200 - int(signalLevel)
				
				if signalLevel == 200:
					value = 0
					self.textLabelControlConnectionLevel.setText('No Contact')
				elif signalLevel == 0:
					value = 100
					self.textLabelControlConnectionLevel.setText('Connected')
				else:
					value = int(100 - ((signalLevel / 200.0) * 100))
				self.textLabelControlConnectionLevel.setText('Connection Level')
				self.progressBarControlConnectionLevel.setValue(value)
			
			#if ('timeFromStart' in packet['emotivStatus']):
				#if not configuration.EMULATE_THINKGEAR_FOR_EMOTIV:
					#self.textEditDebugConsole.append("")
					#try:
						#(date, localtime) = self.parseTimeStamp(packet['timestamp'])
						#self.textEditDebugConsole.append("Timestamp: %s %s" % (date, localtime))
					#except:
						#pass
				#self.textEditDebugConsole.append("timeFromStart: %f" % \
				                                  #packet['emotivStatus']['timeFromStart'])
			
			#if ('headsetOn' in packet['emotivStatus']):
				#self.textEditDebugConsole.append("headsetOn: %s" % \
				                                  #bool(packet['emotivStatus']['headsetOn']))
			
			#if ('wireless' in packet['emotivStatus']):
				#self.textEditDebugConsole.append("wireless: %i" % \
				                                  #packet['emotivStatus']['wireless'])
		
		
		if ('affectiv' in packet.keys()) and tabVisible:
			
			if ('excitement' in packet['affectiv']):
				if self.pushButtonControlConcentrationEnable.isChecked():
					value = int(packet['affectiv']['excitement'] * 100)
					self.progressBarControlConcentration.setValue(value)
			
			elif ('longTermExcitement' in packet['affectiv']):
				if self.pushButtonControlConcentrationEnable.isChecked():
					value = int(packet['affectiv']['longTermExcitement'] * 100)
					self.progressBarControlConcentration.setValue(value)
			
			if ('meditation' in packet['affectiv']) and tabVisible:
				if self.pushButtonControlRelaxationEnable.isChecked():
					value = int(packet['affectiv']['meditation'] * 100)
					self.progressBarControlRelaxation.setValue(value)
			
			#if ('frustration' in packet['affectiv']):
				#self.textEditDebugConsole.append("frustration: %.2f" % \
				                                  #packet['affectiv']['frustration'])
			
			#if ('engagementBoredom' in packet['affectiv']):
				#self.textEditDebugConsole.append("engagementBoredom: %.2f" % \
				                                  #packet['affectiv']['engagementBoredom'])
			
			if MATPLOTLIB_AVAILABLE:
				self.historyEEGEmotivAffectiv.updateValues('affectiv', packet['affectiv'])
				if (self.parent.tabWidget.currentIndex() == self.tabIndex):
					self.historyEEGEmotivAffectiv.updateFigure('affectiv', packet['affectiv'])
		
		
		if ('cognitiv' in packet.keys()):
			
			#if ('currentAction' in packet['cognitiv']):
				#self.textEditDebugConsole.append("currentAction: %i" % \
				                                  #packet['cognitiv']['currentAction'])
			
			#if ('currentActionPower' in packet['cognitiv']):
				#self.textEditDebugConsole.append("currentActionPower: %.2f" % \
				                                  #packet['cognitiv']['currentActionPower'])
			
			if MATPLOTLIB_AVAILABLE:
				#print packet['cognitiv']
				self.historyEEGEmotivCognitiv.updateValues('cognitiv', packet['cognitiv']['currentActionPower'])
				if (self.parent.tabWidget.currentIndex() == self.tabIndex):
					self.historyEEGEmotivCognitiv.updateFigure('cognitiv', packet['cognitiv']['currentActionPower'])
	
	
	##################################################################
	
	def processPacketMuse(self, packet):
		
		if self.DEBUG > 2:
			print "INFO: [Jigsaw:Plugin_Eeg] Muse packet received:"
			print packet
		
		tabVisible = (self.parent.tabWidget.currentIndex() == \
		              self.tabIndex)
		
		
		# Fix for missing timestamps
		if 'timestamp' not in packet.keys():
			packet['timestamp'] = time.time()
		
		
		self.packets['signals'].append(packet)
		
		
		self.processPacketThinkGear(packet)
		
		# Record URL against timestamps
		packet = self.processCustomData(packet)
		
		
		
		#if ('emotivStatus' in packet.keys()):
			
			#if ('contactNumberOfQualityChannels' in packet['emotivStatus']):
				
				#signalLevel =  \
				   #(packet['emotivStatus']['contactNumberOfQualityChannels'] / 18.0) * 200
				#signalLevel = 200 - int(signalLevel)
				
				#if signalLevel == 200:
					#value = 0
					#self.textLabelControlConnectionLevel.setText('No Contact')
				#elif signalLevel == 0:
					#value = 100
					#self.textLabelControlConnectionLevel.setText('Connected')
				#else:
					#value = int(100 - ((signalLevel / 200.0) * 100))
				#self.textLabelControlConnectionLevel.setText('Connection Level')
				#self.progressBarControlConnectionLevel.setValue(value)
			
			##if ('timeFromStart' in packet['emotivStatus']):
				##if not configuration.EMULATE_THINKGEAR_FOR_EMOTIV:
					##self.textEditDebugConsole.append("")
					##try:
						##(date, localtime) = self.parseTimeStamp(packet['timestamp'])
						##self.textEditDebugConsole.append("Timestamp: %s %s" % (date, localtime))
					##except:
						##pass
				##self.textEditDebugConsole.append("timeFromStart: %f" % \
				                                  ##packet['emotivStatus']['timeFromStart'])
			
			##if ('headsetOn' in packet['emotivStatus']):
				##self.textEditDebugConsole.append("headsetOn: %s" % \
				                                  ##bool(packet['emotivStatus']['headsetOn']))
			
			##if ('wireless' in packet['emotivStatus']):
				##self.textEditDebugConsole.append("wireless: %i" % \
				                                  ##packet['emotivStatus']['wireless'])
		
		
		#if ('affectiv' in packet.keys()) and tabVisible:
			
			#if ('excitement' in packet['affectiv']):
				#if self.pushButtonControlConcentrationEnable.isChecked():
					#value = int(packet['affectiv']['excitement'] * 100)
					#self.progressBarControlConcentration.setValue(value)
			
			#elif ('longTermExcitement' in packet['affectiv']):
				#if self.pushButtonControlConcentrationEnable.isChecked():
					#value = int(packet['affectiv']['longTermExcitement'] * 100)
					#self.progressBarControlConcentration.setValue(value)
			
			#if ('meditation' in packet['affectiv']) and tabVisible:
				#if self.pushButtonControlRelaxationEnable.isChecked():
					#value = int(packet['affectiv']['meditation'] * 100)
					#self.progressBarControlRelaxation.setValue(value)
			
			##if ('frustration' in packet['affectiv']):
				##self.textEditDebugConsole.append("frustration: %.2f" % \
				                                  ##packet['affectiv']['frustration'])
			
			##if ('engagementBoredom' in packet['affectiv']):
				##self.textEditDebugConsole.append("engagementBoredom: %.2f" % \
				                                  ##packet['affectiv']['engagementBoredom'])
			
			#if MATPLOTLIB_AVAILABLE:
				#self.historyEEGEmotivAffectiv.updateValues('affectiv', packet['affectiv'])
				#if (self.parent.tabWidget.currentIndex() == self.tabIndex):
					#self.historyEEGEmotivAffectiv.updateFigure('affectiv', packet['affectiv'])
		
		
		#if ('cognitiv' in packet.keys()):
			
			##if ('currentAction' in packet['cognitiv']):
				##self.textEditDebugConsole.append("currentAction: %i" % \
				                                  ##packet['cognitiv']['currentAction'])
			
			##if ('currentActionPower' in packet['cognitiv']):
				##self.textEditDebugConsole.append("currentActionPower: %.2f" % \
				                                  ##packet['cognitiv']['currentActionPower'])
			
			#if MATPLOTLIB_AVAILABLE:
				##print packet['cognitiv']
				#self.historyEEGEmotivCognitiv.updateValues('cognitiv', packet['cognitiv']['currentActionPower'])
				#if (self.parent.tabWidget.currentIndex() == self.tabIndex):
					#self.historyEEGEmotivCognitiv.updateFigure('cognitiv', packet['cognitiv']['currentActionPower'])
	
	
	
	##################################################################
	
	def setPacketCount(self, value):
		
		self.packet_count = value
	
	
	##################################################################
	
	def setBadPackets(self, value):
		
		self.bad_packets = value
	
	
	##################################################################
	
	def incrementPacketCount(self):
		
		self.packet_count += 1
	
	
	##################################################################
	
	def incrementBadPackets(self):
		
		self.bad_packets += 1
	
	
	##################################################################
	
	def getPacketCount(self):
		
		return (self.packet_count)
	
	
	##################################################################
	
	def getBadPackets(self):
		
		return (self.bad_packets)
	
	
	##################################################################
	
	def getSessionTime(self):
		
		return (self.parent.plugin_session.session_start_timestamp)
	
	
	##################################################################
	
	def resetSessionStartTime(self):
	
		#self.synapseServer.protocol.resetSessionStartTime()
		self.parent.plugin_session.resetSessionStartTime()
	
	
	##################################################################
	
	def resetData(self):
		
		self.packets['rawEeg'] = []
		self.packets['signals'] = []
		
		#self.synapseServer.protocol.resetSessionStartTime()
		#self.parent.plugin_session.resetSessionStartTime()
		self.resetSessionStartTime()
		
		
		self.setPacketCount(0)
		self.setBadPackets(0)
		#self.packet_count = 0
		#self.bad_packets = 0
		
		#self.synapseServer.protocol.packet_count = 0
		#self.synapseServer.protocol.bad_packets = 0
		
		self.updateProfileSessionStatus()
		
		#try:
			#self.textEditDebugConsole.setText("")
		#except:
			#pass
		
		if MATPLOTLIB_AVAILABLE:
			self.historyEEGThinkGear.resetData()
			self.historyEEGEmotivCognitiv.resetData()
			self.historyEEGEmotivAffectiv.resetData()
	
	
	##################################################################
	
	def processCustomData(self, packet):
		
		# NOTE: The trigger should move away from being EEG-based
		#         in favor of a Timer
		
		packet['custom'] = {}
		
		for plugin in self.parent.activePlugins:
			if 'EEG' in plugin.protocolSupport:
				packet = plugin.processCustomData(packet)
		
		
		return(packet)
	
	
	##################################################################
	
	def processPacketForExport(self, packet={}, output={}):
		
		if self.synapseServer != None:
			output = self.synapseServer.processPacketForExport(packet, output)
		
		return(output)
	
	
	##################################################################
	
	def stop(self):
		
		if self.synapseClient != None:
			self.synapseClient.exitThread()
		
		if self.synapseServer != None:
			self.stopSynapseServer()
			self.synapseServer.exitThread()


#####################################################################
# Functions
#####################################################################

#####################################################################
# Main
#####################################################################

#if __name__ == '__main__':
	
	#pass

