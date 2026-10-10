# -*- mode: python ; coding: utf-8 -*-
# PyInstaller konfiguratsiyasi: ALLOH_UCHUN.exe (Windows, bitta fayl, konsolsiz)
a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=[],
    hiddenimports=[],
    excludes=["tkinter", "PySide6.QtWebEngineCore", "PySide6.QtQml", "PySide6.QtQuick",
              "PySide6.Qt3DCore", "PySide6.QtMultimedia", "PySide6.QtNetwork"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ALLOH_UCHUN",
    debug=False,
    strip=False,
    upx=False,
    console=False,  # oyna ilovasi: konsol ko'rinmaydi
)
