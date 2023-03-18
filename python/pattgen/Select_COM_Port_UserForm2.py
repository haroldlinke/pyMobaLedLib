from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M07_COM_Port_New
import pattgen.M07_COM_Port
import pattgen.M09_Language
import pattgen.M30_Tools as M30
import ExcelAPI.XLW_Workbook as X02

import ExcelAPI.XLF_FormGenerator as XLF
import pattgen.D00_Forms as D00

LocalComPorts = vbObjectInitialize(objtype=Byte)
OldL_ComPorts = vbObjectInitialize(objtype=Byte)
PortNames = vbObjectInitialize(objtype=String)
OldSpinButton = Long()
Pressed_Button = Long()
LocalPrintDebug = Boolean()
LocalShow_ComPort = Boolean()

def Check_Button_Click():
    global Pressed_Button
    #-------------------------------
    # Left Button
    Pressed_Button = 1
    Me.Hide()
    # no "Unload Me" to keep the entered data and dialog position
    pattgen.M07_COM_Port_New.CheckCOMPort = 0
    # Stop Blink_Ardiono_LED()

def Abort_Button_Click():
    global Pressed_Button
    #-------------------------------
    # Middle Button
    Pressed_Button = 2
    Me.Hide()
    # no "Unload Me" to keep the entered data and dialog position
    pattgen.M07_COM_Port_New.CheckCOMPort = 0
    # Stop Blink_Ardiono_LED()

def Default_Button_Click():
    global Pressed_Button
    #---------------------------------
    # Right Button
    Pressed_Button = 3
    Me.Hide()
    # no "Unload Me" to keep the entered data and dialog position
    pattgen.M07_COM_Port_New.CheckCOMPort = 0
    # Stop Blink_Ardiono_LED()

def SpinButton_Change():
    #------------------------------
    #Debug.Print "Update_SpinButton"
    Update_SpinButton(0)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DefaultPort - ByVal 
def Update_SpinButton(DefaultPort):
    global LocalComPorts, OldSpinButton, OldL_ComPorts
    #------------------------------------------------------
    # Is also called by the OnTime proc which checks the available ports
    LocalComPorts = pattgen.M07_COM_Port.EnumComPorts(self.Show_Unknown_CheckBox, PortNames, PrintDebug= LocalPrintDebug)
    # Read the available COM ports where an Arduino is connected
    if isInitialised(LocalComPorts):
        SpinButton.Max = UBound(LocalComPorts)
        if DefaultPort > 0:
            # DefaultPort is > 0 when it's called the first time
            for i in vbForRange(0, UBound(LocalComPorts)):
                if DefaultPort == LocalComPorts(i):
                    SpinButton = i
        else:
            # Check if a new com port was detected and select it
            if isInitialised(OldL_ComPorts):
                if UBound(LocalComPorts) > UBound(OldL_ComPorts):
                    for ix in vbForRange(0, UBound(OldL_ComPorts)):
                        if LocalComPorts(ix) != OldL_ComPorts(ix):
                            SpinButton = ix
                            break
                    if ix > UBound(OldL_ComPorts):
                        SpinButton = ix
        if SpinButton > SpinButton.Max:
            SpinButton = SpinButton.Max
        pattgen.M07_COM_Port_New.CheckCOMPort_Txt = PortNames(SpinButton)
        pattgen.M07_COM_Port_New.CheckCOMPort = LocalComPorts(SpinButton)
        self.COM_Port_Label = ' COM' + pattgen.M07_COM_Port_New.CheckCOMPort
        if SpinButton != OldSpinButton:
            Show_Status(False, pattgen.M09_Language.Get_Language_Str('Aktualisiere Status ...'))
            OldSpinButton = SpinButton
        for Port in LocalComPorts:
            PortsStr = PortsStr + Port + ' '
        self.Available_Ports_Label = M30.DelLast(PortsStr)
        OldL_ComPorts = LocalComPorts
    else:
        pattgen.M07_COM_Port_New.CheckCOMPort = 999
        self.Available_Ports_Label = ''
        self.COM_Port_Label = ' -'

