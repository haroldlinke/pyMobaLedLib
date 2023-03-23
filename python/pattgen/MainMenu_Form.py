from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M09_Language as M09
import pattgen.M08_Load_Sheet_Data
import pattgen.M07_Save_Sheet_Data
import pattgen.M30_Tools as M30
import pattgen.M65_Special_Modules
import pattgen.M80_Multiplexer_INI_Handling
import pattgen.Pattern_Generator as PG



import ExcelAPI.XLF_FormGenerator as XLF
import pattgen.D00_Forms as D00

import logging



def CloseButton_Click():
    #------------------------------
    D00.MainMenu_Form.Hide()
    # To keep the last position of the dialog

def Close2Button_Click():
    #-------------------------------
    # Tab: "Spezielle Module"
    CloseButton_Click()

def DeleteActualPageButton_Click():
    Sh = Variant()
    #-----------------------------------------
    X02.Application.Calculation = X01.xlCalculationManual
    for Sh in [X02.ActiveSheet]: #*HL   X02.ActiveWindow.SelectedSheets:
        _with32 = Sh
        if _with32.Name != M01.MAIN_SH:
            X02.Application.DisplayAlerts = False
            X02.Sheets(_with32.Name).Delete()
            # Aus irgend einem Grund wird hier auch das Main Menü geschlossen ;-(
            X02.Application.DisplayAlerts = True
        else:
            #if X02.ActiveWindow.SelectedSheets.Count == 1:
            X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Das Sheet \'Main\' kann nicht gelöscht werden'), vbCritical, pattgen.M09_Language.Get_Language_Str('Error'))
    X02.Application.Calculation = X01.xlCalculationAutomatic

def DeleteAlleExamplesButton_Click():
    #-------------------------------------------
    pattgen.M08_Load_Sheet_Data.Del_All_Sheets_Excep_Main()
    #Debug.Print "End DeleteAlleExamplesButton_Click()"
    # Debug
    PG.ThisWorkbook.Sheets(M01.MAIN_SH).Select()
    #D00.MainMenu_Form.Show()

def HelpButton_Click():
    #-----------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    X02.Shell('Explorer https://wiki.mobaledlib.de/anleitungen/spezial/patterngenerator')

def LinkGitHub_Click():
    #-----------------------------
    X02.ActiveWorkbook.FollowHyperlink('https://github.com/Hardi-St/MobaLedLib')

def LinkStummi_Click():
    #-----------------------------
    X02.ActiveWorkbook.FollowHyperlink('https://www.stummiforum.de/viewtopic.php?t=165060')

def LoadAllExamlesButton_Click():
    #---------------------------------------
    pattgen.M08_Load_Sheet_Data.Load_AllExamples_Sheets()

def LoadExampleButton_Click():
    Res = Variant()
    #------------------------------------
    if M01.ExampleName == '':
        M01.ExampleName = pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() + '\\TestExample.MLL_pcf'
    # VB2PY (UntranslatedCode) On Error Resume Next
    X02.ChDrive(( M01.ExampleName ))
    ChDir(( M30.FilePath(M01.ExampleName) ))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Res = X02.Application.GetOpenFilename(fileFilter= pattgen.M09_Language.Get_Language_Str('Pattern configurator example (*.MLL_pcf), *.MLL_pcf'), Title= pattgen.M09_Language.Get_Language_Str('Load Examples'))
    if Res != "":
        D00.StatusMsg_UserForm.Show()
        # 12.01.20:
        M01.ExampleName = Res
        X02.Application.Calculation = X01.xlCalculationAutomatic
        # In case the previous macro was aborted
        pattgen.M08_Load_Sheet_Data.Load_Sheets(M01.ExampleName, '')
        X02.Unload(D00.StatusMsg_UserForm)
        # 12.01.20:
        X02.Application.Calculation = X01.xlCalculationAutomatic

def Prog_ServoMP3_Button_Click():
    pattgen.M65_Special_Modules.Prog_ServoMP3()

