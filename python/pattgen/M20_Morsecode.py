from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M09_Language
import ExcelAPI.XLW_Workbook as X02
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M01_Public_Constants_a_Var as M01
import ExcelAPI.XLWA_WinAPI as X03

""" This Modul has been written by Lorenz
 with some smal modifications by Hardi
 Revision History:
 ~~~~~~~~~~~~~~~~~
 17.10.19: - Speed Up
 19.10.19: - Suport for special codes like {SOS}
           - Error checks
 22.11.19: - Replaced the most cell adresses by public constants
             The Morse code specific cells M2..P5 have not been replaced
 ToDo:
 - Use the public constants: FirstLEDTabRANGE, ...
------------------------------------------------------
UT------------
-------------------------------
---------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------
--------------------------------------------------------------------------------
UT----------------------------------
----------------------------
"""


def Add_Kursive_Text(r, Txt):
    return '*HL'
    Parts = vbObjectInitialize(objtype=String)
    #------------------------------------------------------
    Parts = Split(pattgen.M09_Language.Get_Language_Str(Txt), '#')
    if UBound(Parts) != 2:
        X02.MsgBox('Error: In the Language sheet. The text \'' + Txt + '\' must contain the startposition and the length of the cursive part', vbCritical, 'Internal Error')
        r = Txt
    else:
        r = Parts(2)
        r.Characters(Start= Val(Parts(0)), Length= Val(Parts(1))).Font.FontStyle = 'Italic'  #*HL

def Test_Bold():
    #UT------------
    # Attention: Place the cursor to the destination cell for the test
    Add_Kursive_Text(X02.ActiveCell(), '7#3#Dauer Dit in ms')

def Make_Morsecode_Init():
    Oldupdating = Boolean()

    OldEvents = Boolean()
    #-------------------------------
    # Ist called when the sheet is copied with the "Neues Blatt" button or loaded from a file
    Oldupdating = X02.Application.ScreenUpdating
    OldEvents = X02.Application.EnableEvents
    X02.Application.ScreenUpdating = False
    X02.Application.EnableEvents = False
    X02.RangeDict['M2'] = pattgen.M09_Language.Get_Language_Str('Morsetext')
    Add_Kursive_Text(X02.Range('M3'), '7#3#Dauer Dit in ms')
    X02.RangeDict['M4'] = pattgen.M09_Language.Get_Language_Str('Spruchanfang/-ende senden')
    X02.RangeDict['M5'] = pattgen.M09_Language.Get_Language_Str('Nach dem Erstellen vorführen')
    X02.RangeDict['M5'].HorizontalAlignment = X01.xlRight
    X02.RangeDict['N2'] = pattgen.M09_Language.Get_Language_Str('{SOS} Rettet Hardi')
    X02.RangeDict['N3'] = '240'
    X02.RangeDict['N4'] = pattgen.M09_Language.Get_Language_Str('Nein')
    X02.RangeDict['N5'] = pattgen.M09_Language.Get_Language_Str('Ja')
    X02.RangeDict['N2:N5'].Interior.Color = 65535
    X02.RangeDict['O2:P2'].Interior.Color = 65535
    Hide_Second_Pic()
    X02.Application.ScreenUpdating = Oldupdating
    X02.Application.EnableEvents = OldEvents
    #Button_Init_Proc_Finished = True
    # 05.01.22: Juergen call init function synchronous
    ##If VBA6 Then
    # 05.01.22: Juergen call init function synchronous
    #  Debug.Print "Button_Init_Proc_Finished=" & Button_Init_Proc_Finished
    #  DoEvents
    ##End If

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Zellcounter - ByRef 
def One_Char(Zeichencode, Zellcounter, Morsezeichen):
    Zaehlerincode = Integer()

    c = String()
    #---------------------------------------------------------------------------------------------------
    c = Chr(Zeichencode)
    for Zaehlerincode in vbForRange(1, Len(Morsezeichen(Zeichencode))):
        _select28 = Mid(Morsezeichen(Zeichencode), Zaehlerincode, 1)
        if (_select28 == '·'):
            X02.CellDict[M01.LEDsTAB_R + 0, Zellcounter].Value = 'X'
            X02.CellDict[M01.LEDsTAB_R + 2, Zellcounter].Value = '.'
            X02.CellDict[M01.LEDsTAB_R + 1, Zellcounter].Value = c
            Zellcounter = Zellcounter + 1
        elif (_select28 == '-'):
            X02.Range(X02.Cells(M01.LEDsTAB_R + 0, Zellcounter), X02.Cells(M01.LEDsTAB_R + 0, Zellcounter + 2)).Value = 'X'
            X02.Range(X02.Cells(M01.LEDsTAB_R + 2, Zellcounter), X02.Cells(M01.LEDsTAB_R + 2, Zellcounter + 2)).Value = '-'
            X02.Range(X02.Cells(M01.LEDsTAB_R + 1, Zellcounter), X02.Cells(M01.LEDsTAB_R + 1, Zellcounter + 2)).Value = c
            Zellcounter = Zellcounter + 3
        elif (_select28 == '_') or (_select28 == ' '):
            Zellcounter = Zellcounter + 1
        else:
            X02.MsgBox('Wrong character in \'Morsezeichen(' + Zeichencode + ')\'', vbCritical, 'Interner Fehler')
    return Zellcounter #*HL ByRef