def Show_Status(ErrBox, Msg):
    #-------------------------------------------------------
    if ErrBox:
        if Error_Label != Msg:
            Error_Label = Msg
        # "If" is used to prevent flickering
    else:
        if Status_Label != Msg:
            Status_Label = Msg
    if Error_Label.Visible != ErrBox:
        Error_Label.Visible = ErrBox
    if Status_Label.Visible == ErrBox:
        Status_Label.Visible = not ErrBox

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort_IO - ByRef 
def ShowDialog(Caption, Title, Text, Picture, Buttons, FocusButton, Show_ComPort, Red_Hint, ComPort_IO, PrintDebug=False):
    global LocalPrintDebug, OldSpinButton, Pressed_Button, LocalShow_ComPort
    _fn_return_value = None
    ButtonArr = vbObjectInitialize(objtype=String)

    BNr = Variant()

    c = Variant()

    Found = Boolean()
    #----------------------------------------------------------------------------------------------
    # Variables:
    #  Caption     Dialog Caption
    #  Title       Dialog Title
    #  Text        Message in the text box on the top left side
    #  Picture     Name of the picture to be shown. Available pictures: "LED_Image", "CAN_Image", "Tiny_Image", "DCC_Image"
    #  Buttons     List of 3 buttons with Accelerator. Example "H Hallo; A Abort; O Ok"  Two Buttons: " ; A Abort; "O Ok"
    #  ComPort_IO  is used as input and output
    # Return:
    #  1: If the left   Button is pressed  (Install, ...)
    #  2: If the middle Button is pressed  (Abort)
    #  3: If the right  Button is pressed  (OK)
    Me.Caption = Caption
    Title_Label = Title
    Text_Label = Text
    Error_Label = ''
    Status_Label = ''
    ButtonArr = Split(Buttons, ';')
    if UBound(ButtonArr) != 2:
        X02.MsgBox('Internal Error in Select_COM_Port_UserForm: \'Buttons\' must be a string with 3 buttons separated by \';\'' + vbCr + 'Wrong: \'' + Buttons + '\'', vbCritical, 'Internal Error (Wrong translation?)')
        M30.EndProg()
    M30.Button_Setup(Check_Button, ButtonArr(0))
    M30.Button_Setup(Abort_Button, ButtonArr(1))
    M30.Button_Setup(Default_Button, ButtonArr(2))
    if FocusButton != '':
        Controls(FocusButton).setFocus()
    LocalPrintDebug = PrintDebug
    OldSpinButton = - 1
    Pressed_Button = 0
    Update_SpinButton(ComPort_IO)
    SpinButton.Visible = Show_ComPort
    if Show_ComPort:
        SpinButton.setFocus()
    LocalShow_ComPort = Show_ComPort
    # Show / Hide the COM Port
    COM_Port_Label.Visible = Show_ComPort
    Error_Label.Visible = Show_ComPort
    Status_Label.Visible = Show_ComPort
    AvailPortsTxt_Label.Visible = Show_ComPort
    Available_Ports_Label.Visible = Show_ComPort
    Show_Unknown_CheckBox.Visible = Show_ComPort
    Hint_Label.Visible = Show_ComPort
    if Show_ComPort:
        # Set the height of the main text box
        Text_Label.Height = Error_Label.Top - Text_Label.Top
        # 78
    else:
        Text_Label.Height = Hint_Label.Top + Hint_Label.Height - Text_Label.Top
    for c in Me.Controls:
        if Right(c.Name, Len('Image')) == 'Image':
            if Picture == c.Name:
                c.Visible = True
                Found = True
            else:
                c.Visible = False
    if not Found:
        X02.MsgBox('Internal Error: Unknown picture: \'' + Picture + '\'', vbCritical, 'Internal Error')
    Red_Hint_Label = Red_Hint
    Me.Show()
    # Store the results
    if Show_ComPort:
        if isInitialised(LocalComPorts):
            ComPort_IO = LocalComPorts(SpinButton)
    _fn_return_value = Pressed_Button
    return _fn_return_value

def UserForm_Initialize():
    #--------------------------------
    #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
    Change_Language_in_Dialog(Me)
    X02.Center_Form(Me)

# VB2PY (UntranslatedCode) Option Explicit
#################################################################################################
    
