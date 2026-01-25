# -*- mode: python -*-
import sys


block_cipher = None


a = Analysis(['src/fake_lingoes/main.py'],
             pathex=['src'],
             binaries=[],
             datas=[
                 ('resources', 'resources'),
                 ('configuration', 'configuration'),
                 ('icon.ico', '.')
             ],
             hiddenimports=[
                'pyttsx3.drivers',
                'pyttsx3.drivers.dummy',
                'pyttsx3.drivers.espeak',
                'pyttsx3.drivers.nsss',
                'pyttsx3.drivers.sapi5',
                'fake_lingoes',
                'fake_lingoes.ui',
                'fake_lingoes.services',
                'fake_lingoes.utils'
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
          name='fakelingoes',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='icon.ico')
