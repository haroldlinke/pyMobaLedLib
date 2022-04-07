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
from vb2py.vbconstants import *


import proggen.Prog_Generator as PG

import ExcelAPI.P01_Workbook as P01

from ExcelAPI.X01_Excel_Consts import *


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" Concept for saving pictures:                                           12.07.20:
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Prior the pictures have been saved with "Save_Pic_from_clipboard()".
 This function doesn't support transparent colors ;-(
 Therefore the pictures are read in with a new button created by Misha.
 In the corrosponding function the picture is copied to the "MyPattern_Config_Examples"
 directory. => The transparent color of ".png" files is retained.
 Since the user may change the size of a picture after importing it the scale
 has to be stored in addition to the ".MLL_pcf" file. Croping is not supported.

 To integrate the LED into the picture there are two possibilities.
 The LEDs could be placed on top of the picture or under the picture. In the second
 case the picture must be transparent at the LED positions. The advantage of the
 second methode it the posibility to use any kind of LED shape by defining the
 transparent area in the picture.
--------------------------------------------------------------------------------------------------------------------------------------

"""

class LineDatT:
    def __init__(self):
        self.Visible = MsoTriState()
        self.ForeColor_RGB = MsoRGBType()
        self.Transparency = Single()
        self.Weight = Single()
        self.DashStyle = MsoLineDashStyle()


def __Print_TableRow(Sh, FileNr, r, FirstCol, LastCol, WithEmptyCells):
    #--------------------------------------------------------------------------------------------------------------------------------------
    with_0 = Sh
    #LastUsedCol = LastFilledColumn(.Range(.Cells(r, LED_Text_Col), .Cells(r, LastCol)), r)
    LastUsedCol = LastFilledColumn2(with_0.Range(with_0.Cells(r, LED_Text_Col), with_0.Cells(r, LastCol)), r)
    for c in vbForRange(FirstCol, LastUsedCol):
        if WithEmptyCells == False and Trim(with_0.Cells(r, c)) == '':
            break
        if c > FirstCol:
            VBFiles.writeText(FileNr, Chr(pcfSep))
        if with_0.Cells(r, c).HasFormula:
            VBFiles.writeText(FileNr, Replace(Trim(with_0.Cells(r, c).FormulaLocal), r, '~'))
        else:
            VBFiles.writeText(FileNr, Trim(with_0.Cells(r, c)))
    VBFiles.writeText(FileNr, '', '\n')

def __Get_Cell_Attrib(c):
    fn_return_value = None
    s = String()
    #-----------------------------------------------------
    with_1 = c
    if with_1.Font.Color != 0:
        s = 'c' + with_1.Font.Color + ','
    if with_1.Interior.Color != 16777215:
        s = s + 'i' + with_1.Interior.Color + ','
    if with_1.Font.Bold:
        s = s + 'B' + ','
    if with_1.Font.Italic:
        s = s + 'I' + ','
    if with_1.Font.Underline != - 4142:
        s = s + 'U' + with_1.Font.Underline + ','
    if with_1.WrapText:
        s = s + 'W' + ','
    if with_1.Orientation != xlHorizontal:
        s = s + 'O' + with_1.Orientation + ','
    if Len(s) > 0:
        fn_return_value = Left(s, Len(s) - 1)
    return fn_return_value

def __Print_Attrib_of_TableRow(Sh, FileNr, r, LastCol):
    #---------------------------------------------------------------------------------------------------
    with_2 = Sh
    for c in vbForRange(LED_Text_Col, LastCol):
        Line = Line + __Get_Cell_Attrib(with_2.Cells(r, c)) + Chr(pcfSep)
    while Right(Line, 1) == Chr(pcfSep):
        Line = Left(Line, Len(Line) - 1)
    VBFiles.writeText(FileNr, Line, '\n')

def __Find_Row_with_Txt_in_Col(Sh, Col, Txt):
    fn_return_value = None
    PosStr = String()
    #---------------------------------------------------------------------------------------------
    # New function which uses the Language sheet instead of searching in the sheet.
    # => The position must match with the position in the language sheet
    #    => It's not possible use this function with old sheets
    # The old function dosn't work if the language in the sheet is not german
    PosStr = Find_Cell_Pos_by_Name(Txt)
    if PosStr == '':
        MsgBox('Error: \'' + Txt + '\' not found in the laguage sheet', vbCritical, 'Error')
        return fn_return_value
    fn_return_value = Range(PosStr).Row
    return fn_return_value

def __Print_Typ_and_Pos(FileNr, TypeName, o, str=''):
    #--------------------------------------------------------------------------------------------------------------
    if o.Rotation == 0:
        VBFiles.writeText(FileNr, TypeName + Chr(pcfSep) + o.Left + ';' + o.Top + ';' + o.Width + ';' + o.Height)
    else:
        VBFiles.writeText(FileNr, TypeName + Chr(pcfSep) + o.Left + ';' + o.Top + ';' + o.Width + ';' + o.Height + ';' + o.Rotation)
    #The Print command always uses the decimal point undependent form the user options.
    if str != '':
        VBFiles.writeText(FileNr, Chr(pcfSep) + str)
    VBFiles.writeText(FileNr, '', '\n')

def __Print_RGB_LED_CheckBox(FileNr):
    CheckBoxStr = String()
    #----------------------------------------------------
    if ActiveSheet.RGB_LED_CheckBox.Value:
        CheckBoxStr = '1'
    else:
        CheckBoxStr = '0'
    VBFiles.writeText(FileNr, 'RGB_LED_CheckBox' + Chr(pcfSep), "\t", CheckBoxStr, '\n')

def __Debug_Print_Shape_Info(Name, o):
    #---------------------------------------------------------------
    Debug.Print('Unsupportet ' + Name + ' type:' + o.Type + ' \'' + o.Name + '\' Top:' + o.Top + ' Left:' + o.Left + ' Width:' + o.Width + ' Height:' + o.Height + ' TopLeftCell:' + o.TopLeftCell.Row + ',' + o.TopLeftCell.Column)
    # VB2PY (UntranslatedCode) On Error GoTo ErrorSelect
    #o.Select ' Debug
    return
    Debug.Print('Error Selecting shape')

def __Get_Points_Str(o):
    fn_return_value = None
    i = Long()

    p = Variant()

    s = String()
    #------------------------------------------------------
    for i in vbForRange(1, o.Nodes.Count):
        for p in o.Nodes.Item(i).Points:
            s = s + p + ';'
    fn_return_value = Left(s, Len(s) - 1)
    return fn_return_value

def __Save_Pic_from_clipboard(PicName):
    WasProtected = Boolean()

    xlsChtObj = Variant()

    dblW = Double()

    dblH = Double()

    ScaleSize = Double()
    #-----------------------------------------------------
    WasProtected = ActiveSheet.ProtectContents
    if WasProtected:
        ActiveSheet.Unprotect()
    xlsChtObj = ActiveSheet.ChartObjects.Add(10, 10, 2000, 1000)
    xlsChtObj.Activate()
    xlsChtObj.ShapeRange.Line.Visible = False
    Sleep(100)
    xlsChtObj.Chart.Paste()
    xlsChtObj.Chart.Shapes[1].Top = 0
    xlsChtObj.Chart.Shapes[1].Left = 0
    xlsChtObj.Chart.Shapes[1].LockAspectRatio = False
    ScaleSize = 1
    dblW = xlsChtObj.Chart.Shapes(1).Width
    dblH = xlsChtObj.Chart.Shapes(1).Height
    xlsChtObj.Chart.Shapes[1].Width = ( xlsChtObj.Chart.Shapes(1).Width * ScaleSize )
    xlsChtObj.Chart.Shapes[1].Height = ( xlsChtObj.Chart.Shapes(1).Height * ScaleSize )
    xlsChtObj.Width = ( dblW * ScaleSize )
    xlsChtObj.Height = ( dblH * ScaleSize )
    xlsChtObj.Chart.Shapes[1].Width = dblW * ScaleSize
    xlsChtObj.Chart.Shapes[1].Height = dblH * ScaleSize
    xlsChtObj.Chart.Export(FileName=PicName)
    xlsChtObj.Delete()
    if WasProtected:
        Protect_Active_Sheet()

def __Show_only_this_Picture_and_Enter_Name(ThisPic):
    fn_return_value = None
    o = Variant()

    IsHidden = vbObjectInitialize(objtype=Boolean)

    Cnt = Long()

    OldLine = LineDatT()

    NewName = String()

    OldUpd = Boolean()
    #-----------------------------------------------------------------------------------
    # Show only this pictore
    for o in ActiveSheet.Shapes:
        if (o.Type == msoPicture) or (o.Type == msoLinkedPicture):
            if o.Name != 'MainMenu':
                Cnt = Cnt + 1
                IsHidden = vbObjectInitialize((Cnt,), Variant, IsHidden)
                IsHidden[Cnt - 1] = o.Visible
                if o.Name != ThisPic.Name:
                    o.Visible = False
                else:
                    o.Visible = True
    # Mark the picture with a red dashed border and center it                  ' 12.07.20:
    CenterOnCell(Cells(ThisPic.TopLeftCell.Row, ThisPic.TopLeftCell.Column))
    MainMenu_Form.Hide()
    with_3 = ThisPic.Line
    OldLine.Visible = with_3.Visible
    with_3.Visible = msoTrue
    OldLine.ForeColor_RGB = with_3.ForeColor.rgb
    OldLine.Transparency = with_3.Transparency
    OldLine.Weight = with_3.Weight
    OldLine.DashStyle = with_3.DashStyle
    with_3.ForeColor.rgb = rgb(255, 0, 0)
    with_3.Transparency = 0
    with_3.Weight = 3.5
    with_3.DashStyle = msoLineDash
    # Enter the name for the picture
    OldUpd = Application.ScreenUpdating
    Application.ScreenUpdating = True
    Sleep(500)
    NewName = InputBox(Get_Language_Str('Name des Bildes Eingeben (Gleichen Namen verwenden bei identischen Bildern)'))
    if NewName != '':
        fn_return_value = NewName
    Application.ScreenUpdating = OldUpd
    # Restore the old line style of the picture                               ' 12.07.20:
    with_4 = ThisPic.Line
    with_4.Visible = OldLine.Visible
    with_4.ForeColor.rgb = OldLine.ForeColor_RGB
    with_4.Transparency = OldLine.Transparency
    with_4.Weight = OldLine.Weight
    with_4.DashStyle = OldLine.DashStyle
    MainMenu_Form.Show()
    # Restore the visibility of the pictures
    Cnt = 0
    for o in ActiveSheet.Shapes:
        if (o.Type == msoPicture) or (o.Type == msoLinkedPicture):
            if o.Name != 'MainMenu':
                Cnt = Cnt + 1
                o.Visible = IsHidden(Cnt - 1)
    return fn_return_value

def __Test_Show_only_this_Picture():
    o = Variant()
    #UT--------------------------------------
    for o in ActiveSheet.Shapes:
        if (o.Type == msoPicture) or (o.Type == msoLinkedPicture):
            if o.Name != 'MainMenu':
                __Show_only_this_Picture_and_Enter_Name()(o)

def __Save_Picture(o, DestPath):
    fn_return_value = None
    PicName = String()

    Ext = Variant()
    #------------------------------------------------------------------------
    # Check if the object has got a name which starts with "Picture". Which is the default
    # name for a new picture. If the name startes with "Picture" the user is requested to
    # enter a name.
    # The fucntion checks it a picture with this name already exist with the extention ".png" or ".jpg".
    # If not the file is generated as ".jpg".
    # Unfortunaltely I don't know how to save transparent color to the file. Therefore it's better
    # To copy the file to the destibation directory.
    if Left(o.Name, Len('Picture')) == 'Picture':
        NewName = __Show_only_this_Picture_and_Enter_Name(o)
        if NewName != '':
            o.Name = NewName
        else:
            EndProg()
    # Check if the picture exists as ".jpg" or ".png"
    for Ext in Split('.png|.jpg', '|'):
        PicName = DestPath + o.Name + Ext
        if Dir(PicName) != '':
            if OVERWRITE_EXISTING_PIC:
                Kill(PicName)
            break
    fn_return_value = FileNameExt(PicName)
    if Dir(PicName) == '':
        o.Copy()
        __Save_Pic_from_clipboard(PicName)
    return fn_return_value

def __Get_TextBoxAttrib(o):
    fn_return_value = None
    c = Variant()

    BoldStart = Long()

    IsBold = Boolean()

    i = Long()

    ForColor = Long()

    ColorStart = Long()
    #---------------------------------------------------------
    # Get the text attributes from a text box.
    # Currently only "Bold" and "ForColor" is supported
    #
    ForColor = rgb(0, 0, 0)
    for c in o.TextFrame2.TextRange.Characters:
        i = i + 1
        if c.Font.Fill.ForeColor.rgb != ForColor or i == Len(o.TextFrame.Characters.Text):
            if ColorStart > 0:
                fn_return_value = __Get_TextBoxAttrib() + 'F' + ColorStart + ',' + i - 1 + ',' + ForColor + ' '
            if c.Font.Fill.ForeColor.rgb != rgb(0, 0, 0):
                ColorStart = i
            else:
                ColorStart = 0
            ForColor = c.Font.Fill.ForeColor.rgb
        if c.Font.Bold:
            if IsBold == False:
                BoldStart = i
                IsBold = True
        else:
            if IsBold:
                fn_return_value = __Get_TextBoxAttrib() + 'B' + BoldStart + ',' + i - 1 + ' '
                IsBold = False
    if __Get_TextBoxAttrib() != '':
        fn_return_value = '{Attrib}' + Left(__Get_TextBoxAttrib(), Len(__Get_TextBoxAttrib()) - 1)
    return fn_return_value

def __Save_Objects(FileNr, DestPath):
    o = Variant()

    LanguageNrStr = String()
    #--------------------------------------------------------------
    # Problem:
    # Es gibt unendlich viele Objekte in Excel
    # => Ich werde mich zunächst auf die Textbox und die Bilder konzentrieren
    #
    # Die Objekte werden automatisch beim Speichern in aufsteigender "ZOrderPosition" Reihenfolge
    # gespeichert. Dadurch haben sie beim Laden wieder die gleiche Z-Position.
    for o in ActiveSheet.Shapes:
        #If o.Type <> msoComment Then o.Select ' Debug
        if (o.Type == msoAutoShape):
            if (o.AutoShapeType == msoShapeOval):
                __Print_Typ_and_Pos(FileNr, 'msoShapeOval', o, o.Name)
                #   Case msoShapeRightTriangle:             Print_Typ_and_Pos FileNr, "msoTriangle", o
                #   Case msoShapeRectangle:                 Print_Typ_and_Pos FileNr, "msoShapeRectangle", o
                #  'Case msoShapeRoundedRectangularCallout: Print_Typ_and_Pos FileNr, "msoShapeRoundedRectangularCallout", o ' Sprechblase
                #   Case Else: Debug_Print_Shape_Info "msoAutoShape", o
        elif (o.Type == msoComment):
            # ToDo: Print Comments in the LEDs range
            pass
        elif (o.Type == msoFreeform):
            #Print_Typ_and_Pos FileNr, "msoFreeform", o, Get_Points_Str(o)
            pass
        elif (o.Type == msoGroup):
        elif (o.Type == msoPicture) or (o.Type == msoLinkedPicture):
            if o.Name != 'MainMenu':
                #If o.Name = "KS_Signal_New1" Then Stop ' Debug
                __Print_Typ_and_Pos(FileNr, 'msoPicture', o, __Save_Picture(o, DestPath))
        elif (o.Type == msoTextBox):
            if Left(o.Name, Len('Goto_Graph')) != 'Goto_Graph' and o.Name != 'InternalTextBox':
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    LanguageNrStr = Mid(o.AlternativeText, Len('Language: ') + 1)
                __Print_Typ_and_Pos(FileNr, 'msoTextBox' + LanguageNrStr, o, o.TextFrame.Characters.Text + __Get_TextBoxAttrib(o))
        elif (o.Type == msoFormControl):
            if o.AlternativeText != '_Internal_Button_' and o.AlternativeText != 'Add_Del_Button':
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    LanguageNrStr = Mid(o.AlternativeText, Len('Language: ') + 1)
                __Print_Typ_and_Pos(FileNr, 'msoFormControl' + LanguageNrStr, o, o.DrawingObject.Caption + Chr(pcfSep) + Replace(o.OnAction, ThisWorkbook.Name + '!', ''))
        elif (o.Type == msoOLEControlObject):
            if o.Name == 'RGB_LED_CheckBox':
                __Print_RGB_LED_CheckBox(FileNr)
            else:
                if o.Name != 'Prog_Generator_Button' and o.Name != 'Send2Module_Button' and o.Name != 'Import_from_ProgGen_Button':
                    __Debug_Print_Shape_Info('shape', o)
        else:
            __Debug_Print_Shape_Info('shape', o)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DestName - ByVal 
def Save_One_Sheet(Sh, DestName, AppendFile=True, SheetName=VBMissingArgument):
    FileNr = Integer()

    LastFillRow = Long()

    LEDTabRow = Long()
    #----------------------------------------------------------------------------------------------------------------------------------------
    # The names in the created sheet are german independant from the
    # active language in the sheet to simplify the file loading.
    CreateFolder(DestName)
    FileNr = FreeFile()
    if AppendFile:
        VBFiles.openFile(FileNr, DestName, 'a') 
    else:
        VBFiles.openFile(FileNr, DestName, 'w') 
    if AppendFile:
        VBFiles.writeText(FileNr, '', '\n')
    VBFiles.writeText(FileNr, 'SheetName' + Chr(pcfSep))
    if SheetName == '':
        VBFiles.writeText(FileNr, Sh.Name, '\n')
    else:
        VBFiles.writeText(FileNr, SheetName, '\n')
    VBFiles.writeText(FileNr, 'Version' + Chr(pcfSep) + ACT_MLL_pcf_Version, '\n')
    with_5 = Sh
    with_5.Cells(1, 1).Select()
    for r in vbForRange(PARAMETER_Ro11, PARAMETER_Ro1N):
        if with_5.Cells(r, PARAMETER_Col + 1).Interior.Color == 65535:
            GermanName = Get_German_Name(with_5.Cells(r, PARAMETER_Col))
            if GermanName != '':
                VBFiles.writeText(FileNr, GermanName + Chr(pcfSep) + with_5.Cells(r, PARAMETER_Col + 1), '\n')
    r = __Find_Row_with_Txt_in_Col(Sh, LED_Text_Col, 'Dauer')
    if r > 0:
        VBFiles.writeText(FileNr, 'Dauer' + Chr(pcfSep))
        __Print_TableRow(Sh, FileNr, r, Dauer_Col1, Last_LEDsCol, False)
    r = __Find_Row_with_Txt_in_Col(Sh, Goto_Txt_col, 'Goto Tabelle')
    if r > 0:
        VBFiles.writeText(FileNr, 'Goto Tabelle' + Chr(pcfSep))
        __Print_TableRow(Sh, FileNr, r, GoTo_Col1, Last_LEDsCol, True)
    # LED Tab
    LastFillRow = LastFilledRowIn_w_Attrib(Sh, LED_Text_Col, Last_LEDsCol, Last_LEDs_ChkAttrCol)
    LEDTabRow = __Find_Row_with_Txt_in_Col(Sh, LED_Text_Col, 'Spalte Nr  ->')
    if LEDTabRow == 0:
        LEDTabRow = __Find_Row_with_Txt_in_Col(Sh, LED_Text_Col, 'Status Nr  ->')
    if LEDTabRow == 0:
        MsgBox(Get_Language_Str('Error: LED table not found'), vbCritical)
    else:
        for r in vbForRange(LEDTabRow + 1, LastFillRow):
            VBFiles.writeText(FileNr, 'LED_Tab' + Chr(pcfSep))
            __Print_TableRow(Sh, FileNr, r, LED_Text_Col, Last_LEDsCol, True)
        for r in vbForRange(LEDTabRow + 1, LastFillRow):
            VBFiles.writeText(FileNr, 'LED_Attr' + Chr(pcfSep), ActiveSheet.Rows(r).RowHeight + Chr(pcfSep))
            __Print_Attrib_of_TableRow(Sh, FileNr, r, Last_LEDsCol)
    __Save_Objects(FileNr, FilePath(DestName))
    VBFiles.closeFile(FileNr)

def Save_All_Sheets_to(FileName):
    Sh = Variant()

    AppendSheet = Boolean()

    Oldupdating = Boolean()
    #------------------------------------------------
    Del_All_Sheets_which_contain_Copy_in_their_Name()
    Oldupdating = Application.ScreenUpdating
    Application.ScreenUpdating = False
    for Sh in ThisWorkbook.Sheets:
        if Is_Normal_Data_Sheet(Sh.Name, Get_Language_Str('gespeichert')):
            StatusMsg_UserForm.Set_ActSheet_Label(Get_Language_Str('Schreibe ') + Sh.Name)
            Sh.Activate()
            Sh.Select()
            Save_One_Sheet(ActiveSheet, FileName, AppendSheet)
            AppendSheet = True
    Application.ScreenUpdating = Oldupdating

def Get_MyExampleDir():
    fn_return_value = None
    Dir = String()
    #-------------------------------------------
    Dir() = Environ('USERPROFILE') + '/Documents/' + MyExampleDir
    CreateFolder(Dir() + '/')
    fn_return_value = Dir()
    return fn_return_value

def __Save_All_Sheets():
    #----------------------------
    Save_All_Sheets_to(Get_MyExampleDir() + '\\AllExamples.MLL_pcf')
    #Save_All_Sheets_to ThisWorkbook.Path & "\" & ExampleDir & "\AllExamples.MLL_pcf"

def __Test_Save_One_Sheet():
    #UT------------------------------
    Save_One_Sheet(ActiveSheet, ThisWorkbook.Path + '\\' + ExampleDir + '\\TestExample.MLL_pcf', False)

# VB2PY (UntranslatedCode) Option Explicit
