# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
datas = [("miyouqian/webui", "miyouqian/webui"),
         ("miyouqian/templates", "miyouqian/templates"),
         ("config.example.yaml", ".")]
binaries, hiddenimports = [], []
for package in ["httpx", "yaml", "qrcode", "PIL", "loguru", "pyfiglet", "websockets"]:
    d, b, h = collect_all(package)
    datas += d
    binaries += b
    hiddenimports += h
a = Analysis(["windows_launcher.py"], pathex=["."], binaries=binaries, datas=datas,
             hiddenimports=hiddenimports, hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=["pytest", "tkinter"], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="MiyoQian",
          debug=False, bootloader_ignore_signals=False, strip=False, upx=False,
          console=True, disable_windowed_traceback=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="MiyoQian")
