from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
#import ExcelAPI.XLC_Excel_Consts as X01
#import pattgen.M01_Public_Constants_a_Var as M01
#import pattgen.M09_Language as M09
#import pattgen.M08_Load_Sheet_Data
#import pattgen.M07_Save_Sheet_Data
#import pattgen.M30_Tools as M30
#import pattgen.M65_Special_Modules
#import pattgen.M80_Multiplexer_INI_Handling
import mlpyproggen.Prog_Generator as PG
import proggen.Userform_Animation as UA

import ExcelAPI.XLF_FormGenerator as XLF
#import pattgen.D00_Forms as D00

import tkinter as tk
from tkinter import ttk

import logging
import pgcommon.CanvasFrame as CF

runtype_pingpong = 1
runtype_on_off = 2
runtype_repeat = 0

curvetype_linear = 0
curvetype_accel = 1
curvetype_individuell = 2

timesteptype_auto = 0
timesteptype_fix = 1
timesteptype_individuell = 2

class UserForm_ServoAnim(UA.UserForm_Animation):
    
    def __init__(self,controller):
        super().__init__(controller)
        
        #self.Main_Menu_Form_RSC_grid = {"UserForm":{
                        #"Name"          : "MainMenuForm",
                        #"BackColor"     : "#000008",
                        #"BorderColor"   : "#000012",
                        #"Caption"       : "Servo Animation",
                        #"Height"        : 629,
                        #"Left"          : 0,
                        #"Top"           : 0,
                        #"Type"          : "MainWindow",
                        #"Visible"       : True,
                        #"Width"         : 842,
                        #"Geo_Manager" : "grid",
                        #"Columnconfigure": 1,
                        #"Rowconfigure": 1,
                        #"Components":[{"Name": "TopFrame","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         #"Caption"       : "",
                                         #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 2,"Top": 1,"Type": "Frame","Visible": True,"Width": 20,
                                         #"Components"    :
                                                #[{"Name":"Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                #"Caption":"Unterstützt den Direkt Mode Servo von Eckhard (Servo DM) und die Normalen MLL-Servos (Servo1, Servo2 und Servo3)\nDurch Eingabe der Ein- und Ausschaltparameter wird der Zeitablauf bestimmt. Es stehen 3 Kurven-Modi zur Verfügung: Linear, Beschleunigung und Individuell. " +
                                                #"Die berechneten Kurven werden in der Grafik rechts angezeigt. Bei der Einstellung Individuell können die Kurvenwerte (Grüne Punkte) einzeln eingestellt werden. Wurde unter Servo-Adresse die Adresse des Servos angegeben, kann die Servostellung direkt überprüft werden.\n" +
                                                #"Beim Ausführen kann man wählen zwischen: Wiederholen-die Ein-und Ausschaltsequenz wird automatisch wiederholt, PingPong-die Sequenz wird vor- und zurück abgespielt, Ein/Aus: Bei Schalter auf EIN wird die Einschaltsequenz, bei Schalter auf AUS, wird die Auschaltsequenz abgespielt.",
                                                 #"ControlTipText":"Tooltip1","ForeColor":"#000012","Height":4,"Left":3,"SpecialEffect": "fmSpecialEffectSunken","TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":100},
                                               #{"Name":"Label2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                #"Caption":"by Harold Linke",
                                                #"ControlTipText":"","ForeColor":"#FF0000","Height":1,"Left":4,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":20},
                                               #{"Name":"Anim_Address_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                #"Caption":"Servo Adressse",
                                                #"ControlTipText":"Servo Adresse für Test","ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":20},
                                               #{"Name":"Anim_Address_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                #"Caption":"",
                                                #"ControlTipText":"Servo Adresse für Test","ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 1 ,"Visible":True,"Width":10},
                                               #{"Name":"Anim_Address_Kanal_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                #"Caption":"Anschluß-Kanal",
                                                #"ControlTipText":"Kanal, an dem der Servo angeschlossen wird","ForeColor":"#FF0000","Height":1,"Left":3,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":20},
                                               #{"Name":"Anim_Address_Kanal_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                #"Caption":"",
                                                #"ControlTipText":"Kanal, an dem der Servo angeschlossen wird","ForeColor":"#FF0000","Height":1,"Left":4,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":10},
                                      #]},
                                      #{"Name": "LeftFrame","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                       #"Caption"       : "",
                                       #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 1,"Top":2 ,"Type": "Frame","Visible": True,"Width": 20, "sticky": "nesw",
                                       #"Components"    :
                                            #[                                      
                                            #{"Name": "Frame1","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                             #"Caption"       : "Servotyp",
                                             #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 1,"Top": 3,"Type": "Frame","Visible": True,"Width": 20,
                                             #"Components"    :
                                                  #[
                                                  #{"Name":"ServoType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   #"Caption":"ServoTyp:",
                                                   #"ControlTipText":"Servotyp",
                                                   #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":20},
                                                  #{"Name":"Anim_Type_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   #"Caption":"Servotyp",
                                                   #"ControlTipText":" Servotyp:\nServo DM: Servo mit Direct Mode\nServo1 (Rot): mit WS2811 am roten Anschluß\nServo2 (Grün): mit WS2811 am grünen Anschluß\nServo3(Blau): mit WS2811 am blauen Anschluß",
                                                   #"ForeColor":"#FF0000","Height":3,"Left":2,"TextAlign":"fmTextAlignLeft","Selection": 0, "SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"ListBox","Value": ["Servo DM", "Servo1 (Rot)", "Servo2 (Grün)", "Servo3 (Blau)"] ,"Visible":True,"Width":20},
                                              #]}, 
                                              #{"Name": "Frame4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               #"Caption"       : "EIN-schalt Parameter",
                                               #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 1,"Top": 4,"Type": "Frame","Visible": True,"Width": 20,
                                               #"Components"    :
                                                  #[{"Name":"Anim_PauseS_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Startpause (msec)",
                                                    #"ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_PauseS_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"",
                                                    #"ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":10},
                                                   #{"Name":"Anim_DauerEin_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"Dauer EIN (msec)",
                                                     #"ControlTipText":"Dauer der Einschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_DauerEin_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"",
                                                     #"ControlTipText":"Dauer der Einschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 2500 ,"Visible":True,"Width":10},
                                                   #{"Name":"Anim_PauseE_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"Endepause (msec)",
                                                     #"ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":3,"Type":"Label","Visible":True,"Width":20},
                                                    #{"Name":"Anim_PauseE_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"",
                                                     #"ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":3,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":10},
                                                  #]},
                                              #{"Name": "Frame5","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               #"Caption"       : "AUS-schalt Parameter",
                                               #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 1,"Top": 5,"Type": "Frame","Visible": True,"Width": 20,
                                               #"Components"    :
                                                  #[{"Name":"Anim_PauseS_Aus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Startpause (msec)",
                                                    #"ControlTipText":"Pause bevor die Ausschaltanimation startet in msec",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_PauseS_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"",
                                                    #"ControlTipText":"Pause bevor die Ausschaltanimation startet in msec",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":10},
                                                   #{"Name":"Anim_DauerAus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"Dauer AUS (msec)",
                                                     #"ControlTipText":"Dauer der Ausschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_DauerAus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"",
                                                     #"ControlTipText":"Dauer der Ausschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 2500 ,"Visible":True,"Width":10},
                                                   #{"Name":"Anim_PauseE_Aus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"Endepause (msec)",
                                                     #"ControlTipText":"Pause am Ende der Ausschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":3,"Type":"Label","Visible":True,"Width":20},
                                                    #{"Name":"Anim_PauseE_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                     #"Caption":"",
                                                     #"ControlTipText":"Pause am Ende der Ausschaltanimation in msec",
                                                     #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":3,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":10},
                                                   #]},
                                              #{"Name": "Frame6","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               #"Caption"       : "Kurven Parameter",
                                               #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 1,"Top": 6,"Type": "Frame","Visible": True,"Width": 20,
                                               #"Components"    :
                                                    #[                                                            
                                                   #{"Name":"ServoCurveType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Kurventyp:",
                                                    #"ControlTipText":"Kurventyp der Sequenz",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_CurveType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Kurventyp",
                                                    #"ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nLinear\nBeschleunigung\nIndividuell",
                                                    #"ForeColor":"#FF0000","Height":3,"Left":2,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"ListBox","Value": ["Linear", "Beschleunigung", "Individuell"] ,"Visible":True,"Width":20},
                                                   #{"Name":"Anim_Anfangswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Anfangswert (0..255)",
                                                    #"ControlTipText":"Anfangswert (1..254)",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_Anfangswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"", "Command":"",
                                                    #"ControlTipText":"Anfangswert (1..254)",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 20 ,"Visible":True,"Width":10},
                                                   #{"Name":"Anim_Endwert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Endwert (1..254)",
                                                    #"ControlTipText":"Endwert (1..254)",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","Top":3,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_Endwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"", "Command":"",
                                                    #"ControlTipText":"Endwert (1..254)",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":3,"Type":"NumBox","Value": 220 ,"Visible":True,"Width":10},
                                                   #{"Name":"Ueberblendung","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"ARDUINO Überblendung AUS",
                                                    #"ControlTipText":"ARDUINO interne Überblendung zwischen den Werten NICHT nutzen (zum Testen)","ForeColor":"#000012","Height":1,"Left":1,"Top":4,"Type":"CheckBox","Visible":True,"Width":10,"AlternativeText":""},
                                                   #]},
                                              #{"Name": "Frame7","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               #"Caption"       : "Ausführung Parameter",
                                               #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 1,"Top": 7,"Type": "Frame","Visible": True,"Width": 10,
                                               #"Components"    :
                                                    #[                                                                
                                                   #{"Name":"ServoRunType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Ausführung:",
                                                    #"ControlTipText":"Art der Ausführung der Sequenz",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_RunType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Ausführung",
                                                    #"ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nWiederholen: EIN und AUS-Sequenz werden automatisch wiederholt.\nPingPong: Die EIN-Sequenz wird vorwärts und rückwärts abgespielt\nEin/Aus: Beim Einschalten wird die EIN-Sequenz, beim Ausschalten die AUS-Sequenz EINMAL abgespielt",
                                                    #"ForeColor":"#FF0000","Height":3,"Left":1,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"ListBox","Value": ["Wiederholen", "PingPong", "Ein/Aus"] ,"Visible":True,"Width":20},
                                                   #]},
                                              #{"Name": "Frame3","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                               #"Caption"       : "Zeitstufen Parameter",
                                               #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 1,"Top": 8,"Type": "Frame","Visible": True,"Width": 5,
                                               #"Components"    :
                                                  #[
                                                  #{"Name":"ServoTimeStepType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   #"Caption":"Zeitstufen",
                                                   #"ControlTipText":"Art der Zeitstufen für die Sequenz",
                                                   #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":20},
                                                  #{"Name":"Anim_TimeStepType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                   #"Caption":"Zeitstufen",
                                                   #"ControlTipText":"Wie sollen die Zeitstufen ermittelt werden \nAutomatisch \nFester Wert \nIndividuell",
                                                   #"ForeColor":"#FF0000","Height":3,"Left":1,"TextAlign":"fmTextAlignLeft","Selection": 1,"SpecialEffect": "fmSpecialEffectSunken","Top":1,"Type":"ListBox","Value": ["Automatisch", "Fester Wert", "Individuell"] ,"Visible":True,"Width":20},
                                                  #{"Name":"Anim_Abstand_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"Stufenabstand (msec)",
                                                    #"ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den Servo gesendet werden.",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","Top":2,"Type":"Label","Visible":True,"Width":20},
                                                   #{"Name":"Anim_Abstand_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                                    #"Caption":"",
                                                    #"ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den Servo gesendet werden.",
                                                    #"ForeColor":"#FF0000","Height":1,"Left":1,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":2,"Type":"NumBox","Value": 500 ,"Visible":True,"Width":20},
                                                   #]},
                                              #]}, 
                                      #{"Name": "Frame2","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                       #"Caption"       : "Kurvenverlauf",
                                       #"ControlTipText": "","ForeColor": "#000012","Height": 50,"Left": 2,"Top": 2,"Type": "Frame","Visible": True,"Width": 100, "sticky": "nesw",
                                       #"Components"    :
                                            #[
                                                #]},
                                        #{"Name": "LowerFrame","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         #"Caption"       : "",
                                         #"ControlTipText": "","ForeColor": "#000012","Height": 3,"Left": 2,"Top": 3,"Type": "Frame","Visible": True,"Width": 5,
                                         #"Components"    :
                                              #[
                                            #{"Name":"Kurve_Zeit_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"Zeit:",
                                             #"ControlTipText":"Zeigt die  Zeit an, auf der der Mauszeiger steht",
                                             #"ForeColor":"#FF0000","Height":1,"Left":1, "TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":10},
                                            #{"Name":"Kurve_Zeitanzeige_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"0",
                                             #"ControlTipText":"Zeigt die  Zeit an, auf der der Mauszeiger steht",
                                             #"ForeColor":"#FF0000","Height":1,"Left":2,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":10},                                      
                                            #{"Name":"Kurve_Wert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"Wert:",
                                             #"ControlTipText":"Zeigt den Wert an, auf dem der Mauszeiger steht",
                                             #"ForeColor":"#FF0000","Height":1,"Left":3, "TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":10},
                                            #{"Name":"Kurve_Wertanzeige_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"0",
                                             #"ControlTipText":"Zeigt den Wert an, auf dem der Mauszeiger steht",
                                             #"ForeColor":"#FF0000","Height":1,"Left":4,"TextAlign":"fmTextAlignLeft","Top":1,"Type":"Label","Visible":True,"Width":10},                                         
                                            
                                            #{"Name":"OK_Button","Accelerator":"<Return>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"OK",
                                             #"Command":self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":2,"Left":5,"Top":4,"Type":"CommandButton","Visible":True,"Width":10},
                                            #{"Name":"Abort_Button","Accelerator":"<Escape>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"Abbrechen",
                                             #"Command":self.Abort_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":2,"Left":4,"Top":4,"Type":"CommandButton","Visible":True,"Width":10},
                                            #{"Name":"Update_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"Update Grafik",
                                             #"Command":"","ControlTipText":"","ForeColor":"#000012","Height":2,"Left":3,"Top":4,"Type":"CommandButton","Visible":True,"Width":10},
                                            #{"Name":"Test_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"Starte Test",
                                             #"Command":"","ControlTipText":"","ForeColor":"#000012","Height":2,"Left":2, "Top":4,"Type":"CommandButton","Visible":True,"Width":10},
                                            #{"Name":"Help_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             #"Caption":"Hilfe",
                                             #"Command":"","ControlTipText":"","ForeColor":"#000012","Height":2,"Left":1,"Top":4,"Type":"CommandButton","Visible":True,"Width":10},
                                            #]},
                                                                            
                                      #]}
                        #}
        
        self.Main_Menu_Form_RSC = {"UserForm":{
                        "Name"          : "MainMenuForm",
                        "BackColor"     : "#000008",
                        "BorderColor"   : "#000012",
                        "Caption"       : "Servo Animation",
                        "Height"        : 629,
                        "Left"          : 0,
                        "Top"           : 0,
                        "Type"          : "MainWindow",
                        "Visible"       : True,
                        "Width"         : 842,
                        "Geo_Manager" : "place",
                        "Components":[{"Name":"Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Unterstützt den Direkt Mode Servo von Eckhard (Servo DM) und die Normalen MLL-Servos (Servo1, Servo2 und Servo3)\nDurch Eingabe der Ein- und Ausschaltparameter wird der Zeitablauf bestimmt. Es stehen 3 Kurven-Modi zur Verfügung: Linear, Beschleunigung und Individuell. " +
                                       "Die berechneten Kurven werden in der Grafik rechts angezeigt. Bei der Einstellung Individuell können die Kurvenwerte (Grüne Punkte) einzeln eingestellt werden. Wurde unter Servo-Adresse die Adresse des Servos angegeben, kann die Servostellung direkt überprüft werden.\n" +
                                       "Beim Ausführen kann man wählen zwischen: Wiederholen-die Ein-und Ausschaltsequenz wird automatisch wiederholt, PingPong-die Sequenz wird vor- und zurück abgespielt, Ein/Aus: Bei Schalter auf EIN wird die Einschaltsequenz, bei Schalter auf AUS, wird die Auschaltsequenz abgespielt.",
                                        "ControlTipText":"Tooltip1","ForeColor":"#000012","Height":66,"Left":12,"SpecialEffect": "fmSpecialEffectSunken","TextAlign":"fmTextAlignLeft","Top":18,"Type":"Label","Visible":True,"Width":790},
                                      {"Name":"Label2","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"by Harold Linke",
                                       "ControlTipText":"","ForeColor":"#FF0000","Height":12,"Left":318,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":50},
                                      {"Name":"Anim_Address_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Servo Adressse",
                                       "ControlTipText":"Servo Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":90,"Type":"Label","Visible":True,"Width":100},
                                      {"Name":"Anim_Address_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"Servo Adresse für Test","ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":90,"Type":"NumBox","Value": 1 ,"Visible":True,"Width":50},
                                      {"Name":"Anim_Address_Kanal_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Anschluß-Kanal",
                                       "ControlTipText":"Kanal, an dem der Servo angeschlossen wird","ForeColor":"#FF0000","Height":18,"Left":238,"TextAlign":"fmTextAlignLeft","Top":90,"Type":"Label","Visible":True,"Width":100},
                                      {"Name":"Anim_Address_Kanal_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"",
                                       "ControlTipText":"Kanal, an dem der Servo angeschlossen wird","ForeColor":"#FF0000","Height":18,"Left":182,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":90,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                      {"Name": "Frame1","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                       "Caption"       : "Servotyp",
                                       "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 112,"Type": "Frame","Visible": True,"Width": 154,
                                       "Components"    :
                                            [
                                            {"Name":"ServoType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"ServoTyp:",
                                             "ControlTipText":"Servotyp",
                                             "ForeColor":"#FF0000","Height":18,"Left":72,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                            {"Name":"Anim_Type_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Servotyp",
                                             "ControlTipText":" Servotyp:\nServo DM: Servo mit Direct Mode\nServo1 (Rot): mit WS2811 am roten Anschluß\nServo2 (Grün): mit WS2811 am grünen Anschluß\nServo3(Blau): mit WS2811 am blauen Anschluß",
                                             "ForeColor":"#FF0000","Height":44,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0, "SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Servo DM", "Servo1 (Rot)", "Servo2 (Grün)", "Servo3 (Blau)"] ,"Visible":True,"Width":60},
                                        ]}, 
                                        {"Name": "Frame4","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "EIN-schalt Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 178,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [{"Name":"Anim_PauseS_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Startpause (msec)",
                                              "ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_PauseS_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Pause bevor die Einschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                             {"Name":"Anim_DauerEin_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Dauer EIN (msec)",
                                               "ControlTipText":"Dauer der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_DauerEin_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Dauer der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":30,"Type":"NumBox","Value": 2500 ,"Visible":True,"Width":50},
                                             {"Name":"Anim_PauseE_Ein_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Endepause (msec)",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":148},
                                              {"Name":"Anim_PauseE_Ein_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Pause am Ende der Einschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                            ]},
                                        {"Name": "Frame5","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "AUS-schalt Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 266,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [{"Name":"Anim_PauseS_Aus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Startpause (msec)",
                                              "ControlTipText":"Pause bevor die Ausschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_PauseS_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Pause bevor die Ausschaltanimation startet in msec",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                             {"Name":"Anim_DauerAus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Dauer AUS (msec)",
                                               "ControlTipText":"Dauer der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":30,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_DauerAus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Dauer der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":30,"Type":"NumBox","Value": 2500 ,"Visible":True,"Width":50},
                                             {"Name":"Anim_PauseE_Aus_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"Endepause (msec)",
                                               "ControlTipText":"Pause am Ende der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":54,"Type":"Label","Visible":True,"Width":148},
                                              {"Name":"Anim_PauseE_Aus_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                               "Caption":"",
                                               "ControlTipText":"Pause am Ende der Ausschaltanimation in msec",
                                               "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":54,"Type":"NumBox","Value": 0 ,"Visible":True,"Width":50},
                                             ]},
                                        {"Name": "Frame6","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Kurven Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 354,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                            
                                             {"Name":"ServoCurveType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Kurventyp:",
                                              "ControlTipText":"Kurventyp der Sequenz",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_CurveType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Kurventyp",
                                              "ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nLinear\nBeschleunigung\nIndividuell",
                                              "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Linear", "Beschleunigung", "Individuell"] ,"Visible":True,"Width":60},
                                             {"Name":"Anim_Anfangswert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Anfangswert (0..255)",
                                              "ControlTipText":"Anfangswert (1..254)",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":45,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_Anfangswert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"", "Command":"",
                                              "ControlTipText":"Anfangswert (1..254)",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":45,"Type":"NumBox","Value": 20 ,"Visible":True,"Width":50},
                                             {"Name":"Anim_Endwert_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Endwert (1..254)",
                                              "ControlTipText":"Endwert (1..254)",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":69,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_Endwert_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"", "Command":"",
                                              "ControlTipText":"Endwert (1..254)",
                                              "ForeColor":"#FF0000","Height":18,"Left":12,"TextAlign":"fmTextAlignLeft","SpecialEffect": "fmSpecialEffectSunken","Top":69,"Type":"NumBox","Value": 220 ,"Visible":True,"Width":50},
                                             {"Name":"Ueberblendung","Accelerator":"","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"ARDUINO Überblendung AUS",
                                              "ControlTipText":"ARDUINO interne Überblendung zwischen den Werten NICHT nutzen (zum Testen)","ForeColor":"#000012","Height":12,"Left":12,"Top":93,"Type":"CheckBox","Visible":True,"Width":160,"AlternativeText":""},
                                             ]},
                                        {"Name": "Frame7","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Ausführung Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 478,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                              [                                                                
                                             {"Name":"ServoRunType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung:",
                                              "ControlTipText":"Art der Ausführung der Sequenz",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_RunType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Ausführung",
                                              "ControlTipText":"Wie soll die Bewegung ausgeführt werden: \nWiederholen: EIN und AUS-Sequenz werden automatisch wiederholt.\nPingPong: Die EIN-Sequenz wird vorwärts und rückwärts abgespielt\nEin/Aus: Beim Einschalten wird die EIN-Sequenz, beim Ausschalten die AUS-Sequenz EINMAL abgespielt",
                                              "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 0,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Wiederholen", "PingPong", "Ein/Aus"] ,"Visible":True,"Width":60},
                                             ]},
                                        {"Name": "Frame3","BackColor": "#00000F","BorderColor": "#000006","BorderStyle": "fmBorderStyleNone",
                                         "Caption"       : "Zeitstufen Parameter",
                                         "ControlTipText": "","ForeColor": "#000012","Height": 282,"Left": 6,"Top": 536,"Type": "Frame","Visible": True,"Width": 154,
                                         "Components"    :
                                            [
                                            {"Name":"ServoTimeStepType_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Art der Zeitstufen für die Sequenz",
                                             "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":6,"Type":"Label","Visible":True,"Width":148},
                                            {"Name":"Anim_TimeStepType_ListBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                             "Caption":"Zeitstufen",
                                             "ControlTipText":"Wie sollen die Zeitstufen ermittelt werden \nAutomatisch \nFester Wert \nIndividuell",
                                             "ForeColor":"#FF0000","Height":33,"Left":6,"TextAlign":"fmTextAlignLeft","Selection": 1,"SpecialEffect": "fmSpecialEffectSunken","Top":6,"Type":"ListBox","Value": ["Automatisch", "Fester Wert", "Individuell"] ,"Visible":True,"Width":60},
                                            {"Name":"Anim_Abstand_Label","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"Stufenabstand (msec)",
                                              "ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den Servo gesendet werden.",
                                              "ForeColor":"#FF0000","Height":18,"Left":68,"TextAlign":"fmTextAlignLeft","Top":45,"Type":"Label","Visible":True,"Width":148},
                                             {"Name":"Anim_Abstand_TextBox","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                              "Caption":"",
                                              "ControlTipText":"Abstand in msec zwischen zwei Stufen, die an den Servo gesendet werden.",
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
                                      
                                      {"Name":"OK_Button","Accelerator":"<Return>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"OK",
                                       "Command":self.OK_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":750,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Abort_Button","Accelerator":"<Escape>","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Abbrechen",
                                       "Command":self.Abort_Button_Click,"ControlTipText":"","ForeColor":"#000012","Height":25,"Left":666,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Update_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Update Grafik",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":566,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Test_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Starte Test",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":466,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},
                                      {"Name":"Help_Button","Accelerator":"u","BackColor":"#00000F","BorderColor":"#000006","BorderStyle":"fmBorderStyleNone",
                                       "Caption":"Hilfe",
                                       "Command":"","ControlTipText":"","ForeColor":"#000012","Height":25,"Left":366,"Top":570,"Type":"CommandButton","Visible":True,"Width":72},                                      
                                                                            
                                      ]}
                        }
        
    def create_UI_Paramlist(self):
        self.UI_paramlist = [
            self.Anim_RunType_ListBox, 
            self.Anim_CurveType_ListBox,
            self.Anim_Abstand_TextBox, 
            self.Anim_Anfangswert_TextBox,
            self.Anim_Endwert_TextBox,
            self.Anim_DauerEin_TextBox,
            self.Anim_DauerAus_TextBox, 
            self.Anim_PauseS_Ein_TextBox, 
            self.Anim_PauseE_Ein_TextBox, 
            self.Anim_PauseS_Aus_TextBox, 
            self.Anim_PauseE_Aus_TextBox,
            self.Anim_TimeStepType_ListBox,
            self.Anim_Type_ListBox,
            self.Ueberblendung, 
            self.Anim_Address_Kanal_TextBox,
            self.Anim_Address_TextBox
        ]        
        
    def get_led_value_and_send_to_ARDUINO(self, led_value=None, led_g_value=None, led_b_value=None, point_idx=None):
        if led_value == None:
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
        if self.Anim_Type_ListBox:
            self.servotype = self.Anim_Type_ListBox.Selection
        else:
            self.servotype = 0        
        if self.servotype == 0:
            self._update_servos(LED_address,new_LED_val,1, 0, channel=LED_channel)
        elif self.servotype == 1:
            self._update_servos(LED_address,new_LED_val, 0, 0, channel=LED_channel)
        elif self.servotype == 2:
            self._update_servos(LED_address,0, new_LED_val, 0, channel=LED_channel)
        else:
            self._update_servos(LED_address,0, 0, new_LED_val, channel=LED_channel)    

    def generate_pattern_data(self, anzahl_led, total_points_count, gotoaction):
        # goto action
        if gotoaction:
            dauer_ein = self.Anim_DauerEin_TextBox.Value + self.Anim_PauseS_Ein_TextBox.Value + self.Anim_PauseE_Ein_TextBox.Value
            
            tag_ein_value = "2"
            tag_ein_seq_end = "3"
            tag_aus_value = "4"
            tag_aus_seq_end = "5"
            current_tag = tag_ein_value
            next_tag = current_tag
            end_time = self.curve_points[-1][0]
            
            for point in self.curve_points:
                if anzahl_led == "3":
                    if point[0] == dauer_ein:
                        current_tag = tag_ein_seq_end
                        next_tag = tag_aus_value
                    elif point[0] == end_time:
                        current_tag = tag_aus_seq_end
                        next_tag = "0"
                    else:
                        current_tag = next_tag
                    self.Userform_Res = self.Userform_Res + "," + str(point[1]) + ",1," + current_tag
                else:
                    self.Userform_Res = self.Userform_Res + "," + str(point[1])
            self.Userform_Res = self.Userform_Res + "  "
            for i in range(total_points_count-2):
                if self.curve_points[i][0] == dauer_ein: 
                    self.Userform_Res = self.Userform_Res + ",63,128"
                else:
                    self.Userform_Res = self.Userform_Res + ",0"
            self.Userform_Res = self.Userform_Res + ",63"
            
        else:
            for point in self.curve_points:
                if anzahl_led == "3":
                    self.Userform_Res = self.Userform_Res + "," + str(point[1]) + ",1,0"
                else:
                    self.Userform_Res = self.Userform_Res + "," + str(point[1])
        self.Userform_Res = self.Userform_Res + ')$' + str(self.Anim_Address_Kanal_TextBox.Value)

    


