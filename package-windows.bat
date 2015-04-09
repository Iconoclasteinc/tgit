@echo off
SET CC="C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
SET SIGN="C:\Program Files (x86)\Windows Kits\8.1\bin\x86\signtool.exe"
SET PYTHONDIR="C:\Python34"
SET PYTHONSITEPACKAGESDIR="%PYTHONDIR%\Lib\site-packages"
SET PYQTDIR="%PYTHONSITEPACKAGESDIR%\PyQt5"
SET PYTHON="%PYTHONDIR%\python.exe"
SET PYRCC="%PYQTDIR%\pyrcc5.exe"
SET LRELEASE="%PYQTDIR%\lrelease.exe"
SET SOURCEDIR="%HOMEPATH%\Documents\Code\tgit"
SET CERTDIR="..\.."

CD %SOURCEDIR%

%LRELEASE% resources\tgit_fr.ts -qm resources\tgit_fr.qm
%PYRCC% -o tgit\ui\resources.py resources.qrc
%PYTHON% setup.py build
%CC% tgit_installer.iss
REM %SIGN% sign /v /f %CERTDIR%\Iconoclaste.pfx build\*.exe
