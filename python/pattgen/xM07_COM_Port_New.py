from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M07_COM_Port
import ExcelAPI.XLW_Workbook as X02
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M09_Language
import ExcelAPI.XLWA_WinAPI as X03
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M30_Tools as M30
import pattgen.M02_Public as M02
import pgcommon.G00_common as G00
import pattgen.D00_Forms as D00

""" Select the Arduino COM Port
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Uses the Modules
 - M07_COM_Port
 - Select_COM_Port_UserForm
------------------------------
--------------------------------------------------------------------------------------
UT-----------------------------------------------------
---------------------------------------------------------------------------------------------
----------------------------------------------------------------
UT-------------------------------
--------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

PRINT_DEBUG = False
CheckCOMPort = Long()
CheckCOMPort_Txt = String()
CheckCOMPort_Res = Long()

def Blink_Arduino_LED():
    global CheckCOMPort_Res
    SWMajorVersion = Byte()

    SWMinorVersion = Byte()

    HWVersion = Byte()

    DeviceSignatur = Long()

    BaudRate = Long()
    # 02.05.20:
    #------------------------------
    # Is called by OnTime and flashes the LEDs of the Arduino connected to
    # the port stored in the global variable "CheckCOMPort"
    # It's aborted if CheckCOMPort = 0
    # Attention: This function doesn't check if the connected device is an Arduino
    # because this would be to slow. In addition the blinking frequence is more visible if
    # A baudrate of 50 is used.
    BaudRate = 50
    # Using a wrong slow baudrate to get nice flashing LEDs
    #if CheckCOMPort > 0:
    #    D00.Select_COM_Port_UserForm.Update_SpinButton(0)
    #    # Rescan COM Ports
    #    if CheckCOMPort != 999:
    #        CheckCOMPort_Res = pattgen.M07_COM_Port.DetectArduino(CheckCOMPort, Baudrate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur, 1, PrintDebug= PRINT_DEBUG)
    #    else:
    #        CheckCOMPort_Res = - 9
            
    if G00.port_is_available(CheckCOMPort):    
        Debug.Print("Blink_LED start")
        D00.Select_COM_Port_UserForm.Update_SpinButton(0)
        #if M07.CheckCOMPort != 999:
        if CheckCOMPort != "999":
            CheckCOMPort_Res, DeviceSignatur = pattgen.M07_COM_Port.DetectArduino(CheckCOMPort, BaudRate, HWVersion, SWMajorVersion, SWMinorVersion, DeviceSignatur, 1, PrintDebug= PRINT_DEBUG)
        else:
            CheckCOMPort_Res = - 9
        X02.Application.Cursor = X01.xlNorthwestArrow
        #Debug.Print "CheckCOMPort_Res=" & CheckCOMPort_Res & "  CheckCOMPort=" & CheckCOMPort
        if CheckCOMPort_Res < 0:
            if CheckCOMPort == 999:
                D00.Select_COM_Port_UserForm.Show_Status(True, pattgen.M09_Language.Get_Language_Str('Kein COM Port erkannt.' + vbCr + 'Bitte Arduino an einen USB Anschluss des Computers anschließen'))
            else:
                D00.Select_COM_Port_UserForm.Show_Status(True, pattgen.M09_Language.Get_Language_Str('Achtung: Der Arduino wird von einem anderen Programm benutzt.' + vbCr + '(Serieller Monitor?)' + vbCr + 'Das Programm muss geschlossen werden! '))
        else:
            D00.Select_COM_Port_UserForm.Show_Status(False, CheckCOMPort_Txt)
            # CheckCOMPort_Res >= 0
        X03.Sleep(10)
        X02.DoEvents()
        # To be able to abort with Ctrl+Break
        #X02.Application.OnTime(X02.Now + X02.TimeValue('00:00:00'), 'Blink_Arduino_LED')
        X02.Application.OnTime(1000, Blink_Arduino_LED)
        # Restart it again

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort_IO - ByRef 
def Select_Arduino_w_Blinking_LEDs_Dialog(Caption, Title, Text, Picture, Buttons, ComPort_IO):
    global CheckCOMPort
    _fn_return_value = None
    Res = Long()
    # 02.05.20:
    #--------------------------------------------------------------------------------------
    # This function is called if several Arduinos have been detected
    # or if the COM port of the actual Arduino is buzy
    # Variables:
    #  Caption     Dialog Caption
    #  Title       Dialog Title
    #  Text        Message in the text box on the top left side
    #  Picture     Name of the picture to be shown. Available pictures: "LED_Image", "CAN_Image", "Tiny_Image", "DCC_Image"
    #  Buttons     List of 3 buttons with Accelerator. Example "H Hallo; A Abort; O Ok"  Two Buttons: " ; A Abort; "O Ok"
    #  ComPort_IO  is used as input and output. Negativ numbe if it's buzy (Used by an other program)
    # Return:
    #  1: If the left   Button is pressed  (Install, ...)
    #  2: If the middle Button is pressed  (Abort)
    #  3: If the right  Button is pressed  (OK)
    CheckCOMPort = 999
    # Prevent stopping the Blink_Arduino_LED() function. It's Updated in the dialog
    #X02.Application.OnTime(X02.Now + X02.TimeValue('00:00:00'), 'Blink_Arduino_LED')
    X02.Application.OnTime(1000, Blink_Arduino_LED)
    # Return values of Select_COM_Port_UserForm.ShowDialog:
    #  -1: If Abort is pressed
    #   0: If No COM Port is available
    #  >0: Selected COM Port
    # The variable "CheckCOMPort_Res" is >= 0 if the Port is available
    _fn_return_value = D00.Select_COM_Port_UserForm.ShowDialog(Caption, Title, Text, Picture, Buttons, '', True, pattgen.M09_Language.Get_Language_Str('Tipp: Der ausgewählte Arduino blinkt schnell'), ComPort_IO, PRINT_DEBUG)
    if CheckCOMPort_Res < 0:
        ComPort_IO = G00.port_set_busy(ComPort_IO) #ComPort_IO = - ComPort_IO
    # Port is buzy
    X02.Application.Cursor = X01.xlDefault
    return _fn_return_value, ComPort_IO

def Test_Select_Arduino_w_Blinking_LEDs_Dialog():
    ComPort = Long()
    #UT-----------------------------------------------------
    ComPort = 3
    Debug.Print('Res=' + Select_Arduino_w_Blinking_LEDs_Dialog('LED_Image"Auswahl des Arduinos', 'New Title', 'Mit diesem Dialog wird der COM Port gewählt an den der Arduino angeschlossen ist.', 'LED_Image', 'H Hallo;T Test;O O', ComPort))
    Debug.Print('ComPort=' + ComPort)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort - ByRef 
def Show_USB_Port_Dialog(ComPortColumn, ComPort):
    _fn_return_value = False
    Res = Long()

    Picture = String()

    ArduName = String()
    #---------------------------------------------------------------------------------------------
    ComPort = X02.Cells(M01.SH_VARS_ROW, ComPortColumn)
    if G00.port_is_busy(ComPort):
        G00.port_reset(ComPort)    
    #if ComPort < 0:
    #    ComPort = - ComPort
    _select67 = ComPortColumn
    if (_select67 == M01.COMPort_COL):
        Picture = 'LED_Image'
        ArduName = 'LED'
    elif (_select67 == M01.COMPrtR_COL):
        Picture = 'DCC_Image'
        ArduName = M01.Page_ID
    elif (_select67 == M01.COMPrtT_COL):
        Picture = 'Tiny_Image'
        ArduName = 'ISP'
    else:
        X02.MsgBox('Internal Error: Unsupported  ComPortColumn=' + ComPortColumn + ' in \'USB_Port_Dialog()\'', vbCritical, 'Internal Error')
        M30.EndProg()
    Res, Comport = Select_Arduino_w_Blinking_LEDs_Dialog(pattgen.M09_Language.Get_Language_Str('Überprüfung des USB Ports'), pattgen.M09_Language.Get_Language_Str('Auswahl des Ardiono COM Ports'), Replace(pattgen.M09_Language.Get_Language_Str('Mit diesem Dialog wird der COM Port überprüft ' + 'bzw. ausgewählt an den der #1# Arduino angeschlossen ist.' + vbCr + vbCr + 'OK, wenn die LEDs am richtigen Arduino schnell blinken.'), '#1#', ArduName), Picture, pattgen.M09_Language.Get_Language_Str(' ; A Abbruch; O Ok'), ComPort)
    # 23.06.20: Added Get_Language_Str()
    _fn_return_value = ( Res == 3 )
    return _fn_return_value, Comport


def USB_Port_Dialog(ComPortColumn):
    _fn_return_value = False
    #ComPort = Long()
    #----------------------------------------------------------------
    #if Show_USB_Port_Dialog(ComPortColumn, ComPort):
    #    if ComPort > 0:
    #        _fn_return_value = True
    #    pgcommon.M07_COM_Port.ComPortPage.CellDict[M01.SH_VARS_ROW, ComPortColumn] = ComPort
        # If the port is buzy a negativ number is written
        
    res, ComPort= Show_USB_Port_Dialog(ComPortColumn, 0)
    if res:
        #if IsNumeric(ComPort):
        if G00.port_is_available(ComPort):
            #if int(ComPort) > 0:
            _fn_return_value = True
        pattgen.M07_COM_Port.ComPortPage().CellDict[M01.SH_VARS_ROW, ComPortColumn] = ComPort
        X02.ActiveSheet.Redraw_table()    
    return _fn_return_value

def Test_USB_Port_Dialog():
    #UT-------------------------------
    ## VB2PY (CheckDirective) VB directive took path 2 on PROG_GENERATOR_PROG
    pass

def Detect_Com_Port(RightSide=VBMissingArgument, Pic_ID='DCC'):
    _fn_return_value = " "
    Res = Boolean()

    ComPortColumn = Long()

    ComPort = Long()
    #--------------------------------------------------------------------------------------------------------
    if RightSide:
        ComPortColumn = M01.COMPrtR_COL
    else:
        ComPortColumn = M01.COMPort_COL
    res, ComPort= Show_USB_Port_Dialog(ComPortColumn, ComPort)
    if res:         
        _fn_return_value = ComPort
    return _fn_return_value

def Test_Check_If_Arduino_could_be_programmed_and_set_Board_type():
    BuildOptions = String()
    #-------------------------------------------------------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on PATTERN_CONFIG_PROG
    # TinyUniProg
    _with81 = X02.Cells(M01.SH_VARS_ROW, M01.BuildOT_COL)
    if _with81.Value == '':
        _with81.Value = 115200
    Debug.Print(Check_If_Arduino_could_be_programmed_and_set_Board_type(M01.COMPrtT_COL, M01.BuildOT_COL, BuildOptions) + ' BuildOptions: ' + BuildOptions)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: BuildOptions - ByRef 
def Check_If_Arduino_could_be_programmed_and_set_Board_type(ComPortColumn, BuildOptColumn, BuildOptions):
    _fn_return_value = False
    Start_Baudrate = Long()

    Baudrate = Long()

    ComPort = Long()

    Msg = String()

    Retry = Boolean()

    AutoDetect = Boolean()
    # 04.05.20:
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The "Buzy" check and the automatic board detection is only active if Autodetect is enabled
    # Otherwise the values in the BuildOptColumn are used
    # Result: BuildOptions
    while 1:
        Retry = False
        if pattgen.M07_COM_Port.Check_USB_Port_with_Dialog(ComPortColumn) == False:
            return _fn_return_value, BuildOptions
        # Display Dialog if the COM Port is negativ and ask the user to correct it
        # Now we are sure that the com port is positiv. Check if it could be accesed and get the Baud rate
        BuildOptions = X02.Cells(M01.SH_VARS_ROW, BuildOptColumn)
        AutoDetect = InStr(BuildOptions, M01.AUTODETECT_STR) > 0
        if AutoDetect:
            BuildOptions = Trim(Replace(BuildOptions, M01.AUTODETECT_STR, ''))
            if InStr(BuildOptions, M01.BOARD_NANO_OLD) or InStr(BuildOptions, M01.BOARD_UNO_NORM) > 0:
                # Set the Default Baudrate to speed up the check
                Start_Baudrate = 57600
            else:
                Start_Baudrate = 115200
        ComPort = Val(X02.Cells(M01.SH_VARS_ROW, ComPortColumn))
        Baudrate = pattgen.M07_COM_Port.Get_Arduino_Baudrate(ComPort, Start_Baudrate)
        if Baudrate <= 0:
            if pattgen.M07_COM_Port.Check_If_Port_is_Available(ComPort) == False:
                Msg = pattgen.M09_Language.Get_Language_Str('Fehler: Es ist kein Arduino an COM Port #1# angeschlossen.')
            elif Baudrate == 0:
                Msg = pattgen.M09_Language.Get_Language_Str('Fehler: Das Gerät am COM Port #1# wurde nicht als Arduino erkannt.' + vbCr + 'Evtl. ist es ein defekter Arduino oder der Bootloader ist falsch.')
            else:
                Msg = pattgen.M09_Language.Get_Language_Str('Fehler: Der COM Port #1# wird bereits von einem anderen Programm benutzt.' + vbCr + 'Das kann z.B. der serielle Monitor der Arduino IDE oder das Farbtestprogramm sein.' + vbCr + vbCr + 'Das entsprechende Programm muss geschlossen werden.')
            Msg = Replace(Msg, '#1#', ComPort) + vbCr + vbCr + pattgen.M09_Language.Get_Language_Str('Wollen sie es noch mal mit einem anderen Arduino oder einem anderen COM Port versuchen?')
            if X02.MsgBox(Msg, vbYesNo + vbQuestion, pattgen.M09_Language.Get_Language_Str('Fehler bei der Überprüfung des angeschlossenen Arduinos')) == vbYes:
                Retry = True
                _with82 = X02.Cells(M01.SH_VARS_ROW, ComPortColumn)
                _with82.Value = - Val(_with82.Value)
                # Set to a negativ number to show the COM Port dialog
            else:
                return _fn_return_value, BuildOptions
        else:
            if AutoDetect:
                if Baudrate != Start_Baudrate:
                    # Change the board type to speed up the check the next time
                    if Baudrate == 57600:
                        NewBrd = M01.BOARD_NANO_OLD
                    else:
                        NewBrd = M01.BOARD_NANO_NEW
                        # An UNO can't be detected every time, but it could be programmed like a Nano with the new bootloader
                    LeftArduino = ( ComPortColumn == M01.COMPort_COL )
                    M02.Change_Board_Typ(LeftArduino, NewBrd)
                    # Write the new board type
                    BuildOptions = X02.Cells(M01.SH_VARS_ROW, BuildOptColumn)
                    # Reread the Build options in case the board type was adapted
                    BuildOptions = Trim(Replace(BuildOptions, M01.AUTODETECT_STR, ''))
                    # Remove the Autodetect flag
        if not (Retry):
            break
    _fn_return_value = True
    return _fn_return_value, BuildOptions

# VB2PY (UntranslatedCode) Option Explicit
