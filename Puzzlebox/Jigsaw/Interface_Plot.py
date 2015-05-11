# -*- coding: utf-8 -*-

# Copyright Puzzlebox Productions, LLC (2010-2012)
#
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html

__changelog__ = """\
Last Update: 2013.07.25
"""

import os, sys

import Puzzlebox.Jigsaw.Configuration as configuration
import Puzzlebox.Synapse.Configuration as synapse_configuration

# Note: suggested work-around for multiple versions of Python installed
#if (sys.platform != 'darwin'):
#	sys.path.reverse


### IMPORTS ###
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties 
from numpy import arange, sin, pi

try:
	from scipy import *
	from scipy.fftpack import fftshift, fftfreq
except:
	print "ERROR: [Jigsaw:Interface_Plot] Exception importing SciPy"


if (sys.platform != 'darwin'):
	from pylab import *
else:
	from matplotlib.pylab import *


if configuration.ENABLE_PYSIDE:
	try:
		#import PySide as PyQt4
		from PySide import QtCore, QtGui
	except:
		print "ERROR: [Jigsaw:Interface_Plot] Exception importing PySide:",
		print e
		configuration.ENABLE_PYSIDE = False
	else:
		print "INFO: [Jigsaw:Interface_Plot] Using PySide module"
		os.environ["QT_API"] = "pyside"
		# Required for Windows
		import matplotlib
		matplotlib.use("Qt4Agg")

if not configuration.ENABLE_PYSIDE:
	print "INFO: [Jigsaw:Interface_Plot] Using PyQt4 module"
	from PyQt4 import QtCore, QtGui



#####################################################################
# Globals
#####################################################################

DEBUG = 1

INTERFACE_RAW_EEG_UPDATE_FREQUENCY = 512


#####################################################################
# Classes
#####################################################################

class matplotlibCanvas(FigureCanvasQTAgg):
	
	"""Ultimately, this is a QWidget (as well as a FigureCanvasQTAgg, etc.)."""
	
	def __init__(self, parent=None, width=800, height=400, dpi=100, title=None):
		
		width = width / float(dpi)
		height = height / float(dpi)
		
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		# We want the axes cleared every time plot() is called
		self.axes.hold(False)
		
		if title != None:
			fig.suptitle(title, fontsize=12)
		
		FigureCanvasQTAgg.__init__(self, fig)
		self.setParent(parent)
		
		FigureCanvasQTAgg.setSizePolicy(self,
											QtGui.QSizePolicy.Expanding,
											QtGui.QSizePolicy.Expanding)
		FigureCanvasQTAgg.updateGeometry(self)


#####################################################################
#####################################################################

class dualMatplotlibCanvas(FigureCanvasQTAgg):
	
	"""Ultimately, this is a QWidget (as well as a FigureCanvasQTAgg, etc.)."""
	
	def __init__(self, parent=None, width=800, height=400, dpi=100, title=None):
		
		width = width / float(dpi)
		height = height / float(dpi)
		
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes_top = fig.add_subplot(211)
		self.axes_bottom = fig.add_subplot(212)
		# We want the axes cleared every time plot() is called
		self.axes_top.hold(False)
		self.axes_bottom.hold(False)
		
		if title != None:
			fig.suptitle(title, fontsize=12)
		
		FigureCanvasQTAgg.__init__(self, fig)
		self.setParent(parent)
		
		FigureCanvasQTAgg.setSizePolicy(self,
											QtGui.QSizePolicy.Expanding,
											QtGui.QSizePolicy.Expanding)
		FigureCanvasQTAgg.updateGeometry(self)


#####################################################################
#####################################################################

