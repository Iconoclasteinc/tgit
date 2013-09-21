#!/bin/sh

# Find out how to do that nicely in python to use proper application version number
# There must be a way to integrate with setup.py right?
pyi-build tgit.spec

hdiutil create dist/tgit.dmg -srcfolder dist/TGiT.app/ -volname TGiT -ov -format UDBZ

