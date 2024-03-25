from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M30_Tools as M30
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M01a_Public_Constants_a_Var as M01a
import pattgen.M09_Language
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M13_Goto_Act
import pattgen.M06_Goto_Graph
import pattgen.M14_Select_GotoAct
import proggen.M50_Exchange as M50
import mlpyproggen.Pattern_Generator as PG
import proggen.M06_Write_Header as M06

""" Export macros to the Prog_Generator
 ToDo:
 - Abfrage in Get_Prog_Generator_Name() einbauen mit dem man ein anderes Prog_Generator
   Programm anstelle das standards auswählen kann (Name/Verzeichnis)
   Momentan kommt nur eine Meldung das das Programm nicht gefunden wurde
 - Überprüfung der Prog_Generator Version
---------------------------------------------------
UT---------------------------------------
----------------------------------------------------------------------------------------------------------
-----------------------------------------------
------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
------------------------------------------------------------------
"""

Default_Prog_Generator_Name = 'Prog_Generator_MobaLedLib.xlsm'
Prog_Generator_Name = String()

def Get_Prog_Generator_Name():
    global Prog_Generator_Name
    _fn_return_value = None
    #---------------------------------------------------
    # Make sure that the Prog_Generator excel sheet is opened
    # and activated.
    # The function returns the name if it's activated
    # In case of an error "" is returned
    Prog_Generator_Name = Default_Prog_Generator_Name
    return Prog_Generator_Name


    if Prog_Generator_Name == '':
        if M30.Same_Name_already_open(Default_Prog_Generator_Name):
            Prog_Generator_Name = X02.Workbooks(Default_Prog_Generator_Name).FullName
        else:
            # Prog_Generator not opened
            Path = M01.Get_DestDir_All()
            # Check if it exists in the user dir
            FullPath = Path + Default_Prog_Generator_Name
            if Dir(FullPath) == '':
                # Check if it exists in the lib dir
                Path = M01a.Get_SrcDirInLib()
                FullPath = Path + Default_Prog_Generator_Name
                if Dir(FullPath) == '':
                    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Das Programm \'') + Default_Prog_Generator_Name + '\'' + vbCr + pattgen.M09_Language.Get_Language_Str('existiert nicht im Standard Verzeichnis:') + vbCr + '  \'' + Path + '\'', vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler ') + Default_Prog_Generator_Name + pattgen.M09_Language.Get_Language_Str(' nicht vorhanden'))
                    return _fn_return_value
            Prog_Generator_Name = FullPath
    if M30.Same_Name_already_open(Prog_Generator_Name):
        X02.Workbooks(M30.FileNameExt(Prog_Generator_Name)).Activate()
        if M30.Is_Minimized(M30.FileNameExt(Prog_Generator_Name)) != 0:
            # 31.05.20:
            X02.Application.WindowState = X01.xlNormal
            # In case it was minimized. Unfortunately we don't know the state before
    else:
        X02.Workbooks.Open(FileName=Prog_Generator_Name)
        Prog_Generator_Name = X02.Workbooks(M30.FileNameExt(Prog_Generator_Name)).FullName
        # In case the program was startet the first time from the library and copied to the user directory
    _fn_return_value = Prog_Generator_Name
    return _fn_return_value

def Test_Get_Prog_Generator_Name():
    #UT---------------------------------------
    Debug.Print('Get_Prog_Generator_Name=\'' + Get_Prog_Generator_Name() + '\'')

