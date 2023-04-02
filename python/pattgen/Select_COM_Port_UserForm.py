from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import proggen.M07_COM_Port_New as M07
import proggen.M07_COM_Port as M07a
import pattgen.M09_Language as M09
import pattgen.M30_Tools as M30
import ExcelAPI.XLW_Workbook as X02

import tkinter as tk
from tkinter import ttk

LocalComPorts = [] #vbObjectInitialize(objtype=Byte)
OldL_ComPorts = [] #vbObjectInitialize(objtype=Byte)
PortNames = [] #vbObjectInitialize(objtype=String)
__OldSpinButton = Long()
Pressed_Button = Long()
LocalPrintDebug = Boolean()
__LocalShow_ComPort = Boolean()

class CSelect_COM_Port_UserForm:
    def __init__(self,controller):

        self.controller = controller
        self.IsActive = False
        self.isInitialised = False
        self.res = False
        self.UserForm_Res = ""
        self.__UserForm_Initialize()
        #*HL Center_Form(Me)                

    def ok(self, event=None):
        self.IsActive = False
        self.isInitialised = False
        self.OK_Button_Click()

        #self.Userform_res = value
        self.top.destroy()
        X02.ActiveSheet.Redraw_table()
        self.res = True

    def cancel(self, event=None):
        self.UserForm_Res = '<Abort>'
        self.IsActive = False
        self.isInitialised = False
        X02.ActiveSheet.Redraw_table()
        self.top.destroy()
        self.res = False

    def show(self):

        self.IsActive = True
        self.controller.wait_window(self.top)

        return self.res

    def Check_Button_Click(self,event=None):
        global Pressed_Button,CheckCOMPort
        #-------------------------------
        # Left Button
        Pressed_Button = 1
        #P01.ActiveSheet.Redraw_table()
        self.isInitialised = False
        self.IsActive=False
        self.top.destroy()
        M07.CheckCOMPort = " "
        
    
    def Abort_Button_Click(self,event=None):
        #-------------------------------
        # Middle Button
        global Pressed_Button,CheckCOMPort
        Pressed_Button = 2
        #P01.ActiveSheet.Redraw_table()
        self.isInitialised = False
        self.IsActive=False        
        self.top.destroy()
        M07.CheckCOMPort = " "
        
    
    def Default_Button_Click(self,event=None):
        #---------------------------------
        # Right Button
        global Pressed_Button,CheckCOMPort
        Pressed_Button = 3
        #P01.ActiveSheet.Redraw_table()
        self.isInitialised = False
        self.IsActive=False        
        self.top.destroy()
        M07.CheckCOMPort = " "

    def __SpinButton_Change(self):
        #------------------------------
        #Debug.Print "Update_SpinButton"
        self.Update_SpinButton(0)
        
    def Button_Setup(self,Text,Command,Column=0):
        Text = Trim(Text)
        #Button_visible = ( Text != r'' )
        if Text != r'':
            Err = ( Len(Text) < 3 )
            if not Err:
                Err = ( Mid(Text, 2, 1) != r' ' )
            if Err:
                X02.MsgBox(r'Internal Error: Button text is wrong '' + Text + r''.' + vbCr + r'It must contain an Accelerator followed by the text.' + vbCr + r'Example: "H Hallo"', vbCritical, r'Internal Error (Wrong translation?)')
                M30.EndProg()
            Button_Text=(Mid(Text, 3, 255))
            Button_Accelerator = Left(Text, 1)
            #Button_Text = tk.StringVar(master=self.top)
            Button = tk.Button(self.button_frame, text=Button_Text, command=Command,width=10,font=("Tahoma", 11))
            Button.grid(row=0,column=Column,sticky="e",padx=10,pady=10)
            self.top.bind(Button_Accelerator, Command)
        return      
        
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: DefaultPort - ByVal 
    def Update_SpinButton(self, DefaultPort):

        global COM_Port_Label,PortNames,LocalPrintDebug,LocalComPorts,__OldSpinButton,OldL_ComPorts
        #------------------------------------------------------
        # Is also called by the OnTime proc which checks the available ports
        Debug.Print("Select_Com_Port_UserForm-Update_SpinButton")
        
        if self.isInitialised == False:
            return
        try:
            Show_Unknown_CheckBox_flag = self.Show_Unknown_CheckBox_var.get() #*HL
        except:
            Show_Unknown_CheckBox_flag = True
        if not self.Com_Port_Label.winfo_exists():
            return
            
        SpinButton=int(self.Com_Port_Label.current())
        
        LocalComPorts,PortNames = M07a.EnumComPorts(Show_Unknown_CheckBox_flag, PortNames, PrintDebug= LocalPrintDebug)
        if M30.isInitialised(LocalComPorts):
            SpinButton_Max = len(LocalComPorts)-1
            if DefaultPort != " ":# > 0:
                for i in range(len(LocalComPorts)):
                    if DefaultPort == LocalComPorts[i]:
                        SpinButton = i
            else:
                if M30.isInitialised(OldL_ComPorts):
                    if len(LocalComPorts) > len(OldL_ComPorts):
                        for ix in range(len(OldL_ComPorts)): #vbForRange(0, UBound(__OldL_ComPorts)):
                            if LocalComPorts[ix] != OldL_ComPorts[ix]:
                                SpinButton = ix
                                break
                            if ix > UBound(OldL_ComPorts):
                                SpinButton = ix
            if SpinButton > SpinButton_Max:
                SpinButton = SpinButton_Max
            if PortNames==[]:
                PortNames.append(" ")
                LocalComPorts.append(" ")
            M07.CheckCOMPort_Txt = PortNames[SpinButton]
            tmp_comport = LocalComPorts[SpinButton]
            if tmp_comport==" ":
                tmp_comport = "999"
            #if IsNumeric(tmp_comport):
            #    M07.CheckCOMPort = int(tmp_comport)
            #else:
            M07.CheckCOMPort = tmp_comport 
            LocalComPorts_list = LocalComPorts
            
            #for i in range(len(LocalComPorts)):
            #    LocalComPorts_list.append(LocalComPorts(i))
            self.Com_Port_No=SpinButton
            self.Com_Port_Label["value"] = LocalComPorts_list
            if M07.CheckCOMPort != " ":
                self.Com_Port_Label.set(M07.CheckCOMPort)
                COM_Port_Label = M07.CheckCOMPort
            else:
                self.Com_Port_Label.set(" ")
                COM_Port_Label = ' COM' + "?"
            
            if SpinButton != __OldSpinButton:
                self.Show_Status(False, M09.Get_Language_Str('Aktualisiere Status ...'))
                __OldSpinButton = SpinButton
            PortsStr=""
            for Port in LocalComPorts:
                PortsStr = PortsStr + Port + ' '
            self.AvailPorts_Label.configure(text=M30.DelLast(PortsStr))
            OldL_ComPorts = LocalComPorts
        else:
            M07.CheckCOMPort = "999"#999
            self.AvailPorts_Label.configure(text='')
            COM_Port_Label = ' -'

    def Show_Status(self,ErrBox, Msg):
        global Error_Label,Status_Label
        Debug.Print("Select_Com_Port_UserForm-Show_Status")
        #-------------------------------------------------------
        if self.isInitialised == False:
            return
        if self.Status_Label.winfo_exists():
            if ErrBox:
                #if Error_Label != Msg:
                self.Error_Label.configure(text=Msg)
                    # "If" is used to prevent flickering
            else:
                self.Status_Label.configure(text=Msg)
                #if Status_Label != Msg:
                #    Status_Label = Msg
            #if Error_Label.Visible != ErrBox:
            if ErrBox:
                self.Error_Label.grid()
                self.Status_Label.grid_remove()
                
            else:
                self.Error_Label.grid_remove()
                self.Status_Label.grid()
            self.top.update()

    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ComPort_IO - ByRef 
    def ShowDialog(self, Caption, Title, Text, Picture, Buttons, FocusButton, Show_ComPort, Red_Hint, ComPort_IO, PrintDebug=False):
        global COM_Port_Label,PortNames,LocalPrintDebug,LocalComPorts,__LocalPrintDebug, __OldSpinButton,__LocalShow_ComPort,Pressed_Button
        Debug.Print("Select_Com_Port_UserForm-Showdialog")
        #if  not PG.dialog_parent.getConfigData("UseCOM_Port_UserForm"):
        #    Debug.Print("UseCOM_Port_UserForm=True")
        #    fn_return_value = 3
        #    serportname = PG.dialog_parent.getConfigData("serportname")

        #    if serportname[:3]=="COM":
        #        serportname=int(serportname[3:])
        #    
        #    return fn_return_value,serportname
        # 
            
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
        self.title = M09.Get_Language_Str(Caption)
        
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)

        self.top.grab_set()
        
        self.top.resizable(True, True)  # This code helps to disable windows from resizing
        
        window_height = 500
        window_width = 800
        
        winfo_x = self.controller.winfo_x()
        winfo_y = self.controller.winfo_y()
        
        screen_width = self.controller.winfo_width()
        screen_height = self.controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
        
        #self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))                 
        self.top.geometry("+{}+{}".format(x_cordinate, y_cordinate))                   
        
        if len(self.title) > 0: 
            self.top.title(self.title) 
            

        self.Title_Label = ttk.Label(self.top, text=Title,font=("Tahoma", 14),width=40,wraplength=350,relief=tk.FLAT, borderwidth=1)
        self.Title_Label.focus_set()
        self.Title_Label.grid(row=0,column=0,columnspan=2,sticky="nesw",padx=10,pady=10)
        
        self.Text_Label = ttk.Label(self.top, text=Text,font=("Tahoma", 11),width=40, wraplength=350,relief=tk.FLAT, borderwidth=1)
        self.Text_Label.grid(row=1,column=0,columnspan=2,sticky="nesw",padx=10,pady=10)
        
        self.Status_Label = ttk.Label(self.top, text="",font=("Tahoma", 11),width=15,wraplength=100,relief=tk.FLAT, borderwidth=1)
        self.Status_Label.grid(row=2,column=1,rowspan=3,sticky="ne",padx=10,pady=10)
        
        self.Error_Label = ttk.Label(self.top, text="",font=("Tahoma", 11),width=15, wraplength=100,relief=tk.FLAT, borderwidth=1)
        self.Error_Label.grid(row=2,column=1,rowspan=3,sticky="ne",padx=10,pady=10)        
                
        self.AvailPortsTxt_Label = ttk.Label(self.top, text="",font=("Tahoma", 8),width=15, wraplength=100,relief=tk.FLAT, borderwidth=1)
        self.AvailPortsTxt_Label.grid(row=4,column=0,columnspan=2,sticky="new",padx=10,pady=10)
        
        Debug.Print("ComPort_ShowDialog - Define Imagepath")

        filename = r"/images/"+ Picture+".png"
        filedir = os.path.dirname(os.path.realpath(__file__))
        Debug.Print("ComPort_ShowDialog - Image fileDir:"+filedir)
        self.filedir2 = os.path.dirname(filedir)
        filepath = self.filedir2 + filename
        
        Debug.Print("ComPort_ShowDialog - Image:"+filepath)
        img = tk.PhotoImage(file=filepath)
        Debug.Print("ComPort_ShowDialog - Image:"+filepath+" -OK-")
        
        self.Image_Label = ttk.Label(self.top, image=img,relief=tk.FLAT, borderwidth=1)
        self.Image_Label.grid(row=0,column=2,rowspan=7,sticky="nesw",padx=10,pady=10)
        
        self.Red_Hint_Label = ttk.Label(self.top, text=Red_Hint,font=("Tahoma", 11),foreground="#FF0000",width=20,wraplength=125,relief=tk.FLAT, borderwidth=1)
        self.Red_Hint_Label.grid(row=0,column=2,columnspan=1,rowspan=2,sticky="ne",padx=10,pady=10)
         
        self.Com_Port_Label = ttk.Combobox(self.top, width=30,font=("Tahoma", 11))
        self.Com_Port_Label.grid(row=3,column=0,sticky="nesw",padx=10,pady=10)
        
        self.Com_Port_Label ["value"] = ["valuelist"]
        self.Com_Port_Label.set(0)
        
        self.Show_Unknown_CheckBox_var = tk.IntVar(master=self.top)
        self.Show_Unknown_CheckBox_var.set(0)

        self.Show_Unknown_CheckBox = tk.Checkbutton(self.top, text=M09.Get_Language_Str("Unbekante Ports anzeigen"),width=30,wraplength = 200,anchor="w",variable=self.Show_Unknown_CheckBox_var,font=("Tahoma", 8),onvalue = 1, offvalue = 0)
        self.Show_Unknown_CheckBox.grid(row=4, column=0, columnspan=2,sticky="nesw", padx=2, pady=2)
        
        self.Hint_Label = ttk.Label(self.top, text=M09.Get_Language_Str("Zur Identifikation des Arduinos blinken die LEDs des ausgewählten Arduinos schnell.\nEin anderer COM Port kann über die Pfeiltasten ausgewählt werden.\nDer Arduino kann auch nachträglich angesteckt werden."),font=("Tahoma", 11),width=40,wraplength=350,relief=tk.FLAT, borderwidth=1)
        self.Hint_Label.grid(row=7,column=0,columnspan=2,rowspan=2,sticky="nesw",padx=10,pady=10)
        
        self.AvailPorts_Label = ttk.Label(self.top, text="",font=("Tahoma", 11),width=30, wraplength=350,relief=tk.FLAT, borderwidth=1)
        self.AvailPorts_Label.grid(row=5,column=0,columnspan=2,sticky="nesw",padx=10,pady=10)
        
        # crate buttons
        self.buttonlist = Buttons.split(";")
        
        self.button_frame = ttk.Frame(self.top)
        
        self.Check_Button_Text = tk.StringVar(master=self.top)
        self.Button_Setup(self.buttonlist[0], self.Check_Button_Click,Column=0)
        self.Button_Setup(self.buttonlist[1], self.Abort_Button_Click,Column=1)
        self.Button_Setup(self.buttonlist[2], self.Default_Button_Click,Column=2)
        
        self.button_frame.grid(row=8,column=2,sticky="e",padx=10,pady=10)
        
        self.top.bind("<Return>", self.Default_Button_Click)
        self.top.bind("<Escape>", self.Abort_Button_Click)                   
        
        self.isInitialised = True
                        
        #Me.Caption = Caption
        #Title_Label = Title
        #Text_Label = Text
        #Error_Label = ''
        #Status_Label = ''
        ButtonArr = Split(Buttons, ';')
        if UBound(ButtonArr) != 2:
            X02.MsgBox('Internal Error in Select_COM_Port_UserForm: \'Buttons\' must be a string with 3 buttons separated by \';\'' + vbCr + 'Wrong: \'' + Buttons + '\'', vbCritical, 'Internal Error (Wrong translation?)')
            M30.EndProg()
        #Button_Setup(Check_Button, ButtonArr(0))
        #Button_Setup(Abort_Button, ButtonArr(1))
        #Button_Setup(Default_Button, ButtonArr(2))
        #if FocusButton != '':
        #    Controls(FocusButton).setFocus()
        __LocalPrintDebug = PrintDebug
        __OldSpinButton = - 1
        Pressed_Button = 0
        self.Update_SpinButton(ComPort_IO)
        #SpinButton.Visible = Show_ComPort
        #if Show_ComPort:
        #    SpinButton.setFocus()
        __LocalShow_ComPort = Show_ComPort
        # Show / Hide the COM Port
        #COM_Port_Label.Visible = Show_ComPort
        #Error_Label.Visible = Show_ComPort
        #Status_Label.Visible = Show_ComPort
        #AvailPortsTxt_Label.Visible = Show_ComPort
        #Available_Ports_Label.Visible = Show_ComPort
        #Show_Unknown_CheckBox.Visible = Show_ComPort
        #Hint_Label.Visible = Show_ComPort
        #if Show_ComPort:
        #    Text_Label.Height = Error_Label.Top - Text_Label.Top
        #else:
        #    Text_Label.Height = Hint_Label.Top + Hint_Label.Height - Text_Label.Top
        
        # get image
        #for c in Me.Controls:
        #    if Right(c.Name, Len('Image')) == 'Image':
        #        if Picture == c.Name:
        #            c.Visible = True
        #            Found = True
        #        else:
        #            c.Visible = False
        #if not Found:
        #    MsgBox('Internal Error: Unknown picture: \'' + Picture + '\'', vbCritical, 'Internal Error')
        #Red_Hint_Label = Red_Hint
        self.show() #Me.Show()
        # Store the results
        if Show_ComPort:
            if M30.isInitialised(LocalComPorts):
                ComPort_IO = LocalComPorts[self.Com_Port_No]
        fn_return_value = Pressed_Button
        return fn_return_value, ComPort_IO
    
    def __UserForm_Initialize(self):
        #--------------------------------
        #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #P01.Center_Form(Me)
        pass
    
    def __UserForm_QueryClose(self, CloseMode, Cancel):
        self.Abort_Button_Click()
    
    # VB2PY (UntranslatedCode) Option Explicit


# VB2PY (UntranslatedCode) Option Explicit
#################################################################################################
    

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


    
class CSelect_COM_Port_UserForm2:
    
    
    
    def __init__(self,controller):
        
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
                                                       "Command":self.Abort_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":342,"Top":300,"Type":"CommandButton","Visible":True,"Width":72},
                                                      {"Name":"Check_Button","Accelerator":"P","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                       "Caption":"Prüfen",
                                                       "Command":self.Check_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":258,"Top":300,"Type":"CommandButton","Visible":True,"Width":72},
                                                      {"Name":"Default_Button","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                       "Caption":"Default",
                                                       "Command":self.Default_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":24,"Left":426,"Top":300,"Type":"CommandButton","Visible":True,"Width":72},
                                                      ]
                                }}
        
        self.Name          = "Select_COM_Port_UserForm"
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.UserForm_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        #*HL Center_Form(Me)
        
    def Abort_Button_Click(self):
        pass
    
    def Check_Button_Click(self):
        pass
    
    def Default_Button_Click(self):
        pass    
    
    
    def __UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Form=G00.generate_form(Main_Menu_Form_RSC,self.controller,dlg=self)
                
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
    """