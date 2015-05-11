#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Puzzlebox - Jigsaw - Configuration
#
# Copyright Puzzlebox Productions, LLC (2011-2015)

__changelog__ = """\
Last Update: 2015.03.25
"""

import os, sys

#####################################################################
# General configuration
#####################################################################

DEBUG = 1

CONFIGURATION_FILE_PATH = 'puzzlebox_jigsaw_configuration.ini'

ENABLE_PYSIDE = True
#ENABLE_PYSIDE = False

INTERFACE_WINDOW_SHRINK = True
INTERFACE_WINDOW_POSITION = None
#INTERFACE_WINDOW_POSITION = [300, 0]

ENABLE_CONTROL_PANEL = True

ENABLE_RAW_EEG_DISPLAY = False

if (sys.platform != 'win32'):
	if not os.path.exists(CONFIGURATION_FILE_PATH):
		CONFIGURATION_FILE_PATH = \
			os.path.join('/etc/puzzlebox_jigsaw', CONFIGURATION_FILE_PATH)


#####################################################################
# Jigsaw Configuration
#####################################################################

#####################################################################
# Plug-in Configuration
#####################################################################

ENABLE_PLUGIN_HELP = True

ENABLE_PLUGIN_SESSION = True

ENABLE_PLUGIN_EEG = True
#ENABLE_PLUGIN_EEG = False

ENABLE_PLUGIN_WEB_BROWSER = True
#ENABLE_PLUGIN_WEB_BROWSER = False

#ENABLE_PLUGIN_BLOOM = True
ENABLE_PLUGIN_BLOOM = False

#ENABLE_PLUGIN_ORBIT = True
ENABLE_PLUGIN_ORBIT = False

ENABLE_PLUGIN_BLENDER = False
#ENABLE_PLUGIN_BLENDER = True

ENABLE_PLUGIN_TRENDS = False
#ENABLE_PLUGIN_TRENDS = True

ENABLE_PLUGIN_BRAINSTORMS = False
#ENABLE_PLUGIN_BRAINSTORMS = True

ENABLE_PLUGIN_ALGORITHMS = False
#ENABLE_PLUGIN_ALGORITHMS = True

ENABLE_PLUGIN_F1 = False
#ENABLE_PLUGIN_F1 = True


#####################################################################
# Help Plug-in Configuration
#####################################################################

PUZZLEBOX_FEEDBACK_URL = 'http://brainstorms.puzzlebox.info/contact_cgi.php'

#DEFAULT_HELP_URL = 'http://jigsaw.puzzlebox.info/help'
#DEFAULT_HELP_URL = 'http://jigsaw.puzzlebox.info/tracker/wiki/Help'
DEFAULT_HELP_URL = 'http://jigsaw.puzzlebox.io/tracker/wiki/Help'


#####################################################################
# Session Plug-in Configuration
#####################################################################

SESSION_JSON_INTERFACE = '' # listen on all of host's network interfaces
SESSION_JSON_HOST = '127.0.0.1'
#SESSION_JSON_HOST = '*'
SESSION_JSON_PORT = 8088

SESSION_JSON_DELIMITER = '\r'


#EXPORT_CSV_TRUNCATE_TIMEZONE = False # Remove time zone and 4th/5th/6th timer digits
EXPORT_CSV_TRUNCATE_TIMEZONE = True # Remove time zone and 4th/5th/6th timer digits

#EXPORT_CSV_SCRUB_DATA = True
EXPORT_CSV_SCRUB_DATA = False

EXPORT_CSV_RAW_DATA = False
#EXPORT_CSV_RAW_DATA = True


#####################################################################
# Web Browser Plug-in Configuration
#####################################################################

DEFAULT_BROWSER_URL = 'http://puzzlebox.info'

BROWSER_JAVASCRIPT_ENABLED = True
BROWSER_PLUGINS_ENABLED = True
BROWSER_PRIVATE_BROWSING_ENABLED = True


#####################################################################
# Orbit Plug-in Configuration
#####################################################################

#DEFAULT_ORBIT_AUDIO_FILE = 'throttle_hover_ios.wav'
#DEFAULT_ORBIT_AUDIO_FILE = 'throttle_hover_android_common.wav'
#DEFAULT_ORBIT_AUDIO_FILE = 'throttle_hover_android_htc_one_x.wav'
DEFAULT_ORBIT_AUDIO_FILE = 'throttle_hover_os_x.wav'

