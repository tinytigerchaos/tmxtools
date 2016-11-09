python .\PyInstaller-3.2\pyinstaller.py -F -w main.py -p ..\tmxtools
xcopy /y .\dist\main.exe .\
rd /s /q .\dist
