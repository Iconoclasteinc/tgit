@echo off
SET CC="C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
SET VIRTUALENV="%HOMEPATH%\.virtualenvs\TGiT34"
SET ACTIVATEVIRTUALENV="%VIRTUALENV%\Scripts\activate.bat"
SET DEACTIVATEVIRTUALENV="%VIRTUALENV%\Scripts\deactivate.bat"
SET SOURCEDIR="%HOMEPATH%\Documents\Code\tgit"

CD %SOURCEDIR%

CALL %ACTIVATEVIRTUALENV%
lrelease.exe resources\tgit_fr.ts -qm resources\tgit_fr.qm
pyrcc5.exe -o tgit\ui\resources.py resources.qrc
python.exe setup.py build
%CC% tgit_installer.iss
CALL %DEACTIVATEVIRTUALENV%