#DEFAULT_ORBIT_AUDIO_FRAMEWORK = 'Phonon'
DEFAULT_ORBIT_AUDIO_FRAMEWORK = 'QSound'

DEFAULT_ORBIT_SESSION_GRAPHIC = 'puzzlebox_orbit-flowchart.png'

#DEFAULT_ORBIT_HELP_URL = 'https://orbit.puzzlebox.info/development'
#DEFAULT_ORBIT_HELP_URL = 'path://docs/html/plugin-help-orbit/plugin-help-orbit.html'
DEFAULT_ORBIT_HELP_URL = 'path://docs/html/plugin-orbit/plugin-orbit.html#top'

DEFAULT_ORBIT_POWER_MINIMUM = 60
DEFAULT_ORBIT_POWER_MAXIMUM = 100

ORBIT_CONTROL_SETTINGS = { \
	'hover': { \
		'throttle': 80, \
		'yaw': 78, \
		'pitch': 31
	}, \
	'forward': { \
		'throttle': 80, \
		'yaw': 78, \
		'pitch': 50
	}, \
	'spinleft': { \
		'throttle': 80, \
		'yaw': 42, \
		'pitch': 31
	}, \
	'spinright': { \
		'throttle': 80, \
		'yaw': 114, \
		'pitch': 31
	}, \
}


#####################################################################
# Bloom Support Configuration
#####################################################################

DEFAULT_BLOOM_SESSION_GRAPHIC = 'puzzlebox_bloom.png'
#DEFAULT_BLOOM_HELP_URL = 'path://docs/html/plugin-bloom/Help%20–%20Puzzlebox%20Jigsaw.html'
#DEFAULT_BLOOM_HELP_URL = 'path://docs/html/plugin-bloom/Plug-inBloom_–_Puzzlebox_Jigsaw.html'
DEFAULT_BLOOM_HELP_URL = 'http://jigsaw.puzzlebox.io/tracker/wiki/Plug-inBloom'

DEFAULT_BLOOM_POWER_MINIMUM = 60
DEFAULT_BLOOM_POWER_MAXIMUM = 100

BLOOM_SERVO_STEP_POSITIVE = 3 # ThinkGear @ 1 update / sec
BLOOM_SERVO_STEP_NEGATIVE = 1 # ThinkGear @ 1 update / sec

BLOOM_RGB_STEP_POSITIVE = 8 # ThinkGear @ 1 update / sec
BLOOM_RGB_STEP_NEGATIVE = 6 # ThinkGear @ 1 update / sec


#####################################################################
# Brain Blender Plug-in Configuration
#####################################################################

DEFAULT_X10_HOUSE_CODE = 'E'
DEFAULT_X10_DEVICE = 8

BLENDER_X10_POWER_MINIMUM = 60
BLENDER_X10_POWER_MAXIMUM = 100


#####################################################################
# Trends Plug-in Configuration
#####################################################################

TRENDS_WARNING_ZONE_PERCENTAGE = 0.333

TRENDS_TRIGGER_MINIMUM = 0
TRENDS_TRIGGER_MAXIMUM = 100


#####################################################################
# Brain Brainstorms Plug-in Configuration
#####################################################################

# Discrete control drives the robot for a set time period per detection.
# Setting Variable control to "True" will drive the robot in a
# particular direction for as long as the detection occurs
BRAINSTORMS_VARIABLE_CONTROL_DURATION = True

BLINK_DETECTION_ENABLED = True
BLINK_DETECTION_THRESHOLD = 6 # 6 blinks detected within the valid range
BLINK_DETECTION_VALID_RANGE = 2 # 2 seconds

BLINK_DETECTION_INCLUDE_FORWARD = True
BLINK_DETECTION_INCLUDE_LEFT = True
BLINK_DETECTION_INCLUDE_RIGHT = True
BLINK_DETECTION_INCLUDE_REVERSE = True

BRAINSTORMS_SERVER_INTERFACE = '' # listen on all of server's network interfaces
BRAINSTORMS_SERVER_HOST = '127.0.0.1' # localhost
BRAINSTORMS_SERVER_PORT = 8194

