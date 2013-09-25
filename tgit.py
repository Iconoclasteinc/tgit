#!/usr/bin/env python

import os, sys

import use_sip_api_v2
from tgit.tagger import main

locales_dir = os.path.join(os.path.dirname(sys.argv[0]), 'locales')
main(locales_dir)