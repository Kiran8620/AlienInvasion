   @echo off
   REM Run this from inside your project folder (where alien_invasion.py lives).
   REM Requires Python + pip already installed and on PATH.

   pip install -r requirements.txt
   pip install pyinstaller

   python -m PyInstaller --onefile --windowed --name "AlienInvasion" ^
       --add-data "images;images" ^
       --add-data "sounds;sounds" ^
       alien_invasion.py

   echo.
   echo Build complete. Your .exe is in the "dist" folder.
   pause