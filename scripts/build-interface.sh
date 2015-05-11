#!/bin/bash

#alias pyside-uic="pyside-uic-2.7"

pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Interface.py --indent=0 interface/puzzlebox_jigsaw_interface_design.ui

pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Help.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_help.ui
pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Session.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_session.ui
pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Eeg.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_eeg.ui
pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Web.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_web.ui
#pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Bloom.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_bloom.ui
#pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Orbit.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_orbit.ui
#pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Blender.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_blender.ui
#pyside-uic-2.7 --output=Puzzlebox/Jigsaw/Design_Plugin_Brainstorms.py --indent=0 interface/puzzlebox_jigsaw_interface_design-plugin_brainstorms.ui

python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Interface.py Puzzlebox/Jigsaw/Design_Interface.py

python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Help.py Puzzlebox/Jigsaw/Design_Plugin_Help.py
python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Session.py Puzzlebox/Jigsaw/Design_Plugin_Session.py
python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Eeg.py Puzzlebox/Jigsaw/Design_Plugin_Eeg.py
python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Web.py Puzzlebox/Jigsaw/Design_Plugin_Web.py
#python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Bloom.py Puzzlebox/Jigsaw/Design_Plugin_Bloom.py
#python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Orbit.py Puzzlebox/Jigsaw/Design_Plugin_Orbit.py
#python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Blender.py Puzzlebox/Jigsaw/Design_Plugin_Blender.py
#python scripts/update-interface-pyside.py Puzzlebox/Jigsaw/Design_Plugin_Brainstorms.py Puzzlebox/Jigsaw/Design_Plugin_Brainstorms.py
