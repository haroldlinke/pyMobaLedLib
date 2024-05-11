from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as XLA
import ExcelAPI.XLF_FormGenerator as XLF

class UserForm_Connector:
    
    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.Userform_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        #*HL Center_Form(Me)
        
        self.Connector_Form_RSC = {"UserForm":{
                        "Name"          : "Userform_Connector",
                        "BackColor"     : "#00000F",
                        "BorderColor"   : "#000012",
                        "Caption"       : "Verteiler und Stecker Nummer",
                        "Height"        : 332,
                        "Left"          : 0,
                        "Top"           : 0,
                        "Type"          : "MainWindow",
                        "Visible"       : True,
                        "Width"         : 405,
                        "Components":[{"Name":"Label1","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Zur Dokumentation des benutzten Anschlusses können eine Beschreibung der Verteilerplatine (Ort/Nummer/...) und die Nummer des benutzten Steckplatzes in die Tabelle eingetragen werden.\n\n" +
                                       "Damit kann man später leichter nachvollziehen an welcher Stelle innerhalb der LED Kette ein Objekt angeschlossen ist.\n\n" +
                                       "Die LEDs werden über ihre Position in der Kette adressiert. Die erste LED in der Kette bekommt die Nummer 0. Die Zweite die Nummer 1...\n\n" +
                                       "Dadurch dass die Verteilerplatinen kaskadiert werden können kann es schnell passieren, dass man den Überblick verliert. Darum ist eine ausführliche Dokumentation besonders wichtig.\n\n" +
                                       "Details dazu findet man auch in der Dokumentation.",
                                        "ControlTipText":"","ForeColor":"#000012","Height":198,"Left":6,"SpecialEffect": "fmSpecialEffectSunken","TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":378},
                                      {"Name":"Label2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Verteilernummer oder Beschreibung:",
                                       "ControlTipText":"","ForeColor":"#FF0000","Height":18,"Left":24,"TextAlign":"fmTextAlignLeft","Top":204,"Type":"Label","Visible":True,"Width":270},
                                      {"Name":"Dist_Nr","BackColor":"#000005","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"","ForeColor":"#000008","Height":18,"Left":24,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":222,"Type":"TextBox","Value": "" ,"Visible":True,"Width":174},
                                      {"Name":"Label3","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Steckernummer:",
                                       "ControlTipText":"","ForeColor":"#FF0000","Height":18,"Left":24,"TextAlign":"fmTextAlignLeft","Top":252,"Type":"Label","Visible":True,"Width":270},
                                      {"Name":"Conn_Nr","BackColor":"#000005","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"","ForeColor":"#000008","Height":18,"Left":24,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":270,"Type":"TextBox","Value": "" ,"Visible":True,"Width":174},
                                      {"Name":"Abort_Button","Accelerator":"<Escape>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Abbruch",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":222,"Top":270,"Type":"CommandButton","Visible":True,"Width":72},
                                       
                                      {"Name":"OK_Button","Accelerator":"<Return>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"OK",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":24,"Left":300,"Top":270,"Type":"CommandButton","Visible":True,"Width":72}
                                    ]},
                        }

        self.OK_Pressed = False
        
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
        self.__UserForm_Activate()
        self.controller.wait_window(self.Form)
    
    def Abort_Button_Click(self, event=None):
        #-------------------------------
        self.Hide()
        # no "Unload Me" to keep the entered data and dialog position
    
    def OK_Button_Click(self, event=None):
        global OK_Pressed
        #----------------------------
        self.OK_Pressed = True
        self.Dist_Nr_R.Value = self.Dist_Nr.Value
        self.Conn_Nr_R.Value = self.Conn_Nr.Value        
        self.Hide()
    
    def __UserForm_Initialize(self):
        #--------------------------------
        #Debug.Print vbCr & me.Name & ": UserForm_Initialize"
        self.Userform_Res = ""
        self.Form=XLF.generate_form(self.Connector_Form_RSC,self.controller,dlg=self, jump_table=None, defaultfont=XLA.DefaultFont)
        #Change_Language_in_Dialog(Me)
        # 20.02.20:
        #P01.Center_Form(Me)
    
    def Start(self, Dist_Nr_R, Conn_Nr_R):
        self.__UserForm_Initialize()
        _fn_return_value = False
        self.Dist_Nr_R = Dist_Nr_R
        self.Conn_Nr_R = Conn_Nr_R
        #-----------------------------------------------------------------------------------
        self.Dist_Nr.Value = self.Dist_Nr_R.Value
        self.Conn_Nr.Value = self.Conn_Nr_R.Value
        self.OK_Pressed = False
        self.Dist_Nr.setFocus()
        self.Show()
        _fn_return_value = self.OK_Pressed
        return _fn_return_value
    
    # VB2PY (UntranslatedCode) Option Explicit
