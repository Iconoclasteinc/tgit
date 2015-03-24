# -*- mode: python -*-
a = Analysis(['tgit.py'],
             pathex=[],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)

if is_win:
  ext = '.exe'
else:
  ext = ''

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='tgit' + ext,
          debug=False,
          strip=None,
          upx=True,
          console=False)

excluded = [('QtSql', None, None),
            ('QtSvg', None, None),
            ('QtTest', None, None),
            ('QtWebKit', None, None)]
#           ('QtXml', None, None)]

coll = COLLECT(exe,
               a.binaries - excluded,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='tgit')
app = BUNDLE(coll,
             name='TGiT.app',
             icon='tgit.icns')
