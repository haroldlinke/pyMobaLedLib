from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import pattgen.M03_Analog_Trend
import pattgen.M09_Language
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.M30_Tools as M30
import ExcelAPI.XLC_Excel_Consts as X01

"""--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
---------------------------
--------------------------------------------------------------
--------------------------------------------------------------
---------------------------------------------------
---------------------------------------------------
---------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
"""


def List_Buttons():
    Button = Object()
    #--------------------------------------------------------------------------------------------
    Debug.Print(vbCrLf + 'Button names : ')
    for Button in X02.ActiveSheet.OLEObjects:
        Debug.Print(Button.Name)

def List_Shapes():
    Shape = Shape()
    #--------------------------------------------------------------------------------------------
    Debug.Print(vbCrLf + 'Shape names : ')
    for Shape in X02.ActiveSheet.Shapes:
        Debug.Print(Shape.Name)

def Shape_Exists(ButtonName):
    _fn_return_value = None
    Shape = Object()
    #--------------------------------------------------------------------------------------------
    _fn_return_value = False
    for Shape in X02.ActiveSheet.Shapes:
        if Shape.Name == ButtonName:
            _fn_return_value = True
            return _fn_return_value
    return _fn_return_value

def IS_RGB_Group(ChNr):
    _fn_return_value = None
    #--------------------------------------------------------------------------------------------
    # If next Three Channels have the same name then Channel is first Channel in RGB Group!
    # LED_Type =>  0 (False) = Single LED, 1 (True) = RGB LED
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    _fn_return_value = pattgen.M03_Analog_Trend.IsLEDGroup()
    return _fn_return_value

def Get_Pattern(MacroCodeNr):
    _fn_return_value = None
    MacroRow = Variant()

    OptionNr = Integer()
    #--------------------------------------------------------------------------------------------
    for MacroRow in vbForRange(4, 340, 28): #*HL
        if Left(X02.Cells(MacroRow, 4).Value, 3) == Left(MacroCodeNr, 3):
            OptionNr = Val(Right(MacroCodeNr, 2))
            _fn_return_value = X02.Cells(MacroRow + OptionNr * 3, 3).Value
            if Get_Pattern() == 'To be filled!' or InStr(Get_Pattern(), 'Pattern') == 0:
                _fn_return_value = ''
            return _fn_return_value
    _fn_return_value = ''
    return _fn_return_value

def Get_MacroRow(MacroCodeNr):
    _fn_return_value = None
    MacroRow = Variant()

    OptionNr = Integer()
    #--------------------------------------------------------------------------------------------
    for MacroRow in vbForRange(4, 340, 28):
        if X02.Cells(MacroRow, 4).Value == MacroCodeNr:
            _fn_return_value = MacroRow
            return _fn_return_value
    _fn_return_value = 0
    return _fn_return_value

