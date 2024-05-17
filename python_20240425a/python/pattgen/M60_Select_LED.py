from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M30_Tools as M30
import pattgen.M55_PWM_Data_Send
import ExcelAPI.XLA_Application as X02
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M09_Language
import proggen.M07_COM_Port as M07
import pattgen.D00_Forms as D00

"""----------------------
-----------------------------------------
 Auswahl der LED Adresse:
 ~~~~~~~~~~~~~~~~~~~~~~~~
 - Charliplexing Signal
   - Blauer Kanal blinkt. Die LED ist aber unter der Platte
     => Problem wenn kein Goto verwendet wird
   - Grüner Kanal wechselt zwischen Goto 0, Goto 1
   - Roter Kanal blinkt auch
 - Sound JQ6500
   - Rot = Sound
   - Blau und Grün sind LEDs
 - Sound MP3-TF-16P
   - Rot & Grün = Sound
   - Blau = LED oder ATTiny
 => Für alle 3 Varianten
    - Blau Blinken
    - Grün Wechsel zwischen
--------------------------------------------------------------
--------------------------
-----------------------------------------------
-----------------------------------------------------
----------------------------------
UT----------------------------------------------------
"""

Next_Fash_LED_Time = Double()
LED_Flash_PortId = Integer()
LED_Flash_Pattern = vbObjectInitialize(objtype=String)
LED_Flash_Cnt = Integer()
Act_LED_Pattern = Integer()
LED_Flash_Nr = Integer()
LED_Flash_Act = Boolean()

def Flash_LED():
    global Act_LED_Pattern, Next_Fash_LED_Time
    #----------------------
    if LED_Flash_Act:
        Cmd = '#L' + M30.Hex02(LED_Flash_Nr) + LED_Flash_Pattern(Act_LED_Pattern)
        Debug.Print('Flash_LED ' + LED_Flash_Nr + '  ' + Cmd)
        if LED_Flash_PortId > 0:
            if not pattgen.M55_PWM_Data_Send.Write_Com(LED_Flash_PortId, Cmd):
                return
        Act_LED_Pattern = Act_LED_Pattern + 1
        if Act_LED_Pattern >= LED_Flash_Cnt:
            Act_LED_Pattern = 0
        Next_Fash_LED_Time = X02.Now + TimeSerial(0, 0, 1)
        # It's not possible to use a smaller calling period than 1 sec. with excel ;-(
        # Here is a dscription how to ude windows calls, but this seames to be critical:
        #  http://www.cpearson.com/excel/OnTime.aspx
        X02.Application.OnTime(Next_Fash_LED_Time, 'Flash_LED')

def Set_Flash_LED(LedNr):
    global Act_LED_Pattern, LED_Flash_Nr
    Old_LED = Integer()

    Cmd = String()
    #-----------------------------------------
    X02.Application.EnableEvents = False
    Old_LED = LED_Flash_Nr
    Act_LED_Pattern = 0
    LED_Flash_Nr = LedNr
    X02.Application.EnableEvents = True
    if LED_Flash_Act and LED_Flash_PortId > 0:
        Cmd = '#L' + M30.Hex02(Old_LED) + ' 00 00 00 01' + vbLf
        # Disable the OLD LED
        pattgen.M55_PWM_Data_Send.Write_Com(LED_Flash_PortId, Cmd)
        X03.Sleep(20)
    Cmd = '#L' + M30.Hex02(LED_Flash_Nr) + LED_Flash_Pattern(0)
    if LED_Flash_PortId > 0:
        if not pattgen.M55_PWM_Data_Send.Write_Com(LED_Flash_PortId, Cmd):
            return
        X03.Sleep(20)

