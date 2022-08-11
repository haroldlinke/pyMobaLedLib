# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2021
# * Copyright: Harold Linke 2021
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *  
# * https://github.com/Hardi-St/MobaLedLib
# *
# * MobaLedCheckColors is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * MobaLedCheckColors is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************

#------------------------------------------------------------------------------
# CHANGELOG:
# 2020-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2021-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release

from vb2py.vbfunctions import *
from vb2py.vbdebug import *


#****************************************
#*                                      *
#*       PyProgramGenerator             *
#*       RevisionHistory_ToDo           *
#*                                      *
#****************************************
# 23.12.2021 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 13.03.2022 v4.15 HL: - Update to MLL Version 3.1.0D including MLL Simulator 



#****************************************
#*                                      *
#*       MobaLedLib                     *
#*       M00_RevisionHistory_ToDo       *
#*                                      *
#****************************************
#  MobaLedLib: LED library for model railways
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#  Copyright (C) 2018, 2019, 2020, 2021  Hardi Stengelin: MobaLedLib@gmx.de
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#  -------------------------------------------------------------------------------------------------------------
# Revision History:
# ~~~~~~~~~~~~~~~~~
# 06.08.19: - Started
# 10.09.19: - Send to Franz-Georg
#           - Software upload to the right Arduino only if it's necessary
#           - Corrected the displayed USB pictures (Changed by mistake yesterday)
# 11.09.19: - Added MCP_CAN lib to the directory because it cant't be loaded with the ArduinoIDE
#           - Check_Required_Libs_and_Install_missing() is working
# 12.09.19: - Missing libraries are installed
#           - Boards could be selected in the Options menu
# 24.09.19: - Corrected the Autofilter. It has been disabled/set to the column 1 if rows have been moved
#           - Calling "Update_Start_LedNr" if the Autofilter is changed
#           => Ver. 0.53
# 26.09.19: - Speed up deleeting whole columns
#           - No hidden columns because this generates problems when copying rows when the Autofilter is activ.
#             - Internal Columns at the and are always visble (Hint from Alf)
#             - No Empty column E at DCC and CAN to be able to copy data between DCC,CAN and Selecrix
#               In this case the Column has to be added temporary
#           - House Times and DCC Offset could bedefined in the Config sheet
# 27.09.19: - Copy the program to own directory if it's started the first time form the library
#             and create a link on the desktop.
# 28.09.19: => Ver. 0.54
#           - Debug Meldungen zur Fehlersuche bei Rolf eingefügt
#           => Ver. 0.55
#           - WaitForSingleObject mit LongLong für Win64 bei den beiden Armins
#           => Ver. 0.56
#           - Changed the result variable type also to LongLong
# 02.10.19: => Ver. 0.57
#           - Uploaded to GitHub and posted in the Stummi Forum
# 05.10.19: => Ver. 0.58 (In the previos release Version Const Prog_Version was set to 0.56 by mistake)
#           - Corrected generating of LOC_INCHx defines if the Flash() function was used without Ext_AddrTxt (DCC, ...)
#             In addition a warinig in the library has been disabled.
# 06.10.19: => Uploaded to GitHub and released library version 0.9.1
#           - Added: vbDirectory to Dir() command in Function Check_Required_Libs() to detect also
#             directories without files.
#           => Ver. 0.59
# 29.10.19: - Solved problems when first started after download "Geschützte Ansicht" at Office 2013
#             - ActiveSheet is Nothing for some reasons
#             - Sheet.Select dosn't work
#           => Ver. 0.60
# 02.11.19: - Added Quotation marks to prevent Problems with special characters in the path like '&'
#             in "Compile_and_Upload_Prog_to_Arduino()"
# 16.11.19: => Ver. 0.61
#           - New modul: M50_Exchange which is used to excange data with the Pattern_Configurator
#           - Detect if several Arduinos are connected in the USB port detection function
#             Problem: My USB Hub disables the 5V, but not the data lines => Comunication is still possible
#             if one port is disabled but the arduino is porered by the other Arduino on the main board ;-(
# 01.12.19: - Added the CheckColors Python program from Harold
# 02.12.19: - Start with the existing line when selecting a macro
#           - Rooms could be added/deleted at every position
# 03.12.19: - Position of the SelectMacro, House, Other forms are stored
#           - Parameters in existing macros are used in the dialog. Prior the default values have been shown
# 06.12.19: => Ver. 0.62
#           - Loading the CheckColors EXE from GitHub
#           - Corrected the LED Count if an existing House() Line is changed
# 13.12.19: - LeuchtfeuerALL deleted because it's already couvered by the normal "Leuchtfeuer"
#             In addition there was a problem when editing the line
# 24.12.19: - Corrected crash in Clear_COM_Port_Check_and_Set_Cursor_in_all_Sheets() which came up with office 365
# 25.12.19: - Corrected crash caused by the clip board functions at 64 Bit office
#             (Added the corrections made on 18.12.19 together with Armin)
# 31.12.19: - Clear the "LEDs", "InCnt" and "Loc InCh" column if a "Set_ColTab" macro is added to an existing line.
# 31.12.19: - Improved the Get_USB_Ports() function because the "find" function didn't work on Norberts computer for some reasons
#           => Ver. 0.63
#              Send to Norbert
# 07.01.20: - Using the new USB Connection pictures
# 16.01.20: => Ver. 0.70
# 17.01.20: => Ver. 0.71 uploaded to GitHub
# 14.02.20: - New method to create the desktop icon without a powersheel call.
#             In addition an icon could be defined
#             -> ToDo: Add the correct icon
# 16.02.20: - Added descriptions to the macro selection dialog
# 24.02.20: - Added Misha's changes and translations
#           => Ver. 0.72
# 28.02.20: - Manualy checked the english translations up for all 747 currently existing lines in the languages sheet
#           - Added Italian and Spain
# 29.02.20: - Translated the "Config" sheet
# 02.03.20: - Solved problem with '\' in marco lines. If "#define" lines with sevreal lines which have been separated by
#             a '\' have been used the last last line did also get an '\'. This caused problem if several lines
#             "#define" lines have been used in different cells.
#           - Set minimal LED count in the fire macro to 3. Otherwise the arduino program crashes because: for(uint8_t k= LED_cnt - 3; k > 0; k--)
#           - Compared to the last languages changes from Misha
#           - Activating the empty lines in the filter when "Release_or_Debug_Version()" is called to solve the problem
#             with disapearing lines
#           - Added changes from Christian
#           - Added Italian and Spain translations to the "Par_Description" sheet
# 03.03.20: - The language could be defined in the "Config" sheet.
#           - Updated christians changes in the "Par_Description" sheet
#           - Started the import of data from an old version
# 19.03.20: - Importing of data from old sheets
#           => Ver. 0.74
# 20.03.20: - Save and Load buton are working
# 22.03.20: - Icons added and import of old data checkt when started from the lib Directory
# 29.03.20: - Add DCC/Selectrix test buttons prototype  (Jürgen)
#           - rename requierd -> required
#           - rename headder -> header
# 02.04.20: => Ver. 0.75
#           - Corrected the uploading of the DCC programm (Start_Arduino_Sub.cmd and Start_Arduino.cmd was created in the "LEDs_Autoprog" directory)
#           - Started the Keyboard reading functions (PushButtonAction_4017)
# 03.04.20: - Added Hardis changes to the version from Jürgen
# 06.04.20: - Reading of the switches implemented (Analog, Border, Console, Direct)
# 12.04.20: - Solved Problem: "Manchmal wird der Dialog zum Eingeben der Logic Variablen nicht geöffnet"
# 13.04.20: - Skip0, ResetLong, OptCtrPar added to the "PushButton_w_LED_0_.." Funktion and changed to the function with variable brightness
#           - ConstRGB added
# 15.04.20: -> Send to Misha
# 16.04.20: - Corrected position of Check_Detected_Variables(). It was called before the variables have been filled ;-(
# 17.04.20: - Corrected the finding of macros in the "Lib_Macros" sheet in function "Find_Macro_in_Lib_Macros_Sheet()"
# 18.04.20: - Corrected Mouse Scrol al 64 Bit Office by Jürgen
#           - Changed the separator in Switch?_InpLst to space to be able to edit it in the dialog
#           - CTRL+Shift+T Could be used to translate the text in the Par_Description sheet
#           - Solved problem with MonoFlop2 <-> MonoFlop mix-up in the "Others" dialog
#           => Ver. 0.76
#           -> Send to Armin, Dominik, Frank, Juergen, Karl, Rolf, Michael (Link to GitHub)
# 20.04.20: - Select the Macro with the start letter by keyboard
#             Numbers in the middle are also supported
#           - Adding link to Wiki to the desktop
# 21.04.20: - Support for functions with a list of result variables like the Counter() function
# 24.04.20: - Scalling the House() dialog to 712/748 pixel height if it doesn't fit to the screen.
#             Normaly the dialog is 833 pixel.
#           => Ver. 0.77
#            -> Send to Hans-Peter
#           - Undefined varaibles are also searched in the DCC, SX and CAN imputs in Check_Detected_Variables()
#             to be able to use "INCH_DCC_1_GREEN" also as an input of a funcion
# 25.04.20: -> Uploaded to GitHub for tests
#           => Ver. 0.78
#           - Prevent crash if invisible data sheets are to be saved to a MLL_pgf file
# 26.04.20: - Started adding additional LED channels to the Switches and other separate strings
# 27.04.20: - Solved problem when inserting lines with the button and prior copying data to the clipboard
# 28.04.20: - New Macros "PushButton_RGB_0_?" and "PushButton_0_?"
#           - Additional LED channels finished
#           - Hopefully saved the MouseHook problem by storing the MouseHook to the Worksheet "Start" in the range A2
# 29.04.20: - Corrected the DCC send function to be able to uses 4 digit adresses 1000-9999
#           - If a macros with two inputs used #InCh+1 the InCnt entry is set to 2 to use two DCC channels
#             If the second input is a "Switch.." only one DCC input is used
# 30.04.20: - Using the formula ="" in the "Stat LedNr" column to prevent overlapping texts from the left cell
#           - Changed the parameter Skip0 to Use0 in the PushButton functions because it's easyer to understand
#             Attention: Existing macros have do be adapted !
#           - Changed the separator in userform other from "|" to "$" because "|" could be used in the Mode command of the counter
#             Example: Counter(CF_ROTATE|CF_SKIP0, ...
# 01.05.20: - Added Juergens store to EEPROM functions to texcel and the C-Code
#           => Copied to GitHub for tests
#           - Corrected the loading of MLL_pgf-fils. While importing data from old program the DCC Input type dialog
#             was opened for each line ;-(
#           - Corrected the "#define COLOR_CORRECTION 0x202020"
#           => Ver. 0.79
#           => Copied to GitHub for tests
# 02.05.20: => Ver. 0.80
#           - Corrected problem in the calculation of the reserved variables in Print_Keyboard_Defines_for_Type()
#             It doesen't reserve channels if Buttons > 8 have heen used ;-(
#             => The following variables have been overwritten ;-((
# 05.05.20: - Corrected problem in the DCC program "23_A.DCC_Interface.ino".
#             The serial port was not disabled at startup ;-(
#             If DCC messages have been received and send to the LED Arduino it was disabled
#             This generates problems when flashing the LED Arduino.
#           => Copied to GitHub for tests
# 06.05.20: => Ver. 0.81
#           - Corrected problem if array is empty in Is_Contained_in_Array() which appeares if
#             no Arduino is detected in Show_UserForm_Other()
#           - Macro to update the version in all sheets added
#           - Added the changes made in the DCC programm also to "23_A.Selectrix_Interface.ino"
# 07.05.20: - Changed Update_TestButtons() to be able to start with "Green"
#           - Changed the "InCnt" treatement of macros with 2 inputs. Prior the macros which use
#             exaxt 2 inputs have to be marked with "2!". This was not intuitiv because in all other
#             cases (1, 3, 4...) the number was allwas used direct.
#             Now macros like "RS_FlipFlopTimeout()" which could be used with two separate variables
#             have to be marked with "2?"
#             Example: RS_FlipFlopTimeout(DestVar, InCh, ResetVar) -> One additional,independand variable             => InCnt = 1
#                      RS_FlipFlopTimeout(DestVar, InCh, InCh+1)   -> Two variables read from "Adress or Name" column => InCnt = 2
#           - Check the number of input variables for functions which may use two inputs
#             like: "RS_FlipFlop(Test, #InCh, #InCh+1)"
#             If "SwitchD3" is used as input an Error message is generated because there is no "SwitchD4"
#           - Added MonoFlopReset
#           - Replaced the "|" also in the "House" dialog by "$". It has been replaced already in "M09_SelectMacro" a few days ago.
# 08.05.20: - Dialog "Use same LED as last line" is only shown if same LED Channel is used
# 14.05.20: - Added switch to the config sheet to be able to disable the new SPI communication mode between the two Arduinos
#           - Improved the HV_Reset() in the Tiny_UniProg according to Juergens tipp
# 16.05.20: - Copied to Github for Dominik
#           => Ver. 0.82
# 17.05.20: - Adapted Special_ConstrWarnLight() to the LED_Channels
# 19.05.20: - Copied to Github for Jürgen
#           - Finished the Herz..Relais.. Macros
#           => Ver. 0.83
# 20.05.20: - Bring excel to the top after sending the program to the Arduino. Prior the second program
#             in the ALT+Tab list was shown
#           -  Added macros Andreaskreuz with lamp test
#           - Library:
#             - Changed the SI_1 behavior. Now it's initialized after the Inp_Processed() call in the
#               constructor to trigger also the INP_TURNED_ON event. This was changed to initialize the state
#               for the Bin_InCh_to_TmpVar() macro which is used in the "AndreaskrLT..." macro
#                => ToDo: Check if this change influences other macros
#             - Changed the abort criteria in Proc_InCh_to_TmpVar and Proc_Bin_InCh_to_TmpVar to be able to
#               use SI_1 = 255 as an input to.
#               => ToDo: Check if this change influences other macros
# 22.05.20: - Added Push Button macros "PushButton2I_..." which have two inputs. They could be used to
#             control a function with DCC or a hardware button. THe function uses two DCC channals.
#             Red = off, Green = On / Next state
# 23.05.20: - Copied to Github for the Beta testers
#           - Deleted the old dialog: "UserForm_USB_Connection"
# 27.05.20: - Started with the Library and Board update function
#             - Tested wit Sketchbook Path "E:\Test Arduino Lib mit ä\"
# 28.05.20: - Finished Library and Board update function
#           => Uploaded to GitHub
#           - Corrected "Page_ID" on the Selectrix and CAN page
#           - Corrected "VarPtr" Problem at VBA7
#           => Uploaded to GitHub
#           => Ver. 0.84
# 30.05.20: - Added Options Tab "Updates"
#           - Using the Sketchbook Path also for the working directory
# 02.06.20: - Removed the accellerator keys in the data sheets because they didn't work except the "Options" button.
#             In addition Alt+O is often used in the find dialog.
#           - Added the new "Trig_to_TmpVar" function from Jürgen to the library
# 05.06.20: - Merged the Languages modul with the Pattern_Configuartor
#           - The Bring_to_front function is now working thanks Jürgen
#           - Corrected problem with the new "_USE_INCH_TRIGGER" in "Bin_InCh_to_TmpVar()" which came
#             up if SI_1 is used as input. If the "AndreaskrLT3_RGB()" is used without an DCC input the special
#             input SI_1 = 255 ist used. This generatesd an endless loop in Proc_Bin_InCh_to_TmpVar()
#           - Generate a message if a Windows version < 10 is detected and "curl" should be installed
# 06.06.20: - Using the new pyProg_Generator_MobaLedLib.exe
#           => Ver. 0.85 / 1.0.6
#           => Uploaded to GitHub Beta
#           - Corrected the LED Nr calculation for the Herz_BiRelais() macros.
#             If 3 Herz_BiRelais() lines have been used the second line uses the Blue channel of
#             the first WS2811 and the Red Channel of the second WS2811. The next Herz_BiRelais()
#             is connected to Green and Blue of the same WS2811. But the program assigned it to the
#             third WS2811 by mistake.
# 07.06.20: - Corrected editing of macro lines. The last parameter was not read back from the old line
#             caused by an "improvemend from 20.05.20 ;-(
#           => Ver. 0.86 / 1.0.7
#           => Uploaded to GitHub Beta
#           - Corrected Check of macros which may use two inputs like "RS_FlipFlop()".
#             They are marked with "2?" in the "Lib_Macros" sheet
#             Problem: If the input variable in the "DCC Adress" ended with a number (Example: "Reset1").
#             In This case a second input variable was expected ("Reset2"). Now this is only ecpected if
#             "#InCh+1" is used in the second parameter
# 08.06.20: - Corrected the "_USE_INCH_TRIGGER" functionality did influence the folloing TmpVar line ;-(
# 09.06.20: - Pattern_config:
#             - Splitted the examples in several groups which could be loaded separately
#             - Using also the background color to define a RGB LED group for thr LED simulation from Misha
#           - Added Ronnies KS Signals to the Library and to the Macro selection
#           - Reduced the RAM Uasage of the InCh_to_LovalVar macro form 2 Byte to one according to Jürgens tipp.
# 10.06.20: - New CANDLE room type and new Set_CandleTab() macro based on Roberts sources (352 additional Bytes)
#           - Optimized the switch case in "Proc_House()" file:"House.cpp" (Saved 18 Bytes)
#           - Corrected the editing of the HouseT() macro
# 14.06.20: - Added Misha's multiplexer
#           - Examples have been moved to the sheet "Examples". They could be copied with the options menu
#           => Ver. 1.0.8  (Same version vor the Library and the Excel sheet)
#           - Starting Auto Open macros when opening the Pattern_Configurator
#           - Copy also the Pattern_Configurator to the user directory and create the link
# 15.06.20: => Ver. 1.9.5
#           => Uploaded to official GitHub repository
# 16.06.20: => Ver. 1.9.5A
#           - Taranslated to Danish
#           => Uploaded to GitHub Quelldateien
# 20.06.20: - Disabled the "CHCP 65001" command at Win7 because the "Find" command hangs if this code page is used ;-(
#              The "Überprüfe..." message will be corrupted in this case.
#           - Prevent problems with the random goto activation: Random(#LocInCh, #InCh, RM_NORMAL, 5 Sek,  10 Sek, 1 ms, 1 ms)
#           => Ver. 1.9.5B
#           => Uploaded to GitHub Quelldateien
#           => Ver. 1.9.5C
#           - Don't use "curl" and "tar" if WIN7_COMPATIBLE_DOWNLOAD is set to TRUE
# 23.06.20: - Speed up the Arduino header file generation (took 45 seconds at a larger configuration with 130 LEDs and a lot od DCC (Harald))
# 24.06.20: - Updated the Modul "M07_COM_Port_New" from the Pattern_Config
#             - Translate the "Abbrechen" button
# 28.06.20: - Disabled the "CHCP 65001" command also when updating the libraries
#           => Ver. 1.9.5D
#           => Uploaded to GitHub Quelldateien
# 20.07.20: - Fast Build and Upload from Jürgen added (10 sec. instead og 23 sec.)
#           => Ver. 1.9.6 Uploaded to Github Beta
#           - Changed the destination directory to "\MobaLedLib\Ver_..." to be able to set one
#             exclusion in the virus scan program for all versions
# 23.07.20: - Adapted the fast Built function to a path with not ascii characters (Jürgen)
#           => Ver. 1.9.6 B  Uploaded to Github Beta
# 26.07.20: - Added the macros Herz_BiRelais_V1_?? for the WS2811_Relais modul HW Version 1 whre the Red and Green channels are swapped
# 28.07.20:
#           => Ver. 1.9.6 C  Uploaded to Github Beta
# 04.08.20: - Corrected the "ControlTipText" in the "House" dialog
#           - Limit the maximal servo value to 210 (Old 220) to avoid promlems with measurement errors at 2kHz
#           - Additional Delay and check if the old directory has been deleted when updating the Beta version
#           => Ver. 1.9.6 D  Uploaded to Github Beta
# 06.08.20: - Deletted >100000 columns in the DCC sheet which slowed down the loading of .MLL_pfg files
#           - Added a status display when loading the .MLL_pfg files
#           - Disabled the Message in Check_Hidden_Lines()
#           - Don't read the "Examples sheet from .MLL_pfg file
# 07.08.20: - Don't save the "Examples sheet to .MLL_pfg file
# 02.09.20: - Programming of the fast bootloader added
# 28.09.20: - Jürgen has added "Update_Start_LedNr" to the end of Read_PGF_from_String_V1_0() because other wise NUM_LEDS is 0
# 29.09.20: - Corrected the case in the Pattern*24 macros: t24 => T24
#           - Incremented the number of Pattern functions from 30 to 32
# 01.10.20: - New function "Mainboard_LED(MB_LED, InCh)" which could be used to use the mainboard LEDs as status LEDs
#           - Added macro "WeldingCont()" which continuously flickers while the input is active.
# 04.10.20: - Don't use the Heartbeat LED at PIN A3 if the CAN bus is used AND the SwitchB or SwitchC is used.
#             For some reasons the switches could be read in together with the CAN also without this change...
#           - Generate an error message if Mainboard_LED(4..) is used together with SwitchB or SwitchC.
# 05.10.20: - Created an example file to test the MobaLedLib main board: "Mainboard_Hardware_Test.MLL_pgf"
#             This file is stored in the directory "Prog_Generator_Examples" which is copied to the
#             library destination at startup.
# 07.10.20: - Added DayAndNightTimer which could be used with the Scheduler function
#           => Ver. 1.9.6 F
#           - Corrected the COM port in Write_Bootloader(). COM3 was always used ;-(
#           => Uploaded to Github
#           - Set the zoom factor to 100 in Release_or_Debug_Version()
# 08.10.20: - Added a timeout of one minute to the Restart_ProgGen.cmd in case "~$Prog_Generator_MobaLedLib.xlsm"
#             is not deleted for some reasons
#           => Ver. 1.9.6 G Uploaded to Github
# 09.10.20: - Finished the Mainboard_LED function
#           - New function LED_to_Var()
# 10.10.20: - Updated the Mainboard_Hardware_Test.MLL_pgf
#           - Improved the loading of MLL_pgf files
#             - Corrected problem with lines starting with "=="
#             - Add the sheets to the end => They are sorted in the way they are stored in the file
#           => Ver. 1.9.6 H Uploaded to Github
#           -  Possibilitiy added to ignore problems with the baud rate detection in
#                Check_If_Arduino_could_be_programmed_and_set_Board_type
#           => Ver. 1.9.6 I Uploaded to Github
# 11.10.20:
#           - The Mainboard_LED function also acceppts the arduino pin numbers D2-D5, D7-D13 amd A0-A5
#           => Ver. 1.9.6 J Uploaded to Github
#           - Don't gray out the other rooms in the House/Gaslight dialog. Instead the important buttons
#             use bold font
# 12.10.20: - Corrected the entering of selextrix data and the position of the USB simulation buttons
#           - Disabled the "ENABLE_CRITICAL_EVENTS_WB" to hopefully get rid of the crash which is generated
#             if lines are deleted in the Pattern_Configurator.
#             By disabling this events the LED numbers are not updated if lines ade hidden or shown again.
#           - Corrected the NEON_DEF2D entry. Channel 1 was used instead of channel 2. This caused the occupation
#             of a new RGB channel if NEON_DEF1D and NEON_DEF2D was used in a sequence
#           - Improve the detection probability in "DetectArduino()". Prior the arduino was not always detected
#             at the first trial. Some Arduinos have not been detected at all. By invreasing the delay
#             form 10 ms to 200ms even my critical arduino us detectet every time.
#             The ATMega328PB is also detected.
# 15.10.20: - Extracted the compiler call in "Compile_and_Upload_to_ATTiny85.cmd"
#             into "Compile_and_Upload_to_ATTiny85_Sub.cmd"
#             to be able to check the error code. Prior the Find command has overwritten
#             the result => Errors have not been detected ;-(
#             This has been changed in the Servo and the Charlieplexing directory
# 16.10.20: - Increased the number of Time entries from 30 to 64 and corrected the entries 24-30
#           - New Charliplexing software which supports the 64 time channels
#           => Ver. 1.9.6 K  Uploaded to Github Beta
# 17.10.20: - Corrected problems with the Examples sheet which was caused by excluding the
#             sheet from the Data sheets:
#             - Resetting the COM Port at program start
#             - Copying data from the sheet to an other sheet
#             - Selecting the Macros per dialog
#           - Using Juergens changes in the C-Code (See MobaLedLib.cpp)
#           - Scroll to the left in all data sheets when the release version is generated to make the buttons... visible
# 18.10.20: - Added support of the additional buffer gate on the main board version 1.7
#           => Ver. 2.0.0 Uploaded to Github Beta
# 21.10.20: - Jürgen corrected the check of the Mainboard LED number to be able to enter also numbers
# 25.10.20: - Corrected the Mainboard_LED() function when D4 was used
#           => Ver. 2.0.0A Uploaded to Github Beta
# 26.10.20: - Corrected the loading of old data
#             - Problem when adding empty lines if the "Start" sheet is active
#             - Dont detect old versions if the user started wit Ver. 1.9.6
#           - Define at least 20 LEDs to be able to test then with the color test program
# 27.10.20: - Pattern_Configurator:
#             Disabling the Event which is called when Enter is pressed when the workbook is colosed
#             Hopefully this solves the problem that the Pattern_Config is opened sometimes unintentionally
#           - Prevent crash if a wrong formula is entered like "-Test"
#           => Ver. 2.0.0B Uploaded to Github Beta
# 29.10.20: - Added Jürgens changes (Date 28.10.20)
#             - Integrated privateBuild.cmd into Start_Arduino_Sub.cmd
#             - Copy the hardware directory to LEDs_AutoProg to be able to use the own board
#               definition file "boards.local.txt" which contains the configuration which uses the additional
#               1.5K which are not needed with the new bootloader
#               => Changed to the user directory 01.11.20
#             - Added the detection of the Nano Every and adapted the program to generate the correct code
#           - Reserve only 512 Byte for the bootloader when the fast bootloader is installed
# 30.10.20: - Using the new optiboot bootloader 8.0 to indicate that the fuse HFuse is set to DE (use only 512 byte)
#           - Updating the arduino typ in the "Options" dialog if the USB Port detection is started
# 31.10.20: - Charlie_Buttons and Charlie_Binarycontrol 3 channels (RGB) instead of 2 (GB)
#           - Corrected the maximal time for the Blinker function by adding PF_SLOW
#           - Prior the maximal period was 65 Seconds. Now it's 17 minutes like defined in the Par_Description sheet
#           - Checked all times which are limmited to 17 Minutes (1048560)
# 01.11.20: - Changed the support for the new CPU type "ATmega328P (New Bootloader full Mem)"
#             Now the boards package is copied only once to the user dir if there is not already
#             a board package installed.
#             + Arduino IDE shows the ney CPU type
#             + Also works if the user has installed an own boards package
#             + boards package has to be copied ony once
#           - Pattern_Configurator:
#             Corrected the support for 64 time entries. Unfortunately the prior changes have been made in
#             the wrong worksheet and not in the Main sheet => They have been lost when the release
#             version was build ;-(
# 02.10.20: - Using the new OptiBoot version from Jürgen which has the provate version number 108.1
#             This number is used to detect if the HFUSE have been set to the small memory usage of 512
#             bytes in the boot loader.
#           - Disable the mouse scroll function for Office <= 2007 because here excel generates a crash
#           - Changed the font size of the House buttons because the texts don't fit since they are bold
#           => Ver. 2.1.0 Uploaded to Github Beta
# 04.11.20: - Corrected problems with the new functions to read in the Mainboard switches which disabled the
#             SwitchC and SwitchD functions by mistake
#           => Ver. 2.1.0A Uploaded to Github Beta
#           - Corrected the path for the "optiboot_atmega328_Ver108.1.hex" file and added an error message in
#             "GetShortPath()" in case the patht was not found.
#           - The "WriteFastBootloader.cmd" is created every time. Prior it was written only it it doesn't exist.
#             This generates problems if a beta version is used which uses the same directory. In this case
#             corrections in the "WriteFastBootloader.cmd" creation are not written ;-(
#           - The activation of the compiler switch "USE_SWITCH_AND_LED_ARRAY" is not working !!!!
#           => Ver. 2.1.0 B Uploaded to Github Beta
# 05.11.20: - Sepeed up the Office 2007 in the Mouse scroll function because otherwise the scrolling is to slow
#           - Added: __attribute__ ((packed)) to the typedefs to be able to use it on oa 32 Bit platform
# 09.11.20: - Removde the old Debug functions to simulate DDC commands:
#               TEST_PUSH_BUTTONS()
#               TEST_TOGGLE_BUTTONS()
#               TEST_BUTTONS_INCH()
#           - Tryed to speed up the mouse scroll, but it dosn't work
# 10.11.20: - Started the ESP32 support
#             - Adapted the LED_PINNr_List
#             - Added ESP32 library to the "Libraries" sheet, but it's not installed automatically yet
#               This is disabled by the "*". It could be installed mannually  by checking the select column
#               and pressing "Install selected"
# 11.11.20:   - Added the ESP to the "Options" menu
# 13.11.20:   - Experimental support for the ESP32 finished
#           => Ver. 2.1.1 A Uploaded to Github Beta
# 16.11.20: - Generate error message if the macros BlueLight1(), BlueLight2() and Leuchtfeuer() are used with 3 LEDs
#           - Generate error message if the LED number is negativ which could be caused by a wron Next_LED argument
#           => Ver. 2.1.1 B Uploaded to Github Beta
# 17.11.20: - Sending the partition information always to the ESP32 to make sure that they are correct.
# 28.11.20: - Adapted the Switch? pins for the ESP32
#           - Additional check in "Create_Start_ESP32_Sub" from Jürgen which rebulds the libraries
#             in case the librarys have been changed
#           => Ver. 2.1.1 C Uploaded to Github Beta
# 30.11.20: - Changed some ESP32 pins
#           - Added #define IRAM_ATTR in Keys_4017.h to be able to use it with the Arduino
# 01.11.20: - New experimental console display while compiling the Arduino program which could be
#             enabled in the "Config" sheet.
#           => Ver. 2.1.1 D Uploaded to Github Beta
# 02.12.20:
#           => Ver. 2.1.2 Uploaded to Github Beta
# 06.12.20: - Fixed problem scaling the house dialog for small screens (1366x768).
#             Some entries have not been hidden when "Gaslights" was used because of rounding problems
#           => Ver. 2.1.2 B Uploaded to Github Beta
# 27.12.20: - Corrected the "Get_Nr_From_Var()" function to find the last number in the string.
#             Prior the first naumber was detected. This caused problems when a variable like
#             "Tast1RGB00" was used in the PushButton function.
#           => Ver. 2.1.2 C Uploaded to Github Beta
# 02.01.21: - Corrected the "Bold" Font in the "Gaslight" dialog at small screens
#           => Ver. 2.1.2 D Uploaded to Github Beta
#           - Corrected the spelling in some hints
#           => Ver. 2.1.2 E Uploaded to Github Beta
# 18.01.21: - ColorTest:
#             - Corrected the path for the "MobaLedTest_Close.Txt" to be able to close the programm from excel
#             - The dialog "Standard oder letzte Benutzer Farbtabelle verwenden?" is only shown
#               when it's called from the "Set_ColTab" command.
#             - Generating the file "ColorTestOnly.txt" to the python program to show a different user interface
#               to clarify the function of the program. Some users have been confused that the same color
#               dialog is shown from the "Options" menu and the "Set_ColTab" command. Hope that it's now
#               easier to understand.
#           - Added 7 new signals from Matthias (schma29)
# 19.01.21: - Don't decrement NumLeds if "Next_LED" is used with a negativ argument. (Mail form Juergen 03.12.20)
#           - Jürgen corrected the translation macro
#           - Added the Bin-signals also for the signals from Ronny and Matthias
#           - Brightness of all signals coulc be changed (Attention: This will affect existing configurations)
#           - Improvements from Jürgen:
#             - Status of the test buttons is reset if the program is send to the arduino if Store_Status is not used
#             - Ability to use DMX modules!!! It is enabled with the command "Use_DMX512()"
#               Only a Max485 module is needed!
#             - Ability to switch the LED portocol to WS2811 where the Red and Green channel
#               is swaped compared to the WS2812.
# 20.01.21: - Update DMX channels if the FarbTest is used
#           - Disabled some debug messages in the C-program
#           => Ver. 2.1.3 Uploaded to Github Beta
# 27.01.21: - Corrected the generation of the COLTEST_ONLYFILE.
#           => Ver. 2.1.3 Uploaded to Github Beta (No new version number)
#           - Corrected the Examples 22 and 25
#           - Added new faster method to download and execute the Color test program
#           => Ver. 2.1.3 C Uploaded to Github Beta
# 10.02.21: - Added Mishas changes
#           => Ver. 2.1.3 E Uploaded to Github Beta
# 12.02.21: - Jürgen added a filter to the "Select Macros dialog"
#           => Ver. 2.1.3 F Uploaded to Github Beta
# 13.02.21: - Jürgen corrected the "Select Macros" filter
#           - In addition the comments are also parsed for the filter string
#           => Ver. 2.1.3 G Uploaded to Github Beta
# 03.03.21: - Jürgen changed a lot of things concerning ESP32
#             - List of valid analog/digital for ESP32 pins has been completed
#             - Extension from 4 to 9 Led channels
#             - Generate the code for ESP32 analog support
#             - Check the installed ESP32 toolchain, error message if wrong one is installed
#             - Generate the ESP32 scripts now considering the installation directory of the Arduino IDE
#             - In case the flashing of the ESP failed, no error message was displayed so far -> fixed
#             - Preparation for support of other ESP32 toolchains (not finished yet)
#             - Libraries Sheet: new type BE = BoardExtensions + associated new helper functions Get_Lib_Version and Get_Required_Version
#             - AnalogButtons: New table of analog threshold values for ESP32, currently test output of values on serial interface
#             - MobaLedLib: Output of the configuration on the serial interface
#           => Ver. 2.1.3 H
# 03.03.21: - Jürgen use only one column for start led number display, may be configured on config page
#           - check number of max. allowed leds depending on processor setting: 256 for Arduino, 16384 for ESP32
#           - turn of FastLED's 'Dither' feature - avoids that FastLED sends slithliy different brightness values (problematic for Servo/Sound)
#           => Ver. 2.1.3 I
# 06.03.21: - Jürgen correct ADC Deltas
#           - fix bug that button ADC isn't polled if LDR isn't enabled
#           - fix bug the Com-Port is locked when com port selction dialog is closed with "X"
#           - add xcopy parameter /Y: has blocked build when overwriting "LEDs_AutoProg\boards.local.txt"
#           => Ver. 2.1.3 I2
# 06.03.21: - Jürgen corrected LDR issue
#           => Ver. 2.1.3 I3
# 08.03.21: - Jürgen implemented ESP32 CAN support
#           - need new Library CAN 0.3.1
#           - new feature #define COMMANDS_DEBUG
# 09.03.21: - Jürgen check minimum version of NRMADcc to be 2.0.6
#           - force ESP32 rebuild in case of ProgramGenerator, library or board update
# 11.03.21: - Jürgen:
#           - when running Gen_Release_Version
#             set the cursor to a defined position in data sheets
#             correct column width
#           - add flashing of ESP32 boot and bootloader partition
#           => Ver. 2.1.3 I6
# 12.03.21: - Jürgen: fix colum headers and layout in examples page
#           - check manadatory libraries for ESP32 builds
#           - force ESP32 rebuild if SHIFT key is down while starting sending to arduino
#           => Ver. 2.1.3J -> push to git
# 18.03.21: - Jürgen: fix issue where directory names contain blanks
# 20.03.21: - Jürgen: fix DCC offset problem when sending simulated DCC commands
# 21.03.21: - Jürgen: clear also DCC test buttons when clearing a sheet
#           => Ver. 2.1.3K
# 26.03.21: - Hardi: speed up ResetTestButtons function
#           - Jürgen: fix problem with rows having multiple DCC on/off test buttons
#           => Ver. 2.1.3L
# 06.04.21: - Hardi: Added translations from Theo
#           => Ver. 2.1.3M
# 21.04.21: - deploy Release 3.0.0
#           => Ver. 3.0.0
# 18.04.21: - Jürgen: add experimantal Raspberry Pico support
# 23.04.21: - ubit: Parameter select "Values:" added to UserForm_Other for ServoMP3
# 24.04.21: - Jürgen: add Raspberry Pico Mainboard Leds, Mainboard Buttons, PushButtons
# 25.04.21: - Jürgen: disable Autodetect when changing CPU type to ESP32 or Pico
#           - fix some typos in start sheet text
# 26.04.21: - ubit: Bugfix USerform_Others
# 26.04.21: - Dominik -> change width of Form and new pos for Buttons at Form Other
# 03.10.21: - Hardi: Started new TreeView based macro selection dialog
#           => Ver. 3.0.0 C
# 07.10.21: - The filter is also activated by typing letteres in the Old ListBox macro selection
#           - Corrected start focus and tab index of the Userform_Other (Prior sometimes the 'Abort' button had the focus)
#           - Solved problem if the user has no additional board installed. In this case the "packages" directory
#             has to be created in C:\Users\<Name>\AppData\Local\Arduino15\
#           - Splitted the installation of several board packages into separate calls because otherwise the instalation
#             fails. (I thought that Jürgen fixed this already)
#           => Uploaded to Github Beta
# 10.10.21: - Jürgen: remove NmraDCC library installation workaround as version 2.0.10 fixes the ESP32, no more need to install from private repository
# 12.10.21: - Jürgen: add new feature to control sound modules attached to the mainboard  (currently limited to Arduino Nano and JQ6500)
# 14.10.21: - Jürgen: add new sheet Platform_Paramters containing all platform dependend settings
# 15.10.21: - Jürgen: add new feature Pin_Alias
#           - add ESP32 support for Mainboard Sound Modules
# 18.10.21: - Merged the changes from Micael and Hardis to the version from Jürgen
# 19.10.21: - Always use the full packed mode for the JQ6500 modules because this mode could be used with both
#             types of modules (Original JQ6500 chip or JZ chip (AA20HFJ648, AA..., AS20HGN403)
#             The packed mod sends all bytes at once and not distributing them on several main loops.
#             This is necessary for the JZ chips. This takes 5ms, but that's O.K. since the sound command
#             is not send verry often.
# 20.10.21:
#           => Uploaded to Github Beta
# 20.10.21: - Added "On Error Resume Next" to prevent crash with Office 365 in EnableDisableAllButtons()
#           - Replaced ".Add2" by ".Add" in Sort_by_Column because this new function is not
#             supported by Office 365 ?!? This solves Ulrichs problem.
#             (See: https://www.mrexcel.com/board/threads/vba-difference-in-sort-with-add2-and-add-sortfields-add2-vs-sortfields-add.1072594/)
# 25.10.21: - (Hopefully) prevent formating the "Start LEDNr" as date by setting the NumberFormat to "General" when importing files.
# 29.10.21: - Adapted the cmd files to work with 32 bit windows
#             (Arduono is installed to "Program Files" and not to "Program Files (x86)")
#             Checked also the VBA programs in Prog_Gen and Pattern_Conf
#           - Update the filter if a row is selected which already contains a macro to show the macro
#           - Show please wait screen when loading/updating the tree view
# 31.10.21: - Fixed bug when loadimg the Excel File. Thge Pattern Configurator icons in the lines have been deleted
#           => Uploaded to Github Beta Version 3.0.0 L
# 04.11.21: - Update the icons when copying lines with the button
#           - Improved the scrolling in the userform others
#           - Added a scroll bar to description in the TreeView dialog
#           - Added #define SWITCH_DAMPING_FACT to the Lib_Macros
# 05.11.21: - Imported Michaels changes in the Lib_Macros sheet
#           - Added the possibility to scroll with the mouse in the description box of the TreeView dialog
#           => Uploaded to Github Beta Version 3.0.0 M
# 06.11.21: - Juergen: Fix issue on Scroll in UserForm_Other (focus lost)
#           - make UserForm_Other resizeable
#           - add first prototype of MP3-TF-16P support
#           - Version N
# 10.11.21: - Don't move the LED channel selection in UserForm_Other when resizing the dialog
#           - Prevent crash when the TreeView is closed with the 'x' button and reopened again
#           - Merged Jürgens version with the Changes in the Lib_Macros sheet from Michael
#           => Uploaded to Github Beta Version 3.0.0 P (There is no version O because this looks like a number)
# 11.11.21: - Added missing files from Jürgen
# 12.11.21: - Juergen: change Pico Platform to 1.9.6, add missing Platform Pins
#           - As ESP32 is no longer experimental set library U8g2 to mandatory
#           - fix some typos in start page text
#           - fix issue that load of old configuration was not started while a Beta update
# 13.11.21: - Juergen fix issue #6894 BetaUpdate won't run with UserDir containing blank chars
# 14.11.21: - Juergen fix LED_to_var - Led_Offs to 31. See #6899
#           - publish 3.0.0.RC2
# 14.11.21: - Juergen fix VB6 FindWindow Issue #6914
#           - publish as 3.0.0.RC2a
# 15.11.21: - Juergen fix another VB6 Issue in Userform_RunProgram
#           - workaround for Excel 2007 isNumericBug
#           - add missing EspSoftwareSerial library
#           - publish as 3.0.0.RC2b
# 17.11.21: - Juergen FIX with Platform_Parameters: with AM328 SPI Pins are only usable if no CAN module is in use
#           - remove invalid default 'KEY80_P1' from Pin_Number Parameter
# 19.11.21: - change icons DiceG, Heartbeat, Stairs, Variable
#           - Allow relative path in ImageBoxAdder
#           - Reload all Icons when running GenReleaseVersion
#           - support of BETA update directly from github
#           - add the build date as a tooltip to the version information cell
# 22.11.21: - Juergen: Add Excel version check
# 26.11.21: - Hardi: Using a separate parameter name "Pin_NumberK80 for macro "SOUND_CHANNEL_DEFINITON()"
#             and added the default text "KEY80_P1" because this macro is used not only by experts.
#           - Test_Sufix = "RC4"
#           - Disabled the "DebugMode" in the VBA Editor ("Extras/Eigenschaften") because otherwise
#             Statistics are shown in the TreeView form head line
#           - Corrected some embarrassing typos
#             - Sheet "Par_Description":  "Maximal Active Zeit"  => "Maximal aktive Zeit"
#             - "Fehler beim schreibenn"                         => "Fehler beim Schreiben"
#             - "Fehler beim schreiben"                          => "Fehler beim Schreiben"
#             - "Fehler beim lesen"                              => "Fehler beim Lesen"
#             - "der der Programm"                               => "der Programm"
#             - "Arduio", "Arduiino", "Ardiono", "Ardino"        => "Arduino"
#             - "Schweißlich"                                    => "Schweißlicht"
#             - "Simmulation"                                    => "Simulation"
#             - "bibstabile"                                     => "bistabile"
#             - "Hautpplatine"                                   => "Hauptplatine"
#             - "Pasendauer"                                     => "Pausendauer"
#             - "beeinfusst"                                     => "beeinflusst"
#             - "Durch verwendung"                               => "Durch Verwendung"
#             - "Postionen"                                      => "Positionen"
#             - ...
#           - New function LastColumnDatSheet() which is used in all places where
#             the data sheets are processed. Since 03.04.21 an modified LastUsedColumn()
#             has been used which returned a constant column to skip the hidden variables
#             Unfortunately this modified function has also been used in other sheets.
#           - Improved the translation function to handle '%' in the texts
#           - Lib_Macros Sheet: Corrected the case/wording in the "group names" column in
#             different languages to group the lines correctly
#           - change release to 3.1.0
#           - publish release
#
# 02.12.21: - Fix ESP32 build issue with non-default arduino home directory
#           - Fix issue in case Arduino home directory doesn't exist
# 06.12.21: - Add Selectrix support for ESP32
#           - fix issue with empty lines in libraries sheet
# 10.12.21: - Add Macro RGB_Heartbeat_Color
# 14.12.21: - Improve Macro RGB_Heartbeat_Color to support variable pulse duration
#             Fix some typos
# 16.12.21: - Add missing macros InCh_toTmpVar1 and BinCh_toTmpVar1
#             mark those makros to disable status storage (Goto 0)
#           - add handling of multiline makros in makro storage type detection
# 21.12.21: - code changes to allow programmatic header file creation
# 16.01.21: - fix bug in AnalogPattern
# 21.01.22: - add experimental integration of PlatformIO build
#           - add experimental integration of OTA update
# 12.02.22: - add MobaLedLib Extensions support
#           - add WebApi helpers
# 13.03.22: - experimental platform.io build support
# 04.03.22: - add experimental LED simulator support
# 12.03.22: - add 64bit support for LED simulator
# 15.03.22: - fix issue that back to PatternConfiguration" didn't work anymore
#           - add ColorPicker for Const Makro
# 17.03.22: - Simulator may switch between RGB and Single-LED view with doubelclick
# 24.03.22: - fix DCC Offset bug with simulator
#           - third simulator view displaying combined and single LED
# 09.04.22: - fix rebuild issue with ESP32
#           - change ESP32SoftwareSerial library source to a bugfix repository - as
#             long the bug isn't fixed in then main library
# 17.04.22: - add Led2Var support to simulator
#           - fix empty configuration warning if ony extensions are active
#           - fix extensions include problem
# 01.08.22: - fix CAN baudrate issue with ESP32 V1 chips
# 03.08.22: - change release to 3.2.0
# 09.08.22: - fix memory issue with Arduino Nano and ESP32 librarires
#           - change release to 3.2.1