THINKGEAR_SERVER_INTERFACE = '' # listen on all of server's network interfaces
THINKGEAR_SERVER_HOST = '127.0.0.1'
THINKGEAR_SERVER_PORT = 13854


AUTOCONNECT_TO_NXT_DEVICE = False

DEFAULT_NXT_POWER_LEVEL = 80

DEFAULT_NXT_BLUETOOTH_DEVICE_WINDOWS = 'COM1'
DEFAULT_NXT_BLUETOOTH_DEVICE_LINUX = '/dev/rfcomm0'

if (sys.platform == 'win32'):
	NXT_BLUETOOTH_DEVICE = DEFAULT_NXT_BLUETOOTH_DEVICE_WINDOWS
else:
	NXT_BLUETOOTH_DEVICE = DEFAULT_NXT_BLUETOOTH_DEVICE_LINUX

NXT_MOTORS_MOUNTED_BACKWARDS = False
NXT_MOTOR_PORT_LEFT = 'b'
NXT_MOTOR_PORT_RIGHT = 'a'
NXT_DEFAULT_RC_COMMAND = 'test_drive'


BRAINSTORMS_DELIMITER = '\r'


#####################################################################
# EEG Plug-in Configuration
#####################################################################

DEFAULT_EEG_HELP_URL = 'path://docs/html/plugin-eeg/plugin-eeg.html#functions'

SYNAPSE_SERVER_INTERFACE = '' # listen on all of server's network interfaces
SYNAPSE_SERVER_HOST = '*'
SYNAPSE_SERVER_PORT = 13854

THINKGEAR_SERVER_INTERFACE = '' # listen on all network interfaces
THINKGEAR_SERVER_HOST = '127.0.0.1'
THINKGEAR_SERVER_PORT = 13854

EMOTIV_ENABLE = False
EMOTIV_SERVER_HOST = '127.0.0.1'
EMOTIV_SERVER_PORT_CONTROL_PANEL = 3008
EMOTIV_SERVER_PORT_EMOCOMPOSER = 1726

MUSE_ENABLE = False
MUSE_SERVER_HOST = '127.0.0.1'
MUSE_SERVER_PORT = 5001

SPACEBREW_ENABLE = False
SPACEBREW_HOST = 'server.neuron.brain'

#EEG_PRESERVE_RAW_DATA = True
EEG_PRESERVE_RAW_DATA = False

EMULATE_THINKGEAR_FOR_EMOTIV = True
EMULATE_THINKGEAR_FOR_MUSE = True

#####################################################################
# Bloom Support Configuration
#####################################################################

BLOOM_SERVO_STEP_POSITIVE = 3 # ThinkGear @ 1 update / sec
BLOOM_SERVO_STEP_NEGATIVE = 1 # ThinkGear @ 1 update / sec

BLOOM_RGB_STEP_POSITIVE = 8 # ThinkGear @ 1 update / sec
BLOOM_RGB_STEP_NEGATIVE = 6 # ThinkGear @ 1 update / sec

#####################################################################
# Logging
#####################################################################

LOG_LEVEL_DEBUG = 2
LOG_LEVEL_INFO = 1
LOG_LEVEL_ERROR = 0
LOG_LEVEL_DISABLE = -1

DEFAULT_LOG_LEVEL = LOG_LEVEL_DEBUG
DEFAULT_LOGFILE = 'jigsaw'

LOGFILE_DIR = '/var/log/puzzlebox'
LOGFILE_SUFFIX = '.log'
LOGFILE_SUFFIX_DEBUG = '_debug.log'
LOGFILE_SUFFIX_INFO = '_info.log'
LOGFILE_SUFFIX_ERROR = '_error.log'

SPLIT_LOGFILES = False


#####################################################################
# Remote Control configuration
#####################################################################

#DEFAULT_ARDUINO_DEVICE_WINDOWS = 'COM1'
#DEFAULT_ARDUINO_DEVICE_LINUX = '/dev/ttyACM0'

#if (sys.platform == 'win32'):
	#ARDUINO_DEVICE = DEFAULT_ARDUINO_DEVICE_WINDOWS
