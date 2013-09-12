#!/usr/bin/env python

import os, sys

from tgit.tagger import main

locales_dir = os.path.join(os.path.dirname(sys.argv[0]), 'locales')
main(locales_dir)