def SaveActualExampleButton_Click():
    Names="" #*HL
    Res = Variant()
    AppendSheet=False
    #------------------------------------------
    X02.Application.Calculation = X01.xlCalculationManual
    if M01.SaveDirCreated == False:
        ChDir(( pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() ))
        M01.SaveDirCreated = True
    #if X02.ActiveWindow.SelectedSheets.Count == 1: #HL
    M01.ExampleName = pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() + '\\' + X02.ActiveSheet.Name + '_Example'
        # 03.02.20: Removed ".MLL_pcf" because otherwise the filename is not shown in the following dialog
    if M01.ExampleName == '':
        M01.ExampleName = pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() + '\\TestExample'
        #03.02.20: Removed ".MLL_pcf"
    # VB2PY (UntranslatedCode) On Error Resume Next
    X02.ChDrive(( M01.ExampleName ))
    ChDir(( M30.FilePath(M01.ExampleName) ))
    # VB2PY (UntranslatedCode) On Error GoTo 0
    Res = X02.Application.GetSaveAsFilename(M01.ExampleName, fileFilter= pattgen.M09_Language.Get_Language_Str('Pattern configurator example (*.MLL_pcf), *.MLL_pcf'), Title= pattgen.M09_Language.Get_Language_Str('Save examples'))
    # Old:
    if Res != "": #*HL False:
        M01.ExampleName = Res
        #for Sh in X02.ActiveWindow.SelectedSheets: #HL
        _with33 = X02.ActiveSheet #Sh
        _with33.Activate()
        _with33.Select()
        # Select only one sheet (if several sheets have been selected for saving)
        pattgen.M07_Save_Sheet_Data.Save_One_Sheet(X02.ActiveSheet, M01.ExampleName, AppendSheet)
        Names = Names + _with33.Name + ', '
        AppendSheet = True
        #For end
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Die folgenden Beispiel Seite(n) wurden gespeichert:') + vbCr + '  ' + Left(Names, Len(Names) - 2), vbInformation, pattgen.M09_Language.Get_Language_Str('Beispiel wurde erfolgreich gespeichert'))
    X02.Application.Calculation = X01.xlCalculationAutomatic

def SaveAllExamplesButton_Click():
    #----------------------------------------
    D00.StatusMsg_UserForm.Set_Label(pattgen.M09_Language.Get_Language_Str('Speicher alle Beispiele' + vbLf + 'Bitte etwas Geduld...'))
    D00.StatusMsg_UserForm.Show()
    pattgen.M07_Save_Sheet_Data.Save_All_Sheets_to(pattgen.M07_Save_Sheet_Data.Get_MyExampleDir() + '\\MyExamples.MLL_pcf')
    X02.Unload(D00.StatusMsg_UserForm)

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ":MainMenu_Form Initialize"
    MultiPage1.Value = 0
    # Select the first page
    MultiPage2.Value = 0
    #*HLX02.Center_Form(Me)
    M09.Change_Language_in_Dialog(D00.MainMenu_Form)

def Prog_ISP_Button_Click():
    #----------------------------------
    pattgen.M65_Special_Modules.Prog_Tiny_UniProg()

def Prog_Charlieplex_Button_Click():
    #------------------------------------------
    pattgen.M65_Special_Modules.Prog_Charlieplex()

def Prog_Servo_Button_Click():
    #------------------------------------
    #If GetAsyncKeyState(VK_CONTROL) <> 0 Then
    # 15.04.20: Disabled
    pattgen.M65_Special_Modules.Prog_Servo()
    #'# VB2PY (CheckDirective) VB2PY directive Ignore Text
    #End If

def Close3Button_Click():
    # 02.06.20: Misha
    #-------------------------------
    # Tab: "Extras"
    CloseButton_Click()

def Multiplexer_Editor_Click():
    # 02.06.20: Misha
    #-------------------------------------
    Debug.Print('Multiplexer_Editor_Click')
    X02.Sheets['Multiplexer'].Visible = True
    X02.Worksheets('Multiplexer').Select()
    CloseButton_Click
    D00.StatusMsg_UserForm.Show()
    D00.StatusMsg_UserForm.Set_Label(pattgen.M09_Language.Get_Language_Str('Lade Multiplexer...'))
    D00.StatusMsg_UserForm.Set_ActSheet_Label('          ')
    # Left border for the dot's (Depends on the number of expexted dots)
    pattgen.M80_Multiplexer_INI_Handling.Load_Multiplexer
    X02.Unload(D00.StatusMsg_UserForm)

#################################################################################################
    
