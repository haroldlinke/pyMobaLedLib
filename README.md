# MobaLedLib_pyProgGen for LINUX and MAC
Python based Programgenerator for the MobaLedLib for Linux and Mac

This branch is for development of the LINUX/Mac version of the ProgramGenerator

This Branch is based on V4.16 of the Windows version

Requirements:
MobaledLib 3.1.0F4 has to be installed
Python >V3.9.1


Installation using Python files
1. search for the MLL-subfolder LEDs_Autoprog - this folder must contain the file "LEDs_AutoProg.ino"
2. The path may have this look:  xxx/Arduino/MobaLedLib/Ver_3.1.0/LEDs_AutoProg/pyProg_Generator_MobaLedLib/python
   (the directory needs to be verfied in a LINUX installation)
3. create a subfolder pyProg_Generator_MobaLedLib in the folder LEDs_Autoprog (the name of the subfolder can be any name)
4. create a subfolder python
5. Clone MobaLedLib_PyProgGen to the folder pyProg_Generator_MobaLedLib/Python - the file pyProg_Generator_MobaLedLib.py must be in this folder
6. or download the branch as ZIP-file: unpack the ZIP file and copy the contents of the folder python into the folder pyProg_Generator_MobaLedLib/python
7. or create a logical link for the download folder to the folder python (ln -s xxx/Arduino/MobaLedLib/python/pyProg_Generator_MobaLedLib.py ./myProg.py")
8. open the folder pyProg_Generator_MobaLedLib/python
9. start the Python file: pyProg_Generator_MobaLedLib.py 
(python xx/Arduino/MobaLedLib/Ver_3.1.0/LEDs_AutoProg/pyProg_Generator_MobaLedLib/python pyProg_Generator_MobaLedLib.py

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