# ToDo:
# ~~~~~
# - Pattern_Configurator:    27.11.21:
#   - Support für die zusätzlichen korrigierten schreibweisen der #defines PM_SEQUENCE_W_RESTART, ... in
#       Private Function Get_Mode_Nr(Par As String, XMode As Boolean) As Byte
#    einbauen.
#   -  Schreibfehler in Dialog " ATTiny Porgrammer - Servo-MP3" Siehe Mail von Formue vom 27.11.21:
# - Vor dem Senden sollten die Min und Maxwerte der Makros überprüft werden.
#   Hintergrund: Anfangs habe ich 220 als Max Wert für die Servos vorgegeben. Das funktioniert
#   aber nicht immer weil die PWM Messung bei einem neuen WS2811 mit 2kHz PWM nicht mehr so genau ist.
# - Disable DEBUG_DCCSEND
# - DCC Buttons
#   - nur dann aktiviern wenn Häckchen gesetzt ist
#   - Code soll so lange gesendet werden wie die Maus gedrückt wird
#     damit man auch einen Langen Tastendruck simulieren kann. Problem dabei
#     ist der Timeout in der DCC Routine. Vielleich braucht man das aber auch nicht.
#   - Beim löschen von Zeilen sollten die Buttons auch gelöscht werden
#   - Die Buttons sollen nur erscheien wenn eine Address Nummer und Ein Typ angegeben wird
# - Wenn der "Lösche Tabelle" Button gedrückt wird sollten wieder ein paar leere Zeilen Entstehen
# - Das automatische Hinzufüggrn neuer Zeilen funktioniert nicht in der ersten Zeile
# - FastLED Version und Compiler Version prüfen
# - Schalter einlesen
# - Das Einlesen des LDRs braucht relativ viel Speicher 1404 FLASH (5%), 123 RAM  (06.04.20)
#   Das Hauptproblem ist aber die AnalogScanner Bibliothek: 914 FLASH, 114 RAM
#   Es wird viel Ram belegt weil einige Konstanten unnötig groß sind:
#      ANALOG_INPUTS = 15  (8 würde reichen => 28 Byte könnten gespart werden)
# - Neue Dialoge und Fehlermeldungen übersetzen
# - Manchmal wird der Pattern_Configurator geöffnet wenn man Enter drückt => Untersuchen
#   Tritt nicht mehr auf wenn man Exel schließt und das Programm wieder neu startet
# - Es existiert keine Hilfe für den "Lösche Raum" Button im House Dialog
# - #Include Files verschoben in LEDs_Autoprog.h
# - Parameter Datei verändern und nicht mehr die Config Datei. Mail von Harold 1.1.20
# - Bei einem Fehler muss die "MobaLedTest_config.json" ganz neu erstellt werden können
# - Vor dem senden zum Arduino den ColorTest schließen oder den ComPort trennen
# - Eigene Daten automatisch speichern
# - Prüfen ob eine neue Version des CheckColor Programms verfügbar ist.
# - Library Path erkennen oder in dem Config sheet speichern wenn man nicht den Standard Pfad verwendet
#   => preferences.txt: sketchbook.path=C:\Users\Hardi\Documents\Arduino
# - Testen der Beispiele
# - Hilfe einbauen dass die SINGLE_LEDs in aufsteigender Reihenfolge sein müssen
# - Das Servo Tool verwendet den roten Kanal. Das passt aber nicht bei dem S3PO Modul
# - Manchmal wird nach der Auswahl der Funktion gleich nochmal nachgefagt.
#   Ich hab aber noch nicht herausgefunden wann das passiert.
# - Beim Verschieben von Zeilen mit aktivem Filter sollte die Zielposition
#   direkt unter der darüber liegenden sichtbaren Zeile sein.
#   Momentan wird es vor die erste Zeile geschoben welche sichtbar ist.
# - Die SingleLEDs im Haus gehen nicht sofort aus => Untersuchen
# - Par_Description ergänzen:
#     Blink3...: Pause, Act, In welchen Bereich können die Zeiten liegen
#     Val0, Val1 werden beim Blinker3 anderst verwendet als z.B. Beim Button
#     => Überprüfen
# - Installation:
#   - Updates der MobaLedLib sollen erkannt werden
#     => Wie soll das gehen? Zunächst doch manuel anstoßen
#   - Version aus der library.properties Datei auslesen. Momentan wird nur dann was gemacht wenn die Bibliothek fehlt
#   - Die alten Daten der User müssen bei einem Update erhalten bleiben
#     => Funktion zum Speichern der Daten einbauen
#   - Arduino IDE Installieren per Dialog?
#     Dann bräuchte man nur die Excel Datei herunterladen.
# - Doku:
# - Old Bootloader
#  - Menu / Meldung
#  - Installieren des Bootloaders
# - Rechtschreibprüfung für alle Ausgaben/Dialoge
#   Done:
#   - M07_COM_Port
# - Probleme mit Office 2003 und kleiner bei Wilfied:
#   Hier gibt es auch Probleme mit der Anzahl der Zeilen/Spalten
#   Decode: If Exp_Rows > 64000 And val(Application.Version) < 12 Then  '(BKR): message box only for Office 2003 and older versions
# -----------------------------------
# - Vor dem beenden eine Meldung anzeigen wenn die Datei noch nicht gespeichert wurde
#   - COM Port einstellungen gehen verloren
# - Sound Befehle zusammenfassen wie beim Baustellenlicht
# - Ilumination Makro in die Bibliothek einbauen (Beispiel 16) => Nein: Braucht zu viel Speicher
# - Im Macro Auswahldialog soll man mit den Anfangsbuchstaben zur entsprechenden Zeile springen können
# - Erkennen wenn man in die Makro Spalte etwas kopiert ohne dass auch die folgenden Spalten
#   mit genommen werden. Das gibt ein Problem mit den Versteckten Spalten InChCnt , ...
# - Es ist nicht Gut wenn das Programm mit EndProg beendet wird. Dann werden alle Variablen
#   gelöscht. Das betrifft auch die Dialoge und deren Position.
# - Das Warnlevel für den RAM kann man evtl. mit dieser "Preverenzes" Eintrag verändern: build.warn_data_percentage=75
# - Kommentare im Programm
#   - Kurze Beschreibung zu jedem Modul
# - Im DCC und Selectrix Programm sollen noch zusätzliche Statusmeldungen zur
#   Diagnose eingebaut werden
#   - DCC vorhanden/nicht mehr vorhanden
#   - Pegelwechsel erkennung auch bei Selectrix Taktleitung
# - Der Uno kann mit diesem Board Parameter verwendet werden: '--board arduino:avr:uno
# - Überprüfen ob das richtige Programm für DCC/Selectrix Arduino
#   installiert ist (Rs232 Meldungen lesen)
# - Die Excel Meldung: "Zahl ist als Text Formatiert" und das Grüne Dreieck ist nicht schön
# - Die InputBox() ersetzen da diese nicht mit ESC Abgebrochen werden können und
#   nicht zur Aplication zentriert sind
# - Arduino Bibliotheken überprüfen und geg. installieren
# - Einstellungsbutton
# - Prog_Version in die Sheets übernemen beim Generate Release
# - Manchmal kommt ein Interner Kompiler Fehler.
#   Beim zweiten Compile Versuch ist er weg. => Untersuchen
#   Hier wird das beschrieben: https://arduino.stackexchange.com/questions/58495/strange-compiler-error-segmentation-fault
#      C:\Users\Hardi\Documents\Arduino\libraries\FastLED/controller.h: In member function 'clearLeds':
#      C:\Users\Hardi\Documents\Arduino\libraries\FastLED/controller.h:76:82: internal compiler error: Segmentation fault
#        virtual void clearLeds(int nLeds) { showColor(CRGB::Black, nLeds, CRGB::Black); }
# - Nicht aktive Zeilen sollten Grau dargestellt werden. Evtl. per Bedingter Formatierung. Dann kann der User
#   Trotzdem eigene Farben verwenden.
# - Die beiden Arduinos sollen unterschiedlich Blinken damit man erkennen kann wenn das falsche Programm
#   auf den Rechten Arduino geladen wurde.Die LED des DCC Arduinos macht gar nichts
# - Evtl. muss man noch den Programmer angeben. Aber das klappt nicht. Ich habe verschiedenen
#   Varianten dieses Strings probiert: --useprogrammer "arduino:arduinoisp"
#   Wenn ich nur --useprogrammer verwende, dann will er den ATTiny programmieren
#   Vielleicht braucht man den Parameter gar nicht.
#
# - Warnung bei doppelter Adresse (Gelber Text (Hint))
#   Dazu kann die Notiz Funktion verwendet werden. Zu beginn wird die Notiz in
#   beiden betroffenen Zellen Dauerhaft angezeigt. Nach 10 Sekunden wird sie wieder
#   ausgeblendet. Dann erscheint sie nur noch wenn man mit der Maus drüber fährt.
# - Die Dialoge sollen auch mit ALT+Taste zu bedinen sein. Aufgefallen beim
#   UserForm_Other. Man müsste für jede Variable einen Buchstaben ablegen
#   => Das Programm das einfach selber anhand der Anfangsbuchstaben generieren
# - Die Standard MsgBox ist zum BS zentriert. Das Gefällt mir nicht.
#   Alle Anderen sin zum Fenster zentriert. In der UserForm_Initialize()
#   wird überall Center_Form Me aufgerufen. Dadurch, dass das nur beim
#   initialisieren gemacht wird bleiben die Buttons ach an der Stelle wenn
#   sie verschoben wurden bis das Programm neu gestartet wurde.
# - Wenn die Hilfe Datei nicht lokal vorhanden ist, dann kann man die
#   - Aus dem Bibliotheksverzeichniss
#   - oder von GitHub laden
# - Wenn eine neue Konfiguration geschickt wird welche weniger LEDs ansteuert als die
#   vorangegangene, dann bleiben u.U. alte LEDs an. Das ist sehr verwirrend. Darum
#   soll das Arduino Programm erst alle 256 LEDs 0 setzen.
#   Dazu wird aber viel Flash benötigt. Evtl. kann man das in der Bibliothek machen.
#   Ich habe bisher nur das gefunden: https://forum.arduino.cc/index.php?topic=556914.0
#   Ganz unten steht, dass er zwei Bereiche definiert hat. Einen mit 22 LEDs und einen mit 242
#   Beide menutzen eigene Pins. Diese hat er aber miteinende verbunden und aktiviert
#   immer nur einen als Ausgang.
# - UndoFunktion für Zeilen Löschen
#   Zeilen beim löschen in ein eigenes Sheet verschieben. Auch bei "Lösche Tabelle"
# - Die Signale sollen zusammengefasst werden so dass der User nicht von dem InCh_to_TmpVar() sieht
# - Entry_Signal3_RGB ist nicht in der Bibliothek enthalten
#   - Das braucht man nur für Tests
#   - In die Bibliothek sollte rein Makro welches beides enthält:
#       InCh_to_TmpVar(#InCh, 3) // Eingang in in 8 Bit Var umwandeln
#       Entry_Signal3_RGB(#LED)
#     Am besten auch noch als Binär
#     - Entry_Signal3_But_RGB
#     - Entry_Signal3_Bin_RGB
#     - Entry_Signal3_But
#     - Entry_Signal3_Bin
#   - Das Macro darf nicht im Testprogramm sein sondern muss in dem Excel Makro stehen
# - Mehrbegriffige Signale können mit Selectrix auf verschiedene Arten angesteuert werden
#   - Jeder Zustand wird von einem eigenen Bit gesteuert. Immer wenn sich das Bit
#     ändert wird der Zustand aktiviert. Damit ist die Zuordnung zu den Signalbegriffen
#     einfach aber es werden mehr Kanäle benötigt. Ein 4 begriffiges Signal belegt 4 Kanäle
#   - Die Zustände werden binär kodiert. Hier benötigt man nur zwei Bits für ein 4 begriffiges Signal
# - Beim "Alle Einblenden" Button Fragen was eingeblendet werden soll (AutoFilter / Versteckte Zeilen)
# - Eine Tabelle mit Umschalter (DCC/SX/CAN) oder mehrere Tabellen?
# - Testprogramm 23_B.DCC_Rail_Decoder_Receiver.ino aufräumen und neuen Namen vergeben
#   - Die Progamme für den DCC Arduino beginnen mit 23_A.
#     (z.B.: 23_A.DCC_Interface, 23_A.CAN_Interface, 23_A.Selectrix_Interface, 23_A.LocoNet_Interface)
#   - Das LED Programm heißt LEDs_AutoProg
# - Überprüfung ob alle InCh bedient werden.
#   - Spalte mit Anzahl der erwarteten InCh einbauen.
#   - Wie definiert man InCh von anderen Quellen?
#     - SI_1
#     - Schalter welcher per DigitalIn gelesen wird
#     - Ausgang einervanderen Funktion (z.B. Random)
#     - Andere DCC Zeile
# - Anzahl der ausgeblendeten Zeilen Anzeigen. Wenn man Draufklickt wird gefragt ob alle eingeblendet werden sollen
# - Hinzufügen zu einer bestehenden Configurationszeile ?
# - Überprüfungen
#   - Selbe Routinen bei den Speziellen Dialogen verwenden
# - Achtung: Die Anzahl der Spalten ist auf 16384 gesetzt => Es kann nicht mit einem Alten Excel benutzt werden
# Doku:
# ~~~~~
# - Anleitung Arduino Prozessor auswählen , ... in die Doku
# - Der SKIP_ROOM kann bei dem aktuellen Konzept nicht so einfach genutzt werden.
#   Man muss vor der entsprechenden House Zeile eine Funktion definieren bei der LEDs 0 ist.
#   Hier kann man dann z.B. mit Const(#LED+3, C_ALL, #InCh, 0, 255) auf die SKIP_ROOM LED zugreifen.
#   => Das ist nur was für Experten
# - Inbetriebname des DCC beschreiben
#   - Baudrate des Seriellen Monitors
# ToDo für nächste Version:
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# - Expert Mode
#   - Eigene Variablen
# - Tab in dem man eigene Macros eingeben kann.
# - Integration des Pattern Generators
#   Evtl. auch ein Live Test
# - Zusätzliche Bibliotheken automatisch installiern wenn sie nicht vorhanden sind
# - Hardware Eingänge unterstützen:
#   - Schalter an DIn
#   - Taste an AIn
#   - Mux Taster
#   - Helligkeitssteuerung
# - Ribbon interface?
#   + Verschiebt sich nicht wenn das Blatt nach rechts gescrollt wird
#   + Bessere Hilfe
#   + Schönere Icons möglich (PNG, viele Farben)
#   + Kein Problem mehr mit den Button Sizes: Correct_Buttonsizes() benötigt 600ms
#   - Zusätzlicher Aufwand
#   - Evtl. Probleme in Open Office
#   - Kann man die Ribbons auch mit Tasten steuern? In meinem Filter Addon habe ich CTRL+Shift+Taste verwendet
#     Evtl. kann an unsichtbare Buttons verwenden damit ALT+Taste geht. Das geht dann auch wenn das Ribbon unsichtbar ist
#   - ?
# - Warum dauert es so lange bis die Meldung kommt wenn man auf den "Optionen" Button klickt ?
#   => Correct_Buttonsizes() benötigt 600ms ;-(
# - Der letzte Zustand der InCh Variablen könnte periodisch im EEPROM gespeichert werden und beim neustart
#   wieder geladen werden. Dazu könnte man das gesammte EEPROM Nutzen. Ein neuer Wert wird an die nächste freie Stelle
#   im EEPROM Gespeichert. Wenn der Speicher voll ist wird wieder von vorne begonnen. Der EEPROM wird komplett
#   als frei markiert. Die Daten werden in einer Struck gespeichert welche eine CRC enthält welche
#   Gültige Daten kennzeichnet.
#
# Verworfene Ideen:
# ~~~~~~~~~~~~~~~~~
# - Servo Bestückung an Armin und in Bibliothek
# - Filter Spalte ganz ans Ende ? => Nein
# - Anstelle von einem Haken zum aktivieren einer Zeile könnte man auch ein Verbotsschild
#   zum deaktivieren verwenden: "Wingdings2" Zeichen X
# - Kommentare in der "Beleuchtung, Sound, oder andere Effekte" Spalte Farblich markieren
# - Simulation einer kleinen Configuration. Dazu werden die Daten in das EEPROM geschrieben
#   + Die Übertragung würde viel schneller gehen
#   - Dazu müsten aber die #defines ersetzt werden. Das betrifft auch die Makros
#     => Man müsste dem Präprozessor benutzen
#        ==> Das wird zu aufwändig, Dann wartet man halt 20 Sekunden bis der Kompiler fertig ist
# Mit Armin Festgestellt am 20.8.19 und behoben und wiele weitere Änderungen
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# - Überlappung in der Arduino Send Dialogbox                                               => Geändert: Bei Armin testen
# - Fehler beim Erzeugen Kompelieren wenn im Pfad Namen sonderzeichen vorkommen "Märklin"   => O.K.
# - Genereller Hilfe Text in Haus Dialog
#   - Room_Dark und einige andere haben kein Hint
# - Cursor wird nicht auf die nächste fehlende Typ Zeile gesetzt beim Arduino Button        => O.K.
#   Wenn mehrere Typ Zellen leer sind
# - Wenn kein Eintrag in "Beleuchtung, Sound, oder andere Effekte" ist, dann läßt sich      => O.K.
#   das Programm nicht compelieren weil das Config Array fehlt
# - Maximale Zeit bis zu nächsten Änderung im House Dialog bis 254
#   Hier ist auch kein Hint
# - Beschreibungen zu den Spaltenüberschriften
# - Dialog mit dem reservierte LEDs eingetragen werden können
# - Arduino Program Stürtzt ab, wenn die RGB_AmpelXFade als letzte Zeile verwendet wird
#   Wenn im Anschluss noch ein Blink3 kommt dann geht es
#   => Anzahl der LEDs in Letzter Zeile wurde nicht berücksichtigt
# - Mit Ctrl+Button den Arduino Dialog zeigen wenn dieser über das "Don't show again ausgeblendet wurde"
# - Zeilen zur Doku sollen möglich sein. Wenn InCnt = 0, dann kein Eintrag in Ext_Addr
# - Das Lösche Tabelle und Help Bild wird unschön beim Zeilen verschieben.
# - Beim Löschen der Seite
#   - sollte nach oben gescrollt werden
#   - sollten nur ein paar leere Zeilen bleiben. Wie viele ? Ein Bildschirm ?
# - Die Berechnung von "#define NUM_LEDS" geht nicht wenn nur C1, C2, C3 LEDs benutzt werden
# - Spalten welche nicht von Hand editiert werden sollen grau hinterlegen
# - Schriftart "Consolas" In Config Array Spalte
# - Autofilter muss sich auf alles beziehen auch wenn neue Zeilen angefügt werden
# - Bei Effekten wie dem Andreaskreuz machen nicht alle Cx Möglichkeiten Sinn.
#   Es Funktioniert nur C1, C2 und C3. => Es solte ien anderer Default Wert existieren
#   und die unsinnigen Optionen (C12, C23 und C_ALL) ausgegraut sein.
#   => So unsinnig sind die anderen Optionen nicht C12 und C23 macht genau das was man erwartet.
#      Nur C_ALL steuert nur die erste und zweite LED an
# - Start Seite
# - Doppelte Adressen sind möglich solange der gleich Typ benutzt wird. Sie werden über ein INCH_... Define adressiert.
# - Sollen mehrere Einträge in einer Zeile unterstützt werden?
#   - Wenn man eine Adresse mehrfach benutzen kann dann braucht man das nicht mehr
#   - Für Signale welche per DCC angesteuert werden wird ein Makro generiert welches
#     das InCh_to_TmpVar enthält. Das ist sowieso schwer verständlich
#   => Nein
# - Die InCh der DCC Eingänge werden als #define INCH_ADDR_123_RED generiert.
#   Dann kann man diese an anderer Stelle benutzen
# - Beim Verschieben in einen Bereich außerhalb der Tabelle
#   werden die Formatierungen nicht richtig aktualisiert
# - Beim Löschen von Zeilen muss dafür gesorgt werden, das wieder 3 Leerzeilen am Ende
#   vorhanden sind sonst funktioniert der Filter nicht mehr
# - Bei Signalen erste und letzte Adresse in Adress Spalte untereinader
#   Soll hier auch die Direction berücksichtigt werden (Rot/Grün) ? => Nein erstmal nicht
# - Die Fehlermeldung "Internal error: Unknown Page_ID: '" kommt manchmal wenn man
#   auf ein anderes Blatt schaltet während man eine Zelle editiert
# - Verschieben mit Maus:
#   - Umschalten auf anderes Sheet muss erkannt werden => Abbruch
# - Buttons Zucken beim verschieben bei Armin => liegt am TeamViewer
# - Keine Spaltenüberschriften auf Startseite
# - Startseite: Dialog Button zeigen
# - Beim Programmstart EnableDisableAllButtons True auf allen Seiten aufrufen falls die Buttons
#   durch einen Crash deaktiviert wurden
# - Das bewegen des Cursors ist sehr langsam => Auch wenn Global_Worksheet_SelectionChange deaktiviert ist ist es langsam
# - Schöneren Start Knopf auf Start Seite
# - Verwende immer den Arduino Nano beim Download
# - Eingabe des COM Ports
# - Zusätzlice Ausgaben in cmd File
# - Installation des DDC/Selectrix Arduinos
# - Die Konstanten COMPort_COL, ... sollten auch Dynamisch gefüllt werden
# - Defaultwert für die INCh Variablen. Das wird z.B. bei den Signalen gebraucht
# - CAN:
#   - Adresses from 0 - 0x7FF are possible (2048 adresses)
#   - Spalte "D" muss CAN Adresse heissen oder nur "Adresse"
# - Anpassungen an VBA7
# - Datum und Zeit (Pfad) in Arduino Prog schreiben und beim Booten anzeigen
# - Beim Programmstart sollen ActiveCell auf die erste Leere Zeile gesetzt werden
#   damit der Dummy Dialog richtig funktioniert
# - Anzeige meherere SX Kanäle mit "1 - 2" wie bei DCC. Hier muss eigentlich auch die Bitposition rein
# - Spalte von Adresse und SX Channel so formatieren, das eine Neue Zeile begonnen wird wenn es nicht passt
# - Beim kompilieren des DCC Programms kommt eine Warnung, dass der EEPROM nicht benutzt wird. Das ist unschön
# - Untersuchen warum das Arduino Prog. so viel Speicher braucht
#   => Die serielle Schnittstelle braucht 1078 Byte Flash (4%) und 201 Byte RAM (10%)
#   - HeartBeat:  Der Sketch verwendet 14130 Bytes (45%) des Programmspeicherplatzes. Das Maximum sind 30720 Bytes.
#                 Globale Variablen verwenden 366 Bytes (17%) des dynamischen Speichers, 1682 Bytes fÃ¼r lokale Variablen verbleiben. Das Maximum sind 2048 Bytes.
#   - Ohne Addr   Der Sketch verwendet 15176 Bytes (49%) des Programmspeicherplatzes. Das Maximum sind 30720 Bytes.
#                 Globale Variablen verwenden 457 Bytes (22%) des dynamischen Speichers, 1591 Bytes fÃ¼r lokale Variablen verbleiben. Das Maximum sind 2048 Bytes.
#   - Ohne Serial Der Sketch verwendet 14098 Bytes (45%) des Programmspeicherplatzes. Das Maximum sind 30720 Bytes.
#                 Globale Variablen verwenden 256 Bytes (12%) des dynamischen Speichers, 1792 Bytes fÃ¼r lokale Variablen verbleiben. Das Maximum sind 2048 Bytes.
# - Pattern_Configurator CR/LF Problem auf GitHub !!!
# - Wenn beim Hochladen zum Selextrix Arduino was schief geht dann muss
#   es solange wiederholt werden bis es geht
# - Corrected the House LED count
# - House:
#   - Besser Defaultwerte (1/2 und 2/3 oder so)
#   - Min Und Max LEDs nach den Rooms, und automatisch berechnen
# - Beim Programmstart und -ende ? "BuildDir" löschen. Evtl. auch eine Taste Einbauen.
#   => Ist nicht nötig. Änderungen im original LIB Verzeichniss werden erkannt
# - Eigenes Bild für CAN
# - DCC/Selectrix SW soll nur dann herunter geladen werden wenn Adressen benutzt werden
# - Im DCC Adresse Feld werden keine neuen Zeilen hinzugefügt wenn man am ende ist
# - UNO wird nicht bei der COM Port suche entdeckt obwohl der Mode Befehl einen Port 12 erkennt. => Jetzt geht es wieder
# - Wenn man beim Programmieren von Sound Modules die "Soll der Kanal Gleich Adressiert
#   werden Frage" mit bestätigt, dann kommt bei Geraden Nummern (Grün?)
#   gleich wieder der Auswahl Dialog ?
#   => Kann ich nicht mehr reproduzieren ;-(
# - Signale für Selectrix
# - Der Autofilter war gestern beim Release verschwunden welches ich Karl gegeben habe.
#   Wenn ich in die Datei auf meinem Rechner schaue ist er aber da ?!?
#   Machmal rutscht er auch in die Erste Zeile
# - Beim ändern des Filters müssen die LED Nummern neu berechnet werden !
# - Probleme mit dem Autofilter:
#   - Es ist recht aufwändig diesen über einen Bereich mit lücken zu erweitern
#   - Das Automatische erhöhen einer Zahl mit dem Kästchen Rechts unten geht nicht
#   - Es gibt Probleme beim Kopieren einer Zeile in verbindung mit versteckten Zeilen
#   - Die Autofilter sind nicht intuitiv. Die Leerzeilen werden gerne vergessen
#   => Darum verwende ich jetzt keine versteckten Spalten
# - Proc_Copy_Row spinnt wenn Spalten E und N, O Versteckt sind
# - Globale Zeiten der House() einstellbar machen
# - Bei der Z21 wird die Adresse 1 als -3 auf dem DCC Arduino erkannt
#   => Schalter einbauen ?


