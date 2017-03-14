jigsaw-python
==================


Puzzlebox Jigsaw


Copyright (2011-2017)

by Puzzlebox Productions, LLC

https://puzzlebox.io


License: GNU Affero General Public License v3.0
https://www.gnu.org/licenses/agpl-3.0.html


============

Available for Purchase:

http://store.neurosky.com/products/jigsaw


============

Required Python Modules:
- pyside
- simplejson
- serial
- matplotlib


============

Instructions:

- Requires downloading and configuration of Puzzlebox Synapse:

https://github.com/PuzzleboxIO/synapse-python

- Create a symlink inside root directory to Synapse:

Example: ln -s ../synapse-python/Puzzlebox/Synapse Synapse


============

Examples:

macOS (via MacPorts):

$ sudo port install py27-pyside py27-simplejson py27-serial py27-matplotlib

$ git clone https://github.com/PuzzleboxIO/synapse-python

$ git clone https://github.com/PuzzleboxIO/jigsaw-python

$ cd jigsaw-python/Puzzlebox

$ ln -s ../synapse-python/Puzzlebox/Synapse Synapse

$ cd ..

$ python2.7 jigsaw-gui.py
