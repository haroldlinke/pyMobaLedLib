# pyMobaLedLib for Windows, LINUX and MAC
Python based Programgenerator for the MobaLedLib for Linux and Mac

This branch is for development of the Windows/LINUX/Mac version of the ProgramGenerator

This Branch is based on LX4.19 of the Linux version of MobaLedLib_pyProgGen

Requirements:
- ARDUINO IDE and MobaledLib > 3.2.1 have to be installed
- Python >V3.9.0
- optimised for 1920x1080 resolution - Scale 100%. Smaller screens or higher scaling is possible but more scrolling is then needed to access all parts of the forms.

# Principal Installation using Python files
1. search for the folder ARDUINO HOME/Arduino
2. create a subfolder pyMobaLedLib in this folder (the folder can have any Name)
4. create a subfolder python
5. download the branch as ZIP-file: unpack the ZIP file and copy the contents of the folder python into the folder pyMobaLedLib/python
6. open the folder pyMobaLedLib/python
7. start the Python file: pyMobaLedLib.py with the command python3 pyMobaLedLib.py or python Home/Arduino/pyMobaLedLib/python/pyMobaLedLib.py

# Installation for Windows
1. Download the release package for windows.
2. The programm can be installed in any location. It only needs write access to this folder and the folder above.
3. I use the ARDUINO folder as an example here. Locate the ARDUINO folder - normally it should be Dokumente\ARDUINO.
4. Create a new folder pyMobaLedLib. Copy the downloaded package into this folder and unzip the package.
5. pyMobaLedLib.bat starts the program pyMoabLedLib. With right click "Send to Desktop" create an icon on the desktop.

# Attention LINUX and Mac Users: 
It is not possible to detect the location of the ARDUINO IDE executable automatically, as it can be installed in any directory
Skip the update of the ARDUINO libraries at startup and go to the ARDINO-Einstellungen Page. Click the Button "Pfad zur ARDUINO IDE einstellen" and select the ARDUINO IDE executable in the  following file selection dialog.

For MAC installation you can find detailed instructions in the file MLL-MAC_Installation_V2.pdf 

This Version is a Proof of Concept for a Python based MLL-Programm Generator that simulates the UserInterface of the Excel based Program Generator and can be used on Windows, Linux and Mac.

The VBA code was translated to Python using the Wedbased VB2PY-converter for the ProGenerator: 
http://vb2py.sourceforge.net/online_conversion.html. Therefore some hidden errors are still possible due to incompatibilities of the translation.

The VBA Code of the PatternGenerator was translated by an enhanced version of the VB2PY command line tool.

# Known Issues:
- Pattern Configurator: Icons and other objects on the page may to stay at the corect positon. To refresh select the Menu-Command: Tabelle->Refresh Icons
- ARDUINO connected to USB is not recognized correctly in LINUX and MAC OS automatically. Please select the correct type in the Options Menu and select the correct USB-Port manually.
  

History of Change
5.3.1- 17.05.2024
correction:
- crash when using mousewheel in macro tree and some other forms
new
- servoanimation: servo follows values of Afnagswert und Endwert
- first part of support for translation into other languages added (not final yet)

5.3.0J - 15.05.2024
new:
- check for new Version on Github
correction :
- error: crash when selecting on a Cell outside the available rows

5.3.0I - 14.05.2024
new:
- last tab saved and will be opened at reopening
correction :
- error: testbutton  inactive after after Send-to-ARDUINO

5.3.0H - 13.05.2024
correction
- error when reading individuell servo animation data for single servos.
- error in DCC button handling after reconnection after Send_to_ARDUINO
- error in saving workbook when closing workbook. Use filename of last load instead of standard filename.

5.3.0G - 12.05.2024
correction
- crash when deleting rows and no row selected

5.3.0F - 12.05.2024
correction
- delete LEDs_AutoProg before copying new version

5.3.0D - 11.5.2024
correction
- save and load PGF file errors

5.3.0C - 11.5.2024
corrected
- update of pyMLL program for Farbtest call from Excel

5.3.0B - 11.05.2024
Improved:
- LED Color Animation
Corrected:
- view on small monitors, added scrollbars
- about message open failed
- logfile open is blocking the program

5.3.0 - 08.05.2024
- update to MLL3.3.2B
- corrected issues in servo and led animation
- reorganisation of windows version

5.2.6.001 - 27.04.2024
- corrected ESP32 compatibility for Win
- program generator and patter configurator pages are active as default
- better error handling when images are missing or wrong spelled

