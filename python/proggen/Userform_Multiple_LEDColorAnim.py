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
import proggen.Userform_Multi_Animation as UA
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


class UserForm_Multiple_LEDColorAnim(UA.UserForm_Multi_Animation):
    
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
                        "Geo_Manager" : "grid",
                        "Visible"       : True,
                        "Width"         : 842,
                        "Components":[{"Name":"Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Ermöglicht die Animation der Farbe von beliebig vielen RGB-LED-Beleuchtungen.\nEine Kurve kann bearbeitet werden, wenn sie unten als <Aktiv> ausgewählt wurde und mit <Update Grafik> übernommen wurde.\nKurvenmodus <Linear>/<>Beschleunigung>: Die Start- und Endwerte können über Anfasser an der Kurve geändert werden.\nKurvenmodus <Individuell>: alle Punkte können geändert werden. - <Einf>-Taste fügt neue Punkte hinzu - <Entf>-Taste löscht den aktuellen Punkt\nUm viele Zeitpunkte zu erzeugen, kann man vorher mit dem Zeitstufen Parameter <Fix> ein Zeitstufenraster zu erzeugen.", 
                                        "ControlTipText":"","ForeColor":"#000012","Height":None,"Left":0,"SpecialEffect": "fmSpecialEffectSunken","TextAlign":"fmTextAlignLeft","Top":0,"Type":"Label","Visible":True,"Width":130},
                                      {"Name": "Frame1","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "LED-Start-Adresse",
                                         "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 1,"Type": "Frame","Visible": True,"Width": None,
                                         "Components"    :
                                            [                                      
                                             {"Name":"Anim_Address_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"LED Adressse",
                                              "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":None,"Left":0,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":None},
                                            {"Name":"Anim_Address_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":None,"Left":1,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"NumBox","Value": 1 ,"Visible":True,"Width":5},
                                            {"Name":"Anim_Address_Kanal_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Anschluß-Kanal",
                                             "ControlTipText":"Kanal, an dem die LED angeschlossen wird","ForeColor":"#FF0000","Height":None,"Left":2,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":None},
                                            {"Name":"Anim_Address_Kanal_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                            "Caption":"",
                                             "ControlTipText":"Kanal, an dem die LED angeschlossen wird","ForeColor":"#FF0000","Height":None,"Left":3,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":5},
                                            {"Name":"Anim_No_of_Curves_TextBox_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Anzahl der LEDs",
                                             "ControlTipText":"Anzahl der LEDs","ForeColor":"#FF0000","Height":None,"Left":2,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":None},
                                            {"Name":"Anim_No_of_Curves_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "Command": "","ControlTipText":"Anzahl der LEDs","ForeColor":"#FF0000","Height":None,"Left":1,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 3 ,"Visible":True,"Width":5},
                                            ]},
                                      {"Name": "Frame0","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "",
                                         "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 2,"Type": "Frame","Visible": True,"Width": None,
                                         "Components"    :
                                            [                                          
                                      {"Name": "FrameL2","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "AnimationsParameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 2,"Type": "Frame","Visible": True,"Width": None,
                                         "Components"    :
                                            [
                                            {"Name": "FrameL2a","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               "Caption"       : "Animationsdauer",
                                               "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 2,"Type": "Frame","Visible": True,"Width": None,
                                               "Components"    :
                                                   [{"Name":"Anim_DauerEin_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Dauer der Einschaltanimation in msec",
                                                     "ForeColor":"#FF0000","Height":None,"Left":0,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 1000 ,"Visible":True,"Width":6},
                                                   ]},
                                              {"Name": "Frame2b","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               "Caption"       : "Kurven Parameter",
                                               "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 3,"Type": "Frame","Visible": True,"Width": None,
                                               "Components"    :
                                                    [                                                            
                                                   {"Name":"Anim_CurveType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Farbverlauf",
                                                    "ControlTipText":"Wie soll der automatische Farbverlauf aussehen: \nLinear\nBeschleunigung\nIndividuell",
                                                    "ForeColor":"#FF0000","Height":2,"Left":0,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Linear", "Beschleunigung", "Individuell"] ,"Visible":True,"Width":None},
                                                   {"Name":"Ueberblendung","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"ARDUINO Überblendung AUS",
                                                   "ControlTipText":"ARDUINO interne Überblendung zwischen den Werten NICHT nutzen (zum Testen)","ForeColor":"#000012","Height":None,"Left":0,"Top":430,"Type":"CheckBox","Visible":True,"Width":None,"AlternativeText":""},
                                                   ]},
                                              {"Name": "FrameL2c","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               "Caption"       : "Ausführung Parameter",
                                               "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 4,"Type": "Frame","Visible": True,"Width": None,
                                               "Components"    :
                                                    [                                                                
                                                   {"Name":"Anim_RunType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Ausführung",
                                                    "ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nWiederholen: Sequenz wird automatisch wiederholt.\nPingPong: Die Sequenz wird vorwärts und rückwärts abgespielt\nEin/Aus: Beim Einschalten wird die EIN-Sequenz, beim Ausschalten die AUS-Sequenz EINMAL abgespielt",
                                                    "ForeColor":"#FF0000","Height":3,"Left":0,"TextAlign":"fmTextAlignLeft","Scrollbar":"Yes","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["NORMAL", "SEQUENZ_W_RESTART","SEQUENZ_W_ABORT","SEQUENZ_NO_RESTART","SEQUENZ_STOP","PINGPONG","HSV"  ] ,"Visible":True,"Width":None},
                                                   {"Name":"PMSlow_Checkbox","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"4-Fach langsamer",
                                                   "ControlTipText":"Verlangsame die Animation um den Faktor 4","ForeColor":"#000012","Height":None,"Left":0,"Top":7,"Type":"CheckBox","Visible":True,"Width":None,"AlternativeText":""},
                                                   {"Name":"PMInvertInp_Checkbox","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"Invert Eingansschalter",
                                                   "ControlTipText":"Invertiere den Eingansschalter","ForeColor":"#000012","Height":None,"Left":1,"Top":7,"Type":"CheckBox","Visible":True,"Width":None,"AlternativeText":""}                                             
                                                   ]},
                                              {"Name": "FrameL2d","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               "Caption"       : "Zeitstufen Parameter",
                                               "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 5,"Type": "Frame","Visible": True,"Width": None,
                                               "Components"    :
                                                  [
                                                  {"Name":"LEDTimeStepType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"Zeitstufen",
                                                   "ControlTipText":"Art der Zeitstufen für die Sequenz",
                                                   "ForeColor":"#FF0000","Height":None,"Left":1,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":None},
                                                  {"Name":"Anim_TimeStepType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"Zeitstufen",
                                                   "ControlTipText":"Wie sollen die Zeitstufen ermittelt werden \nAutomatisch \nIndividuell",
                                                   "ForeColor":"#FF0000","Height":2,"Left":0,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Automatisch", "Fix", "Individuell"] ,"Visible":True,"Width":None},
                                                  {"Name":"Anim_Abstand_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"Stufenabstand (msec)",
                                                    "ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den LED gesendet werden.",
                                                    "ForeColor":"#FF0000","Height":None,"Left":1,"TextAlign":"fmTextAlignLeft","Top":45,"Type":"Label","Visible":True,"Width":None},
                                                   {"Name":"Anim_Abstand_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"",
                                                    "ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den LED gesendet werden. (Bei fix Abstand)",
                                                    "ForeColor":"#FF0000","Height":None,"Left":0,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":45,"Type":"NumBox","Value": 500 ,"Visible":True,"Width":6},
                                                   ]},
                                              {"Name": "FrameL2e","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               "Caption"       : "Linien-Parameter",
                                               "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 6,"Type": "Frame","Visible": True,"Width": None,
                                               "Components"    :
                                                  [
                                                  {"Name":"Anim_LEDcolor_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"Linienfarbe",
                                                   "ControlTipText":"Farbe der Linie",
                                                   "ForeColor":"#FF0000","Height":None,"Left":2,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":None},
                                                  {"Name":"Anim_LEDcolor_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"#000000",
                                                   "ControlTipText":"Farbe der Linie",
                                                   "ForeColor":"#FF0000","Height":1,"Left":0,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"TextBox","Value": "" ,"Visible":True,"Width":6},
                                                  {"Name":"Anim_LEDcolor_ColorBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"#000000",
                                                   "ControlTipText":"Farbe der Linie",
                                                   "ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ColorBox","Value": "" ,"Visible":True,"Width":6},                                            
                                                  {"Name":"Anim_LEDwidth_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"Linienbreite",
                                                   "ControlTipText":"Breite der Linie",
                                                   "ForeColor":"#FF0000","Height":None,"Left":1,"TextAlign":"fmTextAlignLeft","Top":7,"Type":"Label","Visible":True,"Width":None},
                                                  {"Name":"Anim_LEDwidth_NumBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   "Caption":"",
                                                   "ControlTipText":"Breite der Linie",
                                                   "ForeColor":"#FF0000","Height":1,"Left":0,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":7,"Type":"NumBox","Value": "2" ,"Visible":True,"Width":6},
                                                  {"Name":"Anim_LEDName_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"LED-Bezeichnung",
                                                    "ControlTipText":"Bezeichnung für die LED",
                                                    "ForeColor":"#FF0000","Height":None,"Left":1,"TextAlign":"fmTextAlignLeft","Top":45,"Type":"Label","Visible":True,"Width":None},
                                                   {"Name":"Anim_LEDName_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    "Caption":"",
                                                    "ControlTipText":"Bezeichnung für die LED",
                                                    "ForeColor":"#FF0000","Height":1,"Left":0,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":45,"Type":"TextBox","Value": "" ,"Visible":True,"Width":10},
                                                   ]},
                                            {"Name": "FrameL2f","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                             "Caption"       : "Goto Parameter",
                                             "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 0,"Top": 7,"Type": "Frame","Visible": True,"Width": None,
                                             "Components"    :
                                                  [                                                                
                                                 {"Name":"GotoRunType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                  "Caption":"Ausführung:",
                                                  "ControlTipText":"Art der Ausführung des Goto",
                                                  "ForeColor":"#FF0000","Height":None,"Left":2,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":None},
                                                 {"Name":"Anim_GotoType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                  "Caption":"Ausführung",
                                                  "ControlTipText":"Wie soll der Goto ausgeführt werden: ** noch nicht implementiert **",
                                                  "ForeColor":"#FF0000","Height":3,"Left":0,"TextAlign":"fmTextAlignLeft","Scrollbar":"Yes","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["No Goto", "N_Buttons","N_Buttons1","N_OneTimeBut","N_OneTimeBut1","Binary","Binary1","Counter","RandButton","RandomTime","RandomCount","RandomPingPong","Nothing" ] ,"Visible":True,"Width":None},
                                                 ]},                                               
                                              ]},
                                        {"Name": "FrameR2","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Kurvenverlauf",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 100,"Left": 1,"sticky": "nesw","Top": 2,"Type": "Frame","Visible": True,"Width": 400,
                                         "Components"    :
                                              [
                                                  ]},
                                        {"Name": "FrameR3","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Kurvenverlauf",
                                         "ControlTipText": "","ForeColor": "#000012","Height": None,"Left": 1, "Top": 3,"Type": "Frame","Visible": True,"Width": None,
                                         "Components"    :
                                              [
                                              {"Name":"Kurve_Zeit_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Zeit:",
                                               "ControlTipText":"Zeigt die  Zeit an, auf der der Mauszeiger steht",
                                               "ForeColor":"#FF0000","Height":None,"Left":170, "TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":None},
                                                {"Name":"Kurve_Zeitanzeige_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                 "Caption":"0",
                                                 "ControlTipText":"Zeigt die  Zeit an, auf der der Mauszeiger steht",
                                                 "ForeColor":"#FF0000","Height":None,"Left":210,"TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":5},
                                                {"Name":"Kurve_Wert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                 "Caption":"Wert:",
                                                 "ControlTipText":"Zeigt den Wert an, auf dem der Mauszeiger steht",
                                                 "ForeColor":"#FF0000","Height":None,"Left":240, "TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":None},
                                                {"Name":"Kurve_Wertanzeige_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                 "Caption":"0",
                                                 "ControlTipText":"Zeigt den Wert an, auf dem der Mauszeiger steht",
                                                 "ForeColor":"#FF0000","Height":None,"Left":280,"TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":4},
                                                {"Name":"Active_Curve_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                 "Caption":"Aktiv:",
                                                 "ControlTipText":"Aktive Kurve",
                                                 "ForeColor":"#FF0000","Height":None,"Left":300,"TextAlign":"fmTextAlignLeft","Top":570,"Type":"Label","Visible":True,"Width":None},
                                                {"Name":"Active_Curve_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                 "Caption":"", "Command": "", 
                                                 "ControlTipText":" Aktive Kurve auswählen",
                                                 "ForeColor":"#FF0000","Height":2,"Left":330,"TextAlign":"fmTextAlignLeft","Scrollbar": "Yes", "Selection": 0, "SpecialEffect": "fmSpecialEffectSunken","Top":570, "Type":"ListBox","Value": ["LED1", "LED2", "LED3"] ,"Visible":True,"Width":None},
                                                                                
                                              {"Name":"OK_Button","Accelerator":"<Return>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"OK",
                                               "Command":self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":2,"Left":680,"Top":570,"Type":"CommandButton","Visible":True,"Width":10},
                                              {"Name":"Abort_Button","Accelerator":"<Escape>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Abbrechen",
                                               "Command":self.Abort_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":2,"Left":600,"Top":570,"Type":"CommandButton","Visible":True,"Width":10},
                                              {"Name":"Update_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Update Grafik",
                                               "Command":"","ControlTipText":"","ForeColor":"#000012","Height":2,"Left":520,"Top":570,"Type":"CommandButton","Visible":True,"Width":10},
                                              {"Name":"Test_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Starte Test",
                                               "Command":"","ControlTipText":"","ForeColor":"#000012","Height":2,"Left":440,"Top":570,"Type":"CommandButton","Visible":True,"Width":10},
                                              {"Name":"Help_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Hilfe",
                                               "Command":"","ControlTipText":"","ForeColor":"#000012","Height":2,"Left":380,"Top":570,"Type":"CommandButton","Visible":True,"Width":10},            
                                              ]},
                                    ]},
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
            self.Active_Curve_ListBox, 
            self.Anim_Abstand_TextBox, 
            self.Anim_DauerEin_TextBox,
            self.Ueberblendung,
            self.Anim_TimeStepType_ListBox,
            self.Anim_Address_Kanal_TextBox,
            self.Anim_Address_TextBox,
            self.Anim_No_of_Curves_TextBox,
            self.Anim_Name_Color_str]
        
    def determine_patterntype_str(self, patterntype_str):
        return patterntype_str

    def get_led_value_and_send_to_ARDUINO(self, led_value_ary=None, led_value=None, led_g_value=None, led_b_value=None, point_idx=None):
        LED_address = self.Anim_Address_TextBox.Value
        LED_channel = self.Anim_Address_Kanal_TextBox.Value
        if led_value_ary == None:
            led_value_ary = []
            for i in range(0, self.no_of_curves):
                led_value_ary.append(self.curve_points_ary[i][point_idx][1])
        no_of_RGB_leds = int((self.no_of_curves-1) / 3) + 1
        curve_no = 0
        for RGB_LED in range (0, no_of_RGB_leds):
            new_LED_Address = LED_address + RGB_LED
            r = led_value_ary[curve_no]
            if (curve_no + 1 >= self.no_of_curves):
                g = 0
            else:
                g = led_value_ary[curve_no+1]
            if (curve_no + 2 >= self.no_of_curves):
                b = 0
            else:
                b = led_value_ary[curve_no+2]
            if self.patterntype == UA.runtype_hsv:
                h = r
                s = g
                v = b
                r, g, b = self.hsv_to_LEDcolor(h, s, v)
            self._update_LEDs(new_LED_Address,r, g, b, channel=LED_channel)
            curve_no += 3

    def generate_pattern_data(self, anzahl_led, total_points_count, gotoaction):
        # goto action
        if gotoaction:
            dauer_ein = self.Anim_DauerEin_TextBox.Value
            for point_no in range(0, len(self.curve_points)):
                for i in range(0, self.no_of_curves):
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
                for i in range(0, self.no_of_curves):
                    color_value = self.curve_points_ary[i][point_no][1]
                    self.Userform_Res = self.Userform_Res + "," + str(color_value)

        self.Userform_Res = self.Userform_Res + ')$' + str(self.Anim_Address_Kanal_TextBox.Value)


