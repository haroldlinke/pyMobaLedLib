from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
#import ExcelAPI.XLC_Excel_Consts as X01
#import pattgen.M01_Public_Constants_a_Var as M01
import proggen.M09_Language as M09
#import pattgen.M08_Load_Sheet_Data
#import pattgen.M07_Save_Sheet_Data
#import pattgen.M30_Tools as M30
#import pattgen.M65_Special_Modules
#import pattgen.M80_Multiplexer_INI_Handling
import mlpyproggen.Pattern_Generator as PG
import proggen.Userform_Animation as UA
from tkcolorpicker.functions import hsv_to_rgb,  rgb_to_hexa

import ExcelAPI.XLF_FormGenerator as XLF
#import pattgen.D00_Forms as D00

import tkinter as tk
#from tkinter import ttk

import logging

def _T(text):
    new_text = M09.Get_Language_Str(text)
    return new_text

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


class UserForm_LEDColorAnim(UA.UserForm_Animation):
    
    def __init__(self,controller):
        super().__init__(controller, no_of_curves=3)
        
        self.Main_Menu_Form_RSC = {"UserForm":{
                        "Name"          : "MainMenuForm",
                        "BackColor"     : "#000008",
                        "BorderColor"   : "#000012",
                        "Caption"       : "LED Farb-Animation",
                        "Height"        : 800,
                        "Left"          : 0,
                        "Top"           : 0,
                        "Type"          : "MainWindow",
                        "Visible"       : True,
                        "Width"         : 842,
                        "Components":[{"Name":"Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"LED Farb-Animation\n\n ermöglicht die Animation der Farbe einer RGB-LED-Beleuchtung.",
                                        "ControlTipText":"Tooltip1","ForeColor":"#000012","Height":66,"Left":12,"SpecialEffect": "fmSpecialEffectSunken","TextAlign":"fmTextAlignLeft","Top":18,"Type":"Label","Visible":True,"Width":790},
                                      {"Name":"Label2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"by Harold",
                                       "ControlTipText":"","ForeColor":"#FF0000","Height":12,"Left":318,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":100},
                                      {"Name":"Anim_Address_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"LED Adressse",
                                       "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":90,"Type":"Label","Visible":True,"Width":348},
                                      {"Name":"Anim_Address_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":90,"Type":"NumBox","Value": 1 ,"Visible":True,"Width":50},
                                      {"Name":"Anim_Address_Kanal_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Anschluß-Kanal",
                                       "ControlTipText":"Kanal, an dem der Servo angeschlossen wird","ForeColor":"#FF0000","Height":18,"Left":238,"TextAlign":"fmTextAlignLeft","Top":90,"Type":"Label","Visible":True,"Width":100},
                                      {"Name":"Anim_Address_Kanal_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"Kanal, an dem der Servo angeschlossen wird","ForeColor":"#FF0000","Height":18,"Left":182,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":90,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                      {"Name": "Frame4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "EIN/Aus-schalt Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 90,"Left": 6,"Top": 112,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                         
                                            [{"Name":"Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"EIN",
                                              "ControlTipText":"",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":40},
                                             {"Name":"Aus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"AUS",
                                              "ControlTipText":"",
                                              "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":40},                                             
                                             {"Name":"Anim_PauseS_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Start(ms)",
                                              "ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":100,"TextAlign":"fmTextAlignLeft","Top":20,"Type":"Label","Visible":True,"Width":40},                                             
                                             {"Name":"Anim_PauseS_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":20,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":40},
                                             {"Name":"Anim_PauseS_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Pause bevor die Ausschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":20,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":40},                                             
                                             {"Name":"Anim_DauerEin_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Dauer (ms)",
                                               "ControlTipText":"Dauer der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":100,"TextAlign":"fmTextAlignLeft","Top":34,"Type":"Label","Visible":True,"Width":40},
                                             {"Name":"Anim_DauerEin_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Dauer der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":34,"Type":"NumBox","Value": 1000 ,"Visible":True,"Width":40},
                                             {"Name":"Anim_DauerAus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Dauer der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":34,"Type":"NumBox","Value": 1000 ,"Visible":True,"Width":40},                                             
                                             {"Name":"Anim_PauseE_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Ende(ms)",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":100,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":40},
                                              {"Name":"Anim_PauseE_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":40},
                                              {"Name":"Anim_PauseE_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":40},                                              
                                            ]},
                                        {"Name": "Frame6","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Kurven Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 155,"Left": 6,"Top": 212,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                            
                                             {"Name":"LEDCurveType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Farbverlauf:",
                                              "ControlTipText":"Farbverlauf",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_CurveType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Farbverlauf",
                                              "ControlTipText":"Wie soll der automatische Farbverlauf aussehen: \nLinear\nBeschleunigung\nIndividuell",
                                              "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Linear", "Beschleunigung", "Individuell"] ,"Visible":True,"Width":60},
                                             {"Name": "Frame61","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                              "Caption"       : "Farbe",
                                              "ControlTipText": "","ForeColor": "#000012","Height":90,"Left": 6,"Top": 45,"Type": "Frame","Visible": True,"Width": 154,
                                              "Components"    :
                                                   [
                                                    {"Name":"Start_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Start", 
                                                    "ControlTipText":"",
                                                    "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":40},
                                                   {"Name":"Ende_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Ende",
                                                    "ControlTipText":"",
                                                    "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":40},                                                        
                                                   {"Name":"Anim_Anfangswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Rot",
                                                    "ControlTipText":"StartRot(0..255)",
                                                    "ForeColor":"#FF0000","Height":18,"Left":100,"TextAlign":"fmTextAlignLeft","Top":20,"Type":"Label","Visible":True,"Width":148},                                                    
                                                    {"Name":"Anim_Anfangswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Rot",
                                                     "ControlTipText":"Start rote Farbe(0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":20,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":40},
                                                    {"Name":"Anim_Endwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Rot",
                                                     "ControlTipText":"Ende rote Farbe(0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":20,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":40},                                                    
                                                    {"Name":"Anim_AnfangsGwert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Grün",
                                                     "ControlTipText":"Start grüne Farbe (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":100,"TextAlign":"fmTextAlignLeft","Top":34,"Type":"Label","Visible":True,"Width":40},
                                                    {"Name":"Anim_AnfangsGwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Start grüne Farbe (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":34,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":40},
                                                    {"Name":"Anim_EndGwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Start grüne Farbe (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":34,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":40},                                                    
                                                    {"Name":"Anim_AnfangsBwert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":" Blau",
                                                     "ControlTipText":"Start blaue Farbe (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":100,"TextAlign":"fmTextAlignLeft","Top":48,"Type":"Label","Visible":True,"Width":40},
                                                    {"Name":"Anim_AnfangsBwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Start blaue Farbe (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":48,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":40},
                                                    {"Name":"Anim_EndBwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Start blaue Farbe (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":58,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":48,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":40},                                                    
                                                    ]},
                                             {"Name":"Ueberblendung","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"ARDUINO Überblendung AUS",
                                              "ControlTipText":"ARDUINO interne Überblendung zwischen den Werten NICHT nutzen (zum Testen)","ForeColor":"#000012","Height":12,"Left":12,"Top":430,"Type":"CheckBox","Visible":True,"Width":160,"AlternativeText":""},
                                             ]},
                                        {"Name": "Frame7","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Ausführung Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 80,"Left": 6,"Top": 370,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                                
                                             {"Name":"LEDRunType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung:",
                                              "ControlTipText":"Art der Ausführung der Sequenz",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_RunType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung",
                                              "ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nWiederholen: EIN und AUS-Sequenz werden automatisch wiederholt.\nPingPong: Die EIN-Sequenz wird vorwärts und rückwärts abgespielt\nEin/Aus: Beim Einschalten wird die EIN-Sequenz, beim Ausschalten die AUS-Sequenz EINMAL abgespielt",
                                              "ForeColor":"#FF0000","Height":44,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Wiederholen", "PingPong", "Ein/Aus", "HSV"] ,"Visible":True,"Width":60},
                                             ]},
                                        {"Name": "Frame3","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Zeitstufen Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 80,"Left": 6,"Top": 460,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [
                                            {"Name":"LEDTimeStepType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Art der Zeitstufen für die Sequenz",
                                             "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                            {"Name":"Anim_TimeStepType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Wie sollen die Zeitstufen ermittelt werden \nAutomatisch \nIndividuell",
                                             "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Automatisch", "Fix", "Individuell"] ,"Visible":True,"Width":60},
                                            {"Name":"Anim_Abstand_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Stufenabstand (msec)",
                                              "ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den LED gesendet werden.",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":45,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_Abstand_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
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
                                        {"Name":"Kurve_Zeit_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                         "Caption":"Zeit:",
                                         "ControlTipText":"Zeigt die  Zeit an, auf der der Mauszeiger steht",
                                         "ForeColor":"#FF0000","Height":18,"Left":170, "TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":40},
                                        {"Name":"Kurve_Zeitanzeige_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                         "Caption":"0",
                                         "ControlTipText":"Zeigt die  Zeit an, auf der der Mauszeiger steht",
                                         "ForeColor":"#FF0000","Height":18,"Left":210,"TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":40},                                      
                                        {"Name":"Kurve_Wert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                         "Caption":"Wert:",
                                         "ControlTipText":"Zeigt den Wert an, auf dem der Mauszeiger steht",
                                         "ForeColor":"#FF0000","Height":18,"Left":240, "TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":40},
                                        {"Name":"Kurve_Wertanzeige_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                         "Caption":"0",
                                         "ControlTipText":"Zeigt den Wert an, auf dem der Mauszeiger steht",
                                         "ForeColor":"#FF0000","Height":18,"Left":280,"TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":40},                                         
                                        
                                        {"Name":"Active_Curve_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                         "Caption":"Aktiv:",
                                         "ControlTipText":"Aktive Kurve",
                                         "ForeColor":"#FF0000","Height":18,"Left":300,"TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":40},
                                        {"Name":"Active_Curve_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                         "Caption":"",
                                         "ControlTipText":" Aktive Kurve:\nRot(H)\nGrün(S)\nBlau(V)",
                                         "ForeColor":"#FF0000","Height":44,"Left":330,"TextAlign":"fmTextAlignLeft","Selection": 0, "SpecialEffect": "fmSpecialEffectSunken","Top":570, "Type":"ListBox","Value": ["Rot", "Grün", "Blau"] ,"Visible":True,"Width":40},
                                                                        
                                      {"Name":"OK_Button","Accelerator":"<Return>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"OK",
                                       "Command":self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":680,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Abort_Button","Accelerator":"<Escape>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Abbrechen",
                                       "Command":self.Abort_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":600,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Update_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Update Grafik",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":520,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Test_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Starte Test",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":440,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Help_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Hilfe",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":380,"Top":570,"Type":"CommandButton","Visible":True,"Width":52},            
                                      ]}
                        }

    def hsv_to_hexcolor(self, h255, s255, v255):
        h360 = round((h255 *360) / 256.)
        s100 = round((s255 * 100) / 256.)
        v100 = round((v255 * 100) / 256.)
        sel_color = hsv_to_rgb(h360, s100, v100)
        color = rgb_to_hexa(sel_color[0], sel_color[1], sel_color[2])
        return color
    
    def hsv_to_LEDcolor(self, h256, s256, v256):
        h360 = round((h256 * 360)/ 256.)
        s100 = round(s256 * 100 / 256.)
        v100 = round(v256 * 100 / 256.)
        sel_color = hsv_to_rgb(h360, s100, v100)
        return sel_color[0], sel_color[1],  sel_color[2]        
        
    def check_for_jump(self, index):
        if index + 1 < len(self.curve_points):
            if self.curve_points[index+1][0] == self.curve_points[index][0]:
                return True
            else:
                return False
        else:
            return None
        
    def add_jump(self, index, value):
        jump = self.check_for_jump(index)
        if jump == None:
            return
        if not jump: # no jump here
            # add jump
            self.curve_points.insert(index+1, (self.curve_points[index][0], value))
            
    def delete_jump(self, index):
        jump = self.check_for_jump(index)
        if jump == None:
            return
        if jump: # jump found
            # remove jump
            del self.curve_points[index+1]
            
    def create_UI_Paramlist(self):
        self.UI_paramlist = [
            self.Anim_RunType_ListBox, 
            self.Anim_CurveType_ListBox,
            self.Anim_Abstand_TextBox, 
            self.Anim_Anfangswert_TextBox,
            self.Anim_AnfangsGwert_TextBox,
            self.Anim_AnfangsBwert_TextBox,
            self.Anim_Endwert_TextBox,
            self.Anim_EndGwert_TextBox,
            self.Anim_EndBwert_TextBox,
            self.Anim_DauerEin_TextBox,
            self.Anim_DauerAus_TextBox, 
            self.Anim_PauseS_Ein_TextBox, 
            self.Anim_PauseE_Ein_TextBox, 
            self.Anim_PauseS_Aus_TextBox, 
            self.Anim_PauseE_Aus_TextBox,
            self.Anim_TimeStepType_ListBox,
            self.Anim_Address_Kanal_TextBox,
            self.Anim_Address_TextBox]
        
    def determine_patterntype_str(self, patterntype_str):
        return patterntype_str

    def get_led_value_and_send_to_ARDUINO(self, led_value=None, led_g_value=None, led_b_value=None, point_idx=None):
        if led_value == None:
            if point_idx != None:
                new_LED_val = self.curve_points_ary[0][point_idx][1]
                if len(self.curve_points_ary) == 3:
                    led_g_value = self.curve_points_ary[1][point_idx][1]
                    led_b_value = self.curve_points_ary[2][point_idx][1]
            else:
                if self.current_curve_point != None:
                    new_LED_val = int(self.current_curve_point[1])
                else:
                    return
        else:
            new_LED_val = led_value
        if new_LED_val > self.value_max:
            new_LED_val = self.value_max
        elif new_LED_val < self.value_min:
            new_LED_val = self.value_min
    
        LED_address = self.Anim_Address_TextBox.Value
        LED_channel = self.Anim_Address_Kanal_TextBox.Value        
        r = new_LED_val
        if led_g_value:
            g = led_g_value
        else:
            g = self.Anim_AnfangsGwert_TextBox.Value
        if led_b_value:
            b = led_b_value
        else:
            b = self.Anim_AnfangsBwert_TextBox.Value
        if self.patterntype == UA.runtype_hsv:
            h = r
            s = g
            v = b
            r, g, b = self.hsv_to_LEDcolor(h, s, v)
        self._update_LEDs(LED_address,r, g, b, channel=LED_channel)

    def generate_pattern_data(self, anzahl_led, total_points_count, gotoaction):
        # goto action
        if gotoaction:
            dauer_ein = self.Anim_DauerEin_TextBox.Value + self.Anim_PauseS_Ein_TextBox.Value + self.Anim_PauseE_Ein_TextBox.Value
            for point_no in range(0, len(self.curve_points)):
                for i in range(0, 3):
                    color_value = self.curve_points_ary[i][point_no][1]
                    self.Userform_Res = self.Userform_Res + "," + str(color_value)
                
            self.Userform_Res = self.Userform_Res + "  "
            for i in range(total_points_count-2):
                if self.curve_points[i][0] == dauer_ein: 
                    self.Userform_Res = self.Userform_Res + ",63,128"
                else:
                    self.Userform_Res = self.Userform_Res + ",0"
            self.Userform_Res = self.Userform_Res + ",63"
            
        else:
            for point_no in range(0, len(self.curve_points)):
                for i in range(0, 3):
                    color_value = self.curve_points_ary[i][point_no][1]
                    self.Userform_Res = self.Userform_Res + "," + str(color_value)

        self.Userform_Res = self.Userform_Res + ')$' + str(self.Anim_Address_Kanal_TextBox.Value)


