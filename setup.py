try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

APP = ['tgit/tgit.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': '/Users/vtence/Development/Projects/tgit/tgit.icns',
    'includes': ['sip', 'PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui']}

setup(
    name='tgit',
    description='TGit',
    author='Iconoclaste',
    url='http://tagtamusique.com',
    download_url='https://bitbucket.org/tagtamusique/tgit',
    author_email='jr@iconoclaste.ca',
    version='0.1',
    install_requires=['nose'],
    packages=['tgit'],
    scripts=[],
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