class rawEEGMatplotlibCanvas(dualMatplotlibCanvas):
	
	'''Graphs Raw EEG Values'''
	
	#def __init__(self, *args, **kwargs):
	
	def __init__(self, parent=None, \
	             width=800, height=400, \
	             title='Raw EEG Waves', \
	             axes_top_text="1.0 seconds", \
	             axes_bottom_text="0.5 seconds", \
	             top_color="b-", \
	             bottom_color="r-", \
	             facecolor=(0,0,0)):
		
		dualMatplotlibCanvas.__init__(self, parent=parent, width=width, height=height, title=title)
		
		self.DEBUG=DEBUG
		
		#timer = QtCore.QTimer(self)
		#QtCore.QObject.connect(timer, QtCore.SIGNAL("timeout()"), self.updateFigure)
		#timer.start(256)
		
		self.axes_top_text=axes_top_text
		self.axes_bottom_text=axes_bottom_text
		self.top_color = top_color
		self.bottom_color = bottom_color
		
		self.update_top_frequency = \
		   INTERFACE_RAW_EEG_UPDATE_FREQUENCY
		self.update_bottom_frequency = \
		   INTERFACE_RAW_EEG_UPDATE_FREQUENCY / 2
		
		self.values_top = []
		self.values_bottom = []
		
		self.axes_top.set_xbound(0, self.update_top_frequency)
		self.axes_top.set_ybound(-2048, 2047)
		
		self.axes_bottom.set_xbound(0, self.update_bottom_frequency)
		self.axes_bottom.set_ybound(-512, 512)
		
		self.axes_top.grid(True)
		self.axes_bottom.grid(True)
		
		self.axes_top.text(self.update_top_frequency + 24, \
		                   0, \
		                   self.axes_top_text, \
		                   rotation='vertical', \
		                   verticalalignment='center')
		
		self.axes_bottom.text(self.update_bottom_frequency + 12, \
		                   0, \
		                   self.axes_bottom_text, \
		                   rotation='vertical', \
		                   verticalalignment='center')
		
		self.axes_top.set_autoscale_on(False)
		self.axes_bottom.set_autoscale_on(False)
		
		self.axes_top.set_xticklabels([])
		self.axes_top.set_yticklabels([])
		self.axes_bottom.set_xticklabels([])
		self.axes_bottom.set_yticklabels([])
		
		#self.figure.set_frameon(False)
		self.facecolor=facecolor
		self.figure.set_facecolor(self.facecolor)
	
	
	##################################################################
	
	def updateValues(self, value):
		
		self.values_top.append(value)
		self.values_bottom.append(value)
		
		if len(self.values_top) == self.update_top_frequency:
			self.update_top_figure()
		
		if len(self.values_bottom) == self.update_bottom_frequency:
			self.update_bottom_figure()
	
	
	##################################################################
	
	def update_top_figure(self): 
		
		self.axes_top.plot(range(self.update_top_frequency), \
		                   self.values_top, \
		                   self.top_color, \
		                   scalex=False, \
		                   scaley=False)
		
		#self.axes_top.set_ylabel('%i Hz' % self.update_top_frequency)
		self.axes_top.grid(True)
		
		self.axes_top.text(self.update_top_frequency + 24, \
		                   0, \
		                   self.axes_top_text, \
		                   rotation='vertical', \
		                   verticalalignment='center')
		
		self.axes_top.set_xticklabels([])
		self.axes_top.set_yticklabels([])
		
		#self.figure.set_frameon(False)
		self.figure.set_facecolor(self.facecolor)
		
		self.draw()
		
		self.values_top = []
	
	
	##################################################################
	
	def update_bottom_figure(self):
		
		self.axes_bottom.plot(range(self.update_bottom_frequency), \
		                      self.values_bottom, \
		                      self.bottom_color, \
		                      scalex=False, \
		                      scaley=False)
		
		#self.axes_bottom.set_ylabel('%i Hz' % self.update_bottom_frequency)
		self.axes_bottom.grid(True)
		
		self.axes_bottom.text(self.update_bottom_frequency + 12, \
		                      0, \
		                      self.axes_bottom_text, \
		                      rotation='vertical', \
		                      verticalalignment='center')
		
		self.axes_bottom.set_xticklabels([])
		self.axes_bottom.set_yticklabels([])
		
		#self.figure.set_frameon(False)
		self.figure.set_facecolor(self.facecolor)
		
		self.draw()
		
		self.values_bottom = []


#####################################################################
#####################################################################

