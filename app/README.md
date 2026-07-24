# ShopSync desktop deployment

ShopSync remains a CustomTkinter desktop application. Configure the SQL Server connection in `config.ini` before first launch. `SHOPSYNC_DB_*` environment variables can override those values for managed deployments.

At first successful connection, the app creates `dbo.Users` and an Admin using the `[authentication]` settings in `config.ini`. Change `initial_admin_password` before deployment. Passwords are stored with salted PBKDF2-SHA256 hashes; the first account is created only if no users exist.

## Run from source

```powershell
python -m pip install -r requirements.txt
python main.py
```

## Build the Windows application

```powershell
python -m pip install pyinstaller
.\build.ps1
```

The build output is `dist\ShopSync.exe`. The PyInstaller specification includes `config.ini` and every asset in `assets\`. Put a writable `config.ini` beside the executable to use machine-specific database settings without rebuilding.
