# MobaLedLib_pyProgGen for LINUX and MAC
Python based Programgenerator for the MobaLedLib for Linux and Mac

This branch is for development of the Windows/LINUX/Mac version of the ProgramGenerator

This Branch is based on LX4.19 of the Linux version

Requirements:
MobaledLib 3.1.0F4 has to be installed
Python >V3.7.0


Installation using Python files
1. search for the ARDUINO HOME/Arduino
2. create a subfolder pyMobaLedLib in this folder (can be any Name)
4. create a subfolder python
5. Clone pyMobaLedLibn to the folder pyMobaLedLib/Python - the file pyMobaLedLib.py must be in this folder
6. or download the branch as ZIP-file: unpack the ZIP file and copy the contents of the folder python into the folder pyMobaLedLib/python
7. or create a logical link for the download folder to the folder python
8. open the folder pyMobaLedLib/python
9. start the Python file: pyMobaLedLib.py 
(python Home/Arduino/pyMobaLedLib/python pyMobaLedLib.py

This manual installation should work for Windows, Linux and Mac.

This Version is a Proof of Concept for a Python based MLL-Programm Generator that simulates the UserInterface of the Excel based Program Generator and can be used on Windows, Linux and Mac.

The VBA code was translated 1 to 1 to Python using the Wedbased VB2PY-converter: 
http://vb2py.sourceforge.net/online_conversion.html. Therefore some hidden errors are still possible due to incompatibilities of the translation.

Open Issues:
- define a simple installation mechanism for LINUX and Mac

- Handling of USB-Ports is not compatible with LINUX and Mac
  Unfortunately the ProgrammGenerator code is using only the ComPortNumber as Integer and is using a negative number to signal a blocked ComPort by another program.
  This needs to be adapted to the way the "old"parts of the ColorCheckprogram access the ARDUINO.
  The paramaters from the "ARDUINO"-Configuration Page are NOT synchronised with the ProgrammGenerator part as both parts of the prohram use 
  a different way of handling USB-Ports. (With VLX4.17 this issue should be solved)
  
- All paths need to be checked and adapted to the LINUX/MAC path rules (replace \ with /)
- all generated batch files need to be adapted from Windows cmds to Linux shell commands