def Copy_Pattern_Macro_Callback(OK_Pressed, SendToArduino, GoBack):
    Macro_Line = String()

    p = Long()

    MacroTxt = String()

    LEDs = String()

    InCnt = Integer()

    LocInCh = Integer()

    Comment = String()

    Activation_Macro = String()

    Kanaele = Long()

    Startkanal = Long()

    Prog_Gen_Name = String()

    Makro_Name = String()

    Old_Comment = String()

    Comment_Range = X02.Range()
    #----------------------------------------------------------------------------------------------------------
    # This Macro is called when the destination sheet and row in the Prog_Generator workbook is selected
    if not OK_Pressed:
        PG.ThisWorkbook.Activate()
        return
    Debug.Print("Copy_Pattern: %s - %s",PG.ThisWorkbook.Name,PG.ThisWorkbook.ActiveSheet.Name)
    Macro_Line = PG.ThisWorkbook.ActiveSheet.Range('Macro_Range').Value
    p = InStr(Macro_Line, ')')
    if p == 0:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler in Makro Zeile: Klammer zu fehlt'), vbCritical, pattgen.M09_Language.Get_Language_Str('Interner Macro Fehler'))
        return
    p = p + 1
    while Mid(Macro_Line, p, 1) == ' ':
        p = p + 1
    InCnt = 1
    LocInCh = 0
    
    #* HL if not pattgen.M13_Goto_Act.Get_Additional_Goto_Activation_Macro(Activation_Macro, InCnt, LocInCh):
    #* HL    return
    res, Activation_Macro, InCnt, LocInCh = pattgen.M13_Goto_Act.Get_Additional_Goto_Activation_Macro(Activation_Macro, InCnt, LocInCh) #*HL ByRef
    if not res:
        return
        
    # Add macros like InCh_to_TmpVar()
    MacroTxt = Activation_Macro + Replace(Replace(Mid(Macro_Line, p), '(LED,', '(#LED,'), ',InCh,', ',#InCh,')
    Kanaele = int(PG.ThisWorkbook.ActiveSheet.Range('Kanaele'))
    Startkanal = int(PG.ThisWorkbook.ActiveSheet.Range('Startkanal'))
    if Kanaele % 3 == 0 and Startkanal == 0:
        LEDs = int(Kanaele / 3)
    else:
        LEDs = 'C' + str(Startkanal + 1) + '-' + str(Startkanal + Kanaele)
    #Prog_Gen_Name = M30.FileNameExt(Get_Prog_Generator_Name())
    # Read the prior opended file name from the global variable
    Makro_Name = PG.ThisWorkbook.ActiveSheet.Range('Makro_Name') + M01.FROM_PAT_CONFIG_TXT
    #Comment_Range = X02.Run(Prog_Gen_Name + '!Get_Description_Range_from_Act_Row')
    Comment_Range = M50.Get_Description_Range_from_Act_Row()
        
    # Wenn Bereits ein Kommentar vorhanden ist, dieser aber nicht dem Makro namen entspricht und
    # nicht mit "(pc)" endet, dann wird gefragt ob der Kommentar überschrieben werden soll
    if Trim(Comment_Range.Value) != '' and Comment_Range.Value != Makro_Name and Right(Comment_Range.Value, Len(M01.FROM_PAT_CONFIG_TXT)) != M01.FROM_PAT_CONFIG_TXT:
        Comment_Range.Select()
        if vbNo == X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Soll die bestehende Beschreibung durch') + vbCr + '  \'' + Makro_Name + pattgen.M09_Language.Get_Language_Str('\' ersetzt werden?'), vbQuestion + vbYesNo + vbDefaultButton2, pattgen.M09_Language.Get_Language_Str('Bestehende Beschreibung ersetzen?')):
            Makro_Name = ''
    Comment = Makro_Name
    M50.Write_Macro_to_Act_Row(MacroTxt, LEDs, CStr(InCnt), CStr(LocInCh), Comment, False)
    if SendToArduino:
        M06.Create_HeaderFile()
    if GoBack:
        PG.ThisWorkbook.Activate()

def Check_Duration_Row():
    _fn_return_value = None
    #-----------------------------------------------
    # Check if the duration row is filled correcly
    ## VB2PY (CheckDirective) VB directive took path 1 on True
    # 15.01.20:
    if InStr(X02.Range(M01.ErgebnisRng), '!') > 0:
        StartNr = 8
        Parts = Split(X02.Range(M01.ErgebnisRng), ',')
        for Nr in vbForRange(StartNr, UBound(Parts) - 1):
            if Left(Parts(Nr), 1) == '!':
                Col = Nr - StartNr + M01.Dauer_Col1
                X02.Application.ScreenUpdating = True
                X02.Cells(M01.Dauer_Row, Col).Select()
                _select31 = Left(Parts(Nr), 6)
                if (_select31 == '!Error'):
                    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler in der markierten Spalte der Dauer Tabelle!' + vbCr + '  Ungültiger Eintrag: \'') + Replace(Mid(Parts(Nr), Len('!Error') + 2), '/16', '') + '\'' + vbCr + vbCr + pattgen.M09_Language.Get_Language_Str('Folgende Bedingungen müssen erfüllt sein:' + vbCr + ' -Der Eintrag muss kleiner als 17 Minuten sein' + vbCr + ' -Es dürfen nur folgende Einheiten benutzt werden:' + vbCr + '   Min, Sek, Sec, sek, sec, Ms, ms' + vbCr + ' -Zwischen Zahl und Einheit muss ein Leerzeichen stehen'), vbCritical, pattgen.M09_Language.Get_Language_Str('Fehler in \'Dauer\' Tabelle'))
                elif (_select31 == '!Empty'):
                    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: In der Dauer Tabelle dürfen keine Lücken sein' + vbCr + vbCr + 'Es müssen nicht alle Spalten der \'Dauer\' Tabelle ausgefüllt ' + 'werden. Bei Fehlenden Einträgen werden die Zeiten aus dem Anfang der ' + 'Tabelle gelesen.'), vbCritical, pattgen.M09_Language.Get_Language_Str('Lücke in der Dauer Tabelle entdeckt'))
                else:
                    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Unbekannter Fehler in der \'Dauer\' Spalte'), vbCritical, pattgen.M09_Language.Get_Language_Str('Internal Error:'))
    else:
        _fn_return_value = True
    return _fn_return_value