Main_Menu_Form_RSC = {"UserForm":{
                        "Name"          : "MainMenuForm",
                        "BackColor"     : "#000008",
                        "BorderColor"   : "#000012",
                        "Caption"       : "Pattern Configurator",
                        "Height"        : 413.25,
                        "Left"          : 0,
                        "Top"           : 0,
                        "Type"          : "MainWindow",
                        "Visible"       : True,
                        "Width"         : 395.25,
                        "Components"    : [{"Name":"Multipage1","Height": 372,"Left": 6,"Top": 6,"Type": "MultiPage","Visible": True,"Width": 372,                            
                            "Components": [{"Name":"Page1","Caption":"Beispiele","Type": "Page","Visible": True,
                                "Components":[{"Name":"Label3","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Achtung:Bei den Schaltern wurde bewusst auf die 'Sind sie sicher...' Abfragen verzichtet. Wenn ein Knopf gedrückt wird,dann löst er die entsprechende Aktion sofort aus.",
                                                "ControlTipText":"Tooltip1","ForeColor":"#000012","Height":30,"Left":6,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":300},
                                              {"Name":"Label2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"by Hardi",
                                               "ControlTipText":"Tooltip2","ForeColor":"#FF0000","Height":12,"Left":318,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":36},
                                              {"Name":"CloseButton","Accelerator":"d","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Dialog schließen",
                                               "Command":CloseButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":282,"Top":312,"Type":"CommandButton","Visible":True,"Width":72},
                                              {"Name":"HelpButton","Accelerator":"h","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Hilfe",
                                               "Command":HelpButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":204,"Top":312,"Type":"CommandButton","Visible":True,"Width":72},
                                              {"Name":"Frame1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Laden",
                                               "ControlTipText":"","ForeColor":"#000012","Height":84,"Left":6,"SpecialEffect":"fmSpecialEffectEtched","Top":42,"Type":"Frame","Visible":True,"Width":348,
                                               "Components":[{"Name":"Label1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Lädt ausgewählte Standard Beispiele aus Verzeichnis'Pattern_Config_Examples'.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":204},
                                                             {"Name":"Label5","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Öffnet einen Auswahldialog mit dem eine TextDatei mit einem oder mehreren Pattern geladen wird.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":30,"Left":132,"TextAlign":"fmTextAlignLeft","Top":42,"Type":"Label","Visible":True,"Width":210},
                                                             {"Name":"LoadAllExamplesButton","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Lade Beispiele",
                                                              "Command":LoadAllExamlesButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":6,"Type":"CommandButton","Visible":True,"Width":114},
                                                             {"Name":"LoadExampleButton","Accelerator":"B","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Eigene Daten laden",
                                                              "Command":LoadExampleButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":42,"Type":"CommandButton","Visible":True,"Width":114}]
                                               },
                                              {"Name":"Frame2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Speichern",
                                               "ControlTipText":"","ForeColor":"#000012","Height":84,"Left":6,"SpecialEffect":"fmSpecialEffectEtched","Top":132,"Type":"Frame","Visible":True,"Width":348,
                                               "Components":[{"Name":"Label4","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Speichert alle Patternseiten in der Datei\n'MyExamples.MLL_pcf' im Verzeichnis\n'EigeneDokumente\MyPattern_Config_Examples'.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":204},
                                                             {"Name":"Label6","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Speichert die aktuelle, oder alle ausgewählten Seiten in einer Datei.(Mit Strg+Klick auf den Seiten namen können mehrere Seiten ausgewählt werden.)",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":30,"Left":132,"TextAlign":"fmTextAlignLeft","Top":42,"Type":"Label","Visible":True,"Width":210},
                                                             {"Name":"SaveAllExamplesButton","Accelerator":"s","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Alle Seiten speichern",
                                                              "Command":SaveAllExamplesButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":6,"Type":"CommandButton","Visible":True,"Width":114},
                                                             {"Name":"SaveActualExampleButton","Accelerator":"p","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Aktuelle Seite(n) speichern",
                                                              "Command":SaveActualExampleButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":42,"Type":"CommandButton","Visible":True,"Width":114}
                                                             ]},
                                              {"Name":"Frame3","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Löschen",
                                               "ControlTipText":"","ForeColor":"#000012","Height":84,"Left":6,"SpecialEffect":"fmSpecialEffectEtched","Top":222,"Type":"Frame","Visible":True,"Width":348,
                                               "Components":[{"Name":"Label7","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Löscht ALLE Datenseiten.",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":36,"Left":132,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":204},
                                                             {"Name":"Label8","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Löscht die aktuelle, oder alle ausgewählten Seiten.\n(Mehrere Seiten können mit Strg+Klick auf den Seitennamen ausgewählt werden.)",
                                                              "ControlTipText":"","ForeColor":"#000012","Height":30,"Left":132,"TextAlign":"fmTextAlignLeft","Top":42,"Type":"Label","Visible":True,"Width":210},
                                                             {"Name":"DeleteAlleExamplesButton","Accelerator":"l","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Alle Datenseiten löschen",
                                                              "Command":DeleteAlleExamplesButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":6,"Type":"CommandButton","Visible":True,"Width":114},
                                                             {"Name":"SaveActualExampleButton","Accelerator":"ö","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                              "Caption":"Aktuelle Seite(n) löschen",
                                                              "Command":DeleteActualPageButton_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":6,"Top":42,"Type":"CommandButton","Visible":True,"Width":114}
                                                             ]}
                                              ]},
                                           {"Name": "Page2",
                                            "Caption": "Spezielle Module",
                                            "Type": "Page","Visible": True,
                                            "Components"    : [{"Name":"Label9","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption"       : "Diese Seite enthält Funktionen mit denen spezielle, auf dem ATTiny basierte Module programmiert und getestet werden können.",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 30,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 300},
                                                               {"Name": "Label10","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                "Caption": "by Hardi",
                                                                "ControlTipText": "","ForeColor": "#FF0000","Height": 12,"Left": 318,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 36},
                                                               {"Name": "Close2Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
                                                                "Caption": "Dialog schließen",
                                                                "Command": Close2Button_Click,"ControlTipText": "","ForeColor": "#000012","Height": 25,"Left": 282,"Top": 312,"Type": "CommandButton","Visible": True,"Width": 72},
                                                               {"Name": "Frame4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                "Caption"       : "Programmieradapter",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 114,"Left": 6,"Top": 42,"Type": "Frame","Visible": True,"Width": 354,
                                                                "Components"    : [{"Name": "Label11","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Ein ATTiny hat keinen USB Anschluss. Darum benötigt man zur Programmierung einen Programmieradapter (In Circuit Programmer). Das kann ein Arduino mit besonderen Programm sein. Mit dem Knopf Links wird das Programm zu Arduino übertragen.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 48,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 264},
                                                                                   {"Name": "Label13","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Dieses Programm kann auf dem Tiny_UniProg und auf einen 'Nackten' Arduino in einem Steckbrett eingesetzt werden.\nDer 'HV Reset' ist allerdings nur mit der 'Tiny_UniProg' Platine möglich. Er wird für das Programmieren des Servo Programms benötigt.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 60,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 54,"Type": "Label","Visible": True,"Width": 342},
                                                                                   {"Name": "Prog_ISP_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Prog. ISP",
                                                                                    "Command": Prog_ISP_Button_Click,"ControlTipText": "","ForeColor": "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72
                                                                                    }]
                                                                },
                                                               {"Name": "MultiPage2","BackColor": "#00000F","ControlTipText": "","ForeColor": "#000012","Height": 150,"Left": 6,"Top": 162,"Type": "MultiPage","Visible": True,"Width": 354,
                                                                   "Components": [{"Name":"Page3",
                                                                                   "Caption":"Charlieplexing",
                                                                                   "Type": "Page","Visible": True,
                                                                                   "Components": [{"Name": "Label12","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                                   "Caption": "Mit dem Charlieplexing Modul können bis zu 12 LEDs über nur 4 Kabel angesteuert werden. Diese Technik wird z.B. bei Lichtsignalen oder Ampeln eingesetzt wo nur wenig Platz für die Anschlussleitungen vorhanden ist.\nZur Programmierung des ATTiny85 wird ein Programmieradapter benötigt (siehe oben) in der der ATTiny eingesteckt wird.",
                                                                                                   "ControlTipText": "","ForeColor": "#000012","Height": 66,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "Label","Visible": True,"Width": 264},
                                                                                                  {"Name": "Prog_Charlieplex_Button","Accelerator":"","BackColor": "#00000F","BorderColor"   : "#000006","BorderStyle"   : "fmBorderStyleNone",
                                                                                                   "Caption" : "Prog. Charlieplex",
                                                                                                   "Command" : Prog_Charlieplex_Button_Click,"ControlTipText": "","ForeColor": "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72}
                                                                                                  ]},
                                                                                  {"Name": "Page4",
                                                                                   "Caption":"Servo",
                                                                                   "Type": "Page","Visible": True,
                                                                                   "Components"    : [{"Name": "Label4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
                                                                                                       "Caption": "Das Servo Modul kann bis zu 3 Servos ansteuern.\n\nZur Programmierung des ATTiny85 wird ein Programmieradapter benötigt (siehe oben) in der der ATTiny eingesteckt wird.\n\nAchtung: Die Software für das Servo Modul ist noch in der Entwicklung.",
                                                                                                       "ControlTipText": "","ForeColor": "#000012", "Height": 96,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "Label","Visible": True,"Width": 264},
                                                                                                      {"Name": "Prog_Servo_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                                       "Caption": "Prog. Servo",
                                                                                                       "Command": Prog_Servo_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72}
                                                                                                      ]},
                                                                                  {"Name": "Page5",
                                                                                   "Caption":"Servo-MP3",
                                                                                   "Type": "Page","Visible": True,
                                                                                   "Components"    : [{"Name": "Label34","BackColor": "#00000F","BorderColor": "#000006","BorderStyle"   : "fmBorderStyleNone",
                                                                                                       "Caption": "Man das Servo-Modul auf zur Ansteuerung von Soundmodulen nutzen (JQ6500/MP3-TF-16p) nutzen.\n\nDabei werden die Soundmodule mit je einem 1k Widerstand an die Signal-Pins der Servoausgänge angeschlossen. Zusätzlich ist die Masse zu verbinden. Die Stromversorgung kann man getrennt lösen - meist funktioniert es aber auch die 5V von den Servoanschlüssen zu nutzen.\n\nZur Programmierung des ATTiny85 wird ein Programmieradapter benötigt (siehe oben) in der der ATTiny eingesteckt wird.\n\nAchtung: Die Software für das Servo Modul ist noch in der Entwicklung.",
                                                                                                       "ControlTipText": "","ForeColor": "#000012", "Height": 120,"Left": 84,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 264},
                                                                                                      {"Name": "Prog_ServoMP3_Button","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                                       "Caption": "Prog.Servo/MP3",
                                                                                                       "Command": Prog_ServoMP3_Button_Click,"ControlTipText": "","ForeColor" : "#000012","Height": 25,"Left": 6,"Top": 12,"Type": "CommandButton","Visible": True,"Width": 72},
                                                                                                      ]}
                                                                                  ]}
                                                               ]},
                                           {"Name": "Page3",
                                            "Caption": "Extras",
                                            "Type": "Page","Visible": True,
                                            "Components"    : [{"Name":"Label31","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                "Caption"       : "Diese Seite enthält zusätzliche Programme, die die Arbeit mit der MobaLedLib unterstützen.",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 30,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 246},
                                                               {"Name": "Frame9","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                "Caption"       : "Pattern Multiplexer",
                                                                "ControlTipText": "","ForeColor": "#000012","Height": 120,"Left": 6,"Top": 36,"Type": "Frame","Visible": True,"Width": 354,
                                                                "Components"    : [{"Name":"Label32","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                                                    "Caption" : "Mit dem Mustermultiplexer können Sie mehrere Muster kombinieren und in beliebiger Kombination verwenden. Mit dem Multiplexer-Editor können Multiplexer erstellt und die gewünschten Muster ausgewählt und eingefügt werden.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 48,"Left": 102,"TextAlign": "fmTextAlignLeft","Top": 6,"Type": "Label","Visible": True,"Width": 246}, 
                                                                                   {"Name": "Label33","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Die erstellten Multiplexer können einfach über einen MLL-Makro im Programmgenerator ausgewählt und eingestellt werden. Mit einer Option im Makro können die Multiplexer auch einfach mehrfach multipliziert werden. Infolgedessen sind weniger Einstellungen für ein sich wiederholendes Muster erforderlich.",
                                                                                    "ControlTipText": "","ForeColor": "#000012","Height": 60,"Left": 6,"Top": 54,"Type": "Label","Visible": True,"Width": 342},
                                                                                   {"Name": "Multiplexer_Editor","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                                                                    "Caption": "Multiplexer Editor",
                                                                                    "Command": Multiplexer_Editor_Click,"ControlTipText": "","ForeColor": "#000012","Height": 25,"Left": 6,"TextAlign": "fmTextAlignLeft","Top": 12,"Type": "CommandButton","Visible": True,"Width": 84
                                                                                    }]
                                                                },
                                                               ]
                                            }]
                            }]
                        }}
"""
    
class dict2obj(dict):
    def __init__(self, dict_):
        super(dict2obj, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for idx, it in enumerate(item):
                    if isinstance(it, dict):
                        item[idx] = dict2obj(it)
            elif isinstance(item, dict):
                self[key] = dict2obj(item)

    def __getattr__(self, key):
        return self[key]
"""    

    
class CMainMenu_Form:
    
    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        #*HL Center_Form(Me)
    
    def __UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Form=XLF.generate_form(Main_Menu_Form_RSC,self.controller,dlg=self)
                
    def __UserForm_Activate(self):
        #------------------------------
        # Is called every time when the form is shown
        #M25.Make_sure_that_Col_Variables_match()
        pass
        
    def Hide(self):
        self.IsActive=False
        self.Form.destroy()
        
    def AddControl(self,control):
        self.Controls.append(control)
        self.Controls_Dict[control.Name]=control
        
    def Show_Dialog(self):
        self.Show()
        
    def Show(self):
        self.IsActive = True
        self.__UserForm_Initialize()
        self.__UserForm_Activate()
        self.controller.wait_window(self.Form)
        
    
    # VB2PY (UntranslatedCode) Option Explicit

