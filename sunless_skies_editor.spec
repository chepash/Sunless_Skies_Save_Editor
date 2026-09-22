# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Sunless Skies Save Editor.

Build with:  pyinstaller sunless_skies_editor.spec
Output:      dist/SunlessSkiesSaveEditor/ (one-folder build)

The application is a plain PyQt5 GUI started from __main__.py; no data files
need to be bundled because all lookup tables live in Data/globals.py.
"""

block_cipher = None

a = Analysis(
    ['__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Keep the build lean: drop unused Qt/PyQt subsystems.
        'PyQt5.QtBluetooth', 'PyQt5.QtNetwork', 'PyQt5.QtQml', 'PyQt5.QtQuick',
        'PyQt5.QtSql', 'PyQt5.QtTest', 'PyQt5.QtWebChannel', 'PyQt5.QtWebSockets',
        'PyQt5.QtXml', 'PyQt5.QtDBus', 'PyQt5.QtMultimedia', 'PyQt5.QtWebEngineWidgets',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SunlessSkiesSaveEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SunlessSkiesSaveEditor',
)
