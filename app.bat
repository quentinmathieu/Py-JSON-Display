@echo off
@REM DO NOT USE THIS FILE !!
exit
cd "%USERPROFILE%\Elan Formation\SharePoint - Equipe-Elan - Documents\Ressources_Equipe\DL\App"

@REM copy the script in startup windows's programs
set startup="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if NOT exist %startup%\app.bat (
    pip install pyQt6 klembord ffmpeg-python psutil
    msg * "Installation complete !"
)
fc %0 %startup%\app.bat

if errorlevel 1 msg * "Installer up to date !"
copy %0 %startup%\app.bat /Y
start pythonw.exe main.py