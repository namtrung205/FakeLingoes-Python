# -*- mode: python -*-

block_cipher = None


a = Analysis(['MainApp.py'],
             pathex=['D:\\DEV\\02. Fake lingoes and ocr\\V5.3'],
             binaries=[],
             datas=[],
             hiddenimports = [
    'pyttsx3.drivers',
    'pyttsx3.drivers.dummy',
    'pyttsx3.drivers.espeak',
    'pyttsx3.drivers.nsss',
    'pyttsx3.drivers.sapi5',
],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='MainApp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
