from cx_Freeze import setup, Executable

DATA_FILES = []

includes = ["re","sip", "atexit", "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets"]

setup(
    name='tgit',
    description='TGit',
    author='Iconoclaste',
    url='http://tagtamusique.com',
    download_url='https://bitbucket.org/tagtamusique/tgit',
    author_email='jr@iconoclaste.ca',
    version='0.1',
    packages=['tgit'],
    scripts=[],
    data_files=DATA_FILES,
    options={"build_exe":{ "includes": includes}},
    executables=[Executable(script="tgit.py")]
)