class historyEEGMatplotlibCanvas(matplotlibCanvas):
	
	'''Draws 30-Second History of eSense Values'''
	
	def __init__(self, parent=None, \
	             width=800, height=400, \
	             title='EEG Brain Signals', \
	             axes_right_text='eSense Values', \
	             facecolor=(0,0,0)):
		
		matplotlibCanvas.__init__(self, parent=parent, width=width, height=height, title=title)
		
		self.DEBUG=DEBUG
		
		self.axes_right_text=axes_right_text
		
		self.graph_length = 30
		
		self.values_esense = {'attention': [], \
		                      'meditation': []}
		
		for key in self.values_esense.keys():
			for x in range(self.graph_length):
				self.values_esense[key].append(0)
		
		
		self.axes.set_xbound(self.graph_length, 0)
		self.axes.set_ybound(0, 100)
		
		self.axes.set_autoscale_on(False)
		
		label_values = self.axes.plot(range(self.graph_length), \
		                  self.values_esense['attention'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['attention'], \
		                  self.values_esense['meditation'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['meditation'], \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.text(self.graph_length + 1, \
		                   50, \
		                   self.axes_right_text, \
		                   rotation='vertical', \
		                   verticalalignment='center')
		
		self.axes.set_xticklabels([])
		#self.axes.set_yticks([0,20,40,50,60,80,100])
		self.axes.set_yticks([0,20,40,60,80,100])
		#self.axes.set_yticklabels(['0','','','50','','','100'])
		self.axes.set_yticklabels([])
		
		self.axes.grid(True)
		
		self.font_properties = FontProperties(size=8)
		
		self.axes.legend( \
			(label_values[0], label_values[1]), \
			#('Attention', 'Meditation'), \
			('Concentration', 'Relaxation'), \
			loc='lower left', \
			prop=self.font_properties)
		
		#self.figure.set_frameon(False)
		self.facecolor=facecolor
		self.figure.set_facecolor(self.facecolor)
	
	
	##################################################################
	
	def updateValues(self, index, values):
		
		for key in values.keys():
			
			self.values_esense[key].append(values[key])
			self.values_esense[key] = \
				self.values_esense[key][1:]
	
	
	##################################################################
	
	def updateFigure(self, index, values):
		
		valuesAttention = self.values_esense['attention']
		valuesMeditation = self.values_esense['meditation']
		
		#print "a:"
		#print valuesAttention
		
		#print "m:"
		#print valuesMeditation
		
		#print
		
		# Fix for "ValueError: x and y must have same first dimension"
		while ( len(valuesAttention) > ( len(valuesMeditation)) ):
			#print "a>m"
			valuesMeditation.append( valuesMeditation[-1] )
		while ( len(valuesAttention) < ( len(valuesMeditation)) ):
			#print "a<m"
			valuesAttention.append( valuesAttention[-1] )
		
		label_values = self.axes.plot(range(self.graph_length), \
		                  valuesAttention, \
		                  synapse_configuration.INTERFACE_CHART_STYLES['attention'], \
		                  valuesMeditation, \
		                  synapse_configuration.INTERFACE_CHART_STYLES['meditation'], \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.grid(True)
		
		self.axes.text(self.graph_length + 1, \
		                      50, \
		                      self.axes_right_text, \
		                      rotation='vertical', \
		                      verticalalignment='center')
		
		try:
			self.axes.set_xticklabels([])
			self.axes.set_yticklabels([])
		except Exception, e:
			print str(e)
		
		self.axes.legend( \
			(label_values[0], label_values[1]), \
#			('Attention', 'Meditation'), \
			('Concentration', 'Relaxation'), \
			loc='lower left', \
			prop=self.font_properties)
		
		#self.figure.set_frameon(False)
		self.figure.set_facecolor(self.facecolor)
		
		self.draw()
	
	
	##################################################################
	
	def resetData(self):
		
		self.values_esense = {'attention': [], \
		                      'meditation': []}
		
		for key in self.values_esense.keys():
			for x in range(self.graph_length):
				self.values_esense[key].append(0)


#####################################################################
#####################################################################

class chartEEGMatplotlibCanvas(matplotlibCanvas):
	
	'''Draws EEG Power Bands'''
	
	def __init__(self, parent=None, \
	             width=800, height=400, \
	             title='EEG Brain Signals'):
		
		matplotlibCanvas.__init__(self, parent=parent, width=width, height=height, title=title)
		
		self.DEBUG=DEBUG
		
		self.graph_length = 30
		
		self.values_eeg_bands = {}
		
		for key in synapse_configuration.THINKGEAR_EEG_POWER_BAND_ORDER:
			self.values_eeg_bands[key] = []
			for x in range(self.graph_length):
				self.values_eeg_bands[key].append(0)
		
		self.values_esense = {'attention': [], \
		                      'meditation': []}
		
		for key in self.values_esense.keys():
			for x in range(self.graph_length):
				self.values_esense[key].append(0)
		
		self.axes_top.set_xbound(self.graph_length, 0)
		self.axes_top.set_ybound(0, 100)
		
		self.axes_bottom.set_xbound(self.graph_length, 0)
		self.axes_bottom.set_ybound(0, 100)
		
		self.axes_top.grid(True)
		self.axes_bottom.grid(True)
		
		self.axes_top.text(self.graph_length + 1, \
		                   50, \
		                   'Frequency Bands', \
		                   rotation='vertical', \
		                   verticalalignment='center')
		
		self.axes_bottom.text(self.graph_length + 1, \
		                   50, \
		                   'eSense Values', \
		                   rotation='vertical', \
		                   verticalalignment='center')
		
		self.axes_top.set_autoscale_on(False)
		self.axes_bottom.set_autoscale_on(False)
	
	
	##################################################################
	
	def updateValues(self, index, values):
		
		if (index == 'eegPower'):
			
			for key in values.keys():
				self.values_eeg_bands[key].append(values[key])
				self.values_eeg_bands[key] = \
					self.values_eeg_bands[key][1:]		
		
		
		elif (index == 'eSense'):
			
			for key in values.keys():
				
				self.values_esense[key].append(values[key])
				self.values_esense[key] = \
					self.values_esense[key][1:]
	
	
	##################################################################
	
	def updateFigure(self, index, values):
		
		if (index == 'eegPower'):
			
			label_values = self.axes_top.plot(range(self.graph_length), \
			                   #self.values_eeg_bands['delta'], \
			                   #configuration.INTERFACE_CHART_STYLES['delta'], \
			                   #self.values_eeg_bands['theta'], \
			                   #configuration.INTERFACE_CHART_STYLES['theta'], \
			                   self.values_eeg_bands['lowAlpha'], \
			                   configuration.INTERFACE_CHART_STYLES['lowAlpha'], \
			                   self.values_eeg_bands['highAlpha'], \
			                   configuration.INTERFACE_CHART_STYLES['highAlpha'], \
			                   self.values_eeg_bands['lowBeta'], \
			                   configuration.INTERFACE_CHART_STYLES['lowBeta'], \
			                   self.values_eeg_bands['highBeta'], \
			                   configuration.INTERFACE_CHART_STYLES['highBeta'], \
			                   #self.values_eeg_bands['lowGamma'], \
			                   #configuration.INTERFACE_CHART_STYLES['lowGamma'], \
			                   #self.values_eeg_bands['highGamma'], \
			                   #configuration.INTERFACE_CHART_STYLES['highGamma'], \
			                   scalex=False, \
			                   scaley=True)
			
			self.axes_top.grid(True)
			
			self.axes_top.text(self.graph_length + 1, \
			                   50, \
			                   '                            Frequency Bands', \
			                   rotation='vertical', \
			                   verticalalignment='center')
			
			self.axes_top.legend( \
			   (label_values[0], label_values[1], label_values[2], label_values[3]), \
			   ('LowAlpha', 'HighAlpha', 'LowBeta', 'HighBeta'), \
			   loc='center left')
			
			self.draw()
		
		
		elif (index == 'eSense'):
			
			label_values = self.axes_bottom.plot(range(self.graph_length), \
			                      self.values_esense['attention'], \
			                      configuration.INTERFACE_CHART_STYLES['attention'], \
			                      self.values_esense['meditation'], \
			                      configuration.INTERFACE_CHART_STYLES['meditation'], \
			                      scalex=False, \
			                      scaley=False)
			
			
			self.axes_bottom.grid(True)
			
			self.axes_bottom.text(self.graph_length + 1, \
			                      50, \
			                      'eSense Values', \
			                      rotation='vertical', \
			                      verticalalignment='center')
			
			self.axes_bottom.legend( \
			   (label_values[0], label_values[1]), \
			   ('Attention', 'Meditation'), \
			   loc='lower left')
			
			self.draw()


#####################################################################
#####################################################################

class fftEEGMatplotlibCanvas(matplotlibCanvas):
	
	'''Draws FFT of Raw EEG Values'''
	
	def __init__(self, parent=None, \
	             width=800, height=400, \
	             title='EEG Raw Signals FFT', \
	             axes_right_text='EEG Raw Signals FFT', \
	             facecolor=(0,0,0)):
		
		matplotlibCanvas.__init__(self, parent=parent, width=width, height=height, title=title)
		
		self.DEBUG=DEBUG
		
		#self.axes_right_text=axes_right_text
		
		#self.graph_length = 30
		self.graph_length = 512
		#self.graph_length = 1000
		
		self.values = []
		
		
		x=arange(0,1,0.001)
		y01=sin(2*pi*x*2)+sin(2*pi*x*6)+sin(2*pi*x*15)+sin(2*pi*x*30)
		#y02=fft(y01)
		#y02=abs(fft(y01))
		#y02=fftshift(fft(y01))
		y02=abs(fftshift(fft(y01)))
		#self.values = y02[:512]
		#self.values = y02
		
		
		#for key in self.values.keys():
			#for x in range(self.graph_length):
				#self.values[key].append(0)
		
		
		# hertz2
		#subplot(grid_rows,grid_columns,chart)
		#plot(x,y02,linewidth=1.5,color='b',lod=False)
		#axis([0.5,0.55,0,600])
		
		label_values = self.axes.plot( \
		                  x, \
		                  #self.values, \
		                  y02, \
		                  synapse_configuration.INTERFACE_CHART_STYLES['FFT'], \
		                  scalex=False, \
		                  scaley=True)
		
		#self.axes.text(self.graph_length + 1, \
		                   #50, \
		                   #self.axes_right_text, \
		                   #rotation='vertical', \
		                   #verticalalignment='center')
		
		
		#self.axes.set_xbound(self.graph_length, 0)
		self.axes.set_xbound(0.5, 0.55)
		self.axes.set_ybound(0, 600)
		
		self.axes.grid(True)
		
		#self.axes.set_autoscale_on(False)
		self.axes.set_autoscale_on(True)
		
		
		#self.axes.set_xticks([0, 5, 10, 15, 20, 25, 30])
		self.axes.set_xticks([.500, .505, .510, .515, .520, .525, .530, .535, .540, .545, .55])
		self.axes.set_xticklabels([])
		#self.axes.set_xticklabels([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
		#self.axes.set_yticks([0,100,200,300,400,500,600])
		self.axes.set_yticks([])
		#self.axes.set_yticklabels(['0','','','50','','','100'])
		self.axes.set_yticklabels([])
		
		self.font_properties = FontProperties(size=4)
		
		#self.axes.legend( \
			#(label_values[0], label_values[1]), \
			##('Attention', 'Meditation'), \
			#('Concentration', 'Relaxation'), \
			#loc='lower left', \
			#prop=self.font_properties)
		
		#self.figure.set_frameon(False)
		self.facecolor=facecolor
		self.figure.set_facecolor(self.facecolor)
	
	
	##################################################################
	
	def update_value(self, value):
		
		self.values.append(value)
		
		#print len(self.values)
		#print self.graph_length
		
		if len(self.values) == self.graph_length:
			self.updateFigure()
	
	
	##################################################################
	
	def updateFigure(self):
		
		
		#x=arange(0,1,0.001)
		x = self.values[:]
		
		#y01=sin(2*pi*x*2)+sin(2*pi*x*6)+sin(2*pi*x*15)+sin(2*pi*x*30)
		#y01=sin(2*pi*x*2)
		y01 = x
		
		#y02=fft(y01)
		#y02=abs(fft(y01))
		#y02=fftshift(fft(y01))
		y02=abs(fftshift(fft(y01)))
		
		
		#print x
		#print
		#print y02
		#print
		#print
		
		
		label_values = self.axes.plot( \
		                  #range(self.graph_length), \
		                  x, \
		                  y02, \
		                  synapse_configuration.INTERFACE_CHART_STYLES['FFT'], \
		                  scalex=False, \
		                  scaley=True)
		
		#self.axes.text(self.graph_length + 1, \
		                      #50, \
		                      #self.axes_right_text, \
		                      #rotation='vertical', \
		                      #verticalalignment='center')
		
		#self.axes.set_xticklabels([])
		#self.axes.set_yticklabels([])
		
		
		##self.axes.set_xbound(self.graph_length, 0)
		#self.axes.set_xbound(0.5, 0.55)
		#self.axes.set_ybound(0, 600)
		
		self.axes.grid(True)
		
		#self.axes.set_autoscale_on(False)
		self.axes.set_autoscale_on(True)
		
		
		#self.axes.set_xticks([0, 5, 10, 15, 20, 25, 30])
		#self.axes.set_xticks([.500, .505, .510, .515, .520, .525, .530, .535, .540, .545, .55])
		self.axes.set_xticklabels([])
		#self.axes.set_xticklabels([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
		#self.axes.set_yticks([0,100,200,300,400,500,600])
		self.axes.set_yticks([])
		#self.axes.set_yticklabels(['0','','','50','','','100'])
		self.axes.set_yticklabels([])
		
		
		#self.axes.legend( \
			#(label_values[0], label_values[1]), \
##			('Attention', 'Meditation'), \
			#('Concentration', 'Relaxation'), \
			#loc='lower left', \
			#prop=self.font_properties)
		
		#self.figure.set_frameon(False)
		self.figure.set_facecolor(self.facecolor)
		
		self.draw()
		
		self.values = []


#####################################################################
#####################################################################

class historyEEGEmotivAffectiv(matplotlibCanvas):
	
	'''Draws 30-Second History of Emotiv Affectiv Values'''
	
	def __init__(self, parent=None, \
	             width=800, height=400, \
	             title='EEG Brain Signals', \
	             axes_right_text='Affectiv Values', \
	             facecolor=(0,0,0)):
		
		matplotlibCanvas.__init__(self, parent=parent, width=width, height=height, title=title)
		
		self.DEBUG=DEBUG
		
		self.axes_right_text=axes_right_text
		
		self.graph_length = 30 * 4 # (four updates per second)
		
		self.signals = {'excitement': [], \
		                'longTermExcitement': [], \
		                'meditation': [], \
		                'frustration': [], \
		                'engagementBoredom': []}
		
		for key in self.signals.keys():
			for x in range(self.graph_length):
				self.signals[key].append(0)
		
		
		self.axes.set_xbound(self.graph_length, 0)
		self.axes.set_ybound(0, 100)
		
		self.axes.set_autoscale_on(False)
		
		label_values = self.axes.plot(range(self.graph_length), \
		                  self.signals['excitement'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['excitement'], \
		                  self.signals['longTermExcitement'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['longTermExcitement'], \
		                  self.signals['meditation'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['meditation'], \
		                  self.signals['frustration'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['frustration'], \
		                  self.signals['engagementBoredom'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['engagementBoredom'], \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.text(self.graph_length + 1, \
		                   50, \
		                   self.axes_right_text, \
		                   rotation='vertical', \
		                   verticalalignment='center')
		
		self.axes.set_xticklabels([])
		#self.axes.set_yticks([0,20,40,50,60,80,100])
		self.axes.set_yticks([0,20,40,60,80,100])
		#self.axes.set_yticklabels(['0','','','50','','','100'])
		self.axes.set_yticklabels([])
		
		self.axes.grid(True)
		
		self.font_properties = FontProperties(size=6)
		
		self.axes.legend( \
			(label_values[0], label_values[1], label_values[2], label_values[3], label_values[4]), \
			('Instantaneous Excitement', 'Long Term Excitement', 'Meditation', 'Frustration', 'Engagement/Boredom'), \
			loc='lower left', \
			prop=self.font_properties)
		
		#self.figure.set_frameon(False)
		self.facecolor=facecolor
		self.figure.set_facecolor(self.facecolor)
	
	
	##################################################################
	
	def updateValues(self, index, values):
		
		for key in values.keys():
			
			value = int(values[key] * 100)
			
			self.signals[key].append(value)
			self.signals[key] = \
				self.signals[key][1:]
	
	
	##################################################################
	
	def updateFigure(self, index, values):
		
		label_values = self.axes.plot(range(self.graph_length), \
		                  self.signals['excitement'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['excitement'], \
		                  self.signals['longTermExcitement'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['longTermExcitement'], \
		                  self.signals['meditation'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['meditation'], \
		                  self.signals['frustration'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['frustration'], \
		                  self.signals['engagementBoredom'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['engagementBoredom'], \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.grid(True)
		
		self.axes.text(self.graph_length + 1, \
		                      50, \
		                      self.axes_right_text, \
		                      rotation='vertical', \
		                      verticalalignment='center')
		
		self.axes.set_xticklabels([])
		self.axes.set_yticklabels([])
		
		self.axes.legend( \
			(label_values[0], label_values[1], label_values[2], label_values[3], label_values[4]), \
			('Instantaneous Excitement', 'Long Term Excitement', 'Meditation', 'Frustration', 'Engagement/Boredom'), \
			loc='lower left', \
			prop=self.font_properties)
		
		#self.figure.set_frameon(False)
		self.figure.set_facecolor(self.facecolor)
		
		self.draw()
	
	
	##################################################################
	
	def resetData(self):
		
		self.signals = {'excitement': [], \
		                'longTermExcitement': [], \
		                'meditation': [], \
		                'frustration': [], \
		                'engagementBoredom': []}
		
		for key in self.signals.keys():
			for x in range(self.graph_length):
				self.signals[key].append(0)


#####################################################################
#####################################################################

class historyEEGEmotivCognitiv(matplotlibCanvas):
	
	'''Draws 30-Second History of Cognitiv Values'''
	
	def __init__(self, parent=None, \
	             width=800, height=400, \
	             title='EEG Brain Signals', \
	             axes_right_text='Cognitiv Values', \
	             legend_values=['Cognitiv'], \
	             facecolor=(0,0,0)):
		
		matplotlibCanvas.__init__(self, parent=parent, width=width, height=height, title=title)
		
		self.DEBUG=DEBUG
		
		self.axes_right_text=axes_right_text
		self.legend_values=legend_values
		
		self.graph_length = 30 * 4 # (four updates per second)
		
		self.signals = {'cognitiv': []}
		#self.signals = {'neutral': [], \
		                #'push': [], \
		                #'meditation': [], \
		                #'frustration': [], \
		                #'engagementBoredom': []}
		
		for key in self.signals.keys():
			for x in range(self.graph_length):
				self.signals[key].append(0)
		
		
		self.axes.set_xbound(self.graph_length, 0)
		self.axes.set_ybound(0, 100)
		
		self.axes.set_autoscale_on(False)
		
		self.font_properties = FontProperties(size=6)
		
		label_values = self.axes.plot( \
		                  range(self.graph_length), \
		                  self.signals['cognitiv'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['cognitiv'], \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.legend( \
		   [label_values[0]], \
		    self.legend_values, \
		    loc='lower left', \
		    prop=self.font_properties)
		
		self.axes.text(self.graph_length + 1, \
		               50, \
		               self.axes_right_text, \
		               rotation='vertical', \
		               verticalalignment='center')
		
		self.axes.grid(True)
		self.axes.set_xticklabels([])
		#self.axes.set_yticks([0,20,40,50,60,80,100])
		self.axes.set_yticks([0,20,40,60,80,100])
		#self.axes.set_yticklabels(['0','','','50','','','100'])
		self.axes.set_yticklabels([])
		
		#self.figure.set_frameon(False)
		self.facecolor=facecolor
		self.figure.set_facecolor(self.facecolor)
	
	
	##################################################################
	
	def updateValues(self, index, value):
		
		value = int(value * 100)
		
		self.signals['cognitiv'].append(value)
		self.signals['cognitiv'] = \
		   self.signals['cognitiv'][1:]
	
	#def updateValues(self, index, values):
		
		#for key in values.keys():
			
			#value = int(values[key] * 100)
			
			#self.signals[key].append(value)
			#self.signals[key] = \
				#self.signals[key][1:]
	
	
	##################################################################
	
	def updateFigure(self, index, values):
		
		label_values = self.axes.plot( \
		                  range(self.graph_length), \
		                  self.signals['cognitiv'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['cognitiv'], \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.legend( \
		   [label_values[0]], \
		    self.legend_values, \
		    loc='lower left', \
		    prop=self.font_properties)
		
		self.axes.text(self.graph_length + 1, \
		               50, \
		               self.axes_right_text, \
		               rotation='vertical', \
		               verticalalignment='center')
		
		self.axes.grid(True)
		self.axes.set_xticklabels([])
		self.axes.set_yticklabels([])
		
		#self.figure.set_frameon(False)
		self.figure.set_facecolor(self.facecolor)
		
		self.draw()
	
	
	##################################################################
	
	def setLegend(self, labels):
		
		self.legend_values = labels
	
	
	##################################################################
	
	def resetData(self):
		
		self.signals = {'cognitiv': []}
		
		for key in self.signals.keys():
			for x in range(self.graph_length):
				self.signals[key].append(0)


#####################################################################
#####################################################################

class trendingMatplotlibCanvas(matplotlibCanvas):
	
	'''Draws 30-Second History of Trending Values'''
	
	def __init__(self, parent=None, \
	             width=400, height=200, \
	             title='Trending Signals', \
	             axes_right_text='Trending Values', \
	             legend_values=['Trending'], \
	             facecolor=(0,0,0), \
	             indexTrigger=72):
		
		# NOTE: Hack
		if width > 360:
			width=360
		
		if height > 160:
			height=160
		
		#width=200
		#height=100
		
		matplotlibCanvas.__init__(self, parent=parent, width=width, height=height, title=title)
		
		self.DEBUG=DEBUG
		
		self.axes_right_text=axes_right_text
		self.legend_values=legend_values
		
		self.graph_length = 30
		
		self.signals = {'trending': []}
		
		for key in self.signals.keys():
			for x in range(self.graph_length):
				self.signals[key].append(0)
		
		
		self.axes.set_xbound(self.graph_length, 0)
		self.axes.set_ybound(0, 100)
		
		self.axes.set_autoscale_on(False)
		
		self.font_properties = FontProperties(size=6)
		
		label_values = self.axes.plot( \
		                  range(self.graph_length), \
		                  self.signals['trending'], \
		                  synapse_configuration.INTERFACE_CHART_STYLES['trendingBlack'], \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.legend( \
		   [label_values[0]], \
		    self.legend_values, \
		    loc='lower left', \
		    prop=self.font_properties)
		
		self.axes.text(self.graph_length + 1, \
		               50, \
		               self.axes_right_text, \
		               rotation='vertical', \
		               verticalalignment='center')
		
		
		self.axes.grid(True)
		self.axes.set_xticklabels([])
		#self.axes.set_yticks([0,20,40,50,60,80,100])
		self.axes.set_yticks([0,20,40,60,80,100])
		#self.axes.set_yticklabels(['0','','','50','','','100'])
		self.axes.set_yticklabels([])
		
		#self.figure.set_frameon(False)
		self.facecolor=facecolor
		self.figure.set_facecolor(self.facecolor)
		
		self.indexTrigger = indexTrigger
	
	
	##################################################################
	
	def updateValues(self, index='trending', value=0):
		
		#value = int(value * 100)
		
		self.signals[index].append(value)
		self.signals[index] = \
		   self.signals[index][1:]
	
	
	##################################################################
	
	def calculateChartStyle(self, value, warning_zone_percentage=0.20):
		
		if value >= self.indexTrigger:
			
			style = synapse_configuration.INTERFACE_CHART_STYLES['trendingGreen']
		
		
		elif int(value * warning_zone_percentage) >= self.indexTrigger:
		
			style = synapse_configuration.INTERFACE_CHART_STYLES['trendingBlack']
		
		else:
			
			style = synapse_configuration.INTERFACE_CHART_STYLES['trendingRed']
		
		
		return(style)
	
	
	##################################################################
	
	def updateFigure(self, warning_zone_percentage=0.20):
		
		style = self.calculateChartStyle(self.signals['trending'][-1], \
		                                 warning_zone_percentage)
		
		label_values = self.axes.plot( \
		                  range(self.graph_length), \
		                  self.signals['trending'], \
		                  style, \
		                  scalex=False, \
		                  scaley=False)
		
		self.axes.legend( \
		   [label_values[0]], \
		    self.legend_values, \
		    loc='lower left', \
		    prop=self.font_properties)
		
		self.axes.text(self.graph_length + 1, \
		               50, \
		               self.axes_right_text, \
		               rotation='vertical', \
		               verticalalignment='center')
		
		self.axes.grid(True)
		self.axes.set_xticklabels([])
		self.axes.set_yticklabels([])
		
		#self.figure.set_frameon(False)
		self.figure.set_facecolor(self.facecolor)
		
		self.draw()
	
	
	##################################################################
	
	def setLegend(self, labels):
		
		self.legend_values = labels
	
	
	##################################################################
	
	def resetData(self):
		
		self.signals = {'trending': []}
		
		for key in self.signals.keys():
			for x in range(self.graph_length):
				self.signals[key].append(0)