#else:
	#ARDUINO_DEVICE = DEFAULT_ARDUINO_DEVICE_LINUX


#####################################################################
# Server configuration
#####################################################################

PUZZLEBOX_DELIMITER = '\r'


#####################################################################
# Client configuration
#####################################################################

CLIENT_NO_REPLY_WAIT = 5 # how many seconds before considering a component dead


#####################################################################
# ThinkGear Connect configuration
#####################################################################

THINKGEAR_DELIMITER = '\r'

#THINKGEAR_CONFIGURATION_PARAMETERS = {"enableRawOutput": False, "format": "Json"}
THINKGEAR_CONFIGURATION_PARAMETERS = {"enableRawOutput": True, "format": "Json"}

THINKGEAR_AUTHORIZATION_ENABLED = False

THINKGEAR_AUTHORIZATION_REQUEST = { \
	"appName": "Puzzlebox Jigsaw", \
	"appKey": "2e285d7bd5565c0ea73e7e265c73f0691d932408"
}

THINKGEAR_EMULATION_MAX_EEG_POWER_VALUE = 16384

#####################################################################
# ThinkGear Connect Server Emulator configuration
#####################################################################

THINKGEAR_ENABLE_SIMULATE_HEADSET_DATA = False

THINKGEAR_BLINK_FREQUENCY_TIMER = 6 # blink every 6 seconds
                                    # (6 seconds is listed by Wikipedia
                                    # as being the average number of times
                                    # an adult blinks in a laboratory setting)

THINKGEAR_DEFAULT_SAMPLE_WAVELENGTH = 30 # number of seconds from 0 to max
                                         # and back to 0 for any given
                                         # detection value below

#THINKGEAR_ATTENTION_MULTIPLIER = 1.0
#THINKGEAR_MEDITATION_MULTIPLIER = 0.8
#THINKGEAR_MEDITATION_PLOT_OFFSET = 5

#THINKGEAR_EEG_POWER_MULTIPLIERS = { \
	#'delta': 1.0, \
	#'theta': 1.0, \
	#'lowAlpha': 1.0, \
	#'highAlpha': 1.0, \
	#'lowBeta': 1.0, \
	#'highBeta': 1.0, \
	#'lowGamma': 1.0, \
	#'highGamma': 1.0, \
#}

#####################################################################
# Client Interface configuration
#####################################################################

THINKGEAR_POWER_THRESHOLDS = { \
	
	'concentration': { \
		0: 0, \
		10: 0, \
		20: 0, \
		30: 0, \
		40: 60, \
		50: 65, \
		60: 70, \
		70: 75, \
		75: 80, \
		80: 85, \
		90: 90, \
		100: 90, \
		}, \
	
	'relaxation': { \
		0: 0, \
		10: 0, \
		20: 0, \
		30: 0, \
		40: 0, \
		50: 10, \
		60: 10, \
		70: 15, \
		80: 15, \
		90: 20, \
		100: 20, \
		}, \
	
}


#####################################################################
# Flash socket policy handling
#####################################################################

FLASH_POLICY_FILE_REQUEST = \
        '<policy-file-request/>%c' % 0 # NULL byte termination
FLASH_SOCKET_POLICY_FILE = '''<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
   <site-control permitted-cross-domain-policies="all" />
   <allow-access-from domain="*" to-ports="__FLASH_SOCKET_POLICY_PORT__" />
</cross-domain-policy>%c''' % 0


#####################################################################
# Configuration File Parser
#####################################################################

if os.path.exists(CONFIGURATION_FILE_PATH):
	
	file = open(CONFIGURATION_FILE_PATH, 'r')
	
	for line in file.readlines():
		line = line.strip()
		if len(line) == 0:
			continue
		if line[0] == '#':
			continue
		if line.find('=') == -1:
			continue
		#if (line == "ARDUINO_DEVICE = ''"):
			## use operating system default if device not set manually
			#continue
		try:
			exec line
		except:
			if DEBUG:
				print "Error recognizing Puzzlebox Jigsaw configuration option:",
				print line


#####################################################################
# Final Configuration Settings
#####################################################################

if ENABLE_PYSIDE:
	os.environ['QT_API'] = 'pyside'
else:
	os.environ['QT_API'] = 'pyqt'

