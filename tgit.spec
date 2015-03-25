# -*- mode: python -*-
a = Analysis(['tgit.py'],
             pathex=[],
             hiddenimports=["PyQt5.QtNetwork", "PyQt5.QtPrintSupport"],
             hookspath=None)
pyz = PYZ(a.pure)

if is_win:
  ext = '.exe'
else:
  ext = ''

if is_darwin:
    plugins = [
        ("qt5_plugins/mediaservice/libqtmedia_audioengine.dylib", "/usr/local/Cellar/qt5/5.4.0/plugins/mediaservice/libqtmedia_audioengine.dylib", "BINARY"),
        ("qt5_plugins/mediaservice/libqavfmediaplayer.dylib", "/usr/local/Cellar/qt5/5.4.0/plugins/mediaservice/libqavfmediaplayer.dylib", "BINARY"),
        ("qt5_plugins/mediaservice/libqavfcamera.dylib", "/usr/local/Cellar/qt5/5.4.0/plugins/mediaservice/libqavfcamera.dylib", "BINARY"),
    ]
else:
    plugins = []

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
               a.binaries + plugins - excluded,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='tgit')
app = BUNDLE(coll,
             name='TGiT.app',
             icon='tgit.icns')