5.2.5.001 - 23.4.2024
- crash when installed in a complete new environment when updating libraries
- improved error reporting

5.2.4.001 - 21.4.2024
- restructuring of event handling
- corrected: Config page was inoperable, because named-ranges pointed to the wrong table entries
- corrected: ServoAnim created a wrong pattern-macro when goto mode was not active
- new: LED Helligkeit Animation (Beta)
- new: LED Farbverlaufanimation (Beta)

5.2.3.001 - 17.4.2024
- restructuring of Excel VBA Objects, following Microsoft VBA structure to improve compatibility of VBA code translated to Python

5.2.2.001 - 11.4.2024
- Corrected: Error when Reading PGF-files in Latin-1 format in LINUX/Mac

5.2.1.001 - 10.4.2024
- new: LED anim Macro providing graphical user interface for LED light animation
- new: Pattern Configurator Page Beta (full functionality available, some graphical issues)
- improved: compatibility with LINUX and MAC
- 
V5.1.0.001 - 25.3.2024 - HL
- restructuring Excel-VBA simulation- replacing Tkintertable with TKSheet
- Beta test of PatternGenerator - Main Functionality is available
- integration of PatternGenerator into ProgGenerator Macros: PatternConfig - Individuelle Pattern
- new Macro: Servo Animation - providing a graphical user interface for servo animation

V4.0.10.001 - 23.3.2023 - HL
- new: support for PNG images
- new: pattern test support goto acts

V4.0.9.001 - 18.3.2023 - HL
- Beta test of PatternGenerator - Main Functionality is available
- new Excelmodel for running translated VBA code

Known Issues:
- test pattern - goto mode support not implemented yet
- main textbox and pictures are not visible yet
- Patterngenerator access to ARDUINO not fully tested yet
- a lot of  GUI issues need to be solevd and updated - functionality was first priority for this beta
- performance of pattern testing is low - will be improved in a later version

V3.2.1.02  - Make use of keyboard module optional
Open Issues:
- define a simple installation mechanism for LINUX and Mac
Known Issues:
 - uploading binaries to DCC ARDUINO not tested yet

V3.2.1.01  - Update to MLL 3.2.1

V3.1.0.018 - 0.22 Implement MAC compatibility

V3.1.0.017 - 08.7.2022 - HL
 - Upload to ARDUINO under LINUX

V3.1.0.016 - 02.7.2022 - HL
 - Update to MLL V3.1.0F5

V3.1.0.014 - 28.5.2022 - HL
 - Manual entering of ARDUINO-Program location for LINUX possible

V3.1.0.013 - 1.5.2022 - HL
 - ARDUINO control window functions replaced by "Excel"-USB-Window

V3.1.0.012 - 19.4.2022 - HL
 - EndProg should not terminate the program but return to main window

V3.1.0.011 - 19.4.2022 - HL
 - error correction

V3.1.0.010 - 18.4.2022 - HL
- error correction - corrected error in Get_Typ_Const with different languages

V3.1.0.010 - 17.4.2022 - HL
- error correction - replace "\" in filenames with "/" for Linux - not all "\" were replaced                             
Open Issues:
- define a simple installation mechanism for LINUX and Mac

V3.1.0.009 - 17.4.2022 - HL
- error correction - replace "\" in filenames with "/" for Linux - not all "\" were replaced

V3.1.0.008 - 17.4.2022 - HL
- error correction - radio button alignment, date format for filenames corrected

V3.1.0.007 - 17.4.2022 - HL
- adaption of USB Dialog for LINUX

V3.1.0.006 - 16.4.2021 - HL
- error correction USB Dialog - automatic detection of new connected ARDUINO

V3.1.0.005 - 15.4.2022 - HL
- replace ARDUINO Configuration page with USB Dialog

V3.1.0.004 - 14.4.2022 - HL
- Dialogs improved (keyboard usage)

V3.1.0.003 - 13.4.2022 - HL
- ARDUINO library check improved

V3.1.0.002 - 9.4.2022 - HL
- progress information for download of Python Program

V3.1.0.001 -  7.4.2022 - HL 
- Initial creation of pyMobaLedLib, derived from MobaledLib-PyProgammGenerator Version LX4.19
- Selection of USB port is LINUX compatible
- ARDUINO Library check at start of program, when libraries are missing, they are downloaded automatically
- Update of MLL ("Aktualisiere Bibilotheken) and Install Beta Test of MLL implemented
- Update of pyMobaLedLib implemented (Button under Optionen - Update)
 
 
 

