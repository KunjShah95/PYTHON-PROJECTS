# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['gmail_monitor_app.py'],
             pathex=[],
             binaries=[],
             datas=[('credentials.json', '.'), 
                    ('gmail_icon.png', '.'),
                    ('gmail_logo.svg', '.'),
                    ('add_account_icon.svg', '.'),
                    ('search_icon.svg', '.'),
                    ('settings_icon.svg', '.')],
             hiddenimports=['PyQt6.QtChart'],
             hookspath=[],
             hooksconfig={},
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
          [],
          exclude_binaries=True,
          name='Gmail Monitor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='gmail_icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Gmail Monitor')