def Check_Table_before_Copy(Send_to_Prog_Gen):
    _fn_return_value = None
    #------------------------------------------------------------------------------
    # Performe some checks before the Pattern function is copied to the Prog_Generator
    pattgen.M06_Goto_Graph.Draw_All_Arrows()
    # redraw and calc Goto_Start_Points
    if pattgen.M06_Goto_Graph.Goto_Start_Points > 1 and Send_to_Prog_Gen:
        # Do we have more than the start point 0 ?
        if Trim(X02.Range('Goto_Aktivierung')) == '':
            # Todo: Translate
            _select32 = X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Wenn der Goto Mode aktiv ist, und mehrere Start Spalten vorhanden sind, dann muss eine Aktivierungsmethode ' + 'angegeben werden sonst können die Einsprung Spalten nicht erreicht werden.' + vbCr + vbCr + 'Soll die Methode jetzt definiert weden?'), vbQuestion + vbYesNoCancel, pattgen.M09_Language.Get_Language_Str('Goto Aktivierung fehlt'))
            if (_select32 == vbYes):
                pattgen.M14_Select_GotoAct.Select_GotoAct(pattgen.M06_Goto_Graph.Goto_Start_Points)
                # Open Select goto dialog
            elif (_select32 == vbCancel):
                return _fn_return_value
    if Trim(X02.Range('Makro_Name')) == '' and Send_to_Prog_Gen:
        X02.Range('Makro_Name').Select()
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Es wurde noch kein Makroname eingegeben ;-('), vbInformation, pattgen.M09_Language.Get_Language_Str('Bitte Makro name eingeben'))
        return _fn_return_value
    # Check if the table is filled
    if X02.Range(M01.TableEmptyMsgRng).Value != '':
        X02.Cells(M01.LEDsTAB_R, M01.LEDsTAB_C).Select()
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Die LED Tabelle ist leer. Bitte die Felder mit einem \'x\' markieren in denen die LEDs leuchten sein sollen'), vbCritical, pattgen.M09_Language.Get_Language_Str('LED Tabelle leer'))
        return _fn_return_value
    # Check if the duration row is filled correcly
    if not Check_Duration_Row():
        return _fn_return_value
    _fn_return_value = True
    return _fn_return_value

def Select_Line_in_Prog_Gen_and_Call_Macro(Get_Dest, Macro_Callback):
    
    X02.activate_workbook("ProgGenerator")

    PG.global_controller.showFramebyName("ProgGeneratorPage")

    M50.Select_Line_for_Patern_Config_and_Call_Macro(Get_Dest, Macro_Callback)  #*HL
    
    return #*HL
    
    Prog_Gen_Name = String()

    Ver = String()
    #-----------------------------------------------------------------------------------------------
    # Select the destination / source row in the Prog_Generator
    # If Get_Dest is true the destintion line which should be used to insert the Macro is requested
    # if Get_Dest is false the source line for importing the macro is requested
    #
    if Get_Dest:
        if False == Check_Table_before_Copy(True):
            return
    Prog_Gen_Name = M30.FileNameExt(Get_Prog_Generator_Name())
    # Make sure that the Prog_Generator workbook is opened
    if Prog_Gen_Name == '':
        return
    # VB2PY (UntranslatedCode) On Error GoTo Wrong_Version
    Ver = X02.Run(Prog_Gen_Name + '!Get_Prog_Version_Nr')
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if not M30.VersionStr_is_Greater(M01.Exp_Prog_Gen_Version, Ver):
        # 14.06.20: Old:  If Ver >= Val(Exp_Prog_Gen_Version) Then
        # The dialog has to be located in the Prog_Generator because otherwise the window is not always shown on top of the screen
        X02.Run(Prog_Gen_Name + '!Select_Line_for_Patern_Config_and_Call_Macro', Get_Dest, PG.ThisWorkbook.Name + '!' + Macro_Callback)
        return
    X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Das Prog_Generator Programm hat nicht die richtige Version.' + vbCr + vbCr + 'Es muss mindesten die Version ') + M01.Exp_Prog_Gen_Version + pattgen.M09_Language.Get_Language_Str(' haben'), vbCritical, pattgen.M09_Language.Get_Language_Str('Falsche Prog_Generator Version'))

def Select_Destination_for_the_Pattern_Macro_and_Call_Copy():
    #------------------------------------------------------------------
    # Select the destination row in the Prog_Generator and copy the pattern macro into this line
    Select_Line_in_Prog_Gen_and_Call_Macro(True, Copy_Pattern_Macro_Callback)

# VB2PY (UntranslatedCode) Option Explicit
