# Clean existing build and packaging directories
rm -rf build dist


# Package new application
#python setup.py2app.py py2app
python setup.py2app.py py2app | grep -v copying | grep -v creating | grep -v byte-compiling | grep -v strip
#python2.7 PuzzleboxJigsaw.bundlebuilder.spec build
#/opt/local/bin/cxfreeze-2.7 jigsaw-gui.py --compress --target-dir dist --base-name Console --icon=images/puzzlebox.icns -s


# Copy data files
cp -r /opt/local/lib/Resources/qt_menu.nib \
	dist/Puzzlebox\ Jigsaw.app/Contents/Resources/

cp -r images \
	dist/Puzzlebox\ Jigsaw.app/Contents/Resources


#rm -f build/Puzzlebox\ Jigsaw.app/Contents/Resources/Puzzlebox/Synapse
#mv build/Puzzlebox\ Jigsaw.app/Contents/Resources/Synapse build/Puzzlebox\ Jigsaw.app/Contents/Resources/Puzzlebox/

# Remove images as they appear to be breaking something
#rm -rf dist/Puzzlebox\ Jigsaw.app/Contents/Resources/images/*


# Avoid error in which Qt libraries are loaded twice
# and configure library paths for Qt image PlugIns
echo '[Paths]' > dist/Puzzlebox\ Jigsaw.app/Contents/Resources/qt.conf
echo '  Plugins=PlugIns' >> dist/Puzzlebox\ Jigsaw.app/Contents/Resources/qt.conf

mkdir dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns
cp -r /opt/local/share/qt4/plugins/imageformats dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns

#find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec otool -L {} \;

find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec install_name_tool -change /opt/local/lib/libQtGui.4.dylib @executable_path/../Frameworks/libQtGui.4.dylib {} \;
find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec install_name_tool -change /opt/local/lib/libQtCore.4.dylib @executable_path/../Frameworks/libQtCore.4.dylib {} \;
find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec install_name_tool -change /opt/local/lib/libQtXml.4.dylib @executable_path/../Frameworks/libQtXml.4.dylib {} \;
find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec install_name_tool -change /opt/local/lib/libQtSvg.4.dylib @executable_path/../Frameworks/libQtSvg.4.dylib {} \;
find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec install_name_tool -change /opt/local/lib/libjpeg.8.dylib @executable_path/../Frameworks/libjpeg.8.dylib {} \;
find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec install_name_tool -change /opt/local/lib/libmng.1.dylib @executable_path/../Frameworks/libmng.1.dylib {} \;
find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec install_name_tool -change /opt/local/lib/libtiff.3.dylib @executable_path/../Frameworks/libtiff.3.dylib {} \;

find dist/Puzzlebox\ Jigsaw.app/Contents/PlugIns -type f -exec otool -L {} \; | grep opt

