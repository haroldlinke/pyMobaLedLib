@ECHO OFF
Color 80
REM This file was generated by 'Prog_Generator_MobaLedLib.xlsm'  13:39:18
REM
REM It updates/installs all required libraries for the MobaLedLib projects.
REM
REM Attention:
REM This program must be started from the arduino libraries directory
REM

CHCP 65001 >NUL
ECHO *********************************
ECHO  Installing the following boards
ECHO *********************************
ECHO   ATTinyCore:avr
ECHO.
@if exist "%USERPROFILE%\AppData\Local\Temp\MobaLedLib_build\ESP32\includes.cache" del "%USERPROFILE%\AppData\Local\Temp\MobaLedLib_build\ESP32\includes.cache"
"C:\Program Files (x86)\Arduino\arduino_debug.exe" --install-boards ATTinyCore:avr --pref "boardsmanager.additional.urls=https://raw.githubusercontent.com/Hardi-St/MobaLedLib_Docu/refs/heads/master/Tools/ATTinyCore/ATTinyCode_index.json" 2>&1
ECHO.
ECHO Error %ERRORLEVEL%
IF ERRORLEVEL 1 Goto ErrorMsg

Exit

:ErrorMsg
   COLOR 4F
   ECHO   ****************************************
   ECHO    Da ist was schief gegangen ;-(
   ECHO   ****************************************
   Pause