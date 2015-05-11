#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Puzzlebox - Jigsaw - Script - Update Interface Pyside
#
# Copyright Puzzlebox Productions, LLC (2011)

__changelog__ = """\
Last Update: 2011.12.25
"""

import sys

#####################################################################
# Globals
#####################################################################

DEFAULT_INPUT_FILE = 'Puzzlebox/Jigsaw/Design_Interface.py'
DEFAULT_OUTPUT_FILE = 'Puzzlebox/Jigsaw/Design_Interface.py'

REPLACE_STRINGS = { \
	'from PyQt4 import QtCore, QtGui\n': \
	 """
import Configuration as configuration

if configuration.ENABLE_PYSIDE:
	try:
		#import PySide as PyQt4
		from PySide import QtCore, QtGui, QtNetwork, QtWebKit
	except Exception, e:
		print "ERROR: Exception importing PySide:",
		print e
		configuration.ENABLE_PYSIDE = False
	else:
		print "INFO: [Jigsaw:__MODULE_NAME__] Using PySide module"

if not configuration.ENABLE_PYSIDE:
	print "INFO: [Jigsaw:__MODULE_NAME__] Using PyQt4 module"
	from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit

#try:
  #from PySide import QtCore, QtGui, QtWebKit
#except:
  #from PyQt4 import QtCore, QtGui, QtWebKit
""", \

	'from PyQt4 import QtWebKit\n': \
		'#from PyQt4 import QtWebKit\n', \

	'		self.gridLayout_2.setMargin(0)\n': \
		'#		self.gridLayout_2.setMargin(0)\n', \

	'		self.verticalLayout.setMargin(10)\n': \
		'#		self.verticalLayout.setMargin(10)\n', \

	'		self.verticalLayoutSessionProfile_2.setMargin(0)\n': \
		'#		self.verticalLayoutSessionProfile_2.setMargin(0)\n', \


	# Plug-in Web
	'		Form.setObjectName(_fromUtf8("Form"))\n': \
		'		#Form.setObjectName(_fromUtf8("Form"))\n', \

	'		Form.resize(400, 300)\n': \
		'		#Form.resize(400, 300)\n', \

	#'		Form.setSizePolicy(sizePolicy)\n': \
		#'		#Form.setSizePolicy(sizePolicy)\n', \

	'		self.verticalLayoutWidget = QtGui.QWidget(Form)\n': \
		"""		#self.verticalLayoutWidget = QtGui.QWidget(Form)
		self.verticalLayoutWidget = QtGui.QWidget()
""", \

	'		self.verticalLayout.setMargin(0)\n': \
	'		#self.verticalLayout.setMargin(0)\n', \


	# Plug-in Brain Blender
	'		Form.resize(752, 660)\n': \
	'		#Form.resize(752, 660)\n', \
	
	'		self.horizontalLayoutWidget = QtGui.QWidget(Form)\n': \
	"""		#self.horizontalLayoutWidget = QtGui.QWidget(Form)
		self.horizontalLayoutWidget = QtGui.QWidget()
""", \
	
	'		self.horizontalLayout.setMargin(0)\n': \
	'		#self.horizontalLayout.setMargin(0)\n', \
}

#####################################################################
# Functions
#####################################################################

def remove_form_resize(line):
	
	if 'Form.resize' in line:
		return('#Form.resize()\n')
	else:
		return(line)


#####################################################################

def replace_line(line):
	
	if line in REPLACE_STRINGS.keys():
		return(REPLACE_STRINGS[line])
	else:
		return(line)


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
	
	try:
		inputFile = sys.argv[1]
		outputFile = sys.argv[2]
	except:
		inputFile = DEFAULT_INPUT_FILE
		outputFile = DEFAULT_OUTPUT_FILE
	
	module_name = outputFile.split('/')[-1]
	module_name = module_name.replace('.py', '')
	
	data = ''
	
	input = open(inputFile, 'r')
	
	for line in input.readlines():
		
		line = remove_form_resize(line)
		line = replace_line(line)
		
		#if line in REPLACE_STRINGS.keys():
			#data = data + REPLACE_STRINGS[line]
		#else:
			#data = data + line
		
		data = data + line
	
	
	input.close()
	
	data = data.replace('__MODULE_NAME__', module_name)
	
	output = open(outputFile, 'w')
	output.write(data)
	output.close()

