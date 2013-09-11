#!/usr/bin/env python

import os, sys

sys.path.insert(0, '.')
from tgit.tgit import main

locales_dir = os.path.join(os.path.dirname(sys.argv[0]), 'locales')
main(locales_dir)