@echo off

pip install pyQt6 klembord ffmpeg-python psutil
start pythonw main.py

@REM copy the script in startup windows's programs
set startup="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if NOT exist %startup%\app.bat (
    
    msg * "Installation complete !"
)
copy %0 %startup%\app.bat /Y