Main_Menu_Form_RSC = {"UserForm":{
                        "Name"          : "Select_COM_Port_UserForm",
                        "BackColor"     : "#000008",
                        "BorderColor"   : "#000012",
                        "Caption"       : "Select_COM_Port_UserForm",
                        "Height"        : 360,
                        "Left"          : 0,
                        "Top"           : 0,
                        "Type"          : "MainWindow",
                        "Visible"       : True,
                        "Width"         : 518.25,
                                "Components":[{"Name":"Title_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Titel",
                                                "ControlTipText":"","ForeColor":"#000012","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":270},
                                              {"Name":"Text_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Text",
                                               "ControlTipText":"","ForeColor":"#000012","Height":84,"Left":12,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":270},
                                              {"Name":"AvailPortsTxt_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Text",
                                               "ControlTipText":"","ForeColor":"#00000012","Height":12,"Left":12,"TextAlign":"fmTextAlignLeft","Top":156,"Type":"Label","Visible":True,"Width":72},
                                              {"Name":"COM_Port_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"","ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":126,"Type":"Label","Visible":True,"Width":48},
                                              {"Name":"Error_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"","ForeColor":"#0000FF","Height":66,"Left":102,"TextAlign":"fmTextAlignLeft","Top":114,"Type":"Label","Visible":True,"Width":180},
                                              {"Name":"Hint_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Zur Identifikation des Arduinos blinken die LEDs des ausgewählten Arduinos schnell.\n\nEin anderer COM Port kann über die Pfeiltasten ausgewählt werden.\n\nDer Arduino kann auch nachträglich angesteckt werden.",
                                               "ControlTipText":"","ForeColor":"#000012","Height":114,"Left":12,"TextAlign":"fmTextAlignLeft","Top":210,"Type":"Label","Visible":True,"Width":246},                                              
                                              {"Name":"Red_Hint_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Zur Identifikation des Arduinos blinken die LEDs des ausgewählten Arduinos schnell.\n\nEin anderer COM Port kann über die Pfeiltasten ausgewählt werden.\n\nDer Arduino kann auch nachträglich angesteckt werden.",
                                               "ControlTipText":"","ForeColor":"#0000FF","Height":90,"Left":396,"TextAlign":"fmTextAlignLeft","Top":18,"Type":"Label","Visible":True,"Width":96},
                                              {"Name":"Status_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"...",
                                               "ControlTipText":"","ForeColor":"#00000012","Height":42,"Left":102,"TextAlign":"fmTextAlignLeft","Top":126,"Type":"Label","Visible":True,"Width":180},
                                              
                                              {"Name":"Show_Unknown_CheckBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Unbekannte Ports zeigen",
                                               "ControlTipText":"","ForeColor":"#000012","Height":30,"Left":66,"TextAlign":"fmTextAlignLeft","Top":120,"Type":"SpinButton","Visible":True,"Width":24},
                                              
                                              {"Name":"SpinButton","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Unbekannte Ports zeigen",
                                               "ControlTipText":"","ForeColor":"#000012","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":186,"Type":"CheckBox","Visible":True,"Width":128.4},                                                    
                                              
                                              {"Name":"CAN_Image","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "ControlTipText":"","Height":282,"Left":282,"Top":0,"Type":"Image","Visible":True,"Width":210},
                                              {"Name":"DCC_Image","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "ControlTipText":"","Height":282,"Left":282,"Top":0,"Type":"Image","Visible":True,"Width":210},
                                              {"Name":"LED_Image","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "ControlTipText":"","Height":282,"Left":282,"Top":0,"Type":"Image","Visible":True,"Width":210},
                                              {"Name":"Tiny_Image","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "ControlTipText":"","Height":282,"Left":282,"Top":0,"Type":"Image","Visible":True,"Width":210},                                                                  
                                              
                                              {"Name":"Abort_Button","Accelerator":"A","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Abbruch",
                                               "Command":Abort_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":342,"Top":300,"Type":"CommandButton","Visible":True,"Width":72},
                                              {"Name":"Check_Button","Accelerator":"P","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Prüfen",
                                               "Command":Check_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":258,"Top":300,"Type":"CommandButton","Visible":True,"Width":72},
                                              {"Name":"Default_Button","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Default",
                                               "Command":Default_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":426,"Top":300,"Type":"CommandButton","Visible":True,"Width":72},
                                              ]
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

    
class CSelect_COM_Port_UserForm:
    
    def __init__(self,controller):
        self.Name          = "Select_COM_Port_UserForm"
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
        setattr(self,control.Name,control)
        
        # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort_IO - ByRef 
    def ShowDialog(self, Caption, Title, Text, Picture, Buttons, FocusButton, Show_ComPort, Red_Hint, ComPort_IO, PrintDebug=False):
        global LocalPrintDebug, OldSpinButton, Pressed_Button, LocalShow_ComPort
        _fn_return_value = None
        ButtonArr = vbObjectInitialize(objtype=String)
        self.__UserForm_Initialize()
    
        BNr = Variant()
    
        c = Variant()
    
        Found = Boolean()
        #----------------------------------------------------------------------------------------------
        # Variables:
        #  Caption     Dialog Caption
        #  Title       Dialog Title
        #  Text        Message in the text box on the top left side
        #  Picture     Name of the picture to be shown. Available pictures: "LED_Image", "CAN_Image", "Tiny_Image", "DCC_Image"
        #  Buttons     List of 3 buttons with Accelerator. Example "H Hallo; A Abort; O Ok"  Two Buttons: " ; A Abort; "O Ok"
        #  ComPort_IO  is used as input and output
        # Return:
        #  1: If the left   Button is pressed  (Install, ...)
        #  2: If the middle Button is pressed  (Abort)
        #  3: If the right  Button is pressed  (OK)
        self.Caption = Caption
        self.Title_Label.Caption = Title
        self.Text_Label.Caption = Text
        self.Error_Label = ''
        self.Status_Label = ''
        ButtonArr = Split(Buttons, ';')
        if UBound(ButtonArr) != 2:
            X02.MsgBox('Internal Error in Select_COM_Port_UserForm: \'Buttons\' must be a string with 3 buttons separated by \';\'' + vbCr + 'Wrong: \'' + Buttons + '\'', vbCritical, 'Internal Error (Wrong translation?)')
            M30.EndProg()
        M30.Button_Setup(self.Check_Button, ButtonArr(0))
        M30.Button_Setup(self.Abort_Button, ButtonArr(1))
        M30.Button_Setup(self.Default_Button, ButtonArr(2))
        #if FocusButton != '':
        #    self.Controls(FocusButton).setFocus()
        LocalPrintDebug = PrintDebug
        OldSpinButton = - 1
        Pressed_Button = 0
        Update_SpinButton(ComPort_IO)
        self.SpinButton.Visible = Show_ComPort
        if Show_ComPort:
            self.SpinButton.setFocus()
        LocalShow_ComPort = Show_ComPort
        # Show / Hide the COM Port
        self.COM_Port_Label.Visible = Show_ComPort
        self.Error_Label.Visible = Show_ComPort
        self.Status_Label.Visible = Show_ComPort
        self.AvailPortsTxt_Label.Visible = Show_ComPort
        self.Available_Ports_Label.Visible = Show_ComPort
        self.Show_Unknown_CheckBox.Visible = Show_ComPort
        self.Hint_Label.Visible = Show_ComPort
        if Show_ComPort:
            # Set the height of the main text box
            self.Text_Label.Height = self.Error_Label.Top - self.Text_Label.Top
            # 78
        else:
            self.Text_Label.Height = self.Hint_Label.Top + self.Hint_Label.Height - self.Text_Label.Top
        for c in self.Controls:
            if Right(c.Name, Len('Image')) == 'Image':
                if Picture == c.Name:
                    c.Visible = True
                    Found = True
                else:
                    c.Visible = False
        if not Found:
            X02.MsgBox('Internal Error: Unknown picture: \'' + Picture + '\'', vbCritical, 'Internal Error')
        self.Red_Hint_Label.Caption = self.Red_Hint.Caption
        self.Show()
        # Store the results
        if self.Show_ComPort:
            if isInitialised(LocalComPorts):
                ComPort_IO = LocalComPorts(self.SpinButton)
        _fn_return_value = Pressed_Button
        return _fn_return_value
        
    def Show(self):
        self.IsActive = True
        self.__UserForm_Initialize()
        self.__UserForm_Activate()
        self.controller.wait_window(self.Form)
        
    
    # VB2PY (UntranslatedCode) Option Explicit