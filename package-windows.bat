@echo off
SET CC="C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
SET SIGN="C:\Program Files (x86)\Windows Kits\8.1\bin\x86\signtool.exe"
SET VIRTUALENV="%HOMEPATH%\.virtualenvs\TGiT34"
SET ACTIVATEVIRTUALENV="%VIRTUALENV%\Scripts\activate.bat"
SET DEACTIVATEVIRTUALENV="%VIRTUALENV%\Scripts\deactivate.bat"
SET SOURCEDIR="%HOMEPATH%\Documents\Code\tgit"
SET CERTDIR="..\.."

CD %SOURCEDIR%

CALL %ACTIVATEVIRTUALENV%
lrelease.exe resources\tgit_fr.ts -qm resources\tgit_fr.qm
pyrcc5.exe -o tgit\ui\resources.py resources.qrc
python.exe setup.py build
%CC% tgit_installer.iss
REM %SIGN% sign /v /f %CERTDIR%\Iconoclaste.pfx build\*.exe
CALL %DEACTIVATEVIRTUALENV%
