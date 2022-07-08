# MobaLedLib_pyProgGen for Windows, LINUX and MAC
Python based Programgenerator for the MobaLedLib for Linux and Mac

This branch is for development of the Windows/LINUX/Mac version of the ProgramGenerator

This Branch is based on LX4.19 of the Linux version of MobaLedLib_pyProgGen

Requirements:
- ARDUINO IDE and MobaledLib > 3.1.0F4 has to be installed
- Python >V3.7.0


Installation using Python files
1. search for the folder ARDUINO HOME/Arduino
2. create a subfolder pyMobaLedLib in this folder (the folder can have any Name)
4. create a subfolder python
5. download the branch as ZIP-file: unpack the ZIP file and copy the contents of the folder python into the folder pyMobaLedLib/python
6. open the folder pyMobaLedLib/python
7. start the Python file: pyMobaLedLib.py with the command python3 pyMobaLedLib.py or python Home/Arduino/pyMobaLedLib/python/pyMobaLedLib.py

Attention LINUX Users: 

It is not possible to detect the location of the ARDUINO IDE executable automatically, as it can be installed in any directory
Skip the update of the ARDUINO libraries at startup and go to the ARDINO-Einstellungen Page. Click the Button "Pfad zur ARDUINO IDE einstellen" and select the ARDUINO IDE executable in the  following file selection dialog.

This manual installation should work for Windows, Linux and Mac.

This Version is a Proof of Concept for a Python based MLL-Programm Generator that simulates the UserInterface of the Excel based Program Generator and can be used on Windows, Linux and Mac.

The VBA code was translated 1 to 1 to Python using the Wedbased VB2PY-converter: 
http://vb2py.sourceforge.net/online_conversion.html. Therefore some hidden errors are still possible due to incompatibilities of the translation.

History of Change

V3.1.0.001 -  7.4.2022 - HL 
- Initial creation of pyMobaLedLib, derived from MobaledLib-PyProgammGenerator Version LX4.19
- Selection of USB port is LINUX compatible
- ARDUINO Library check at start of program, when libraries are missing, they are downloaded automatically
- Update of MLL ("Aktualisiere Bibilotheken) and Install Beta Test of MLL implemented
- Update of pyMobaLedLib implemented (Button under Optionen - Update)

V3.1.0.002 - 9.4.2022 - HL
- progress information for download of Python Program

V3.1.0.003 - 13.4.2022 - HL
- ARDUINO library check improved

V3.1.0.004 - 14.4.2022 - HL
- Dialogs improved (keyboard usage)

V3.1.0.005 - 15.4.2022 - HL
- replace ARDUINO Configuration page with USB Dialog

V3.1.0.006 - 16.4.2021 - HL
- error correction USB Dialog - automatic detection of new connected ARDUINO

V3.1.0.007 - 17.4.2022 - HL
- adaption of USB Dialog for LINUX

V3.1.0.008 - 17.4.2022 - HL
- error correction - radio button alignment, date format for filenames corrected

V3.1.0.009 - 17.4.2022 - HL
- error correction - replace "\" in filenames with "/" for Linux - not all "\" were replaced

V3.1.0.010 - 17.4.2022 - HL
- error correction - replace "\" in filenames with "/" for Linux - not all "\" were replaced                             
Open Issues:
- define a simple installation mechanism for LINUX and Mac

V3.1.0.010 - 18.4.2022 - HL
- error correction - corrected error in Get_Typ_Const with different languages

V3.1.0.011 - 19.4.2022 - HL
 - error correction

V3.1.0.012 - 19.4.2022 - HL
 - EndProg should not terminate the program but return to main window

V3.1.0.013 - 1.5.2022 - HL
 - ARDUINO control window functions replaced by "Excel"-USB-Window

V3.1.0.014 - 28.5.2022 - HL
 - Manual entering of ARDUINO-Program location for LINUX possible
 
V3.1.0.016 - 02.7.2022 - HL
 - Update to MLL V3.1.0F5
 
V3.1.0.017 - 08.7.2022 - HL
 - Upload to ARDUINO under LINUX

Open Issues:
- define a simple installation mechanism for LINUX and Mac

Known Issues:
 - in 016 and 017, the library check at the start of the program asks tio update libraries with blank library names. Answer "no" to the update request and the program continues
 - uploading binaries to DCC ARDUINO not tested yet

