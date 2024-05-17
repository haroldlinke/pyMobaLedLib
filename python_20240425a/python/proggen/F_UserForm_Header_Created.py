# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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

from vb2py.vbfunctions import *
from vb2py.vbdebug import *


class UserForm_Header_Created:
    def __init__(self):
        self.DontShowAgain = False
        self.FileName = "Name"
    
    def Show():
        pass


def __Abort_Button_Click():
    #-------------------------------
    Me.Hide()

def __EditFile_Click():
    #---------------------------
    Me.Hide()
    ShellExecute(0, 'open', 'Notepad', '"' + FileName + '"', '', SW_NORMAL)

def __Image1_Click():
    #-------------------------
    __OK_Click()

def __OK_Click():
    #---------------------
    Me.Hide()
    Compile_and_Upload_LED_Prog_to_Arduino()

def __OpenPath_Click():
    Name = String()
    #---------------------------
    Me.Hide()
    #Call ShellExecute(0, "open", "Explorer", "/e,""" & ThisWorkbook.Path & """", "", SW_NORMAL)
    Name = ThisWorkbook.Path + '/' + Ino_Dir_LED + Include_FileName
    if Dir(Name) != FileNameExt(Name):
        Shell('Explorer /root,"' + FilePath(Name) + '"', vbNormalFocus)
        Shell('Explorer /Select,"' + Name + '"', vbNormalFocus)

def __Right_Arduino_Button_Click():
    #---------------------------------------
    Ask_to_Upload_and_Compile_and_Upload_Prog_to_Right_Arduino()

def __USB_Button_Click():
    #-----------------------------
    USB_Port_Dialog(COMPort_COL)

def __UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    Center_Form(Me)

