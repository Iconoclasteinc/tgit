# -*- mode: python -*-
a = Analysis(['tgit.py'],
             pathex=['/Users/vtence/Development/Projects/tgit'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=['tgit/use_sip_api_v2.py'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='tgit',
          debug=False,
          strip=None,
          upx=True,
          console=False )

locales = Tree('locales', prefix = 'locales')
excluded = [('QNetwork', None, None), ('QtOpenGL', None, None), ('QtSql', None, None), ('QtSvg',
None, None), ('QtTest', None, None), ('QtWebKit', None, None), ('QtXml', None, None) ]

coll = COLLECT(exe,
               a.binaries - excluded,
               a.zipfiles,
               a.datas + locales,
               strip=None,
               upx=True,
               name='tgit')
app = BUNDLE(coll,
             name='TGiT.app',
             icon='tgit.icns')
