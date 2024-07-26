from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.M09_Language as M09
import pattgen.M08_Load_Sheet_Data
import pattgen.M07_Save_Sheet_Data
import pattgen.M30_Tools as M30
import pattgen.M65_Special_Modules
import pattgen.M80_Multiplexer_INI_Handling
import mlpyproggen.Pattern_Generator as PG

import ExcelAPI.XLF_FormGenerator as XLF
import pattgen.D00_Forms as D00

import tkinter as tk
from tkinter import ttk

import logging



def OK_Button_Click():
    #------------------------------
    pass
    #D00.MainMenu_Form.Hide()
    # To keep the last position of the dialog

def Close2Button_Click():
    #-------------------------------
    # Tab: "Spezielle Module"
    OK_Button_Click()


def Abort_Button_Click():
    #-----------------------------
    ## VB2PY (CheckDirective) VB directive took path 1 on 1
    #X02.Shell('Explorer https://wiki.mobaledlib.de/anleitungen/spezial/patterngenerator')
    pass


class UserForm_LEDAnim:
    
    def __init__(self,controller):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.Userform_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        self.Macro_str = "" 
        #*HL Center_Form(Me)
        
        self.Main_Menu_Form_RSC = {"UserForm":{
                        "Name"          : "MainMenuForm",
                        "BackColor"     : "#000008",
                        "BorderColor"   : "#000012",
                        "Caption"       : "LED Animation",
                        "Height"        : 629,
                        "Left"          : 0,
                        "Top"           : 0,
                        "Type"          : "MainWindow",
                        "Visible"       : True,
                        "Width"         : 842,
                        "Components":[{"Name":"Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"LED Animation\n\n ermöglicht die Animation einer LED-Beleuchtung. Für Einzel-LEDs und RGB-LEDS kann die Helligkeit gesteuert werden.",
                                        "ControlTipText":"Tooltip1","ForeColor":"#000012","Height":66,"Left":12,"SpecialEffect": "fmSpecialEffectSunken","TextAlign":"fmTextAlignLeft","Top":18,"Type":"Label","Visible":True,"Width":790},
                                      {"Name":"Label2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"by Harold Linke",
                                       "ControlTipText":"","ForeColor":"#FF0000","Height":12,"Left":318,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":100},
                                      {"Name":"LED_Address_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"LED Adressse",
                                       "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":90,"Type":"Label","Visible":True,"Width":348},
                                      {"Name":"LED_Address_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":90,"Type":"NumBox","Value": 1 ,"Visible":True,"Width":50},
                                      {"Name": "Frame1","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                       "Caption"       : "LEDtyp",
                                       "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 112,"Type": "Frame","Visible": True,"Width": 154,
                                       "Components"    :
                                            [
                                            {"Name":"LEDType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"LEDTyp:",
                                             "ControlTipText":"LEDtyp",
                                             "ForeColor":"#FF0000","Height":18,"Left":72,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                            {"Name":"LED_Type_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"LEDtyp",
                                             "ControlTipText":" LEDtyp:\nRGB LED (nur weiß)\nLED1 (Rot): mit WS2811 am roten Anschluß\nLED2 (Grün): mit WS2811 am grünen Anschluß\nLED3(Blau): mit WS2811 am blauen Anschluß",
                                             "ForeColor":"#FF0000","Height":44,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0, "SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["RGB LED", "LED1 (Rot)", "LED2 (Grün)", "LED3 (Blau)"] ,"Visible":True,"Width":60},
                                        ]}, 
                                        {"Name": "Frame4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "EIN-schalt Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 178,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [{"Name":"LED_PauseS_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Startpause (msec)",
                                              "ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_PauseS_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                             {"Name":"LED_DauerEin_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Dauer EIN (msec)",
                                               "ControlTipText":"Dauer der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_DauerEin_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Dauer der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":30,"Type":"NumBox","Value": 2500 ,"Visible":True,"Width":50},
                                             {"Name":"LED_PauseE_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Endepause (msec)",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":148},
                                              {"Name":"LED_PauseE_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                            ]},
                                        {"Name": "Frame5","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "AUS-schalt Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 266,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [{"Name":"LED_PauseS_Aus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Startpause (msec)",
                                              "ControlTipText":"Pause bevor die Ausschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_PauseS_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Pause bevor die Ausschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                             {"Name":"LED_DauerAus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Dauer AUS (msec)",
                                               "ControlTipText":"Dauer der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_DauerAus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Dauer der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":30,"Type":"NumBox","Value": 2500 ,"Visible":True,"Width":50},
                                             {"Name":"LED_PauseE_Aus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Endepause (msec)",
                                               "ControlTipText":"Pause am Ende der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":148},
                                              {"Name":"LED_PauseE_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Pause am Ende der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                             ]},
                                        {"Name": "Frame6","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Kurven Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 354,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                            
                                             {"Name":"LEDCurveType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Kurventyp:",
                                              "ControlTipText":"Kurventyp der Sequenz",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_CurveType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Kurventyp",
                                              "ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nLinear\nBeschleunigung\nIndividuell",
                                              "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Linear", "Beschleunigung", "Individuell"] ,"Visible":True,"Width":60},
                                             {"Name":"LED_Anfangswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Anfangshelligkeit (0..255)",
                                              "ControlTipText":"Anfangswert (0..255)",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":45,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_Anfangswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Anfangshelligkeit (0..255)",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":45,"Type":"NumBox","Value": 20 ,"Visible":True,"Width":50},
                                             {"Name":"LED_Endwert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Endhelligkeit (0..255)",
                                              "ControlTipText":"Endhelligkeit (0..255)",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":69,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_Endwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Endhelligkeit (0..255)",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":69,"Type":"NumBox","Value": 220 ,"Visible":True,"Width":50},
                                             {"Name":"Ueberblendung","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"ARDUINO Überblendung AUS",
                                              "ControlTipText":"ARDUINO interne Überblendung zwischen den Werten NICHT nutzen (zum Testen)","ForeColor":"#000012","Height":12,"Left":12,"Top":194,"Type":"CheckBox","Visible":True,"Width":160,"AlternativeText":""},
                                             ]},
                                        {"Name": "Frame7","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Ausführung Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 464,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                                
                                             {"Name":"LEDRunType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung:",
                                              "ControlTipText":"Art der Ausführung der Sequenz",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_RunType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung",
                                              "ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nWiederholen: EIN und AUS-Sequenz werden automatisch wiederholt.\nPingPong: Die EIN-Sequenz wird vorwärts und rückwärts abgespielt\nEin/Aus: Beim Einschalten wird die EIN-Sequenz, beim Ausschalten die AUS-Sequenz EINMAL abgespielt",
                                              "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Wiederholen", "PingPong", "Ein/Aus"] ,"Visible":True,"Width":60},
                                             ]},
                                        {"Name": "Frame3","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Zeitstufen Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 522,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [
                                            {"Name":"LEDTimeStepType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Art der Zeitstufen für die Sequenz",
                                             "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                            {"Name":"LED_TimeStepType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Wie sollen die Zeitstufen ermittelt werden \nAutomatisch \nFester Wert",
                                             "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 1,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Automatisch", "Fester Wert"] ,"Visible":True,"Width":60},
                                            {"Name":"LED_Abstand_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Stufenabstand (msec)",
                                              "ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den LED gesendet werden.",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":45,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_Abstand_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den LED gesendet werden.",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":45,"Type":"NumBox","Value": 500 ,"Visible":True,"Width":50},
                                             ]},                                                            
                                      {"Name": "Frame2","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                       "Caption"       : "Kurvenverlauf",
                                       "ControlTipText": "","ForeColor": "#000012","Height": 430,"Left": 170,"Top": 112,"Type": "Frame","Visible": True,"Width": 580,
                                       "Components"    :
                                            [
                                                ]},
                                      {"Name":"OK_Button","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"OK",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":750,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Abort_Button","Accelerator":"h","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Abbrechen",
                                       "Command":self.Abort_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":666,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Update_Button","Accelerator":"h","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Update Grafik",
                                       "Command":self.Update_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":566,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      ]}
                        }
    def get_params_from_param_list(self, param_list):
        i = 0
        for param in param_list:
            if self.UI_paramlist[i].Type == "ListBox":
                self.UI_paramlist[i].Selection = param
            else:
                self.UI_paramlist[i].Value = param
            i += 1

    def create_paramstring_from_param_list(self, param_list):
        i = 0
        result_string = ""
        for param in param_list:
            if self.UI_paramlist[i].Type == "ListBox":
                result_string = result_string + str(self.UI_paramlist[i].Selection)
            else:
                result_string = result_string + str(self.UI_paramlist[i].Value)
            if i < len(param_list) - 1:
                result_string = result_string + ","
            i += 1
        return result_string
    
    def calculate_on_off_line(self):
        time_val =  self.LED_DauerEin_TextBox.Value + self.LED_PauseS_Ein_TextBox.Value + self.LED_PauseE_Ein_TextBox.Value
        return time_val
    
    def determine_curve_points_from_Macro(self, Macro_str):
        curve_points = []
        macro_str_lines = Macro_str.split("\n")
        if len(macro_str_lines) == 3:
            pattern_macro_complete = macro_str_lines[2]
            pattern_macro_split = pattern_macro_complete.split(" ") # split into macro and gotoact part
            pattern_macro_params = pattern_macro_split[0].split(",")
            timestep = int(pattern_macro_params[8])
            param_idx = 9
            curr_time = 0
            while param_idx < len(pattern_macro_params):
                curve_points.append([curr_time, int(pattern_macro_params[param_idx])])
                param_idx += 3
                curr_time += timestep
        return curve_points
        
    
    def __UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialise the form
        #Debug.Print vbCr & Me.Name & ": UserForm_Initialize"
        #Change_Language_in_Dialog(Me)
        #Center_Form(Me)
        self.Userform_Res = ""
        self.Form=XLF.generate_form(self.Main_Menu_Form_RSC,self.controller,dlg=self, jump_table=PG.ThisWorkbook.jumptable, defaultfont=X02.DefaultFont)
        self.patterntype = 0
        self.curvetype = 0
        self.curve_points = []
        self.start_value = ()
        self.UI_paramlist = [
            self.LED_RunType_ListBox, 
            self.LED_CurveType_ListBox,
            self.LED_Abstand_TextBox, 
            self.LED_Anfangswert_TextBox, 
            self.LED_Endwert_TextBox, 
            self.LED_DauerEin_TextBox,
            self.LED_DauerAus_TextBox, 
            self.LED_PauseS_Ein_TextBox, 
            self.LED_PauseE_Ein_TextBox, 
            self.LED_PauseS_Aus_TextBox, 
            self.LED_PauseE_Aus_TextBox,
            self.LED_TimeStepType_ListBox,
            self.LED_Type_ListBox
        ]
        if self.Macro_str != "":
            # read parameters from Macrostring
            if self.Macro_str.find("#LEDAnim") != -1:
                macro_parts = self.Macro_str.split("(")
                if len(macro_parts) >= 2:
                    param1_string = macro_parts[1]
                    param1_parts = param1_string.split(")")
                    if len(param1_parts) >= 2:
                        param_string = param1_parts[0]
                        self.param_list = param_string.split(",")
                        if len(self.param_list) >=7:
                            #self.patterntype = param_list[0]
                            #self.curvetype = param_list[1]
                            self.get_params_from_param_list(self.param_list)
                            self.patterntype = self.LED_RunType_ListBox.Selection
                            self.curvetype = self.LED_CurveType_ListBox.Selection
                            self.LEDtype = self.LED_Type_ListBox.Selection 

        #anzahl_werte_Ein = int(self.LED_DauerEin_TextBox.Value / self.LED_Abstand_TextBox.Value)
        #if self.patterntype != 1: # Not PINGPONG Ausschaltsequenz anhängen
        #    anzahl_werte_Aus = int(self.LED_DauerAus_TextBox.Value / self.LED_Abstand_TextBox.Value)
        #else:
        #    anzahl_werte_Aus = 0
        #anzahl_werte = anzahl_werte_Ein + anzahl_werte_Aus +1
        if self.LED_TimeStepType_ListBox.Selection == 0: # automatic
            self.LED_Abstand_TextBox.Value = int(self.LED_DauerEin_TextBox.Value / 4)
        if self.curvetype == 2: # individuel
            self.curve_points = self.determine_curve_points_from_Macro(self.Macro_str)
            
        self.canvas = self.init_graph(frame=self.Frame2.TKWidget)
        self.curve_points = self.calculate_complete_curve()
        anzahl_werte = len(self.curve_points) - 1
        on_off_line =  self.calculate_on_off_line()
        self.draw_graph(num_horizontal=anzahl_werte, graph=self.curve_points, on_off_line=on_off_line)
        self.controller.connect_if_not_connected()
        self.controller.ARDUINO_begin_direct_mode()

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
    
    def Show_With_Existing_Data(self, MacroName, ConfigLine, LED_Channel, Def_Channel):
        Txt = String()
        #----------------------------------------------------------------------------------------------------------------------
        #self.__SetMode(MacroName)
        self.__LED_CntList = ''
        #self.IndividualTimes_CheckBox_svar.set(False)
        #self.show() #*HL
        self.Macro_str = ConfigLine
        self.Show()
        
    def calculate_accell_curve(self, duration, start_val, end_val, start_time, time_distance, skip_first=False):
        curve_points = []
        a = 2 * (end_val - start_val) / (duration * duration)
        if skip_first:
            t = time_distance
        else:
            t = 0
        while t <= duration:
            val = int(round(0.5 * a * t * t, 0)) + start_val
            curve_points.append((t+start_time, val))
            t += time_distance
        return curve_points        
        
    def calculate_linear_curve(self, duration, start_val, end_val, start_time, time_distance, skip_first=False):
        curve_points = []
        if skip_first:
            t = time_distance
        else:
            t = 0
        steigung =  (end_val - start_val) / duration
        while t <= duration:
            val = int(round(steigung * t + start_val, 0))
            curve_points.append((t+start_time, val))
            t += time_distance
        return curve_points
    
    def calculate_pause_curve(self, duration, val, start_time, time_distance, skip_first=False):
        curve_points = []
        if skip_first:
            t = time_distance
        else:
            t = 0
        while t <= duration: 
            curve_points.append((t+start_time, val))
            t += time_distance
        return curve_points
    
    def calculate_curve(self, duration, start_val, end_val, start_time, time_distance, pauseS=None, pauseE=None, skip_first=False):
        if pauseS != None and pauseS > 0:
            point_list1 = self.calculate_pause_curve(pauseS, start_val, start_time, time_distance, skip_first=skip_first)
            start_time += pauseS
        else:
            point_list1 = []
        if point_list1 != []:
            skip_first = True
        if self.curvetype == 0: # linear
            point_list2 = self.calculate_linear_curve(duration, start_val, end_val, start_time, time_distance, skip_first=skip_first)
        elif self.curvetype == 1: # Beschleunigung
            point_list2 = self.calculate_accell_curve(duration, start_val, end_val, start_time, time_distance, skip_first=skip_first)
        else: # individuell
            point_list2 = []
        point_list1.extend(point_list2)
        if point_list1 != []:
            skip_first = True
        start_time += duration
        if pauseE != None and pauseE > 0:
            point_list3 = self.calculate_pause_curve(pauseE, end_val, start_time, time_distance, skip_first=skip_first)
        else:
            point_list3 = []
        point_list1.extend(point_list3)
        return point_list1
    
    def calculate_complete_curve(self):
        self.curvetype = self.LED_CurveType_ListBox.Selection
        self.patterntype = self.LED_RunType_ListBox.Selection
        if self.curvetype != 2: # individuel
            curve_points = self.calculate_curve(self.LED_DauerEin_TextBox.Value, self.LED_Anfangswert_TextBox.Value, self.LED_Endwert_TextBox.Value, 0 , self.LED_Abstand_TextBox.Value, pauseS=self.LED_PauseS_Ein_TextBox.Value, pauseE=self.LED_PauseE_Ein_TextBox.Value)
            if self.patterntype != 1:
                t = self.LED_PauseS_Ein_TextBox.Value + self.LED_DauerEin_TextBox.Value + self.LED_PauseE_Ein_TextBox.Value
                curve_points_Aus = self.calculate_curve(self.LED_DauerAus_TextBox.Value, self.LED_Endwert_TextBox.Value, self.LED_Anfangswert_TextBox.Value, t, self.LED_Abstand_TextBox.Value, pauseS=self.LED_PauseS_Aus_TextBox.Value, pauseE=self.LED_PauseE_Aus_TextBox.Value, skip_first=True) 
                curve_points.extend(curve_points_Aus)
        else:
            # check if curve points are in range 0 .. 255:
            for index, curve_point in enumerate(self.curve_points):
                if curve_point[1] > 255:
                    curve_point[1] = 255
                    self.curve_points[index] = curve_point
                if curve_point[1] < 0:
                    curve_point[1] = 0
                    self.curve_points[index] = curve_point
            curve_points = self.curve_points
    
    def OK_Button_Click(self):
        #------------------------------
        runtype = self.LED_RunType_ListBox.Selection
        self.curvetype =  self.LED_CurveType_ListBox.Selection 
        if runtype == 2: #"Ein/Aus":
            gotoaction = True
            self.patterntype_str = "PM_NORMAL"
        elif runtype == 1: #"PingPong":
            gotoaction = False
            self.patterntype_str = "PM_PINGPONG"
        else:
            gotoaction = False
            self.patterntype_str = "PM_NORMAL"
        self.curve_points = self.calculate_complete_curve()
        self.LEDtype = self.LED_Type_ListBox.Selection
        if self.LEDtype == 0:
            LED = "1"
        else:
            LEDtype_str = str(self.LEDtype)
            LED = "C"+LEDtype_str+"-"+LEDtype_str
         
        if gotoaction:
            self.Userform_Res = LED + "$// Activation: Binary #LEDAnim("
            self.Userform_Res = self.Userform_Res + self.create_paramstring_from_param_list (self.UI_paramlist)
            self.Userform_Res = self.Userform_Res + ")\n" + "Bin_InCh_to_TmpVar(#InCh, 1) \n"
        else:
            self.Userform_Res = LED + "$// #LEDAnim("
            self.Userform_Res = self.Userform_Res + self.create_paramstring_from_param_list (self.UI_paramlist)
            self.Userform_Res = self.Userform_Res + ")\n"
        
        if self.Ueberblendung.Value !=1:
            self.Userform_Res = self.Userform_Res + "A"
        self.Userform_Res = self.Userform_Res + "PatternT1(#LED,"
        
        if self.LEDtype==0 :
            self.Userform_Res = self.Userform_Res +"28,"
            anzahl_led = "3"
        else:
            self.Userform_Res = self.Userform_Res + str(27 +self.LEDtype)+","
            anzahl_led = "1"
        
        if gotoaction:
            self.Userform_Res = self.Userform_Res + "SI_LocalVar," + anzahl_led + ",0,128,0,"
        else:
            self.Userform_Res = self.Userform_Res + "#InCh," + anzahl_led + ",0,128,0,"

        self.Userform_Res = self.Userform_Res + self.patterntype_str
        self.Userform_Res = self.Userform_Res + "," + str(self.LED_Abstand_TextBox.Value)

        for point in self.curve_points:
            if anzahl_led == "3":
                self.Userform_Res = self.Userform_Res + "," + str(point[1]) + "," + str(point[1]) + "," + str(point[1])
            else:
                self.Userform_Res = self.Userform_Res + "," + str(point[1])
                
        total_points = len(self.curve_points)

        # goto action
        if gotoaction:
            anzahl_werte_Ein = int((self.LED_DauerEin_TextBox.Value + self.LED_PauseS_Ein_TextBox.Value + self.LED_PauseE_Ein_TextBox.Value) / self.LED_Abstand_TextBox.Value)
            anzahl_werte_Aus = int((self.LED_DauerAus_TextBox.Value + self.LED_PauseS_Aus_TextBox.Value + self.LED_PauseE_Aus_TextBox.Value)/ self.LED_Abstand_TextBox.Value) -2
            if anzahl_werte_Aus + anzahl_werte_Ein + 3 != total_points:
                logging.debug("UserForm_LEDAnim: Ok-ButtonClick-total_points wrong")
            self.Userform_Res = self.Userform_Res + "  "
            for i in range(anzahl_werte_Ein):
                self.Userform_Res = self.Userform_Res + ",0"
            self.Userform_Res = self.Userform_Res + ",63,128"
            for i in range(anzahl_werte_Aus):
                self.Userform_Res = self.Userform_Res + ",0"
            self.Userform_Res = self.Userform_Res + ",63"
            
        self.Userform_Res = self.Userform_Res + ')$0'
        #if self.__Mode == 'House':
        #    self.Userform_Res = self.Userform_Res + self.MinCnt_TextBox_svar.get() + ', ' + self.MaxCnt_TextBox_svar.get() + ', '
        #    if self.Analoge_Crossfade.get()=="1":
        #        self.Userform_Res = self.Userform_Res + self.OnTime_TextBox_svar.get() + ', ' + self.OffTime_TextBox_svar.get() + ', '
        #self.Userform_Res = self.Userform_Res + self.SelectedRooms_TextBox.get(1.0, tk.END+"-1c") + ')$' + self.LED_Channel_TextBox_svar.get()
        #Store_Pos(Me, HouseForm_Pos)
        #Unload(Me)        
        # To keep the last position of the dialog
        self.Hide()
        
    def Abort_Button_Click(self):
        #-----------------------------
        ## VB2PY (CheckDirective) VB directive took path 1 on 1
        #X02.Shell('Explorer https://wiki.mobaledlib.de/anleitungen/spezial/patterngenerator')
        self.Hide()
        self.Userform_Res = ""
        
    def Update_Button_Click(self):
        anzahl_werte_Ein = int((self.LED_PauseS_Ein_TextBox.Value + self.LED_DauerEin_TextBox.Value + self.LED_PauseE_Ein_TextBox.Value) / self.LED_Abstand_TextBox.Value)
        runtype = self.LED_RunType_ListBox.TKWidget.curselection()
        if runtype == ():
            self.pattertype = 0
        else:
            self.pattertype = runtype[0]
        if self.patterntype != 1: # PINGPONG Ausschaltsequenz anhängen
            anzahl_werte_Aus = int((self.LED_PauseS_Aus_TextBox.Value + self.LED_DauerAus_TextBox.Value + self.LED_PauseE_Aus_TextBox.Value)/ self.LED_Abstand_TextBox.Value)
        else:
            anzahl_werte_Aus = 0
        anzahl_werte = anzahl_werte_Ein + anzahl_werte_Aus +1
        
        if self.LED_TimeStepType_ListBox.Selection == 0: # automatic
            self.LED_Abstand_TextBox.Value = int(self.LED_DauerEin_TextBox.Value / 5)
        self.curve_points = self.calculate_complete_curve()
        anzahl_werte = len(self.curve_points) - 1
        on_off_line = self.calculate_on_off_line()
        horizontal_range = (self.curve_points[0][0],self.curve_points[-1][0])
        self.draw_graph(num_horizontal=anzahl_werte, graph=self.curve_points, on_off_line=on_off_line, horizontal_range=horizontal_range)
        
    def init_graph(self, frame=None, vertical_params=None, horizontal_params=None, num_vertical=None, num_horizontal=None):
        frame.update()
        # Get the actual width and height
        self.framewidth = frame.winfo_width()
        self.frameheight = frame.winfo_height() 
        self.graphTop = 40
        self.graphLeft = 40
        self.graphWidth = self.framewidth - self.graphLeft - 40
        self.graphHeight = self.frameheight - self.graphTop - 40

        canvas=tk.Canvas(frame,width=self.framewidth,height=self.frameheight,bg="white")
        canvas.grid(row=1, column=1)
        #canvas.bind("<Button-1>", self.on_click)
        #canvas.bind("<B1-Motion>", self.on_drag)
        return canvas
    

    def draw_point(self, x, y, xvalue, yvalue):
        python_green = "#00FF00"
        size = 4
        x1, y1 = (x - size), (y - size)
        x2, y2 = (x + size), (y + size)
        objid = self.canvas.create_oval(x1, y1, x2, y2, fill=python_green, tag=["point", x , y ,str(xvalue), str(yvalue)])
        #self.controller.ToolTip_canvas(self.canvas, objid, text="("+str(xvalue)+","+str(yvalue)+")",button_1=True)
        self.canvas.tag_bind(objid,"<Button-1>" ,lambda e,Object=objid:self.MouseButton1(e,Object))
        self.canvas.tag_bind(objid,"<ButtonRelease 1>",lambda e,Object=objid:self.MouseRelease1())
        
        # Event für Mausbewegung
        self.canvas.tag_bind(objid,"<B1-Motion>",lambda e,Object=objid:self.MouseMove(e,Object))
      
        
    def tx2cx(self, x):
        return self.graphLeft + x
    
    def ty2cy(self, y):
        return self.graphTop + self.graphHeight - y
    
    def cy2val(self,cy):
        ty = self.graphTop + self.graphHeight - cy
        val = ty / self.vertical_value_factor
        return val
    
    def draw_graph(self, line_params=None,  vertical_params=None, horizontal_params=None, num_vertical=8, num_horizontal=10, graph=None, vertical_range=(0, 256), horizontal_range=(0, 20000), on_off_line = 0):
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.tx2cx(0), self.ty2cy(0), self.tx2cx(self.graphWidth), self.ty2cy(self.graphHeight), width=4)
        # Print the grid lines
        s_color="#000000"
        s_width=1
        s_linedashed=""
        th_color="#000000"
        th_width=6
        gr_linedashed=""
        gr_color="#FF0000"
        gr_width=2
        th_linedashed=""        
        vertical_max = vertical_range[1] - vertical_range[0]
        if num_horizontal == 0:
            num_horizontal = 10
        #vertical_line_dist = int(self.graphHeight / num_vertical)
        horizontal_line_dist = int(self.graphWidth / num_horizontal)
        
        if graph != []:
            horizontal_max = graph[-1][0]
            self.horizontal_value_factor = self.graphWidth / horizontal_max
        else:
            self.horizontal_value_factor = 0
        
        self.vertical_value_factor = self.graphHeight / vertical_max
        vertical_line_dist = int(self.graphHeight  / num_vertical)
        
        horizontal_text_pos = self.graphHeight + 10
        
        cur_value = 0
        value_dist = int(vertical_max / num_vertical)
        for i in range (num_vertical+1):
            cur_y = cur_value * self.vertical_value_factor
            objid = self.canvas.create_line(self.tx2cx(0), self.ty2cy(cur_y), self.tx2cx(self.graphWidth), self.ty2cy(cur_y), width=s_width, fill=s_color,dash=s_linedashed,tag="Grid")
            text_objid = self.canvas.create_text(20, self.ty2cy(cur_y), text = cur_value, width=30, fill=s_color,tag="Grid")
            cur_value += value_dist

        if graph != []:
            self.graph_points = []
            last_text_x = -40
            for i in range(len(graph)):
                value = graph[i][1]
                timestr = str(graph[i][0])
                timepoint = graph[i][0]
                cur_y = int((value * self.vertical_value_factor))
                cur_x = int(graph[i][0] * self.horizontal_value_factor)
                self.graph_points.extend([self.tx2cx(cur_x), self.ty2cy(cur_y)])
                # draw_vertical line
                objid = self.canvas.create_line(self.tx2cx(cur_x), self.ty2cy(0), self.tx2cx(cur_x), self.ty2cy(self.graphHeight), width=s_width, fill=s_color,dash=s_linedashed,tag="Grid")
                if cur_x - last_text_x >= 40:
                    text_objid = self.canvas.create_text(self.tx2cx(cur_x), self.ty2cy(horizontal_text_pos), text = timestr, width=30, fill=s_color,tag="Grid")
                    last_text_x = cur_x
                self.draw_point(self.tx2cx(cur_x), self.ty2cy(cur_y), timepoint, value)
                
            self.line_objid = self.canvas.create_line(self.graph_points, width=gr_width, fill=gr_color,dash=gr_linedashed,tag="Line")
            # create EIN/AUS Line
            if on_off_line > 0:
                cur_x = on_off_line * self.horizontal_value_factor
                objid = self.canvas.create_line(self.tx2cx(cur_x), self.ty2cy(0), self.tx2cx(cur_x), self.ty2cy(self.graphHeight), width=th_width, fill=th_color,dash=th_linedashed,tag="Grid")
        
        self.canvas.tag_raise("Line")
        self.canvas.tag_raise("point")
        
    def MouseButton1(self,event,cvobject):
        if self.LED_CurveType_ListBox.Selection == 2: # individuel
            tags = self.canvas.gettags(cvobject)
            objecttype = tags[0]
            if objecttype == "point":
                self.start_value= (tags[1], tags[2], tags[3], tags[4])
                self.canvas.startxy = (event.x, event.y)
            else:
                self.start_value = ()

    def MouseMove(self,event,cvobject):
        if self.start_value != ():
            dx, dy = event.x-self.canvas.startxy[0], event.y-self.canvas.startxy[1]
            # move the selected item
            self.canvas.move(cvobject, 0, dy)
            # update last position
            self.canvas.startxy = (self.canvas.startxy[0], event.y)
            # update graph points:
            search_x = int(self.start_value[0])
            for index, point in enumerate(self.graph_points):
                if index % 2 == 0 and point == search_x:
                    self.graph_points[index+1] += dy
                    self.current_curve_point = [self.curve_points[int(index/2)][0], int(self.cy2val(event.y))]
                    self.curve_points[int(index/2)] = self.current_curve_point
                    #self.get_led_value_and_send_to_ARDUINO()
                    #print(self.current_curve_point)
                    break
            self.canvas.coords(self.line_objid,self.graph_points)
            
            
    def MouseRelease1(self):
        # update line
        # update graphpoints
        # update graph
        if self.start_value != ():
            self.get_led_value_and_send_to_ARDUINO()
        self.start_value = ()
        
    def get_led_value_and_send_to_ARDUINO(self):
        new_LED_val = self.current_curve_point[1]
        if new_LED_val > 255:
            new_LED_val = 255
        elif new_LED_val < 0:
            new_LED_val = 0
            
        LED_address = self.LED_Address_TextBox.Value
        self.LEDtype = self.LED_Type_ListBox.Selection
        if self.LEDtype == 0:
            self._update_LEDs(LED_address,new_LED_val, new_LED_val, new_LED_val)
        elif self.LEDtype == 1:
            self._update_LEDs(LED_address,new_LED_val, 0, 0)
        elif self.LEDtype == 2:
            self._update_LEDs(LED_address,0, new_LED_val, 0)
        else:
            self._update_LEDs(LED_address,0, 0, new_LED_val)        
                
    def on_click(self, event):
        selected = self.canvas.find_overlapping(event.x-10, event.y-10, event.x+10, event.y+10)
        if selected:
            self.canvas.selected = selected[-1]  # select the top-most item
            self.canvas.startxy = (event.x, event.y)
            #print(self.canvas.selected, self.canvas.startxy)
        else:
            self.canvas.selected = None
    
    def on_drag(self, event):
        if self.canvas.selected:
            # calculate distance moved from last position
            dx, dy = event.x-self.canvas.startxy[0], event.y-self.canvas.startxy[1]
            # move the selected item
            self.canvas.move(self.canvas.selected, dx, dy)
            # update last position
            self.canvas.startxy = (event.x, event.y)
            
    def _update_LEDs(self, lednum, red_value, green_value, blue_value):
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(red_value) + " " + '{:02x}'.format(green_value) + " " + '{:02x}'.format(blue_value) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:02x}'.format(lednum) + " " + '{:02x}'.format(red_value) + " " + '{:02x}'.format(green_value) + " " + '{:02x}'.format(blue_value) + " " + '{:04x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        time.sleep(0.2)    

    


