# PyInstaller build specification for the ShopSync desktop application.
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

project_dir = Path(SPECPATH)
datas = [(str(project_dir / "config.ini"), ".")]
assets_dir = project_dir / "assets"
if assets_dir.exists():
    datas.extend(collect_data_files(str(assets_dir), include_py_files=False))

analysis = Analysis([str(project_dir / "main.py")], pathex=[str(project_dir)], binaries=[], datas=datas,
    hiddenimports=["matplotlib.backends.backend_tkagg", "pyodbc"], hookspath=[], hooksconfig={},
    runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(analysis.pure)
exe = EXE(pyz, analysis.scripts, analysis.binaries, analysis.zipfiles, analysis.datas,
    name="ShopSync", debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False)
