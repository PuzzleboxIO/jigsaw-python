rem cx_Freeze
xcopy images dist\images /I /Y
xcopy packaging\win32\imageformats dist\imageformats /I /Y

rem ***Output to Console for Debugging
rem \Python27\Scripts\cxfreeze jigsaw-gui.py --compress --target-dir dist --base-name Console --include-modules PySide.QtNetwork,serial.win32 --icon=images\puzzlebox.ico

rem ***GUI Mode only for Distribution
\Python27\Scripts\cxfreeze jigsaw-gui.py --compress --target-dir dist --base-name Win32GUI --include-modules PySide.QtNetwork,serial.win32 --icon=images\puzzlebox.ico


rem PyInstaller
rem \Python27\python.exe \Development\pyinstaller-1.5.1\Makespec.py --onefile --windowed --icon=images\puzzlebox.ico --name=PuzzleboxJigsaw jigsaw-gui.py

rem \Python27\python.exe \Development\pyinstaller-1.5.1\Build.py PuzzleboxJigsaw.spec
