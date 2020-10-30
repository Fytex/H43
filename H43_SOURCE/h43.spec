# -*- mode: python ; coding: utf-8 -*-

from os.path import join as path_join

block_cipher = None


a = Analysis(['h43.py'],
             pathex=[],
             binaries=[],
             datas=[
				(path_join('extras', 'Guilds_Icon.png'), 'extras'),
				(path_join('extras', 'art_h43.txt'), 'extras')
				],
             hiddenimports=[
				'cogs.exploit',
				'cogs.admin_ext',
				'cogs.error_handler'
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
          name='H43 BOT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
		  icon=path_join('extras', 'icon_h43.ico'))
