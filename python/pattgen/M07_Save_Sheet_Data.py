from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M30_Tools as M30
import pattgen.M01_Public_Constants_a_Var as M01
import proggen.M02_Public as M02
import ExcelAPI.XLC_Excel_Consts as X01
import ExcelAPI.XLA_Application as X02
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M09_Language as M09
import pattgen.M08_Load_Sheet_Data
import mlpyproggen.Pattern_Generator as PG
import pattgen.D00_Forms as D00

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
-----------------------------------------------------
---------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on True
 24.06.19:
---------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
----------------------------------------------------
---------------------------------------------------------------
------------------------------------------------------
-----------------------------------------------------
-----------------------------------------------------------------------------------
UT--------------------------------------
------------------------------------------------------------------------
---------------------------------------------------------
--------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------
-------------------------------------------
----------------------------
UT------------------------------
"""

class LineDatT:
    def __init__(self):
        self.Visible = MsoTriState()
        self.ForeColor_RGB = MsoRGBType()
        self.Transparency = Single()
        self.Weight = Single()
        self.DashStyle = MsoLineDashStyle()


def Print_TableRow(Sh, FileNr, r, FirstCol, LastCol, WithEmptyCells):
    #--------------------------------------------------------------------------------------------------------------------------------------
    _with26 = Sh
    #LastUsedCol = LastFilledColumn(.Range(.Cells(r, LED_Text_Col), .Cells(r, LastCol)), r)
    LastUsedCol = M30.LastFilledColumn2(_with26.Range(_with26.Cells(r, M01.LED_Text_Col), _with26.Cells(r, LastCol)), r)
    # 20.11.19: Faster function
    for c in vbForRange(FirstCol, LastUsedCol):
        if WithEmptyCells == False and Trim(_with26.Cells(r, c)) == '':
            break
        if c > FirstCol:
            VBFiles.writeText(FileNr, Chr(M01.pcfSep))
        if _with26.Cells(r, c).HasFormula:
            VBFiles.writeText(FileNr, Replace(Trim(_with26.Cells(r, c).FormulaLocal), r, '~'))
        else:
            VBFiles.writeText(FileNr, Trim(_with26.Cells(r, c)))
    VBFiles.writeText(FileNr, '', '\n')

def Get_Cell_Attrib(c):
    _fn_return_value = ""
    s = String()
    #-----------------------------------------------------
    _with27 = c
    if _with27.Font.Color != "#000000": # 0:
        s = 'c' + _with27.Font.Color + ','
    if _with27.Interior.Color != 16777215: # #FFFFFF
        s = s + 'i' + str(_with27.Interior.Color) + ','
    if _with27.Font.Bold:
        s = s + 'B' + ','
    if _with27.Font.Italic:
        s = s + 'I' + ','
    if _with27.Font.Underline != - 4142:
        s = s + 'U' + _with27.Font.Underline + ','
    if _with27.WrapText:
        s = s + 'W' + ','
    if _with27.Orientation != X01.xlHorizontal:
        s = s + 'O' + _with27.Orientation + ','
    if Len(s) > 0:
        _fn_return_value = Left(s, Len(s) - 1)
    return _fn_return_value

def Print_Attrib_of_TableRow(Sh, FileNr, r, LastCol):
    #---------------------------------------------------------------------------------------------------
    _with28 = Sh
    Line=""
    for c in vbForRange(M01.LED_Text_Col, LastCol):
        Line = Line + Get_Cell_Attrib(_with28.Cells(r, c)) + Chr(M01.pcfSep)
    while Right(Line, 1) == Chr(M01.pcfSep):
        Line = Left(Line, Len(Line) - 1)
    VBFiles.writeText(FileNr, Line, '\n')

def Find_Row_with_Txt_in_Col(Sh, Col, Txt):
    _fn_return_value = 0
    PosStr = String()
    #---------------------------------------------------------------------------------------------
    # New function which uses the Language sheet instead of searching in the sheet.
    # => The position must match with the position in the language sheet
    #    => It's not possible use this function with old sheets
    # The old function dosn't work if the language in the sheet is not german
    PosStr = M09.Find_Cell_Pos_by_Name(Txt)
    # Find the position in the language sheet
    if PosStr == '':
        X02.MsgBox('Error: \'' + Txt + '\' not found in the laguage sheet', vbCritical, 'Error')
        return _fn_return_value
    _fn_return_value = X02.Range(PosStr).Row
    return _fn_return_value

def Print_Typ_and_Pos(FileNr, TypeName, o, pstr=''):
    #--------------------------------------------------------------------------------------------------------------
    if o.Rotation == 0:
        VBFiles.writeText(FileNr, TypeName + Chr(M01.pcfSep) + str(o.Left/X02.guifactor) + ';' + str(o.Top/X02.guifactor) + ';' + str(o.Width/X02.guifactor) + ';' + str(o.Height/X02.guifactor))
    else:
        VBFiles.writeText(FileNr, TypeName + Chr(M01.pcfSep) + str(o.Left/X02.guifactor) + ';' + str(o.Top/X02.guifactor) + ';' + str(o.Width/X02.guifactor) + ';' + str(o.Height/X02.guifactor) + ';' + str(o.Rotation))
        # Added .Rotation by Misha 30-6-2020.
    #The Print command always uses the decimal point undependent form the user options.
    if pstr != '':
        VBFiles.writeText(FileNr, Chr(M01.pcfSep) + pstr)
    VBFiles.writeText(FileNr, '', '\n')

def Print_RGB_LED_CheckBox(FileNr):
    CheckBoxStr = String()
    # 13.06.20:
    #----------------------------------------------------
    if X02.ActiveSheet.RGB_LED_CheckBox.Value:
        CheckBoxStr = '1'
    else:
        CheckBoxStr = '0'
    VBFiles.writeText(FileNr, 'RGB_LED_CheckBox' + Chr(M01.pcfSep), "\t", CheckBoxStr, '\n')

def Debug_Print_Shape_Info(Name, o):
    #---------------------------------------------------------------
    Debug.Print('Unsupportet ' + Name + ' type:' + str(o.Type) + ' \'' + str(o.Name) + '\' Top:' + str(o.Top) + ' Left:' + str(o.Left) + ' Width:' + str(o.Width) + ' Height:' + str(o.Height) + ' TopLeftCell:' + str(o.TopLeftCell.Row) + ',' + str(o.TopLeftCell.Column))
    # VB2PY (UntranslatedCode) On Error GoTo ErrorSelect
    #o.Select
    # Debug
    return
    Debug.Print('Error Selecting shape')

def Get_Points_Str(o):
    _fn_return_value = None
    i = Long()

    p = Variant()

    s = String()
    #------------------------------------------------------
    for i in vbForRange(1, o.Nodes.Count):
        for p in o.Nodes.Item(i).Points:
            s = s + p + ';'
    _fn_return_value = Left(s, Len(s) - 1)
    return _fn_return_value

def Save_Pic_from_clipboard(PicName):
    WasProtected = Boolean()

    xlsChtObj = Variant()

    dblW = Double()

    dblH = Double()

    ScaleSize = Double()
    #-----------------------------------------------------
    WasProtected = X02.ActiveSheet.ProtectContents
    if WasProtected:
        X02.ActiveSheet.Unprotect()
    xlsChtObj = X02.ActiveSheet.ChartObjects.Add(10, 10, 2000, 1000)
    xlsChtObj.Activate()
    xlsChtObj.ShapeRange.Line.Visible = False
    # Otherwise the border is contained in the picture
    X03.Sleep(100)
    # Wait a little until the picture is copied to the clipboard
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
        M30.Protect_Active_Sheet()

def Show_only_this_Picture_and_Enter_Name(ThisPic):
    _fn_return_value = None
    o = Variant()

    IsHidden = vbObjectInitialize(objtype=Boolean)

    Cnt = Long()

    OldLine = LineDatT()

    NewName = String()

    OldUpd = Boolean()
    #-----------------------------------------------------------------------------------
    # Show only this pictore
    for o in X02.ActiveSheet.Shapes:
        _select16 = o.Type
        if (_select16 == msoPicture) or (_select16 == msoLinkedPicture):
            # 11, 13: Picture
            if o.Name != 'MainMenu':
                Cnt = Cnt + 1
                IsHidden = vbObjectInitialize((Cnt,), Variant, IsHidden)
                IsHidden[Cnt - 1] = o.Visible
                if o.Name != ThisPic.Name:
                    o.Visible = False
                else:
                    o.Visible = True
    # Mark the picture with a red dashed border and center it
    # 12.07.20:
    M30.CenterOnCell(X02.Cells(ThisPic.TopLeftCell.Row, ThisPic.TopLeftCell.Column))
    MainMenu_Form.Hide()
    _with29 = ThisPic.Line
    OldLine.Visible = _with29.Visible
    _with29.Visible = msoTrue
    OldLine.ForeColor_RGB = _with29.ForeColor.rgb
    OldLine.Transparency = _with29.Transparency
    OldLine.Weight = _with29.Weight
    OldLine.DashStyle = _with29.DashStyle
    _with29.ForeColor.rgb = rgb(255, 0, 0)
    _with29.Transparency = 0
    _with29.Weight = 3.5
    _with29.DashStyle = msoLineDash
    # Enter the name for the picture
    OldUpd = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = True
    X03.Sleep(500)
    NewName = X02.InputBox(pattgen.M09_Language.Get_Language_Str('Name des Bildes Eingeben (Gleichen Namen verwenden bei identischen Bildern)'))
    if NewName != '':
        _fn_return_value = NewName
    X02.Application.ScreenUpdating = OldUpd
    # Restore the old line style of the picture
    # 12.07.20:
    _with30 = ThisPic.Line
    _with30.Visible = OldLine.Visible
    _with30.ForeColor.rgb = OldLine.ForeColor_RGB
    _with30.Transparency = OldLine.Transparency
    _with30.Weight = OldLine.Weight
    _with30.DashStyle = OldLine.DashStyle
    MainMenu_Form.Show()
    # Restore the visibility of the pictures
    Cnt = 0
    for o in X02.ActiveSheet.Shapes:
        _select17 = o.Type
        if (_select17 == msoPicture) or (_select17 == msoLinkedPicture):
            # 11, 13: Picture
            if o.Name != 'MainMenu':
                Cnt = Cnt + 1
                o.Visible = IsHidden(Cnt - 1)
    return _fn_return_value

def Test_Show_only_this_Picture():
    o = Variant()
    #UT--------------------------------------
    for o in X02.ActiveSheet.Shapes:
        _select18 = o.Type
        if (_select18 == msoPicture) or (_select18 == msoLinkedPicture):
            # 11, 13: Picture
            if o.Name != 'MainMenu':
                Show_only_this_Picture_and_Enter_Name(o)

def Save_Picture(o, DestPath):
    _fn_return_value = None
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
        # Check if the name is already entered
        NewName = Show_only_this_Picture_and_Enter_Name(o)
        if NewName != '':
            o.Name = NewName
        else:
            M30.EndProg()
    # Check if the picture exists as ".jpg" or ".png"
    #for Ext in Split('.png|.jpg', '|'):
    PicName = DestPath + M30.FileNameExt(o.Name) # + Ext
    #    # 09.07.20: Using "Ext"
    #    if Dir(PicName) != '':
    #        if M01.OVERWRITE_EXISTING_PIC:
    #            Kill(PicName)
    #        break
    if PicName != o.Name:
        shutil.copy2(o.Name,DestPath)
    _fn_return_value = M30.FileNameExt(PicName)
    #if Dir(PicName) == '':
    #    o.Copy()
    #    # copy to clipboard
    #    Save_Pic_from_clipboard(PicName)
    return _fn_return_value

def Get_TextBoxAttrib(o):
    _fn_return_value = None
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
    # 19.10.19:
    ForColor = rgb(0, 0, 0)
    for c in o.TextFrame2.TextRange.Characters:
        i = i + 1
        if c.Font.Fill.ForeColor.rgb != ForColor or i == Len(o.TextFrame.Characters.Text):
            # 19.10.19:
            if ColorStart > 0:
                _fn_return_value = _fn_return_value + 'F' + ColorStart + ',' + i - 1 + ',' + ForColor + ' '
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
                _fn_return_value = _fn_return_value + 'B' + BoldStart + ',' + i - 1 + ' '
                IsBold = False
    if _fn_return_value != '':
        _fn_return_value = '{Attrib}' + Left(_fn_return_value, Len(_fn_return_value) - 1)
    return _fn_return_value

def Save_Objects(FileNr, DestPath):
    o = Variant()

    LanguageNrStr = String()
    #--------------------------------------------------------------
    # Problem:
    # Es gibt unendlich viele Objekte in Excel
    # => Ich werde mich zunächst auf die Textbox und die Bilder konzentrieren
    #
    # Die Objekte werden automatisch beim Speichern in aufsteigender "ZOrderPosition" Reihenfolge
    # gespeichert. Dadurch haben sie beim Laden wieder die gleiche Z-Position.
    # 11.02.20:
    for o in X02.ActiveSheet.Shapes:
        #If o.Type <> msoComment Then o.Select
        # Debug
        _select19 = o.Type
        if (_select19 == X01.msoAutoShape):
            # 1: Rectangle, Triangle, Sprechblase
            _select20 = o.AutoShapeType
            if (_select20 == X01.msoShapeOval):
                Print_Typ_and_Pos(FileNr, 'msoShapeOval', o, o.Name)
                # Added by Misha 26-6-2020
                #   Case msoShapeRightTriangle:             Print_Typ_and_Pos FileNr, "msoTriangle", o
                #   Case msoShapeRectangle:                 Print_Typ_and_Pos FileNr, "msoShapeRectangle", o
                #  'Case msoShapeRoundedRectangularCallout: Print_Typ_and_Pos FileNr, "msoShapeRoundedRectangularCallout", o
                # Sprechblase
                #   Case Else
                Debug_Print_Shape_Info('msoAutoShape', o)
        elif (_select19 == X01.msoComment):
            # 4: Comment
            # ToDo: Print Comments in the LEDs range
            pass
        elif (_select19 == X01.msoFreeform):
            # 5: Freeform (Nicht rechtwinkliges Dreieck z.B.)
            #Print_Typ_and_Pos FileNr, "msoFreeform", o, Get_Points_Str(o)
            pass
        elif (_select19 == X01.msoGroup):
            # 6: Group
            pass
        elif (_select19 == X01.msoPicture) or (_select19 == X01.msoLinkedPicture):
            # 11, 13: Picture
            if o.Name != 'MainMenu':
                #If o.Name = "KS_Signal_New1" Then Stop
                # Debug
                Print_Typ_and_Pos(FileNr, 'msoPicture', o, Save_Picture(o, DestPath))
        elif (_select19 == X01.msoTextBox):
            # 17: TextBox
            if Left(o.Name, Len('Goto_Graph')) != 'Goto_Graph' and o.Name != 'InternalTextBox':
                # "InternalTextBox" = "by Hardi"
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    # 11.02.20:
                    LanguageNrStr = Mid(o.AlternativeText, Len('Language: ') + 1)
                Print_Typ_and_Pos(FileNr, 'msoTextBox' + LanguageNrStr, o, o.TextFrame2.Characters.Text + Get_TextBoxAttrib(o))
        elif (_select19 == X01.msoFormControl):
            # 8: Button
            # 19.10.19:
            if o.AlternativeText != '_Internal_Button_' and o.AlternativeText != 'Add_Del_Button':
                if Left(o.AlternativeText, Len('Language: ')) == 'Language: ':
                    # 11.02.20:
                    LanguageNrStr = Mid(o.AlternativeText, Len('Language: ') + 1)
                Print_Typ_and_Pos(FileNr, 'msoFormControl' + LanguageNrStr, o, o.DrawingObject.Caption + Chr(M01.pcfSep) + Replace(o.OnAction, PG.ThisWorkbook.Name + '!', ''))
        elif (_select19 == X01.msoOLEControlObject):
            # 12: Button with picture
            if o.Name == 'RGB_LED_CheckBox':
                Print_RGB_LED_CheckBox(FileNr)
                # Save the state of the RGB Checkbox
            else:
                if o.Name != 'Prog_Generator_Button' and o.Name != 'Send2Module_Button' and o.Name != 'Import_from_ProgGen_Button':
                    Debug_Print_Shape_Info('shape', o)
        else:
            Debug_Print_Shape_Info('shape', o)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DestName - ByVal 
def Save_One_Sheet(Sh, DestName, AppendFile=True, SheetName=""):
    FileNr = Integer()

    LastFillRow = Long()

    LEDTabRow = Long()
    #----------------------------------------------------------------------------------------------------------------------------------------
    # The names in the created sheet are german independant from the
    # active language in the sheet to simplify the file loading.
    M30.CreateFolder(DestName)
    FileNr = FreeFile()
    if AppendFile:
        VBFiles.openFile(FileNr, DestName, 'a') 
    else:
        VBFiles.openFile(FileNr, DestName, 'w') 
    if AppendFile:
        VBFiles.writeText(FileNr, '', '\n')
    VBFiles.writeText(FileNr, 'SheetName' + Chr(M01.pcfSep))
    if SheetName == '':
        VBFiles.writeText(FileNr, Sh.Name, '\n')
    else:
        VBFiles.writeText(FileNr, SheetName, '\n')
    VBFiles.writeText(FileNr, 'Version' + Chr(M01.pcfSep) + str(M01.ACT_MLL_pcf_Version), '\n')
    # 17.11.19:
    _with31 = Sh
    _with31.Cells(1, 1).Select()
    # for better comparison of the copied sheet
    for r in vbForRange(M01.PARAMETER_Ro11, M01.PARAMETER_Ro1N):
        if _with31.Cells(r, M01.PARAMETER_Col + 1).Interior.Color == 65535:
            GermanName = M09.Get_German_Name(_with31.Cells(r, M01.PARAMETER_Col))
            if GermanName != '':
                VBFiles.writeText(FileNr, GermanName + Chr(M01.pcfSep) + _with31.Cells(r, M01.PARAMETER_Col + 1), '\n')
    r = Find_Row_with_Txt_in_Col(Sh, M01.LED_Text_Col, 'Dauer')
    # 24.06.19: Adapted this and the following lines to multiple languages
    if r > 0:
        VBFiles.writeText(FileNr, 'Dauer' + Chr(M01.pcfSep))
        Print_TableRow(Sh, FileNr, r, M01.Dauer_Col1, M01.Last_LEDsCol, False)
        # Duration Row
        # 21.05.19: Replaced 24 by Last_LEDsCol
    r = Find_Row_with_Txt_in_Col(Sh, M01.Goto_Txt_col, 'Goto Tabelle')
    if r > 0:
        VBFiles.writeText(FileNr, 'Goto Tabelle' + Chr(M01.pcfSep))
        Print_TableRow(Sh, FileNr, r, M01.GoTo_Col1, M01.Last_LEDsCol, True)
        # Goto Table
    # LED Tab
    LastFillRow = M30.LastFilledRowIn_w_Attrib(Sh, M01.LED_Text_Col, M01.Last_LEDsCol, M01.Last_LEDs_ChkAttrCol)
    LEDTabRow = Find_Row_with_Txt_in_Col(Sh, M01.LED_Text_Col, 'Spalte Nr  ->')
    if LEDTabRow == 0:
        LEDTabRow = Find_Row_with_Txt_in_Col(Sh, M01.LED_Text_Col, 'Status Nr  ->')
    if LEDTabRow == 0:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Error: LED table not found'), vbCritical)
    else:
        for r in vbForRange(LEDTabRow + 1, LastFillRow):
            VBFiles.writeText(FileNr, 'LED_Tab' + Chr(M01.pcfSep))
            Print_TableRow(Sh, FileNr, r, M01.LED_Text_Col, M01.Last_LEDsCol, True)
        for r in vbForRange(LEDTabRow + 1, LastFillRow):
            VBFiles.writeText(FileNr, 'LED_Attr' + Chr(M01.pcfSep), str(X02.ActiveSheet.Rows(r).RowHeight) + Chr(M01.pcfSep))
            Print_Attrib_of_TableRow(Sh, FileNr, r, M01.Last_LEDsCol)
    Save_Objects(FileNr, M30.FilePath(DestName))
    VBFiles.closeFile(FileNr)

def Save_All_Sheets_to(FileName):
    Sh = Variant()

    AppendSheet = Boolean()

    Oldupdating = Boolean()
    #------------------------------------------------
    pattgen.M08_Load_Sheet_Data.Del_All_Sheets_which_contain_Copy_in_their_Name()
    Oldupdating = X02.Application.ScreenUpdating
    X02.Application.ScreenUpdating = False
    for Sh in PG.ThisWorkbook.sheets:
        if pattgen.M08_Load_Sheet_Data.Is_Normal_Data_Sheet(Sh.Name, pattgen.M09_Language.Get_Language_Str('gespeichert')):
            D00.StatusMsg_UserForm.Set_ActSheet_Label(pattgen.M09_Language.Get_Language_Str('Schreibe ') + Sh.Name)
            Sh.Activate()
            Sh.Select()
            Save_One_Sheet(X02.ActiveSheet, FileName, AppendSheet)
            AppendSheet = True
    X02.Application.ScreenUpdating = Oldupdating

def Get_MyExampleDir():
    _fn_return_value = None
    EDir = String()
    #-------------------------------------------
    EDir = Environ(M02.Env_USERPROFILE) + '\\Documents\\' + M01.MyExampleDir
    M30.CreateFolder(EDir + '\\')
    _fn_return_value = EDir
    return _fn_return_value

def Save_All_Sheets():
    #----------------------------
    Save_All_Sheets_to(Get_MyExampleDir() + '\\AllExamples.MLL_pcf')
    #Save_All_Sheets_to ThisWorkbook.Path & "\" & ExampleDir & "\AllExamples.MLL_pcf"

def Test_Save_One_Sheet():
    #UT------------------------------
    Save_One_Sheet(X02.ActiveSheet, PG.ThisWorkbook.Path + '\\' + M01.ExampleDir + '\\TestExample.MLL_pcf', False)

# VB2PY (UntranslatedCode) Option Explicit
