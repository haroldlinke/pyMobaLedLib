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

runtype_pingpong = 1
runtype_on_off = 2
runtype_repeat = 0

curvetype_linear = 0
curvetype_accel = 1
curvetype_individuell = 2

timesteptype_auto = 0
timesteptype_fix = 1
timesteptype_individuell = 2

class UserForm_LEDColorAnim(UA.UserForm_Animation):
    
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
                        "Caption"       : "LED Farb-Animation",
                        "Height"        : 629,
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
                                      {"Name":"LED_Address_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"LED Adressse",
                                       "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":90,"Type":"Label","Visible":True,"Width":348},
                                      {"Name":"LED_Address_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"LED Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":90,"Type":"NumBox","Value": 1 ,"Visible":True,"Width":50},
                                      {"Name": "Frame4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "EIN-schalt Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 90,"Left": 6,"Top": 112,"Type": "Frame","Visible": True,"Width": 154,
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
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":30,"Type":"NumBox","Value": 6000 ,"Visible":True,"Width":50},
                                             {"Name":"LED_PauseE_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Endepause (msec)",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":148},
                                              {"Name":"LED_PauseE_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                            ]},
                                        {"Name": "Frame6","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Kurven Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 300,"Left": 6,"Top": 210,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                            
                                             {"Name":"LEDCurveType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Farbverlauf:",
                                              "ControlTipText":"Farbverlauf",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_CurveType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Farbverlauf",
                                              "ControlTipText":"Wie soll der automatische Farbverlauf aussehen: \nAufsteigend\nAbsteigend\nIndividuell",
                                              "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Aufsteigend", "Absteigend", "Individuell"] ,"Visible":True,"Width":60},
                                             {"Name": "Frame61","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                              "Caption"       : "Startfarbe",
                                              "ControlTipText": "","ForeColor": "#000012","Height":90,"Left": 6,"Top": 45,"Type": "Frame","Visible": True,"Width": 154,
                                              "Components"    :
                                                   [
                                                    {"Name":"LED_AnfangsFarbwert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Farbton (0..255)",
                                                     "ControlTipText":"Startfarbton (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                                    {"Name":"LED_AnfangsFarbwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Startfarbton (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                                    {"Name":"LED_AnfangsSättigungswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Sättigung (0..255)",
                                                     "ControlTipText":"Startfarbton (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":148},
                                                    {"Name":"LED_AnfangsSättigungswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Startsättigung (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":30,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":50},
                                                    {"Name":"LED_AnfangsHelligkeitswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Helligkeit (0..255)",
                                                     "ControlTipText":"Starthelligkeit (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":148},
                                                    {"Name":"LED_AnfangsHelligkeitswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Starthelligkeit (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":50},
                                                    ]},
                                             {"Name": "Frame62","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                              "Caption"       : "Endefarbe",
                                              "ControlTipText": "","ForeColor": "#000012","Height":90,"Left": 6,"Top": 141,"Type": "Frame","Visible": True,"Width": 154,
                                              "Components"    :
                                                   [
                                                    {"Name":"LED_EndFarbwert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Farbton (0..255)",
                                                     "ControlTipText":"Endefarbton (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                                    {"Name":"LED_EndFarbwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Endefarbton (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                                    {"Name":"LED_EndSättigungswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Sättigung (0..255)",
                                                     "ControlTipText":"Endefarbton (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":148},
                                                    {"Name":"LED_EndSättigungswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Endesättigung (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":30,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":50},
                                                    {"Name":"LED_EndHelligkeitswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"Helligkeit (0..255)",
                                                     "ControlTipText":"Endehelligkeit (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":148},
                                                    {"Name":"LED_EndHelligkeitswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     "Caption":"",
                                                     "ControlTipText":"Endehelligkeit (0..255)",
                                                     "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 255 ,"Visible":True,"Width":50},
                                                    ]},                                             
                                             ]},
                                        {"Name": "Frame7","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Ausführung Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 60,"Left": 6,"Top": 460,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                                
                                             {"Name":"LEDRunType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung:",
                                              "ControlTipText":"Art der Ausführung der Sequenz",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"LED_RunType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung",
                                              "ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nWiederholen: Die Sequenz wird automatisch wiederholt.\nPingPong: Die Sequenz wird vorwärts und rückwärts abgespielt",
                                              "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Wiederholen", "PingPong"] ,"Visible":True,"Width":60},
                                             ]},
                                        {"Name": "Frame3","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Zeitstufen Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 80,"Left": 6,"Top": 525,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [
                                            {"Name":"LEDTimeStepType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Art der Zeitstufen für die Sequenz",
                                             "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                            {"Name":"LED_TimeStepType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Wie sollen die Zeitstufen ermittelt werden \nAutomatisch \nIndividuell",
                                             "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Automatisch", "Individuell"] ,"Visible":True,"Width":60},
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
                                      {"Name":"OK_Button","Accelerator":"<Return>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"OK",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":666,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Abort_Button","Accelerator":"<Escape>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Abbrechen",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":566,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Update_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Update Grafik",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":466,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
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
    
    def get_params(self):
        self.get_params_from_param_list(self.param_list)
        self.patterntype = self.Servo_RunType_ListBox.Selection
        self.curvetype = self.Servo_CurveType_ListBox.Selection
        self.servotype = 0
        
    def create_UI_Paramlist(self):
        self.UI_paramlist = [
            self.LED_RunType_ListBox, 
            self.LED_CurveType_ListBox,
            self.LED_Abstand_TextBox, 
            self.LED_AnfangsFarbwert_TextBox,
            self.LED_AnfangsHelligkeitswert_TextBox,
            self.LED_AnfangsSättigungswert_TextBox, 
            self.LED_EndFarbwert_TextBox,
            self.LED_EndHelligkeitswert_TextBox,
            self.LED_EndSättigungswert_TextBox, 
            self.LED_DauerEin_TextBox,
            self.LED_PauseS_Ein_TextBox, 
            self.LED_PauseE_Ein_TextBox, 
            self.LED_TimeStepType_ListBox
        ]
        
    def calculate_linear_curve(self, duration, start_val, end_val, start_time, time_distance, up=True):
        curve_points = []
        if up:
            if end_val > start_val:
                steigung =  (end_val - start_val) / duration
                calc_jumptime = False
                jump_time = duration
            else:
                steigung = (256 - start_val + end_val) / duration
                calc_jumptime = True
                jump_time = round((256 - start_val) / steigung) + start_time
            # calculate time steps only 2 or 3 time steps: - start_time -> jumptime -> endtime
            curve_points.append((start_time, start_val))
            if calc_jumptime:
                jump_time = round((256 - start_val) / steigung) + start_time
                curve_points.append((jump_time, 255))
                curve_points.append((jump_time, 0))
            else:
                t = time_distance
                while t < duration:
                    val = int(round(steigung * t + start_val, 0))
                    curve_points.append((t+start_time, val))
                    t += time_distance                
        else:
            if start_val > end_val:
                steigung =  (end_val - start_val) / duration
                calc_jumptime = False
                jump_time = duration
            else:
                steigung = (256 - end_val + start_val) / duration
                calc_jumptime = True
                jump_time = round((start_val) / steigung) + start_time
            # calculate time steps only 2 or 3 time steps: - start_time -> jumptime -> endtime
            curve_points.append((start_time, start_val))
            if calc_jumptime:
                jump_time = round((start_val) / steigung) + start_time
                curve_points.append((jump_time, 0))
                curve_points.append((jump_time, 255))
            else:
                t = time_distance
                while t < duration:
                    val = int(round(steigung * t + start_val, 0))
                    curve_points.append((t+start_time, val))
                    t += time_distance                    
        curve_points.append((start_time+duration, end_val))
            
        #while t <= duration:
        #    val = int(round(steigung * t + start_val, 0))
        #    curve_points.append((t+start_time, val))
        #    t += time_distance
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
            point_list1 = self.calculate_pause_curve(pauseS, start_val, start_time, skip_first=False)
            start_time += pauseS
        else:
            point_list1 = []
        if self.curvetype == 0: # linear aufsteigend
            point_list2 = self.calculate_linear_curve(duration, start_val, end_val, start_time, time_distance, up=True)
        elif self.curvetype == 1: # linear aufsteigend
            point_list2 = self.calculate_linear_curve(duration, start_val, end_val, start_time, time_distance, up=False)
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
            curve_points = self.calculate_curve(self.LED_DauerEin_TextBox.Value, self.LED_AnfangsFarbwert_TextBox.Value, self.LED_EndFarbwert_TextBox.Value, 0 , self.LED_Abstand_TextBox.Value, pauseS=self.LED_PauseS_Ein_TextBox.Value, pauseE=self.LED_PauseE_Ein_TextBox.Value)
            if self.patterntype != 1:
                t = self.LED_PauseS_Ein_TextBox.Value + self.LED_DauerEin_TextBox.Value + self.LED_PauseE_Ein_TextBox.Value
        else:
            # check if curve points are in range 0 .. 255:
            for index, curve_point in enumerate(self.curve_points):
                if curve_point[1] > 255:
                    #self.add_jump(index, 0)
                    curve_point[1] = 255
                    self.curve_points[index] = curve_point
                elif curve_point[1] < 0:
                    #self.add_jump(index, 255)
                    curve_point[1] = 0
                    self.curve_points[index] = curve_point
                #else:
                    #if self.check_for_jump(index) == True:
                    #    if curve_point[1] > 0 and curve_point[1] < 255:
                    #        self.delete_jump(index)
            curve_points = self.curve_points
        return curve_points
        
    
    def OK_Button_Click(self, event=None):
        #------------------------------
        runtype = self.LED_RunType_ListBox.Selection
        self.curvetype =  self.LED_CurveType_ListBox.Selection 
        if runtype == 1: #"PingPong":
            self.patterntype_str = "PM_HSV"
        else: # Wiederholen
            self.patterntype_str = "PM_HSV"
        self.curve_points = self.calculate_complete_curve()
        self.LEDtype = 0 #self.LED_Type_ListBox.Selection
        if self.LEDtype == 0:
            LED = "1"
        else:
            LEDtype_str = str(self.LEDtype)
            LED = "C"+LEDtype_str+"-"+LEDtype_str
            
        total_points = len(self.curve_points)
        
        self.Userform_Res = LED + "$// #LEDColorAnim("
        self.Userform_Res = self.Userform_Res + self.create_paramstring_from_param_list (self.UI_paramlist)
        self.Userform_Res = self.Userform_Res + ")\n"
        
        #APatternT1(#LED,28,SI_LocalVar,3,0,128,0,PM_NORMAL,250,10,1,0,40,1,0,70,1,0,100,1,0,130,1,0,180,1,0,210,1,0,240,1,0,250,1,0,250,1,0,220,1,0,190,1,0,160,1,0,130,1,0,100,1,0,70,1,0,40,1,0,10,1,0  ,0,0,0,0,0,0,0,0,63,128,0,0,0,0,0,0,0,63)
        self.Userform_Res = self.Userform_Res + "A"
        self.Userform_Res = self.Userform_Res + "PatternT"+str(total_points)+"(#LED,"

        self.Userform_Res = self.Userform_Res +"28,"
        
        self.Userform_Res = self.Userform_Res + "#InCh,3,0,255,0,"

        self.Userform_Res = self.Userform_Res + self.patterntype_str
        
        timepoint_str = ""
        lasttimepoint = 0
        timepointdelta = 0
        s = self.LED_AnfangsSättigungswert_TextBox.Value
        v = self.LED_AnfangsHelligkeitswert_TextBox.Value
        
        for point in self.curve_points:
            timepoint = point[0]
            timepointdelta = timepoint - lasttimepoint
            timepoint_str += "," + str(timepointdelta)
            lasttimepoint = timepoint
                    
        self.Userform_Res = self.Userform_Res + timepoint_str # "," + str(self.LED_Abstand_TextBox.Value)

        for point in self.curve_points:
            #self.Userform_Res = self.Userform_Res + "," + str(point[1]) + "," + str(point[1]) + "," + str(point[1])
            self.Userform_Res = self.Userform_Res + "," + str(point[1]) + ","+str(s)+"," + str(v) # + str(point[1]) + "," + str(point[1])
                
        
            
        self.Userform_Res = self.Userform_Res + ')$0'
        self.Hide()
        
    def Abort_Button_Click(self, event=None):
        #-----------------------------
        ## VB2PY (CheckDirective) VB directive took path 1 on 1
        #X02.Shell('Explorer https://wiki.mobaledlib.de/anleitungen/spezial/patterngenerator')
        self.Hide()
        self.Userform_Res = ""
        
    def Update_Button_Click_1(self, event=None):
        anzahl_werte_Ein = int((self.LED_PauseS_Ein_TextBox.Value + self.LED_DauerEin_TextBox.Value + self.LED_PauseE_Ein_TextBox.Value) / self.LED_Abstand_TextBox.Value)
        runtype = self.LED_RunType_ListBox.TKWidget.curselection()
        if runtype == ():
            self.pattertype = 0
        else:
            self.pattertype = runtype[0]
        if self.LED_TimeStepType_ListBox.Selection == 0: # automatic
            self.LED_Abstand_TextBox.Value = int(self.LED_DauerEin_TextBox.Value / 5)
        self.curve_points = self.calculate_complete_curve()
        anzahl_werte = len(self.curve_points) - 1
        if anzahl_werte >= 1:
            horizontal_range = (self.curve_points[0][0],self.curve_points[-1][0])
        else:
            horizontal_range = (0,self.LED_PauseS_Ein_TextBox.Value + self.LED_DauerEin_TextBox.Value + self.LED_PauseE_Ein_TextBox.Value )
        self.draw_graph(num_horizontal=anzahl_werte, graph=self.curve_points, horizontal_range=horizontal_range)
        
    def init_graph_1(self, frame=None, vertical_params=None, horizontal_params=None, num_vertical=None, num_horizontal=None):
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
    

    def draw_point_1(self, x, y, xvalue, yvalue, color="00FF00"):
        size = 8
        x1, y1 = (x - size), (y - size)
        x2, y2 = (x + size), (y + size)
        objid = self.canvas.create_oval(x1, y1, x2, y2, fill=color, tag=["point", x , y ,str(xvalue), str(yvalue)])
        #self.controller.ToolTip_canvas(self.canvas, objid, text="("+str(xvalue)+","+str(yvalue)+")",button_1=True)
        self.canvas.tag_bind(objid,"<Button-1>" ,lambda e,Object=objid:self.MouseButton1(e,Object))
        self.canvas.tag_bind(objid,"<ButtonRelease 1>",lambda e,Object=objid:self.MouseRelease1())
        # Event für Mausbewegung
        self.canvas.tag_bind(objid,"<B1-Motion>",lambda e,Object=objid:self.MouseMove(e,Object))
      
        
    def tx2cx_1(self, x):
        return self.graphLeft + x
    
    def ty2cy_1(self, y):
        return self.graphTop + self.graphHeight - y
    
    def cy2val_1(self,cy):
        ty = self.graphTop + self.graphHeight - cy
        val = ty / self.vertical_value_factor
        return val
    
    def draw_graph_1(self, line_params=None,  vertical_params=None, horizontal_params=None, num_vertical=16, num_horizontal=10, graph=None, vertical_range=(0, 256), horizontal_range=(0, 20000)):
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.tx2cx(0), self.ty2cy(0), self.tx2cx(self.graphWidth), self.ty2cy(self.graphHeight), width=4)
        # Print the grid lines
        s_color="#000000"
        s_width=4
        s_linedashed="--"
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
            line_color = self.hsv_to_hexcolor(cur_value, 255, 255)
            objid = self.canvas.create_line(self.tx2cx(0), self.ty2cy(cur_y), self.tx2cx(self.graphWidth), self.ty2cy(cur_y), width=s_width, fill=line_color,dash=s_linedashed,tag="Grid")
            text_objid = self.canvas.create_text(20, self.ty2cy(cur_y), text = cur_value, width=30, fill=s_color,tag="Grid", font=X02.DefaultFont)
            cur_value += value_dist

        if graph != []:
            self.graph_points = []
            last_text_x = -40
            skip_next_point = False
            for i in range(len(graph)):
                value = graph[i][1]
                timestr = str(graph[i][0])
                timepoint = graph[i][0]
                cur_y = int((value * self.vertical_value_factor))
                cur_x = int(graph[i][0] * self.horizontal_value_factor)
                self.graph_points.extend([self.tx2cx(cur_x), self.ty2cy(cur_y)])
                # draw_vertical line
                objid = self.canvas.create_line(self.tx2cx(cur_x), self.ty2cy(0), self.tx2cx(cur_x), self.ty2cy(self.graphHeight), width=s_width, fill=s_color,dash=gr_linedashed,tag="Grid")
                if cur_x - last_text_x >= 40:
                    text_objid = self.canvas.create_text(self.tx2cx(cur_x), self.ty2cy(horizontal_text_pos), text = timestr, width=30, fill=s_color,tag="Grid", font=X02.DefaultFont)
                    last_text_x = cur_x
                if skip_next_point:
                    skip_next_point = False
                else:
                    h = value / 255. * 360
                    s = 100
                    v = 100
                    sel_color = hsv_to_rgb(h, s, v)
                    color = rgb_to_hexa(sel_color[0], sel_color[1], sel_color[2])
                    self.draw_point(self.tx2cx(cur_x), self.ty2cy(cur_y), timepoint, value, color=color)
                jump = self.check_for_jump(i)
                if jump == True:
                    skip_next_point = True
                
            self.line_objid = self.canvas.create_line(self.graph_points, width=gr_width, fill=gr_color,dash=gr_linedashed,tag="Line")
            # create EIN/AUS Line
        
        self.canvas.tag_raise("Line")
        self.canvas.tag_raise("point")
        
    def MouseButton1_1(self,event,cvobject):
        if self.LED_CurveType_ListBox.Selection == 2: # individuel
            tags = self.canvas.gettags(cvobject)
            objecttype = tags[0]
            if objecttype == "point":
                self.start_value= (tags[1], tags[2], tags[3], tags[4])
                self.canvas.startxy = (event.x, event.y)
            else:
                self.start_value = ()

    def MouseMove_1(self,event,cvobject):
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
            
    def MouseRelease1_1(self):
        # update line
        # update graphpoints
        # update graph
        if self.start_value != ():
            self.get_led_value_and_send_to_ARDUINO()
        self.start_value = ()
        #* redraw graph
        self.curve_points = self.calculate_complete_curve()
        anzahl_werte = len(self.curve_points) - 1
        horizontal_range = (self.curve_points[0][0],self.curve_points[-1][0])
        self.draw_graph(num_horizontal=anzahl_werte, graph=self.curve_points, horizontal_range=horizontal_range)        
        
    def get_led_value_and_send_to_ARDUINO(self, led_value=None):
        if led_value == None:
            if self.current_curve_point != None:
                new_LED_val = int(self.current_curve_point[1])
            else:
                return
        else:
            new_LED_val = led_value
        if new_LED_val > 255:
            new_LED_val = 255
        elif new_LED_val < 0:
            new_LED_val = 0
            LED_address = self.LED_Address_TextBox.Value
            h = new_LED_val
            s = self.LED_AnfangsSättigungswert_TextBox.Value
            v = self.LED_AnfangsHelligkeitswert_TextBox.Value
            r, g, b = self.hsv_to_LEDcolor(h, s, v)
            self._update_LEDs(LED_address,r, g, b)
                
    def on_click_1(self, event):
        selected = self.canvas.find_overlapping(event.x-10, event.y-10, event.x+10, event.y+10)
        if selected:
            self.canvas.selected = selected[-1]  # select the top-most item
            self.canvas.startxy = (event.x, event.y)
            #print(self.canvas.selected, self.canvas.startxy)
        else:
            self.canvas.selected = None
    
    def on_drag_1(self, event):
        if self.canvas.selected:
            # calculate distance moved from last position
            dx, dy = event.x-self.canvas.startxy[0], event.y-self.canvas.startxy[1]
            # move the selected item
            self.canvas.move(self.canvas.selected, dx, dy)
            # update last position
            self.canvas.startxy = (event.x, event.y)
            
    def _update_LEDs_1(self, lednum, red_value, green_value, blue_value):
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(red_value) + " " + '{:02x}'.format(green_value) + " " + '{:02x}'.format(blue_value) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:02x}'.format(lednum) + " " + '{:02x}'.format(red_value) + " " + '{:02x}'.format(green_value) + " " + '{:02x}'.format(blue_value) + " " + '{:04x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        time.sleep(0.2)    

    