def Make_Morsecode():
    Zaehler = Double()

    Zeichencode = Integer()

    Morsezeichen = vbObjectInitialize(((1, 255),), String)

    Morsecode = String()

    Ditdauer = Double()

    Spruchanfangende = String()

    Zellcounter = Long()

    WrongChar = String()
    #------------------------------------------------------------------------------------------------------------------------------------
    #Dim Zaehlerincode As Integer
    X02.Application.EnableEvents = False
    # 17.10.19: Hardi:
    X02.Application.ScreenUpdating = False
    X02.Application.Calculation = X01.xlCalculationManual
    # Morsetable corresponding to ASCII codes
    Morsezeichen[32] = '_'
    # Additional codes from https://de.wikipedia.org/wiki/Morsezeichen#@-Zeichen  19.10.19: Hardi
    # How to handle special signals ?
    Morsezeichen[Asc('À')] = '· - - · -'
    Morsezeichen[Asc('Å')] = '· - - · -'
    Morsezeichen[Asc('Ä')] = '· - · -'
    Morsezeichen[Asc('È')] = '· - · · -'
    Morsezeichen[Asc('É')] = '· · - · ·'
    Morsezeichen[Asc('Ö')] = '- - - ·'
    #  (OE)
    Morsezeichen[Asc('Ü')] = '· · - -'
    # ??       "- - - -" CH
    Morsezeichen[Asc('ß')] = '· · · - - · ·'
    #  (SZ)
    Morsezeichen[Asc('Ñ')] = '- - · - -'
    Morsezeichen[Asc('.')] = '· - · - · -'
    #  (AAA)
    Morsezeichen[Asc(',')] = '- - · · - -'
    #  (MIM)
    Morsezeichen[Asc(':')] = '- - - · · ·'
    #  (OS)
    Morsezeichen[Asc(';')] = '- · - · - ·'
    #  (NNN)
    Morsezeichen[Asc('?')] = '· · - - · ·'
    #  (IMI)
    Morsezeichen[Asc('-')] = '- · · · · -'
    #  (BA)
    Morsezeichen[Asc('_')] = '· · - - · -'
    #  (UK)
    Morsezeichen[Asc('(')] = '- · - - ·'
    #  (KN)
    Morsezeichen[Asc(')')] = '- · - - · -'
    #  (KK)
    Morsezeichen[Asc('\'')] = '· - - - - ·'
    #  (JN)
    Morsezeichen[Asc('=')] = '- · · · -'
    #  (BT)
    Morsezeichen[Asc('+')] = '· - · - ·'
    #  (AR)
    Morsezeichen[Asc('/')] = '- · · - ·'
    #  (DN)
    Morsezeichen[Asc('@')] = '· - - · - ·'
    #  (AC)
    Morsezeichen[48] = '-_-_-_-_-'
    # 0
    Morsezeichen[49] = '·_-_-_-_-'
    Morsezeichen[50] = '·_·_-_-_-'
    Morsezeichen[51] = '·_·_·_-_-'
    Morsezeichen[52] = '·_·_·_·_-'
    Morsezeichen[53] = '·_·_·_·_·'
    Morsezeichen[54] = '-_·_·_·_·'
    Morsezeichen[55] = '-_-_·_·_·'
    Morsezeichen[56] = '-_-_-_·_·'
    Morsezeichen[57] = '-_-_-_-_·'
    # 9
    Morsezeichen[65] = '·_-'
    # A
    Morsezeichen[66] = '-_·_·_·'
    Morsezeichen[67] = '-_·_-_·'
    Morsezeichen[68] = '-_·_·'
    Morsezeichen[69] = '·'
    Morsezeichen[70] = '·_·_-_·'
    Morsezeichen[71] = '-_-_·'
    Morsezeichen[72] = '·_·_·_·'
    Morsezeichen[73] = '·_·'
    Morsezeichen[74] = '·_-_-_-'
    Morsezeichen[75] = '-_·_-'
    Morsezeichen[76] = '·_-_·_·'
    Morsezeichen[77] = '-_-'
    Morsezeichen[78] = '-_·'
    Morsezeichen[79] = '-_-_-'
    Morsezeichen[80] = '·_-_-_·'
    Morsezeichen[81] = '-_-_·_-'
    Morsezeichen[82] = '·_-_·'
    Morsezeichen[83] = '·_·_·'
    Morsezeichen[84] = '-'
    Morsezeichen[85] = '·_·_-'
    Morsezeichen[86] = '·_·_·_-'
    Morsezeichen[87] = '·_-_-'
    Morsezeichen[88] = '-_·_·_-'
    Morsezeichen[89] = '-_·_-_-'
    Morsezeichen[90] = '-_-_·_·'
    # Z
    Zellcounter = M01.Dauer_Col1
    # Number of Cell to fill with LED command
    Morsecode = X02.Cells(2, 14).Value
    # String contains morse text to send
    Ditdauer = X02.Cells(3, 14).Value
    # Duration of Dit
    Spruchanfangende = X02.Cells(4, 14).Value
    if Spruchanfangende == pattgen.M09_Language.Get_Language_Str('Ja'):
        Morsecode = 'KA ' + Morsecode + 'AR'
        # Add start and end codes to morsecode
    # send start and end code yes/no
    X02.Range(M01.Dauer_Rng).ClearContents()
    X02.Range(M01.LEDs__TAB).ClearContents()
    X02.Range(M01.GoTo_RNG).ClearContents()
    Morsecode = UCase(Morsecode)
    # Set all Letters in Morsecode to uppercase
    X02.CellDict[M01.Dauer_Row, Zellcounter].Value = Ditdauer
    # Duration Ditdauer into first cell of "Dauer"
    for Zaehler in vbForRange(1, Len(Morsecode)):
        # Loop for length of morse code sentence
        c = Mid(Morsecode, Zaehler, 1)
        Zeichencode = Asc(c)
        if c != '{' and Morsezeichen(Zeichencode) == '':
            # 19.10.19: Hardi
            if InStr(WrongChar, c) == 0:
                WrongChar = WrongChar + c + ' '
        if c == '{':
            # Handle special signals
            # 19.10.19: Hardi
            Parts = Split(Mid(Morsecode, Zaehler), '}')
            _select29 = Mid(Parts(0), 2)
            if (_select29 == 'KA') or (_select29 == 'BT') or (_select29 == 'AR') or (_select29 == 'VE') or (_select29 == 'SK') or (_select29 == 'SOS') or (_select29 == 'HH') or (_select29 == 'OE') or (_select29 == 'SZ') or (_select29 == 'AAA') or (_select29 == 'MIM') or (_select29 == 'OS') or (_select29 == 'NNN') or (_select29 == 'IMI') or (_select29 == 'BA') or (_select29 == 'UK') or (_select29 == 'KN') or (_select29 == 'KK') or (_select29 == 'JN') or (_select29 == 'BT') or (_select29 == 'AR') or (_select29 == 'DN') or (_select29 == 'AC'):
                for ix in vbForRange(2, Len(Parts(0))):
                    Zellcounter = One_Char(Asc(Mid(Parts(0), ix, 1)), Zellcounter, Morsezeichen)
                    Zellcounter = Zellcounter + 1
            else:
                X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Unbekanntes Spezial Signal \'') + Parts(0) + '}\'', vbCritical, pattgen.M09_Language.Get_Language_Str('Unbekanntes Signal'))
            Zaehler = Zaehler + Len(Parts(0)) + 1
        else:
            ## VB2PY (CheckDirective) VB directive took path 1 on 1
            Zellcounter = One_Char(Zeichencode, Zellcounter, Morsezeichen)
        Zellcounter = Zellcounter + 3
    Zellcounter = Zellcounter - 3
    # 17.10.19: Hardi
    X02.CellDict[M01.LEDsTAB_R + 0, Zellcounter] = '.'
    # Turn of the led at the end of the code
    if WrongChar != '':
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Achtung die folgenden Zeichen existieren nicht im Morse Alphabet:') + vbCr + '  ' + WrongChar + vbCr + pattgen.M09_Language.Get_Language_Str('Die Zeichen wurden weggelassen'), vbCritical, pattgen.M09_Language.Get_Language_Str('Falsche Zeichen erkannt'))
    if Zellcounter > 148 + 5:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Der Morsecode ist zu lang (') + Zellcounter - 5 + pattgen.M09_Language.Get_Language_Str('). Maximal 148 Abschnitte sind möglich.'), vbInformation, pattgen.M09_Language.Get_Language_Str('Morsecode zu lang'))
        # Problem: Der Range mit dem die Macros "CalculatePattern", ... aufgerufen werden ist nicht größer
        #          damit die Berechnung bei anderen sheets nicht zu lange dauert.
        #          => Erst mal muss diese Länge reichen.
    X02.Application.EnableEvents = True
    X02.Application.ScreenUpdating = True
    X02.Application.Calculation = X01.xlCalculationAutomatic
    X02.ActiveSheet.Calculate()
    if X02.Cells(5, 14).Value == pattgen.M09_Language.Get_Language_Str('Ja') or X02.Cells(5, 14).Value == 'Ja':
        # 12.02.20: Added 'Or Cells(5, 14).Value = "Ja"' for tests. Normaly the answers are also translated
        Simulate_MorseCode(Ditdauer, Zellcounter)