def Start_Flash_LED(PortId, LedNr):
    global LED_Flash_PortId, LED_Flash_Nr, LED_Flash_Act, Act_LED_Pattern, LED_Flash_Cnt, LED_Flash_Pattern
    #--------------------------------------------------------------
    if not LED_Flash_Act:
        LED_Flash_PortId = PortId
        LED_Flash_Nr = LedNr
        LED_Flash_Act = True
        Act_LED_Pattern = 0
        if LED_Flash_Cnt == 0:
            LED_Flash_Cnt = 2
            LED_Flash_Pattern = vbObjectInitialize((LED_Flash_Cnt,), Variant)
            #         Red                            Green                    Blue Cnt
            LED_Flash_Pattern[0] = ' ' + M30.Hex02(pattgen.M55_PWM_Data_Send.Get_Goto_pwm(0)) + ' ' + M30.Hex02(pattgen.M55_PWM_Data_Send.Get_Goto_pwm(1)) + ' FF 01' + vbLf
            # 30.01.20: Red LED is also flashing
            LED_Flash_Pattern[1] = ' ' + M30.Hex02(pattgen.M55_PWM_Data_Send.Get_Goto_pwm(1)) + ' ' + M30.Hex02(pattgen.M55_PWM_Data_Send.Get_Goto_pwm(0)) + ' 00 01' + vbLf
            #   "
        X02.Application.OnTime(X02.Now, 'Flash_LED')

def Stop_Flash_LED():
    global LED_Flash_Act
    #--------------------------
    if LED_Flash_Act:
        LED_Flash_Act = False
        # VB2PY (UntranslatedCode) On Error Resume Next
        # In case the OnTime function is not running
        X02.Application.OnTime(Next_Fash_LED_Time, 'Flash_LED', Schedule=False)
        # VB2PY (UntranslatedCode) On Error GoTo 0
        X03.Sleep(100)
        Debug.Print('Stop_Flash_LED ' + LED_Flash_Nr)
        if LED_Flash_PortId > 0:
            # Turn the LED off
            Cmd = '#L' + M30.Hex02(LED_Flash_Nr) + ' 00 00 00 01' + vbLf
            pattgen.M55_PWM_Data_Send.Write_Com(LED_Flash_PortId, Cmd)
            X03.Sleep(20)

def Select_Special_Mode():
    _fn_return_value = None
    Res = String()
    #-----------------------------------------------
    Res = D00.Select_from_Sheet_Form.Show_Form(M01.SPECIAL_MODEDLG_SH, pattgen.M09_Language.Get_Language_Str('Auswahl der Spezial Modes'), pattgen.M09_Language.Get_Language_Str('Spezial Mode'), pattgen.M09_Language.Get_Language_Str('Mit dem Pattern_Configurator können spezielle Module konfiguriert werden.' + vbCr + 'Die Muster werden in diesem Fall direkt zu dem entsprechenden Modul geschickt. Dort wird die Konfiguration dann autark abgearbeitet.'), oDialog_Dat_ROW1= X02.Sheets(M01.SPECIAL_MODEDLG_SH).Range('Special_Mode_Head').Row + 1, oMiddleWinCOL= 6)
    if Res != '':
        X02.RangeDict['Special_Mode'].Value = Split(Res, ',')(0)
        _fn_return_value = True
    return _fn_return_value

def Select_LED_Address_Dialog():
    _fn_return_value = None
    PortId = Integer()
    #-----------------------------------------------------
    _fn_return_value = - 1
    PortId = M07.Get_USB_Port_with_Dialog()
    if PortId > 0:
        LastLEDNr = pattgen.M55_PWM_Data_Send.Open_Port_With_Error_Msg_and_get_LastLED(PortId)
        if LastLEDNr <= 0:
            return _fn_return_value
        _fn_return_value = Select_LED_Address.ShowForm(PortId, LastLEDNr - 1)
        Debug.Print('Select_LED_Address_Dialog = ' + Select_LED_Address_Dialog())
        # Debug
    pattgen.M55_PWM_Data_Send.End_Test_and_Close(PortId)
    return _fn_return_value

def Get_LED_Address_Dialog():
    Res = Integer()
    #----------------------------------
    Res = Select_LED_Address_Dialog()
    if Res >= 0:
        X02.RangeDict['RGB_Modul_Nr'] = Res

def Test_Without_LED_Write_Select_LED_Address():
    #UT----------------------------------------------------
    Debug.Print(Select_LED_Address.ShowForm(0, 10))

# VB2PY (UntranslatedCode) Option Explicit
