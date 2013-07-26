# -*- mode: python -*-
a = Analysis(['tgit/tgit.py'],
             pathex=['/Users/vtence/Development/Projects/tgit'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='tgit',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='tgit.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='tgit')
app = BUNDLE(coll,
             name='tgit.app',
             icon='tgit.icns')