def Find_Second_Pic():
    _fn_return_value = None
    o = Variant()

    Nr = Integer()
    #--------------------------------------------
    for o in X02.ActiveSheet.Shapes:
        #If o.Type <> msoComment Then o.Select
        # Debug
        _select30 = o.Type
        if (_select30 == X01.msoPicture) or (_select30 == X01.msoLinkedPicture):
            if o.Name != 'MainMenu':
                Nr = Nr + 1
                if Nr == 2:
                    _fn_return_value = o
                    return _fn_return_value
    _fn_return_value = None
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Ditdauer - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Zellcounter - ByVal 
def Simulate_MorseCode(Ditdauer, Zellcounter):
    Led_An = Variant()

    i = Integer()

    Zaehler = Long()

    StartActCell = Long()
    #--------------------------------------------------------------------------------
    Led_An = Find_Second_Pic()
    X02.Application.Cursor = X01.xlWait
    # Otherwise the cursor flashes
    for Zaehler in vbForRange(M01.LEDsTAB_C, Zellcounter):
        if X02.Cells(M01.LEDsTAB_R, Zaehler).Value == 'X':
            if StartActCell == 0:
                StartActCell = Zaehler
            X02.CellDict[M01.LEDsTAB_R + 1, Zaehler].Interior.ColorIndex = 6
        else:
            if StartActCell > 0:
                X02.Range(X02.Cells(M01.LEDsTAB_R + 1, StartActCell), X02.Cells(M01.LEDsTAB_R + 1, Zaehler)).Interior.ColorIndex = 2
                StartActCell = 0
        Led_An.Visible = ( X02.Cells(M01.LEDsTAB_R, Zaehler).Value == 'X' )
        # Show / Hide the flash light
        X02.ActiveSheet.Calculate()
        X02.DoEvents()
        X03.Sleep(Ditdauer)
    Zaehler += 1 #* loop variable in Python 1 less as in VBA
    #Cells(LEDsTAB_R+1, Zaehler - 1).Interior.ColorIndex = 2
    if StartActCell > 0:
        X02.Range(X02.Cells(M01.LEDsTAB_R + 1, StartActCell), X02.Cells(M01.LEDsTAB_R + 1, Zaehler)).Interior.ColorIndex = 2
    Led_An.Visible = False
    X02.Application.Cursor = X01.xlDefault

def Test_Simulate_MorseCode():
    #UT----------------------------------
    Simulate_MorseCode(240, 30)

def Hide_Second_Pic():
    
    Led_An = Variant()
    #----------------------------
    Led_An = Find_Second_Pic()
    if Led_An is None:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler die Bilder wurden nicht geladen. Bitte sicherstellen, dass sie in der \'MLL_pcf\' Datei VOR dem Button (msoFormControl) stehen.'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler in Beispiel Datei'))
    else:
        Led_An.Visible = False

# VB2PY (UntranslatedCode) Option Explicit