def iColor(Rng, formatType=VBMissingArgument):
    _fn_return_value = None
    colorVal = Variant()
    #--------------------------------------------------------------------------------------------
    #formatType: Hex for #RRGGBB, RGB for (R, G, B) and IDX for VBA Color Index
    colorVal = Rng.DisplayFormat.Interior.Color
    _select76 = UCase(formatType)
    if (_select76 == 'HEX'):
        _fn_return_value = '#' + X02.Format(Hex(colorVal % 256), '00') + X02.Format(Hex(( colorVal // 256 )  % 256), '00') + X02.Format(Hex(( colorVal // 65536 )), '00')
    elif (_select76 == 'RGB'):
        _fn_return_value = X02.Format(( colorVal % 256 ), '00') + ', ' + X02.Format(( ( colorVal // 256 )  % 256 ), '00') + ', ' + X02.Format(( colorVal // 65536 ), '00')
    elif (_select76 == 'IDX'):
        _fn_return_value = Rng.Interior.ColorIndex
    else:
        _fn_return_value = colorVal
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Brightness - ByVal 
def iColor_with_Brightness(Rng, Brightness):
    _fn_return_value = None
    colorVal = Variant()

    r = Byte()

    G = Byte()

    B = Byte()
    # 04.06.20: Hardi
    #----------------------------------------------------------------------------------------
    #formatType: Hex for #RRGGBB, RGB for (R, G, B) and IDX for VBA Color Index
    colorVal = Rng.DisplayFormat.Interior.Color
    #colorValstr= colorValstr.replace("#","0x")
    #colorVal = int(colorValstr,0)
    R = Brightness *  ( colorVal % 256 )  / 256
    G = Brightness *  ( ( colorVal // 256 )  % 256 )  / 256
    B = Brightness *  ( colorVal // 65536 )  / 256
    _fn_return_value = X02.Format(R, '00') + ', ' + X02.Format(G, '00') + ', ' + X02.Format(B, '00')
    return _fn_return_value

def ControlNr(MacroName, Patterns):
    _fn_return_value = None
    c = Variant()

    OptionNr = Variant()

    PartsCount = Variant()

    PartNr = Integer()

    OptionPattern = Variant()

    TimerEntrys = Variant()

    Nr = Long()

    Parts = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------------------------
    for c in vbForRange(1, Len(MacroName)):
        _fn_return_value = ControlNr() + Asc(Mid(MacroName, c, 1))
    # PatternT(x)(Start LED, Brightness Level (bits), InCh, Number Output Channels, Min Brightness, Max Brightness, SwitchMode, CtrMode, < Patternconfig >)
    # Parts(y)        0               1                 2             3                   4               5             6          7          8 ...>
    # Example => PatternT2(LED,4,InCh,12,0,128,0,PM_NORMAL,0.3 sec,0.5 sec,0,0,0,195,48,12)
    for OptionNr in vbForRange(1, 8):
        OptionPattern = Patterns(OptionNr)
        Parts = Split(Mid(OptionPattern, InStr(OptionPattern, '(') + 1, Len(OptionPattern)), ',')
        TimerEntrys = Val(Mid(OptionPattern, InStr(OptionPattern, 'PatternT') + 8, Len(OptionPattern) -  ( Len(OptionPattern) - InStr(OptionPattern, '(') )))
        PartsCount = UBound(Parts())
        Parts[PartsCount] = Replace(Parts(PartsCount), ')', '')
        if PartsCount > 0:
            _fn_return_value = ControlNr() + Parts(1)
            _fn_return_value = ControlNr() + Parts(3)
            _fn_return_value = ControlNr() + Parts(4)
            _fn_return_value = ControlNr() + Parts(5)
            _fn_return_value = ControlNr() + Parts(6)
            for Nr in vbForRange(8 + TimerEntrys, PartsCount):
                _fn_return_value = ControlNr() + Parts(Nr)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DecimalIn - ByVal 
def DecToBin(DecimalIn):
    _fn_return_value = None
    #--------------------------------------------------------------------------------------------
    # The DecimalIn argument is limited to 79228162514264337593543950245
    # (approximately 96-bits) - large numerical values must be entered
    # as a String value to prevent conversion to scientific notation.
    _fn_return_value = ''
    DecimalIn = CDec(DecimalIn)
    while DecimalIn != 0:
        _fn_return_value = Trim(str(DecimalIn - 2 * Int(DecimalIn / 2))) + DecToBin()
        DecimalIn = Int(DecimalIn / 2)
    return _fn_return_value

def Bin2Dec(sMyBin):
    _fn_return_value = None
    x = Integer()

    iLen = Integer()
    #--------------------------------------------------------------------------------------------
    iLen = Len(sMyBin) - 1
    for x in vbForRange(0, iLen):
        _fn_return_value = Bin2Dec() + Mid(sMyBin, iLen - x + 1, 1) * 2 ** x
    return _fn_return_value

def Count_Ones(Waarde):
    _fn_return_value = None
    t = Integer()

    binOptions = String()

    Count = Integer()
    #--------------------------------------------------------------------------------------------
    for t in vbForRange(1, 8):
        binOptions = DecToBin(Waarde)
        #        Debug.Print Waarde, " / ", binOptions
        if Right(binOptions, 1) == 1:
            # LSB = 1
            Count = Count + 1
        Waarde = X02.Application.WorksheetFunction.Bitrshift(Waarde, 1)
    _fn_return_value = Count
    #    Debug.Print "Count_Ones    = ", Count
    return _fn_return_value

def Make_Seconds(vSeconds):
    _fn_return_value = None
    Parts = vbObjectInitialize(objtype=String)
    #--------------------------------------------------------------------------------------------
    Parts = Split(vSeconds, ' ')
    if InStr(vSeconds, 'Min'):
        # 03.06.20: Hardi: Old: cSeconds
        _fn_return_value = Parts(0) * 60 / 1000
    else:
        _fn_return_value = Parts(0) / 1000
    return _fn_return_value

def Test_ReadIniFileString():
    Value = Variant()

    Section = Variant()

    KeyName = String()
    #--------------------------------------------------------------------------------------------
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Description'
    Value = ReadIniFileString(Section, KeyName)
    Debug.Print(Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 1 Name'
    Value = ReadIniFileString(Section, KeyName)
    Debug.Print(Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 7 Pattern'
    Value = ReadIniFileString(Section, KeyName)
    Debug.Print(Value)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Section - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyName - ByVal 
def ReadIniFileString(Section, KeyName):
    _fn_return_value = None
    iNoOfCharInIni = Long()

    sIniString = Variant()

    sProfileString = String()

    Worked = Long()

    RetStr = FixedString(1500)

    StrSize = Long()
    #--------------------------------------------------------------------------------------------
    iNoOfCharInIni = 0
    sIniString = ''
    if Section == '' or KeyName == '':
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Abschnitt oder Schlüssel zum Lesen Nicht angegeben !!!'), vbExclamation, 'INI')
    else:
        sProfileString = ''
        RetStr = Space(1500)
        StrSize = Len(RetStr)
        Worked = X03.GetPrivateProfileString(Section, KeyName, '', RetStr, StrSize, pattgen.M80_Multiplexer_INI_Handling.IniFileName)
        if Worked:
            iNoOfCharInIni = Worked
            sIniString = Left(RetStr, Worked)
    _fn_return_value = sIniString
    return _fn_return_value

def Test_WriteIniFileString():
    Test = Variant()

    Section = Variant()

    KeyName = Variant()

    Value = String()
    #--------------------------------------------------------------------------------------------
    Section = 'Multiplexer_Macro'
    KeyName = 'INI File Production Date'
    Value = X02.Now()
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Macro Syntax'
    Value = 'Multiplexer_RGB_Ext4(#LED, #InCh, #LocInCh, Brightness, Groups4, #Options, RndMinTime, RndMaxTime, #CtrMode)'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 1 Name'
    Value = 'RGB_Multiplexer_3_4_Running_Blue (pc)'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 2 Pattern'
    Value = 'PatternT2(LED,4,#LOC_INCH+1,12,0,Brightness,0,PM_NORMAL,0.1 sec,0.1 sec,0,0,0,195,48,12)'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 3 Pattern'
    Value = 'PatternT1(LED,4,#LOC_INCH+2,12,0,Brightness,0,PM_NORMAL,100 ms,0,0,48,0,192,0,0,3,0,12,0,0)'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 4 Pattern'
    Value = 'PatternT1(LED,4,#LOC_INCH+3,12,0,Brightness,0,PM_NORMAL,100 ms,0,240,255,255,15,0)'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 5 Pattern'
    Value = 'To be filled!'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 6 Pattern'
    Value = 'To be filled!'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 7 Pattern'
    Value = 'To be filled!'
    Test = WriteIniFileString(Section, KeyName, Value)
    Section = 'Test_Multiplexer_RGB_Ext4'
    KeyName = 'Option 8 Pattern'
    Value = 'To be filled!'
    Test = WriteIniFileString(Section, KeyName, Value)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Section - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Wstr - ByVal 
def WriteIniFileString(Section, KeyName, Wstr):
    _fn_return_value = None
    iNoOfCharInIni = Variant()

    Worked = Long()

    sIniString = String()
    #--------------------------------------------------------------------------------------------
    iNoOfCharInIni = 0
    sIniString = ''
    if Section == '' or KeyName == '':
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Abschnitt oder Schlüssel zum Schreiben nicht angegeben !!!'), vbExclamation, 'INI')
    else:
        Worked = X03.WritePrivateProfileString(Section, KeyName, Wstr, pattgen.M80_Multiplexer_INI_Handling.IniFileName)
        if Worked:
            iNoOfCharInIni = Worked
            sIniString = Wstr
        _fn_return_value = sIniString
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strkey - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strDefault='' - ByVal 
def ReadFromINI(strSection, strkey, strfullpath, strDefault=''):
    _fn_return_value = None
    strBuffer = String()
    #function to return the key value of any keys inside an ini section.
    strBuffer = String(750, Chr(0))
    _fn_return_value = Left(strBuffer, X03.GetPrivateProfileString(strSection, LCase(strkey), strDefault, strBuffer, Len(strBuffer), strfullpath))
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strkey - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strkeyvalue - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def WriteToINI(strSection, strkey, strkeyvalue, strfullpath):
    #sub to write a key and its value inside an ini section.
    X03.WritePrivateProfileString(strSection, UCase(strkey), strkeyvalue, strfullpath)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def DeleteIniSection(strSection, strfullpath):
    #sub to delete an entire ini section.
    X03.WritePrivateProfileString(strSection, 0, 0, strfullpath)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strKeyname - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def DeleteIniKey(strSection, strKeyname, strfullpath):
    #sub to delete a particular key inside an ini section.
    X03.WritePrivateProfileString(strSection, strKeyname, 0, strfullpath)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strKeyname - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def CheckIfIniKeyExists(strSection, strKeyname, strfullpath):
    _fn_return_value = None
    str_A = String()

    str_B = String()
    #function to check if an ini key exists.
    str_A = ReadFromINI(strSection, strKeyname, strfullpath, 'A')
    str_B = ReadFromINI(strSection, strKeyname, strfullpath, 'B')
    if str_A == str_B:
        _fn_return_value = True
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def CheckIfIniSectionExists(strSection, strfullpath):
    _fn_return_value = None
    strBuffer = String()
    #function to check if an ini section exists.
    strBuffer = String(750, Chr(0))
    _fn_return_value = CBool(X03.GetPrivateProfileSection(strSection, strBuffer, Len(strBuffer), strfullpath) > 0)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strKeyname - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lngDefault=0 - ByVal 
def GetLongFromINI(strSection, strKeyname, strfullpath, lngDefault=0):
    _fn_return_value = None
    #function to return the Long portion of a key value. (will return 0 if the optional argument has not been passed and key value is non numeric or if key does not exist or is empty)
    _fn_return_value = X03.GetPrivateProfileInt(strSection, strKeyname, lngDefault, strfullpath)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strKeyname - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strNewKeyname - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def RenameIniKey(strSection, strKeyname, strNewKeyname, strfullpath):
    tmpKeyValue = String()
    #sub to rename a particular key inside an ini section.
    if CheckIfIniKeyExists(strSection, strKeyname, strfullpath) == False:
        return
    tmpKeyValue = ReadFromINI(strSection, strKeyname, strfullpath)
    WriteToINI(strSection, strNewKeyname, tmpKeyValue, strfullpath)
    DeleteIniKey(strSection, strKeyname, strfullpath)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strNewSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def RenameIniSection(strSection, strNewSection, strfullpath):
    KeyAndVal = vbObjectInitialize(objtype=String)

    Key_Val = vbObjectInitialize(objtype=String)

    strBuffer = String()

    intx = Integer()
    #sub to rename an ini section name.
    strBuffer = String(750, Chr(0))
    X03.GetPrivateProfileSection(strSection, strBuffer, Len(strBuffer), strfullpath)
    KeyAndVal = Split(strBuffer, vbNullChar)
    for intx in vbForRange(LBound(KeyAndVal), UBound(KeyAndVal)):
        Key_Val = Split(KeyAndVal(intx), '=')
        if UBound(Key_Val) == - 1:
            break
        WriteToINI(strNewSection, Key_Val(0), Key_Val(1), strfullpath)
    DeleteIniSection(strSection, strfullpath)
    Erase(KeyAndVal)
    Erase(Key_Val)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def LoadIniSectionsArray(strfullpath):
    _fn_return_value = None
    sectnNames = vbObjectInitialize(objtype=String)

    strBuffer = String()
    #function for populating array with all ini section names.
    strBuffer = Space(1024)
    X03.GetPrivateProfileSectionNames(strBuffer, Len(strBuffer), strfullpath)
    sectnNames = Split(strBuffer, vbNullChar)
    _fn_return_value = Split(strBuffer, vbNullChar, UBound(sectnNames) - 1)
    Erase(sectnNames)
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lstB - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def LoadIniSectionKeysLB(strSection, lstB, strfullpath):
    KeyAndVal = vbObjectInitialize(objtype=String)

    Key_Val = vbObjectInitialize(objtype=String)

    strBuffer = String()

    intx = Integer()
    #sub to load all keys from an ini section into a listbox.
    strBuffer = String(750, Chr(0))
    X03.GetPrivateProfileSection(strSection, strBuffer, Len(strBuffer), strfullpath)
    KeyAndVal = Split(strBuffer, vbNullChar)
    for intx in vbForRange(LBound(KeyAndVal), UBound(KeyAndVal)):
        if KeyAndVal(intx) == vbNullString:
            break
        Key_Val = Split(KeyAndVal(intx), '=')
        if UBound(Key_Val) == - 1:
            break
        lstB.AddItem(Key_Val(0))
        #lstB.additem inikey(1) '<--to get the key values past the "=" delimiter only
    #If lstB.ListCount > 0 Then lst.Selected(0) = True '<<--if you want first list item in listbox selected
    Erase(KeyAndVal)
    Erase(Key_Val)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strSection - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: strfullpath - ByVal 
def GetSectionKeyCount(strSection, strfullpath):
    _fn_return_value = None
    KeyAndVal = vbObjectInitialize(objtype=String)

    strBuffer = String()

    intx = Integer()

    SectionKeyCount = Integer()
    #function to get the key count of a particular ini section.
    strBuffer = String(750, Chr(0))
    X03.GetPrivateProfileSection(strSection, strBuffer, Len(strBuffer), strfullpath)
    KeyAndVal = Split(strBuffer, vbNullChar)
    for intx in vbForRange(LBound(KeyAndVal), UBound(KeyAndVal)):
        if KeyAndVal(intx) == vbNullString:
            break
        SectionKeyCount = SectionKeyCount + 1
    _fn_return_value = SectionKeyCount
    Erase(KeyAndVal)
    return _fn_return_value

def Center_Form2(f):
    #---------------------------
    _with124 = f
    _with124.StartupPosition = 0
    _with124.Left = X02.Application.Left +  ( X02.Application.Width - _with124.Width )  / 2
    _with124.Top = X02.Application.Top +  ( X02.Application.Height - _with124.Height )  / 2
    if _with124.Top < X02.Application.Top:
        _with124.Top = X02.Application.Top
    # 02.03.20
    if _with124.Left < X02.Application.Left:
        _with124.Left = X02.Application.Left

def Restore_Pos_or_Center_Form2(f, OldPos):
    #--------------------------------------------------------------
    if OldPos.Valid:
        f.StartupPosition = 0
        f.Left = OldPos.Left
        f.Top = OldPos.Top
    else:
        X02.Center_Form(f)

def Restore_Pos_or_Leftaligne_Form2(f, OldPos):
    #--------------------------------------------------------------
    if OldPos.Valid:
        f.StartupPosition = 0
        f.Left = OldPos.Left
        f.Top = OldPos.Top
    else:
        X02.Center_Form(f)
        f.Left = X02.Application.Left

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: PosVar - ByRef 
def Store_Pos2(f, PosVar):
    #---------------------------------------------------
    PosVar.Valid = True
    PosVar.Left = f.Left
    PosVar.Top = f.Top

def ActiveSheet_ProtectShapes(WasProtected):
    #*HL s = Shape()
    #---------------------------------------------------
    if pattgen.M80_Multiplexer_INI_Handling.Multiplexer_Init:
        return
    X02.ActiveSheet.Unprotect(Password='')
    for s in X02.ActiveSheet.Shapes:
        s.Locked = True
    #    ActiveSheet.Protect Password:=""
    if WasProtected:
        M30.Protect_Active_Sheet()

def ActiveSheet_UnProtectShapes():
    #*HL s = Shape()
    #---------------------------------------------------
    X02.ActiveSheet.Unprotect(Password='')
    for s in X02.ActiveSheet.Shapes:
        s.Locked = False

def Format_Row(Rng):
    #--------------------------------------------------------------------------------------------
    _with125 = Rng
    _with125.HorizontalAlignment = X01.xlLeft
    _with125.VerticalAlignment = X01.xlCenter
    _with125.WrapText = False
    _with125.Orientation = 0
    _with125.AddIndent = False
    _with125.IndentLevel = 0
    _with125.ShrinkToFit = False
    _with125.ReadingOrder = X01.xlContext
    _with125.MergeCells = True
    _with125.RowHeight = 24
    _with125.Interior.Pattern = X01.xlNone
    _with125.Interior.TintAndShade = 0
    _with125.Interior.PatternTintAndShade = 0
    _with125.Font.Size = 14
    _with125.Merge()
    _with125.Locked = False
    _with125.FormulaHidden = False

def Format_Multiplexer_Group(Row, Col):
    #--------------------------------------------------------------------------------------------
    _with126 = X02.Cells(Row, Col)
    _with126.HorizontalAlignment = X01.xlCenter
    _with126.VerticalAlignment = X01.xlCenter
    _with126.WrapText = False
    _with126.Orientation = 0
    _with126.AddIndent = False
    _with126.IndentLevel = 0
    _with126.ShrinkToFit = False
    _with126.ReadingOrder = X01.xlContext
    _with126.MergeCells = False
    _with126.Locked = True
    _with126.FormulaHidden = False
    _with126.Interior.Pattern = X01.xlNone
    _with126.Interior.TintAndShade = 0
    _with126.Interior.PatternTintAndShade = 0
    _with126.Font.Size = 14

def Format_Group(MacroRow):
    #--------------------------------------------------------------------------------------------
    _with127 = X02.Range(X02.Cells(MacroRow, 10).Address(), X02.Cells(MacroRow, 15).Address())
    _with127.Borders[X01.xlDiagonalDown].LineStyle = X01.xlNone
    _with127.Borders[X01.xlDiagonalUp].LineStyle = X01.xlNone
    _with127.Borders[X01.xlEdgeLeft].LineStyle = X01.xlContinuous
    _with127.Borders[X01.xlEdgeLeft].ColorIndex = X01.xlAutomatic
    _with127.Borders[X01.xlEdgeLeft].TintAndShade = 0
    _with127.Borders[X01.xlEdgeLeft].Weight = X01.xlThin
    _with127.Borders[X01.xlEdgeTop].LineStyle = X01.xlContinuous
    _with127.Borders[X01.xlEdgeTop].ColorIndex = X01.xlAutomatic
    _with127.Borders[X01.xlEdgeTop].TintAndShade = 0
    _with127.Borders[X01.xlEdgeTop].Weight = X01.xlThin
    _with127.Borders[X01.xlEdgeBottom].LineStyle = X01.xlContinuous
    _with127.Borders[X01.xlEdgeBottom].ColorIndex = X01.xlAutomatic
    _with127.Borders[X01.xlEdgeBottom].TintAndShade = 0
    _with127.Borders[X01.xlEdgeBottom].Weight = X01.xlThin
    _with127.Borders[X01.xlEdgeRight].LineStyle = X01.xlContinuous
    _with127.Borders[X01.xlEdgeRight].ColorIndex = X01.xlAutomatic
    _with127.Borders[X01.xlEdgeRight].TintAndShade = 0
    _with127.Borders[X01.xlEdgeRight].Weight = X01.xlThin
    _with127.Borders[X01.xlInsideVertical].LineStyle = X01.xlNone
    _with127.Borders[X01.xlInsideHorizontal].LineStyle = X01.xlNone

# VB2PY (UntranslatedCode) Option Explicit
