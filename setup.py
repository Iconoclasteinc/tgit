try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'TGiT',
    'author': 'Iconoclaste',
    'url': 'http://tagtamusique.com',
    'download_url': 'https://bitbucket.org/tagtamusique/tgit',
    'author_email': 'jr@iconoclaste.ca',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['tgit'],
    'scripts': [],
    'name': 'tgit'
}

setup(**config)