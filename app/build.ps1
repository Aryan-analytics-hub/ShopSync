# Requires: pip install -r requirements.txt pyinstaller
$ErrorActionPreference = "Stop"
python -m PyInstaller --noconfirm --clean ShopSync.spec
Copy-Item -LiteralPath .\config.ini -Destination .\dist\config.ini -Force
Write-Host "Build complete: dist\\ShopSync.exe"
