# MobaLedLib_pyProgGen for Windows, LINUX and MAC
Python based Programgenerator for the MobaLedLib for Linux and Mac

This branch is for development of the Windows/LINUX/Mac version of the ProgramGenerator

This Branch is based on LX4.19 of the Linux version of MobaLedLib_pyProgGen

Requirements:
- MobaledLib 3.1.0F4 has to be installed
- Python >V3.7.0


Installation using Python files
1. search for the ARDUINO HOME/Arduino
2. create a subfolder pyMobaLedLib in this folder (the folder can have any Name)
4. create a subfolder python
5. download the branch as ZIP-file: unpack the ZIP file and copy the contents of the folder python into the folder pyMobaLedLib/python
6. open the folder pyMobaLedLib/python
7. start the Python file: pyMobaLedLib.py 
(python Home/Arduino/pyMobaLedLib/python pyMobaLedLib.py)

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

V3.1.0.003 - 13.4.2021 - HL
- ARDUINO library check improved

V3.1.0.004 - 14.4.2021 - HL
- Dialogs improved (keyboard usage)

V3.1.0.005 - 15.4.2021 - HL
- replace ARDUINO Configuration page with USB Dialog

V3.1.0.006 - 16:4.2021 - HL
- error correction USB Dialog - automatic detection of new connected ARDUINO
- 
                              
Open Issues:
- define a simple installation mechanism for LINUX and Mac

- all generated batch files need to be adapted from Windows cmds to Linux shell commands

