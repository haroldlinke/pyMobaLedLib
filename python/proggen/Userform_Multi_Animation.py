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

import ExcelAPI.XLF_FormGenerator as XLF
#import pattgen.D00_Forms as D00

import tkinter as tk
from tkinter import ttk

import logging
import webbrowser
import pgcommon.CanvasFrame as CF

runtype_pingpong = 1
runtype_on_off = 2
runtype_hsv = 3
runtype_repeat = 0

curvetype_linear = 0
curvetype_accel = 1
curvetype_individuell = 2

timesteptype_auto = 0
timesteptype_fix = 1
timesteptype_individuell = 2

class UserForm_Multi_Animation:
    
    def __init__(self,controller, no_of_curves=1):
        self.controller    = controller
        self.IsActive      = False
        self.Form          = None
        self.Userform_Res  = ""
        self.Controls      = []
        self.Controls_Dict = {}
        self.Macro_str = ""
        self.test_started = False
        self.test_continue = False
        self.test_pause = False
        self.value_max = 254
        self.value_min = 1
        self.no_of_curves = no_of_curves
        self.active_curve = 0
        self.old_active_curve = 0
        self.graph_colors = ["#FF0000", "#00FF00", "#0000FF"]
        self.Anim_Anfangswert_TextBox = None
        self.Anim_AnfangsGwert_TextBox  = None
        self.Anim_AnfangsBwert_TextBox  = None
        self.Anim_Endwert_TextBox  = None
        self.Anim_EndGwert_TextBox  = None
        self.Anim_EndBwert_TextBox = None
        self.Anim_Type_ListBox = None
        self.Active_Curve_ListBox = None
        self.Anim_No_of_Curves_TextBox = None
        self.Anim_RunType_ListBox = None 
        self.Anim_CurveType_ListBox  = None
        self.Anim_Abstand_TextBox  = None
        self.Anim_DauerEin_TextBox  = None
        self.Anim_DauerAus_TextBox  = None 
        self.Anim_PauseS_Ein_TextBox  = None 
        self.Anim_PauseE_Ein_TextBox = None
        self.Anim_PauseS_Aus_TextBox = None
        self.Anim_PauseE_Aus_TextBox  = None
        self.Anim_TimeStepType_ListBox = None
        self.Anim_Address_Kanal_TextBox  = None
        self.Anim_Address_TextBox  = None
        self.Anim_LEDName_TextBox = None
        self.Anim_LEDcolor_TextBox = None
        self.Anim_LEDcolor_ColorBox = None
        self.Anim_LEDwidth_NumBox = None
        self.Anim_Name_Color_str = ""
        self.Ueberblendung = None
        self.use_ueberblendung = True
        #*HL Center_Form(Me)
        self.Main_Menu_Form_RSC = {}
        self.endwertpoint_idx = 0
        self.LEDname_list = ["LED1", "LED2", "LED3"]
        self.LEDcolor_list = ["#FF0000", "#00FF00", "#0000FF"]
        self.LEDwidth_list = [2, 2, 2]
        
    def get_params_from_param_list(self, param_list):
        i = 0
        for param in param_list:
            if i < len(self.UI_paramlist):
                if type(self.UI_paramlist[i]) == str:
                    self.Anim_Name_Color_str = param
                elif self.UI_paramlist[i].Type == "ListBox":
                    self.UI_paramlist[i].Selection = param
                else:
                    self.UI_paramlist[i].Value = param
                i += 1
            

    def create_paramstring_from_param_list(self, param_list):
        i = 0
        result_string = ""
        for param in param_list:
            #if self.UI_paramlist[i].Type == "ListBox":
                #result_string = result_string + str(self.UI_paramlist[i].Selection)
            #else:
                #result_string = result_string + str(self.UI_paramlist[i].Value)
            #if i < len(param_list) - 1:
                #result_string = result_string + ","
            #i += 1
            if type(param) == str:
                color_name_param = ""
                for i in range(len(self.LEDname_list)):
                    if i < len(self.LEDcolor_list):
                        color_name_param += self.LEDcolor_list[i]
                    else:
                        "#000000"
                    color_name_param += ";"
                    color_name_param += self.LEDname_list[i]
                    color_name_param += ";"
                    if i < len(self.LEDwidth_list):
                        color_name_param += str(self.LEDwidth_list[i])
                    else:
                        color_name_param += "2"
                    if i < len(self.LEDname_list) - 1:
                        color_name_param += ";"
                result_string = result_string + color_name_param
            elif param.Type == "ListBox":
                result_string = result_string + str(param.Selection)
            else:
                result_string = result_string + str(param.Value)
            if i < len(param_list) - 1:
                result_string = result_string + ","
            i += 1            
        return result_string
    
    def calculate_on_off_line(self):
        time_val =  self.get_Textbox_value(self.Anim_DauerEin_TextBox) + self.get_Textbox_value(self.Anim_PauseS_Ein_TextBox) + self.get_Textbox_value(self.Anim_PauseE_Ein_TextBox)
        return time_val
    
    def determine_curve_points_ary_from_Macro(self, Macro_str):
        curve_points_ary = [[], [], []] # separete curves for R,G,B
        macro_str_lines = Macro_str.split("\n")
        if len(macro_str_lines) > 1:
            pattern_macro_complete = macro_str_lines[-1]
            pattern_macro_complete = pattern_macro_complete[:-1]
            pattern_macro_split = pattern_macro_complete.split(" ") # split into macro and gotoact part
            pattern_macro_params = pattern_macro_split[0].split(",")
            pattern_macro_start = pattern_macro_params[0].split("(")
            pattern_macro_start_parts =  pattern_macro_start[0].split("T")
            number_of_timeslots = int(pattern_macro_start_parts[1])
            param_idx = 8
            timedelta_list = []
            for i in range(0, number_of_timeslots):
                timedelta_list.append(int(pattern_macro_params[param_idx]))
                param_idx += 1
            curr_time = 0
            time_idx = 0
            if self.servotype == 0:
                param_idx_delta = 3
            else:
                param_idx_delta = 1
            while param_idx < len(pattern_macro_params):
                curve_points_ary[0].append([curr_time, int(pattern_macro_params[param_idx])])
                if param_idx_delta == 3 and self.no_of_curves > 1:
                    curve_points_ary[1].append([curr_time, int(pattern_macro_params[param_idx+1])])
                    curve_points_ary[2].append([curr_time, int(pattern_macro_params[param_idx+2])])
                param_idx += param_idx_delta
                curr_time += timedelta_list[time_idx]
                if time_idx < number_of_timeslots - 1:
                    time_idx += 1
        return curve_points_ary
    
    def determine_curve_points_from_Macro(self, Macro_str):
        curve_points = []
        macro_str_lines = Macro_str.split("\n")
        if len(macro_str_lines) > 1:
            pattern_macro_complete = macro_str_lines[-1]
            pattern_macro_complete = pattern_macro_complete[:-1]
            pattern_macro_split = pattern_macro_complete.split(" ") # split into macro and gotoact part
            pattern_macro_params = pattern_macro_split[0].split(",")
            pattern_macro_start = pattern_macro_params[0].split("(")
            pattern_macro_start_parts =  pattern_macro_start[0].split("T")
            number_of_timeslots = int(pattern_macro_start_parts[1])
            param_idx = 8
            timedelta_list = []
            for i in range(0, number_of_timeslots):
                timedelta_list.append(int(pattern_macro_params[param_idx]))
                param_idx += 1
            curr_time = 0
            time_idx = 0
            if self.servotype == 0:
                param_idx_delta = 3
            else:
                param_idx_delta = 1
            while param_idx < len(pattern_macro_params):
                curve_points.append([curr_time, int(pattern_macro_params[param_idx])])
                param_idx += param_idx_delta
                curr_time += timedelta_list[time_idx]
                if time_idx < number_of_timeslots - 1:
                    time_idx += 1
        return curve_points
    
    def get_params(self):
        self.get_params_from_param_list(self.param_list)
        self.patterntype = self.get_Anim_RunType() #self.Anim_RunType_ListBox.Selection
        self.patterntype_str = "PM_" + self.get_Anim_RunType_Str()
        self.curvetype = self.get_Anim_CurveType() #self.Anim_CurveType_ListBox.Selection
        if self.Anim_Type_ListBox:
            self.servotype = self.Anim_Type_ListBox.Selection
        else:
            self.servotype = 0
            
        if self.Anim_Name_Color_str != "": # string with LED1Color;LED1Name;LED1lineWidth;LED2Color;LED2Name;LED2lineWidth, ...
            self.LEDcolor_list = []
            self.LEDname_list = []
            self.LEDwidth_list = []
            param_parts_list = self.Anim_Name_Color_str.split(";")
            for i in range(0, len(param_parts_list)):
                if i % 3 == 0: #color
                    self.LEDcolor_list.append(param_parts_list[i])
                elif i % 3 == 1: #Name
                    self.LEDname_list.append(param_parts_list[i])
                elif i % 3 == 2: #Width
                    self.LEDwidth_list.append(int(param_parts_list[i]))
        self.Active_Curve_ListBox.Value = self.LEDname_list
        
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
            self.Anim_Type_ListBox,
            self.Ueberblendung, 
            self.Anim_Address_Kanal_TextBox,
            self.Anim_Address_TextBox,
            self.Anim_No_of_Curves_TextBox
        ]
        
    def determine_endwertpoint_idx(self, on_off_line):
        
        if on_off_line != 0:
            curve_points = self.curve_points_ary[0] 
            for i in range(0, len(curve_points)):
                endpoint = curve_points[i][0] == on_off_line
                if endpoint:
                    self.endwertpoint = int(curve_points[i][0])
                    self.endwertpoint_idx = i
        else:
            self.endwertpoint_idx = len(curve_points) - 1
            self.endwertpoint = int(curve_points[self.endwertpoint_idx][0])
            
    
    def __UserForm_Initialize(self):
        #--------------------------------
        # Is called once to initialice the form
        self.Userform_Res = ""
        self.Anim_PauseS_Aus_TextBox = None
        DefaultFont =  ("Calibri",9)
        self.Form=XLF.generate_form(self.Main_Menu_Form_RSC,self.controller,dlg=self, jump_table=PG.ThisWorkbook.jumptable, defaultfont=DefaultFont)
        self.patterntype = 0
        self.curvetype = curvetype_linear
        self.curve_points = []
        self.curve_points_ary = []
        for i in range(0, self.no_of_curves):
            self.curve_points_ary.append([])
            self.graph_colors.append("#000000")
        self.active_curve = 0
        self.old_active_curve = 0
        self.curve_points_ary[self.active_curve] = self.curve_points
        self.current_curve_point = None
        self.start_value = ()
        self.create_UI_Paramlist()
        if self.Macro_str != "":
            # read parameters from Macrostring
            if self.Macro_str.find("#"+self.MacroName) != -1 :
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
                            self.get_params()
            self.curve_points_ary = self.determine_curve_points_ary_from_Macro(self.Macro_str)
            
            self.use_ueberblendung = True if self.Ueberblendung and self.Ueberblendung.Value != 1 else False
        self.last_t_aus = 0
        self.last_t_ein = 0        

        #if self.Anim_TimeStepType_ListBox.Selection == 0: # automatic
        #    self.Anim_Abstand_TextBox.Value = int(self.Anim_DauerEin_TextBox.Value / 4)
        #if self.curvetype == curvetype_individuell: # individuel
            #self.curve_points = self.determine_curve_points_from_Macro(self.Macro_str)
            #self.curve_points_ary = self.determine_curve_points_ary_from_Macro(self.Macro_str)

        self.canvas = self.init_graph(frame=self.FrameR2.TKWidget)
        graph_only = False
        self.controller.clear_ToolTip_canvas()
        on_off_line =  self.calculate_on_off_line()
        self.determine_endwertpoint_idx(on_off_line)
        for i in range(0, self.no_of_curves):
            
            self.curve_points = self.curve_points_ary[i]
            
            self.curve_points = self.calculate_complete_curve(curve_no=i)
            self.curve_points_ary[i] = self.curve_points
            anzahl_werte = len(self.curve_points) - 1
            
            graph_active = (i == self.active_curve)
            self.draw_graph(num_horizontal=anzahl_werte, graph=self.curve_points, on_off_line=on_off_line, graphcolor=self.LEDcolor_list[i], graph_only=graph_only, graph_active=graph_active, ueberblendung=self.use_ueberblendung, width=self.LEDwidth_list[i], graphname=self.LEDname_list[i])
            graph_only = True
        self.curve_points = self.curve_points_ary[self.active_curve]
        if self.Anim_LEDcolor_TextBox != None:
            self.Anim_LEDcolor_TextBox.Value = self.LEDcolor_list[self.active_curve]
            self.Anim_LEDcolor_ColorBox.TKWidget.Color = self.LEDcolor_list[self.active_curve] 
            self.Anim_LEDName_TextBox.Value = self.LEDname_list[self.active_curve]
            self.Anim_LEDwidth_NumBox.Value = self.LEDwidth_list[self.active_curve]        
        self.controller.connect_if_not_connected()
        self.controller.ARDUINO_begin_direct_mode()
        

    def __UserForm_Activate(self):
        #------------------------------
        # Is called every time when the form is shown
        #M25.Make_sure_that_Col_Variables_match()
        pass
        
    def Hide(self):
        self.IsActive=False
        self.controller.ARDUINO_end_direct_mode()
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
    
    def Show_With_Existing_Data(self, MacroName, ConfigLine, LED_Channel, Def_Channel, use_NButtons=False):
        Txt = String()
        #----------------------------------------------------------------------------------------------------------------------
        
        self.MacroName = MacroName
        self.use_NButtons = use_NButtons
        self.__LED_CntList = ''
        self.Macro_str = ConfigLine
        self.Show()
        
    def calculate_accell_curve(self, duration, start_val, end_val, start_time, time_distance, skip_first=False):
        curve_points = []
        if self.Anim_TimeStepType_ListBox.Selection == 0: # automatic
            time_distance = int(duration / 2.0)        
        a = 2 * (end_val - start_val) / (duration * duration)
        if skip_first:
            t = time_distance
        else:
            t = 0
        while t < duration:
            val = int(round(0.5 * a * t * t, 0)) + start_val
            curve_points.append([t+start_time, val])
            t += time_distance
        # generate last point at duration.
        val = val = int(round(0.5 * a * duration * duration, 0)) + start_val
        curve_points.append([duration+start_time, val])                
        return curve_points
        
    def calculate_linear_curve(self, duration, start_val, end_val, start_time, time_distance, skip_first=False):
        curve_points = []
        if self.Anim_TimeStepType_ListBox.Selection == 0: # automatic
            time_distance = int(duration) # int(duration / 2.0)
        if skip_first:
            t = time_distance
        else:
            t = 0
        steigung =  (end_val - start_val) / duration
        while t < duration:
            val = int(round(steigung * t + start_val, 0))
            curve_points.append([t+start_time, val])
            t += time_distance
        # generate last point at duration.
        val = int(round(steigung * duration + start_val, 0))
        curve_points.append([duration+start_time, val])        
        return curve_points
    
    def calculate_pause_curve(self, duration, val, start_time, time_distance, skip_first=False):
        curve_points = []
        if self.Anim_TimeStepType_ListBox.Selection == 0: # automatic
            time_distance = int(duration / 2.0)
        if skip_first:
            t = time_distance
        else:
            t = 0
        while t < duration: 
            curve_points.append([t+start_time, val])
            t += time_distance
        # generate last point at duration.
        curve_points.append([duration+start_time, val])
        return curve_points
    
    def calculate_curve(self, duration, start_val, end_val, start_time, time_distance, pauseS=None, pauseE=None, skip_first=False):
        if duration > 0:
            if pauseS != None and pauseS > 0:
                point_list1 = self.calculate_pause_curve(pauseS, start_val, start_time, time_distance, skip_first=skip_first)
                start_time += pauseS
            else:
                point_list1 = []
            if point_list1 != []:
                skip_first = True
            if self.curvetype == curvetype_linear: # linear
                point_list2 = self.calculate_linear_curve(duration, start_val, end_val, start_time, time_distance, skip_first=skip_first)
            elif self.curvetype == curvetype_accel: # Beschleunigung
                point_list2 = self.calculate_accell_curve(duration, start_val, end_val, start_time, time_distance, skip_first=skip_first)
            else: # individuell, should not happen here
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
        else:
            point_list1 = []
        return point_list1
    
    def update_timepoints(self, t_from=0, t_to=0, t_shift=0, t_factor=1):
        if t_factor==1 and t_shift==0:
            return
        for index, curve_point in enumerate(self.curve_points):
                if curve_point[0] > t_from:
                    if curve_point[0] <= t_to:
                        curve_point[0] = round((curve_point[0] - t_from)* t_factor) + t_shift
                    else:
                        break
                    
    def get_Textbox_value(self, textbox):
        if textbox:
            return textbox.Value
        else:
            return 0
        
    def get_Numbox_value(self, numbox):
        if numbox:
            return numbox.Value
        else:
            return 0
        
    def get_Listbox_value(self, listbox):
        if listbox:
            return listbox.Value
        else:
            return 0    
        
    def get_Colorbox_value(self, colorbox):
        if colorbox:
            return colorbox.TKWidget.Color
        else:
            return "#000000"
        
    def set_Textbox_value(self, textbox, value):
        if textbox:
            textbox.Value = value
        
    def set_Numbox_value(self, numbox, value):
        if numbox:
            numbox.Value = value
            
    def set_Listbox_value(self, listbox, value):
        if listbox:
            listbox.Value = value    
        
    def set_Colorbox_value(self, colorbox, value):
        if colorbox:
            colorbox.TKWidget.Color = value
        
    def get_Anim_CurveType(self):
        if self.Anim_CurveType_ListBox:
            return self.Anim_CurveType_ListBox.Selection
        else:
            return 0
        
    def get_Anim_RunType(self):
        if self.Anim_CurveType_ListBox:
            return self.Anim_RunType_ListBox.Selection
        else:
            return 0
    
    def get_Anim_RunType_Str(self):
        if self.Anim_CurveType_ListBox:
            return self.Anim_RunType_ListBox.Selection_Str
        else:
            return "PM_NORMAL"        
    
    def calculate_complete_curve(self, curve_no=0):
        #self.curvetype = self.Anim_CurveType_ListBox.Selection
        self.curvetype = self.get_Anim_CurveType()
        #self.patterntype = self.Anim_RunType_ListBox.Selection
        self.patterntype = self.get_Anim_RunType()
        #t_ein = self.Anim_PauseS_Ein_TextBox.Value + self.Anim_DauerEin_TextBox.Value + self.Anim_PauseE_Ein_TextBox.Value
        t_ein = self.get_Textbox_value(self.Anim_PauseS_Ein_TextBox) + self.get_Textbox_value(self.Anim_DauerEin_TextBox) + self.get_Textbox_value(self.Anim_PauseE_Ein_TextBox)
        t_aus = self.get_Textbox_value(self.Anim_PauseS_Aus_TextBox) + self.get_Textbox_value(self.Anim_DauerAus_TextBox) + self.get_Textbox_value(self.Anim_PauseE_Aus_TextBox)
        
        if self.curvetype != curvetype_individuell: # individuel
            if self.Anim_Anfangswert_TextBox:
                Anfangoffset =  self.UI_paramlist.index(self.Anim_Anfangswert_TextBox)
                Anfangswert_TextBox = self.UI_paramlist[curve_no+Anfangoffset]
                if Anfangswert_TextBox == None:
                    Anfangswert = self.curve_points[0][1]
                else:
                    Anfangswert = self.get_Textbox_value(Anfangswert_TextBox)
                Endoffset =  self.UI_paramlist.index(self.Anim_Endwert_TextBox)
                Endwert_TextBox = self.UI_paramlist[curve_no+Endoffset] 
                if Endwert_TextBox == None:
                    Endwert = self.curve_points[self.endwertpoint_idx][1]
                else:
                    Endwert = self.get_Textbox_value(Endwert_TextBox)
            else:
                if len(self.curve_points) >= 2:
                    Anfangswert = self.curve_points[0][1]
                    if self.endwertpoint_idx >= len(self.curve_points):
                        self.endwertpoint_idx = len(self.curve_points) - 1
                    Endwert = self.curve_points[self.endwertpoint_idx][1]
                else:
                    Anfangswert = 0
                    Endwert = 0
            curve_points = self.calculate_curve(self.get_Textbox_value(self.Anim_DauerEin_TextBox), Anfangswert, Endwert, 0 , self.get_Textbox_value(self.Anim_Abstand_TextBox), pauseS=self.get_Textbox_value(self.Anim_PauseS_Ein_TextBox), pauseE=self.get_Textbox_value(self.Anim_PauseE_Ein_TextBox))
            if False: # self.patterntype != 1 and self.Anim_DauerAus_TextBox != None:   **HL**
                t = self.get_Textbox_value(self.Anim_PauseS_Ein_TextBox) + self.get_Textbox_value(self.Anim_DauerEin_TextBox) + self.get_Textbox_value(self.Anim_PauseE_Ein_TextBox)
                curve_points_Aus = self.calculate_curve(self.get_Textbox_value(self.Anim_DauerAus_TextBox), Endwert, Anfangswert, t, self.get_Textbox_value(self.Anim_Abstand_TextBox), pauseS=self.get_Textbox_value(self.Anim_PauseS_Aus_TextBox), pauseE=self.get_Textbox_value(self.Anim_PauseE_Aus_TextBox), skip_first=True)
                curve_points.extend(curve_points_Aus)
        else:
            # check if curve points are in range 0 .. 255:
            if self.curve_points == []: # when no curvepoints defined calculate linear curve (0,0)
                Anfangswert = 0
                Endwert = 0                
                curve_points = self.calculate_linear_curve(self.get_Textbox_value(self.Anim_DauerEin_TextBox), Anfangswert, Endwert, 0 , self.get_Textbox_value(self.Anim_Abstand_TextBox))
                self.curve_points = curve_points
            for index, curve_point in enumerate(self.curve_points):
                if curve_point[1] > self.value_max:
                    curve_point[1] = self.value_max
                    self.curve_points[index] = curve_point
                if curve_point[1] < self.value_min:
                    curve_point[1] = self.value_min
                    self.curve_points[index] = curve_point
            if t_ein != self.last_t_ein and self.last_t_ein > 0:
                time_factor_ein = t_ein / self.last_t_ein
            else:
                time_factor_ein = 1
            if t_aus != self.last_t_aus and self.last_t_aus > 0:
                time_factor_aus = t_aus / self.last_t_aus
            else:
                time_factor_aus = 1
            if time_factor_aus != 1 or time_factor_ein != 1:
                if time_factor_ein < 1:
                    self.update_timepoints(t_from=0, t_to=self.last_t_ein, t_factor = time_factor_ein)
                    self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein+self.last_t_aus, t_shift=t_ein, t_factor = time_factor_aus)
                if time_factor_ein > 1:
                    self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein+self.last_t_aus, t_shift=t_ein, t_factor = time_factor_aus)
                    self.update_timepoints(t_from=0, t_to=self.last_t_ein, t_factor = time_factor_ein)
                if time_factor_ein == 1:
                    self.update_timepoints(t_from=self.last_t_ein, t_to=self.last_t_ein+self.last_t_aus, t_shift=t_ein, t_factor = time_factor_aus)
            curve_points = self.curve_points
        self.last_t_ein = t_ein
        self.last_t_aus = t_aus
        return curve_points
    
    def determine_delta_timepoints_count(self):
        delta_timepoints_count = len(self.curve_points) - 1 # number of deltas between timepoints
        #check for repeating timedeltas from the end:
        if delta_timepoints_count > 1:
            curr_time = self.curve_points[-1][0]  # time of last curve point
            curr_delta = curr_time - self.curve_points[-2][0]
            curr_time = self.curve_points[-2][0]
            for i in range(delta_timepoints_count-2, -1, -1):
                new_delta=curr_time - self.curve_points[i][0]
                if new_delta == curr_delta:
                    delta_timepoints_count -= 1
                    curr_time = self.curve_points[i][0] 
                else:
                    break
        return delta_timepoints_count
    
    def determine_patterntype_str(self, patterntype_str):
        return patterntype_str
        
    
    def OK_Button_Click(self, event=None):
        #------------------------------
        runtype = self.get_Anim_RunType() #self.Anim_RunType_ListBox.Selection
        self.curvetype =  self.get_Anim_CurveType() #self.Anim_CurveType_ListBox.Selection
        gotoaction = False
        #if runtype == runtype_on_off: #"Ein/Aus":
            #gotoaction = True
            #self.patterntype_str = "PM_NORMAL"
        #elif runtype == runtype_pingpong: #"PingPong":
            #gotoaction = False
            #self.patterntype_str = "PM_PINGPONG"
        #elif runtype == runtype_hsv:
            #gotoaction = False
            #self.patterntype_str = "PM_HSV"
        #else:
            #gotoaction = False
            #self.patterntype_str = "PM_NORMAL"
        self.patterntype_str = "PM_" + self.get_Anim_RunType_Str()
        self.patterntype_str = self.determine_patterntype_str(self.patterntype_str)
        for i in range(0, self.no_of_curves):
            self.curve_points = self.curve_points_ary[i]
            self.curve_points = self.calculate_complete_curve(curve_no=i)
            self.curve_points_ary[i] = self.curve_points        
        self.curve_points = self.curve_points_ary[self.active_curve]
        if self.Anim_Type_ListBox:
            self.servotype = self.Anim_Type_ListBox.Selection
        else:
            self.servotype = 0
        if self.servotype == 0:
            LED = "1"
        else:
            servotype_str = str(self.servotype)
            LED = "C"+servotype_str+"-"+servotype_str
        if self.Anim_No_of_Curves_TextBox:
            LED = str(int((int(self.Anim_No_of_Curves_TextBox.Value)-1) / 3) + 1)
        total_points_count = len(self.curve_points)
        delta_timepoints_count = total_points_count - 1 # number of deltas between timepoints
        delta_timepoints_count = self.determine_delta_timepoints_count()
        
        if gotoaction:
            if self.use_NButtons:
                #self.Userform_Res = LED + "$// Activation: N_Buttons #ServoAnim2B("
                self.Userform_Res = LED + "$// Activation: N_Buttons #" + self.MacroName + "("
                self.Userform_Res = self.Userform_Res + self.create_paramstring_from_param_list (self.UI_paramlist)
                self.Userform_Res = self.Userform_Res + ")\n" + "InCh_to_TmpVar(#InCh, 2) \n#define ENABLE_STORE_STATUS()\n"                
            else:
                #self.Userform_Res = LED + "$// Activation: Binary #ServoAnim("
                self.Userform_Res = LED + "$// Activation: Binary #" + self.MacroName + "("
                self.Userform_Res = self.Userform_Res + self.create_paramstring_from_param_list (self.UI_paramlist)
                self.Userform_Res = self.Userform_Res + ")\n" + "Bin_InCh_to_TmpVar(#InCh, 1) \n#define ENABLE_STORE_STATUS()\n"
        else:
            #self.Userform_Res = LED + "$// #ServoAnim("
            self.Userform_Res = LED + "$// #" + self.MacroName + "("
            self.Userform_Res = self.Userform_Res + self.create_paramstring_from_param_list (self.UI_paramlist)
            self.Userform_Res = self.Userform_Res + ")\n"            
        
        #APatternT1(#LED,28,SI_LocalVar,3,0,128,0,PM_NORMAL,250,10,1,0,40,1,0,70,1,0,100,1,0,130,1,0,180,1,0,210,1,0,240,1,0,250,1,0,250,1,0,220,1,0,190,1,0,160,1,0,130,1,0,100,1,0,70,1,0,40,1,0,10,1,0  ,0,0,0,0,0,0,0,0,63,128,0,0,0,0,0,0,0,63)
        if self.Ueberblendung and self.Ueberblendung.Value !=1:
            self.Userform_Res = self.Userform_Res + "A"
        self.Userform_Res = self.Userform_Res + "PatternT"+str(delta_timepoints_count)+"(#LED,"
        if self.servotype==0 :
            self.Userform_Res = self.Userform_Res +"28,"
            anzahl_led = self.no_of_curves # "3"
        else:
            self.Userform_Res = self.Userform_Res + str(27 +self.servotype)+","
            anzahl_led = "1"
        if gotoaction:
            self.Userform_Res = self.Userform_Res + "SI_LocalVar," + str(anzahl_led) + ",0,128,0,"
        else:
            self.Userform_Res = self.Userform_Res + "#InCh," + str(anzahl_led) + ",0,128,0,"
        self.Userform_Res = self.Userform_Res + self.patterntype_str
        
        #self.Userform_Res = self.Userform_Res + "," + str(self.Anim_Abstand_TextBox.Value)
        timepoint_str = ""
        lasttimepoint = 0
        timepointdelta = 0
        for i in range(delta_timepoints_count):
            point = self.curve_points[i+1]
            timepoint = point[0]
            timepointdelta = timepoint - lasttimepoint
            if timepointdelta < 0:
                timepointdelta = 0
            timepoint_str += "," + str(timepointdelta)
            lasttimepoint = timepoint
        self.Userform_Res = self.Userform_Res + timepoint_str # "," + str(self.LED_Abstand_TextBox.Value)

        
        # goto action
        #if gotoaction:
            #dauer_ein = self.Anim_DauerEin_TextBox.Value + self.Anim_PauseS_Ein_TextBox.Value + self.Anim_PauseE_Ein_TextBox.Value
            
            #tag_ein_value = "2"
            #tag_ein_seq_end = "3"
            #tag_aus_value = "4"
            #tag_aus_seq_end = "5"
            #current_tag = tag_ein_value
            #next_tag = current_tag
            #end_time = self.curve_points[-1][0]
            
            #for point in self.curve_points:
                #if anzahl_led == "3":
                    #if point[0] == dauer_ein:
                        #current_tag = tag_ein_seq_end
                        #next_tag = tag_aus_value
                    #elif point[0] == end_time:
                        #current_tag = tag_aus_seq_end
                        #next_tag = "0"
                    #else:
                        #current_tag = next_tag
                    #self.Userform_Res = self.Userform_Res + "," + str(point[1]) + ",1," + current_tag
                #else:
                    #self.Userform_Res = self.Userform_Res + "," + str(point[1])
            #self.Userform_Res = self.Userform_Res + "  "
            #for i in range(total_points_count-2):
                #if self.curve_points[i][0] == dauer_ein: 
                    #self.Userform_Res = self.Userform_Res + ",63,128"
                #else:
                    #self.Userform_Res = self.Userform_Res + ",0"
            #self.Userform_Res = self.Userform_Res + ",63"
            
        #else:
            #for point in self.curve_points:
                #if anzahl_led == "3":
                    #self.Userform_Res = self.Userform_Res + "," + str(point[1]) + ",1,0"
                #else:
                    #self.Userform_Res = self.Userform_Res + "," + str(point[1])
        #self.Userform_Res = self.Userform_Res + ')$' + str(self.Anim_Address_Kanal_TextBox.Value)
        self.generate_pattern_data(anzahl_led, total_points_count, gotoaction)
        self.Hide()
        
    def generate_pattern_data(self, anzahl_led, total_points_count, gotoaction):
        # goto action
        if gotoaction:
            dauer_ein = self.get_Textbox_value(self.Anim_DauerEin_TextBox) + self.get_Textbox_value(self.Anim_PauseS_Ein_TextBox) + self.get_Textbox_value(self.Anim_PauseE_Ein_TextBox)
            
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
        
    def Abort_Button_Click(self, event=None):
        #-----------------------------
        ## VB2PY (CheckDirective) VB directive took path 1 on 1
        #X02.Shell('Explorer https://wiki.mobaledlib.de/anleitungen/spezial/patterngenerator')
        self.Hide()
        self.Userform_Res = ""
        
    def update_active_curve_listbox(self, no_of_items):
        # Clear the current contents of the listbox
        self.Active_Curve_ListBox.Clear()
        
        # Add new items to the listbox
        for i in range(0, no_of_items):
            self.Active_Curve_ListBox.AddItem("LED"+str(i+1))
        
    def Update_Button_Click(self, event=None):
        self.test_started = False
        self.test_continue = False
        self.test_pause = False
        if self.Active_Curve_ListBox:
            self.active_curve = self.Active_Curve_ListBox.Selection
        else:
            self.active_curve = 0
        
        if self.Anim_No_of_Curves_TextBox:
            self.no_of_curves = self.get_Textbox_value(self.Anim_No_of_Curves_TextBox)
            if len(self.curve_points_ary) < self.no_of_curves:
                for i in range(len(self.curve_points_ary), self.no_of_curves):
                    self.curve_points_ary.append([])
            if len(self.LEDcolor_list) < self.no_of_curves:
                for i in range(len(self.LEDcolor_list), self.no_of_curves):
                    self.LEDcolor_list.append("#000000")
                    self.LEDname_list.append("LED"+str(i+1))
                    self.LEDwidth_list.append(2)
            else:
                self.LEDcolor_list = self.LEDcolor_list[:self.no_of_curves]
                self.LEDname_list = self.LEDname_list[:self.no_of_curves]
                self.LEDwidth_list =  self.LEDwidth_list[:self.no_of_curves]
        if self.old_active_curve == self.active_curve:
            self.LEDcolor_list[self.active_curve] = self.Anim_LEDcolor_TextBox.Value
            self.LEDcolor_list[self.active_curve] = self.Anim_LEDcolor_ColorBox.TKWidget.Color
            self.LEDname_list[self.active_curve] = self.Anim_LEDName_TextBox.Value
            self.LEDwidth_list[self.active_curve] = self.Anim_LEDwidth_NumBox.Value
        else:
            self.old_active_curve = self.active_curve
            self.Anim_LEDcolor_TextBox.Value = self.LEDcolor_list[self.active_curve]
            self.Anim_LEDcolor_ColorBox.TKWidget.Color = self.LEDcolor_list[self.active_curve]
            self.Anim_LEDName_TextBox.Value = self.LEDname_list[self.active_curve]
            self.Anim_LEDwidth_NumBox.Value = self.LEDwidth_list[self.active_curve]
        self.Active_Curve_ListBox.Value = self.LEDname_list
        self.Test_Button.TKWidget.configure(text="Starte Test")
        self.redraw_canvas()
       
    def Help_Button_Click(self, event=None):
        helppageurl = "https://wiki.mobaledlib.de/anleitungen/spezial/pyprogramgenerator/servo_animation"
        webbrowser.open_new_tab(helppageurl)
        
    def stop_test(self):
        #print("Stop Test")
        self.Test_Button.TKWidget.configure(text="Fortsetzen Test")
        self.test_continue = False
        self.test_pause = True
        self.test_started = False
        
    def test_calculate_current_curve_points(self, curr_time):
        result_ary = []
        for i in range(0, self.no_of_curves):
            last_point = (i + 1 == self.no_of_curves)
            result = self.test_calculate_current_curve_point2(curr_time, self.curve_points_ary[i], last_point=last_point)
            result_ary.append(result)
        return result_ary
    
    def test_calculate_current_curve_point2(self, curr_time, curve_points, last_point=True):
        curr_point_time = curve_points[self.curr_idx][0]
        next_point_time = curve_points[self.curr_idx+1][0]
        if curr_time == curr_point_time:
            return curve_points[self.curr_idx][1]
        if curr_time > curr_point_time and curr_time < next_point_time:
            curr_value = curve_points[self.curr_idx][1]
            next_value = curve_points[self.curr_idx+1][1]
            return round(curr_value + (next_value - curr_value) * (curr_time - curr_point_time) / (next_point_time -curr_point_time)) # calculate intermediate curve point
        if (curr_time + self.test_deltatime >= next_point_time) and last_point:
            self.curr_idx += 1
            return curve_points[self.curr_idx][1]
        else:
            return curve_points[self.curr_idx+1][1]
        
    def test_calculate_current_curve_point(self, curr_time):
        curr_point_time = self.curve_points[self.curr_idx][0]
        next_point_time = self.curve_points[self.curr_idx+1][0]
        if curr_time == curr_point_time:
            return self.curve_points[self.curr_idx][1]
        if curr_time > curr_point_time and curr_time < next_point_time:
            curr_value = self.curve_points[self.curr_idx][1]
            next_value = self.curve_points[self.curr_idx+1][1]
            return round(curr_value + (next_value - curr_value) * (curr_time - curr_point_time) / (next_point_time -curr_point_time)) # calculate intermediate curve point
        if curr_time + self.test_deltatime >= next_point_time:
            self.curr_idx += 1
            return self.curve_points[self.curr_idx][1]
    
    def run_test_point(self):
        if self.controller.is_connection_open():
            self.test_maxtime =  self.curve_points[-1][0]
            if self.curr_time > self.test_maxtime:
                self.curr_time = 0
                self.curr_idx = 0
            if self.curr_time <= self.test_maxtime and self.test_continue:
                #curr_led_value = self.test_calculate_current_curve_point(self.curr_time)
                #if curr_led_value != self.test_last_led_value:
                    #self.get_led_value_and_send_to_ARDUINO(led_value=curr_led_value)
                    #self.test_last_led_value = curr_led_value
                curr_led_value_ary = self.test_calculate_current_curve_points(self.curr_time)
                curr_led_value = curr_led_value_ary[self.active_curve]
                self.get_led_value_and_send_to_ARDUINO(led_value=curr_led_value_ary, led_g_value=curr_led_value_ary[1], led_b_value=curr_led_value_ary[2], led_value_ary=curr_led_value_ary)
                
                self.canvasframe.after(self.test_deltatime, self.run_test_point)
                self.Kurve_Zeitanzeige_Label.Value = self.curr_time
                if self.controller.detailed_debug_on:
                    self.Kurve_Wertanzeige_Label.Value = str(self.test_deltatime) + "(" + str(int(self.controller.used_time * 1000)) + ")"
                else:
                    self.Kurve_Wertanzeige_Label.Value = str(curr_led_value)
                new_x = self.valx2cx(self.curr_time)
                self.canvas.coords(self.test_cursor_line, new_x, self.ty2cy(0), new_x, self.ty2cy(self.graphHeight))
                self.curr_time += self.test_deltatime
        else:
            self.stop_test()
        
    def start_test(self):
        if self.controller.connect_if_not_connected():
            if self.test_pause:
                self.Test_Button.TKWidget.configure(text="Stop Test")
                self.test_pause = False
                self.test_continue = True
                self.run_test_point()
            else:
                #print("Start Test")
                self.Test_Button.TKWidget.configure(text="Stop Test")
                self.max_idx = len(self.curve_points)
                self.test_deltatime = 40 # 20 # 20ms steps
                self.test_last_led_value = -1
                self.curr_idx = 0
                if self.max_idx > 1:
                    self.test_maxtime = self.curve_points[-1][0]
                    self.curr_time =0
                    self.test_continue = True
                    self.run_test_point()
        else:
            pass
            #print("Error_message-start test")
        
        
    def Test_Button_Click(self, event=None):
        if self.test_started:
            self.stop_test()
            self.test_started = False
        else:
            self.test_started = True
            self.curve_points = self.curve_points_ary[0]
            self.start_test()

    def Anim_Anfangswert_TextBox_Click(self, event=None):
        new_LED_val = self.Anim_Anfangswert_TextBox.Value
        if new_LED_val > self.value_max:
            new_LED_val = self.value_max
        elif new_LED_val < self.value_min:
            new_LED_val = self.value_min
        self.Anim_Anfangswert_TextBox.Value = new_LED_val
        LED_channel = self.Anim_Address_Kanal_TextBox.Value
            
        LED_address = self.Anim_Address_TextBox.Value
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
            
    def Anim_Endwert_TextBox_Click(self, event=None):
        new_LED_val = self.Anim_Endwert_TextBox.Value
        if new_LED_val > self.value_max:
            new_LED_val = self.value_max
        elif new_LED_val < self.value_min:
            new_LED_val = self.value_min
        self.Anim_Endwert_TextBox.Value = new_LED_val
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
            
    def Active_Curve_ListBox_Click(self, event=None):
        self.Update_Button_Click(event)
            
    def Anim_No_of_Curves_TextBox_Click(self, event=None):
        new_val = self.Anim_No_of_Curves_TextBox.Value
        self.update_active_curve_listbox(new_val)
        
    def init_graph(self, frame=None, vertical_params=None, horizontal_params=None, num_vertical=None, num_horizontal=None):
        frame.update()
        # Get the actual width and height
        self.framewidth = frame.winfo_width() - 40
        self.frameheight = frame.winfo_height() - 45
        self.graphTop = 40
        self.graphLeft = 40
        self.graphWidth = self.framewidth - self.graphLeft - 40
        self.graphHeight = self.frameheight - self.graphTop - 40
        self.canvasframe = CF.CanvasFrame(frame, self.frameheight, self.framewidth)
        self.canvasframe.grid(row=1, column=1)
        canvas = self.canvasframe.canvas
        
        canvas.bind("<Up>", self.OnKeyup)
        canvas.bind("<Down>", self.OnKeydown)
        canvas.bind("<Right>", self.OnKeyright)
        canvas.bind("<Left>", self.OnKeyleft)
        canvas.bind("<Delete>", self.OnKeyDelete)
        canvas.bind("<Insert>", self.OnKeyInsert)
        return canvas
    

    def draw_point(self, x, y, xvalue, yvalue, index, color="#00FF00", endpoint=False):
        objid = -1
        if self.get_Anim_CurveType() == curvetype_individuell or endpoint:
            python_green = color
            size = 4
            x1, y1 = (x - size), (y - size)
            x2, y2 = (x + size), (y + size)
            objid = self.canvas.create_oval(x1, y1, x2, y2, fill=python_green, tag=["point", "x:" + str(xvalue), "y:" + str(yvalue), "idx:" + str(index)], width=1, activewidth=3)
            #self.controller.ToolTip_canvas(self.canvas, objid, text="("+str(xvalue)+","+str(yvalue)+")",button_1=True)
            self.canvas.tag_bind(objid,"<Button-1>" ,lambda e,Object=objid:self.MouseButton1(e,Object))
            self.canvas.tag_bind(objid,"<ButtonRelease 1>",lambda e,Object=objid:self.MouseRelease1())
            # Event für Mausbewegung
            self.canvas.tag_bind(objid,"<B1-Motion>",lambda e,Object=objid:self.MouseMove(e,Object))
        return objid
        
        
    def tx2cx(self, x):
        x1 = self.canvas.canvasx(x)
        res = self.graphLeft + x1 * self.canvasframe.total_scalefactor
        return res
    
    def ty2cy(self, y):
        y1 = self.canvas.canvasy(y)
        res = (self.graphTop + self.graphHeight) - y1 * self.canvasframe.total_scalefactor 
        return res
    
    def cy2val(self,cy):
        y1 = cy # self.canvas.canvasy(cy)
        ty = (self.graphTop + self.graphHeight) - (y1 / self.canvasframe.total_scalefactor) 
        val = round((ty / self.vertical_value_factor))
        #print("cy2val:", cy, val, self.canvasframe.total_scalefactor)
        return val
    
    def cx2val(self,cx):
        x1 = cx #self.canvas.canvasx(cx)
        tx = (x1 / self.canvasframe.total_scalefactor) - self.graphLeft
        val = round((tx / self.horizontal_value_factor))
        #print("cx2val:", cx, val, self.canvasframe.total_scalefactor)
        val20 = round(val / 20) * 20
        return val20
    
    def valx2cx(self, val):
        tx = val * self.horizontal_value_factor
        x1 = round((tx + self.graphLeft) * self.canvasframe.total_scalefactor)
        return x1
    
    def valy2cy(self, val):
        ty = val * self.vertical_value_factor
        y1 = round(((self.graphTop + self.graphHeight) - ty) * self.canvasframe.total_scalefactor)
        return y1
    
    def draw_graph(self, line_params=None,  vertical_params=None, horizontal_params=None, num_vertical=8, num_horizontal=10, graph=None, vertical_range=(0, 256), horizontal_range=(0, 20000), on_off_line = 0, graphcolor="#FF0000", graph_only = False,graph_active=True, ueberblendung=True, width=2, graphname=""):
        s_color="#000000"
        s_width=1
        s_linedashed=""
        th_color="#000000"
        th_width=6
        gr_linedashed=""
        gr_color=graphcolor # "#FF0000"
        gr_width=width
        th_linedashed=""        
        vertical_max = vertical_range[1] - vertical_range[0]
        if num_horizontal == 0:
            num_horizontal = 10
        #vertical_line_dist = int(self.graphHeight / num_vertical)
        horizontal_line_dist = int(self.graphWidth / num_horizontal)
        self.vertical_value_factor = self.graphHeight / vertical_max
        vertical_line_dist = int(self.graphHeight  / num_vertical)
        
        horizontal_text_pos = self.graphHeight + 10        
        
        if graph != []:
            horizontal_max = graph[-1][0]
            self.horizontal_value_factor = self.graphWidth / horizontal_max
        else:
            self.horizontal_value_factor = 1                
        
        if not graph_only:
            self.canvasframe.resize(1.0/self.canvasframe.total_scalefactor)
            self.canvas.delete("all")
            # Print the grid lines
            
            self.canvas.create_rectangle(self.tx2cx(0), self.ty2cy(0), self.tx2cx(self.graphWidth), self.ty2cy(self.graphHeight), width=4)
            self.max_y = self.ty2cy(0)
            self.min_y = self.ty2cy(self.graphHeight)
            self.min_x = self.tx2cx(0)
            self.max_x = self.tx2cx(self.graphWidth)
            cur_value = 0
            value_dist = int(vertical_max / num_vertical)
            for i in range (num_vertical+1):
                cur_y = cur_value * self.vertical_value_factor
                objid = self.canvas.create_line(self.tx2cx(0), self.ty2cy(cur_y), self.tx2cx(self.graphWidth), self.ty2cy(cur_y), width=s_width, fill=s_color,dash=s_linedashed,tag="Grid")
                text_objid = self.canvas.create_text(20, self.ty2cy(cur_y), text = cur_value, width=30, fill=s_color,tag="Grid", font=X02.DefaultFont)
                cur_value += value_dist

            objid = -1

        if graph != []:
            self.graph_points = []
            last_text_x = -40
            self.timeline_data_ary = {}
            
            for i in range(len(graph)):
                value = graph[i][1]
                timestr = str(int(graph[i][0]))
                timepoint = graph[i][0]
                cur_y = int((value * self.vertical_value_factor))
                cur_x = int(graph[i][0] * self.horizontal_value_factor)
                point_idx = i
                if not ueberblendung and i > 0:
                    self.graph_points.extend([self.tx2cx(cur_x), self.graph_points[-1]])
                self.graph_points.extend([self.tx2cx(cur_x), self.ty2cy(cur_y)])
                # draw_vertical line
                if not graph_only:
                    objid = self.canvas.create_line(self.tx2cx(cur_x), self.ty2cy(0), self.tx2cx(cur_x), self.ty2cy(self.graphHeight), width=s_width, fill=s_color,dash=s_linedashed,tag="TimeGrid", activewidth=s_width*2)
                    self.timeline_data_ary = {objid: [cur_x, False, ""],} # objid = cur_x, EndWertline, gotoaction
                    #self.canvas.tag_bind(objid,"<Button-1>" ,lambda e,Object=objid:self.MouseButton1(e,Object))
                    #self.canvas.tag_bind(objid,"<ButtonRelease 1>",lambda e,Object=objid:self.MouseRelease1())
                    # Event für Mausbewegung
                    #self.canvas.tag_bind(objid,"<B1-Motion>",lambda e,Object=objid:self.MouseMove(e,Object))                
                    
                    if cur_x - last_text_x >= 40:
                        text_objid = self.canvas.create_text(self.tx2cx(cur_x), self.ty2cy(horizontal_text_pos), text = timestr, width=40, fill=s_color,tag="Grid", font = X02.DefaultFont)
                        last_text_x = cur_x
                if graph_active:
                    if on_off_line != 0:
                        endpoint = cur_x == int(on_off_line * self.horizontal_value_factor) # Ein/Auslinie
                        if endpoint:
                            self.endwertpoint = int(graph[i][0])
                            self.endwertpoint_idx = i
                    else:
                        endpoint = i == len(graph) - 1
                        if endpoint:
                            self.endwertpoint = int(graph[i][0])
                            self.endwertpoint_idx = i
                    if i == 0:
                        endpoint = True
                    point_id = self.draw_point(self.tx2cx(cur_x), self.ty2cy(cur_y), timepoint, value, point_idx, endpoint=endpoint)
                
            #if ueberblendung:
                #draw_graph_points = self.graph_points
            #else:
                #draw_graph_points = []
                #for i in range(0, len(self.graph_points)):
                    #draw_graph_points.append(self.graph_points[i])
                    #if i % 2 == 0 and i > 0 and i < len(self.graph_points) - 1:
                        #draw_graph_points.append(self.graph_points[i-1])
                        #draw_graph_points.append(self.graph_points[i])
                        
            if graph_active:
                self.line_objid = self.canvas.create_line(self.graph_points, width=gr_width*2, fill=gr_color,dash=gr_linedashed,tag="Line", activewidth=gr_width*4)
                self.controller.ToolTip_canvas(self.canvas, self.line_objid, graphname)
            else:
                line_objid = self.canvas.create_line(self.graph_points, width=gr_width, fill=gr_color,dash=gr_linedashed,tag="Line", activewidth=gr_width*2)
                self.controller.ToolTip_canvas(self.canvas, line_objid, graphname)
            # create EIN/AUS Line
            
            if on_off_line > 0:
                cur_x = on_off_line * self.horizontal_value_factor
                objid = self.canvas.create_line(self.tx2cx(cur_x), self.ty2cy(0), self.tx2cx(cur_x), self.ty2cy(self.graphHeight), width=th_width, fill=th_color,dash=th_linedashed,tag="TimeGrid", activewidth=th_width*2)
            self.test_cursor_line = self.canvas.create_line(self.tx2cx(0), self.ty2cy(0), self.tx2cx(0), self.ty2cy(self.graphHeight), width=gr_width, fill=gr_color,dash=gr_linedashed,tag="TestCursor", activewidth=th_width*2)
        self.canvas.tag_raise("Line")
        self.canvas.tag_raise("point")
        
    def round2interval(self, val, interval=20):
        val_new = round(val / interval) * interval
        return val_new
    
    def synch_timepoints_between_curves(self):
        if self.no_of_curves <= 1:
            return
        graph = self.curve_points_ary[self.active_curve]
        for i in range(len(graph)):
            timepoint = graph[i][0]
            for j in range(0, self.no_of_curves):
                if j != self.active_curve:
                    if len(self.curve_points_ary) == j:
                        self.curve_points_ary.append([])
                    if len(self.curve_points_ary[j]) < i +1:
                        self.curve_points_ary[j].append([timepoint, 0])
                    else:
                        self.curve_points_ary[j][i][0] = timepoint
        
    def redraw_canvas(self):
        if self.Active_Curve_ListBox:
            self.active_curve = self.Active_Curve_ListBox.Selection
        else:
            self.active_curve = 0
            
        self.use_ueberblendung = True if self.Ueberblendung and self.Ueberblendung.Value != 1 else False
                
        self.canvas = self.init_graph(frame=self.FrameR2.TKWidget)
        self.canvas.delete("all")
        graph_only = False
        self.synch_timepoints_between_curves()
        self.controller.clear_ToolTip_canvas()
        for i in range(0, self.no_of_curves):
            self.curve_points = self.curve_points_ary[i]
            self.curve_points = self.calculate_complete_curve(curve_no=i)
            self.curve_points_ary[i] = self.curve_points
            anzahl_werte = len(self.curve_points) - 1
            on_off_line =  self.calculate_on_off_line()
            graph_active = (i == self.active_curve)
            self.draw_graph(num_horizontal=anzahl_werte, graph=self.curve_points, on_off_line=on_off_line, graphcolor=self.LEDcolor_list[i], graph_only=graph_only, graph_active=graph_active, ueberblendung=self.use_ueberblendung, width=self.LEDwidth_list[i], graphname=self.LEDname_list[i])
            graph_only = True
        self.curve_points = self.curve_points_ary[self.active_curve]
        
    def MouseButton1(self,event,cvobject):
        self.startxy = None
        self.canvas.focus_set()
        self.point_idx = -1
        self.current_objid = -1
        if cvobject != -1: #and self.get_Anim_CurveType() == 2: # individuel
            tags = self.canvas.gettags(cvobject)
            objecttype = tags[0]
            if objecttype == "point":
                point_idx_str= tags[3].split(":")
                if point_idx_str[0] == "idx":
                    self.point_idx = int(point_idx_str[1])
                    valx = self.curve_points[self.point_idx][0]
                    valy = self.curve_points[self.point_idx][1]
                    self.startxy = (self.valx2cx(valx),self.valy2cy(valy))
                    #print("MouseButton,1:", valx, valy, self.startxy)
                    self.current_curve_point = self.curve_points[self.point_idx]
                else:
                    self.point_idx = -1
                    self.startxy = (event.x, event.y)
                self.mm_canvas_coord_list = self.canvas.coords(self.line_objid)
                self.mm_canvas_coord_list_org = self.mm_canvas_coord_list.copy()
                self.Kurve_Zeitanzeige_Label.Value = valx
                self.Kurve_Wertanzeige_Label.Value = valy
                self.current_objid = cvobject

    def MouseMove(self,event,cvobject):
        if self.point_idx != - 1:
            if not self.use_ueberblendung:
                tmp_point_idx = self.point_idx * 2
                tmp_last_point_delta = 2
            else:
                tmp_point_idx = self.point_idx
                tmp_last_point_delta = 1
            pos_x1 = self.canvas.canvasx(event.x)
            pos_y1 = self.canvas.canvasy(event.y)
            if pos_y1 > self.max_y:
                pos_y1 = self.max_y
            if pos_y1 < self.min_y:
                pos_y1 = self.min_y
            dx = pos_x1-self.startxy[0]
            dy = pos_y1-self.startxy[1]
            if self.Anim_TimeStepType_ListBox.Selection != timesteptype_individuell or tmp_point_idx == 0 or tmp_point_idx == len(self.curve_points) - 1:
                # keep x pos
                dx = 0
            new_x =  self.mm_canvas_coord_list[tmp_point_idx*2] + dx
            if dx != 0:
                xmin = self.mm_canvas_coord_list[(tmp_point_idx-tmp_last_point_delta)*2]
                if (tmp_point_idx + 1) *2 < len(self.mm_canvas_coord_list):
                    xmax = self.mm_canvas_coord_list[(tmp_point_idx+1)*2]
                else:
                    xmax = self.mm_canvas_coord_list[(tmp_point_idx)*2]
                if (new_x < xmin):
                    dx = 0
                    pos_x = xmin
                elif (new_x > xmax):
                    dx = 0
                    pos_x = xmax
                else:
                    pos_x = self.startxy[0] + dx
            else:
                pos_x = self.startxy[0] + dx
            pos_y = self.startxy[1] + dy
            self.startxy = (pos_x, pos_y)
            self.canvas.move(cvobject, dx, dy)
            # update graph points:
            
            self.mm_canvas_coord_list[tmp_point_idx*2 +1] += dy
            self.mm_canvas_coord_list[tmp_point_idx*2] += dx
            if not self.use_ueberblendung and tmp_point_idx * 2 < len(self.mm_canvas_coord_list) - 2:
                self.mm_canvas_coord_list[tmp_point_idx*2 +3] += dy
                #self.mm_canvas_coord_list[tmp_point_idx*2+2] += dx
                
            #val_x =  self.curve_points[self.point_idx][0]
            val_x = int(self.cx2val(pos_x))
            val_y = int(self.cy2val(pos_y))
            if self.current_curve_point != None:
                dval_y = self.current_curve_point[1] - val_y
            else:
                dval_y = 0
            self.current_curve_point = [val_x, val_y]
            #print("MouseMove:", val_x, val_y, self.current_curve_point, pos_x, pos_y, event.x, event.y)
            self.curve_points[self.point_idx] = self.current_curve_point
            self.canvas.coords(self.line_objid,self.mm_canvas_coord_list)
            self.Kurve_Zeitanzeige_Label.Value = self.current_curve_point[0]
            self.Kurve_Wertanzeige_Label.Value = self.current_curve_point[1]
            if self.Anim_Anfangswert_TextBox:
                if self.current_curve_point[0] == 0:
                    self.Anim_Anfangswert_TextBox.Value = self.current_curve_point[1]
            if self.Anim_Endwert_TextBox:
                if self.current_curve_point[0] == self.endwertpoint:
                    self.Anim_Endwert_TextBox.Value = self.current_curve_point[1]             
                
            if self.startxy != None and dval_y != 0 and not self.test_continue:
                self.get_led_value_and_send_to_ARDUINO(point_idx=self.point_idx)
            
            
    def MouseRelease1(self):
        # update line
        # update graphpoints
        # update graph
        if self.startxy != None:
            self.get_led_value_and_send_to_ARDUINO(point_idx=self.point_idx)
        self.startxy = None
        
    def move_point(self, objid, dvalx, dvaly):
        if objid != -1:
            tags = self.canvas.gettags(objid)
            objecttype = tags[0]
            if objecttype == "point":
                point_idx_str= tags[3].split(":")
                if point_idx_str[0] == "idx":
                    self.point_idx = int(point_idx_str[1])
                    if self.Anim_TimeStepType_ListBox.Selection != timesteptype_individuell or self.point_idx == 0 or self.point_idx == len(self.curve_points) - 1:
                        dvalx = 0
                    xmin = self.mm_canvas_coord_list[(self.point_idx-1)*2]
                    xmax = self.mm_canvas_coord_list[(self.point_idx+1)*2]
                    val_xmin = self.cx2val(xmin)
                    val_xmax = self.cx2val(xmax)
                    val_x1 = self.curve_points[self.point_idx][0]
                    pos_x1 = self.valx2cx(val_x1)
                    val_x2 = val_x1 + dvalx
                    if val_x2 < val_xmin:
                        val_x2 = val_xmin
                    if val_x2 > val_xmax:
                        val_x2 = val_xmax
                    pos_x2 = self.valx2cx(val_x2)
                    val_y1 = self.curve_points[self.point_idx][1]
                    pos_y1 = self.valy2cy(val_y1)
                    val_y2 = val_y1 + dvaly
                    pos_y2 = self.valy2cy(val_y2)
                
                    self.mm_canvas_coord_list = self.canvas.coords(self.line_objid)
                    self.mm_canvas_coord_list_org = self.mm_canvas_coord_list.copy()
                    
                    pos_x = self.valx2cx(val_x2)
                    pos_y = self.valy2cy(val_y2)
                    self.startxy = (pos_x, pos_y)
                    dx = pos_x2 - pos_x1
                    dy = pos_y2 - pos_y1
                    self.canvas.move(objid, dx, dy)
                    # update graph points:
                    self.mm_canvas_coord_list[self.point_idx*2 +1] += dy
                    self.mm_canvas_coord_list[self.point_idx*2] += dx
                    #val_x =  self.curve_points[self.point_idx][0]
                    self.current_curve_point = [val_x2, val_y2]
                    #print("MouseMove:", val_x, val_y, self.current_curve_point, pos_x, pos_y, event.x, event.y)
                    self.curve_points[self.point_idx] = self.current_curve_point
                    self.canvas.coords(self.line_objid,self.mm_canvas_coord_list)
                    self.Kurve_Zeitanzeige_Label.Value = self.current_curve_point[0]
                    self.Kurve_Wertanzeige_Label.Value = self.current_curve_point[1]
                    if dvaly != 0 and not self.test_continue:
                        self.get_led_value_and_send_to_ARDUINO(point_idx=self.point_idx)
                        
                        
    def delete_point(self, objid):
        if objid != -1:
            tags = self.canvas.gettags(objid)
            objecttype = tags[0]
            if objecttype == "point":
                point_idx_str= tags[3].split(":")
                if point_idx_str[0] == "idx":
                    self.point_idx = int(point_idx_str[1])
                    if self.point_idx != 0 and self.point_idx != len(self.curve_points) - 1:
                        #del self.curve_points[self.point_idx]
                        for i in range(0, self.no_of_curves):
                            del self.curve_points_ary[i][self.point_idx]
                        del self.mm_canvas_coord_list[self.point_idx]
                        self.current_objid = -1
                        self.redraw_canvas()
                        
    def insert_new_curvepoint(self):
        for i in range(0, self.no_of_curves):
            self.curve_points = self.curve_points_ary[i]
            curve_point1 =  self.curve_points[self.point_idx]
            curve_point2 =  self.curve_points[self.point_idx+1]
            newx = curve_point1[0] + (curve_point2[0] - curve_point1[0]) / 2
            newx = self.round2interval(newx, 20)
            newy = curve_point1[1] + (curve_point2[1] - curve_point1[1]) / 2
            newy = self.round2interval(newy, 1)
            new_curve_point = [newx, newy]
            self.curve_points.insert(self.point_idx+1, new_curve_point)
            self.curve_points_ary[i] = self.curve_points 
                    
    def insert_point(self, objid):
        if objid != -1:
            tags = self.canvas.gettags(objid)
            objecttype = tags[0]
            if objecttype == "point":
                point_idx_str= tags[3].split(":")
                if point_idx_str[0] == "idx":
                    self.point_idx = int(point_idx_str[1])
                    if self.point_idx != len(self.curve_points) - 1:
                        self.insert_new_curvepoint()
                        #curve_point1 =  self.curve_points[self.point_idx]
                        #curve_point2 =  self.curve_points[self.point_idx+1]
                        #newx = curve_point1[0] + (curve_point2[0] - curve_point1[0]) / 2
                        #newx = self.round2interval(newx, 20)
                        #newy = curve_point1[1] + (curve_point2[1] - curve_point1[1]) / 2
                        #newy = self.round2interval(newy, 1)
                        #new_curve_point = [newx, newy]
                        #self.curve_points.insert(self.point_idx+1, new_curve_point)
                        self.redraw_canvas()
                    

    def OnKeyDelete(self,event=None):
        if self.current_objid != -1:
            self.delete_point(self.current_objid)

    def OnKeyInsert(self,event=None):
        if self.current_objid != -1:
            self.insert_point(self.current_objid)

        
    def OnKeyup(self,event=None):
        if self.current_objid != -1:
            self.move_point(self.current_objid, 0, 1)
    
    def OnKeydown(self,event=None):
        if self.current_objid != -1:
            self.move_point(self.current_objid, 0, -1)
        
    def OnKeyright(self,event=None):
        if self.current_objid != -1:
            self.move_point(self.current_objid, 20, 0)
    
    def OnKeyleft(self,event=None):
        if self.current_objid != -1:
            self.move_point(self.current_objid, -20, 0)
        
    def get_led_value_and_send_to_ARDUINO(self, led_value_ary = None, led_value=None, led_g_value=None, led_b_value=None, point_idx=None):
        if led_value == None:
            if point_idx != None:
                new_LED_val = self.curve_points_ary[0][point_idx]
                if len(self.curve_points_ary) == 3:
                    led_g_value = self.curve_points_ary[1][point_idx]
                    led_b_value = self.curve_points_ary[2][point_idx] 
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
        if self.Anim_Type_ListBox:
            self.servotype = self.Anim_Type_ListBox.Selection
        else:
            self.servotype = 0        
        LED_channel = self.self.Anim_Address_Kanal_TextBox.Value
        if self.servotype == 0:
            self._update_servos(LED_address,new_LED_val,1, 0, channel=LED_channel)
        elif self.servotype == 1:
            self._update_servos(LED_address,new_LED_val, 0, 0, channel=LED_channel)
        elif self.servotype == 2:
            self._update_servos(LED_address,0, new_LED_val, 0, channel=LED_channel)
        else:
            self._update_servos(LED_address,0, 0, new_LED_val, channel=LED_channel)    
                
    def on_click(self, event):
        selected = self.canvas.find_overlapping(event.x-10, event.y-10, event.x+10, event.y+10)
        if selected:
            self.canvas.selected = selected[-1]  # select the top-most item
            self.startxy = (event.x, event.y)
            #print(self.canvas.selected, self.canvas.startxy)
        else:
            self.canvas.selected = None
    
    def on_drag(self, event):
        if self.canvas.selected:
            # calculate distance moved from last position
            dx, dy = event.x-self.startxy[0], event.y-self.startxy[1]
            # move the selected item
            self.canvas.move(self.canvas.selected, dx, dy)
            # update last position
            self.startxy = (event.x, event.y)
            
    def _update_servos(self, lednum, positionValueHigh, controlValue, positionValueLow, channel=0):
        if channel != 0:
            # update lednum according to offset for selected channel number
            lednum += self.controller.get_lednum_offset_for_channel(channel)
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(controlValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:04x}'.format(lednum) + " " + '{:02x}'.format(positionValueHigh) + " " + '{:02x}'.format(controlValue) + " " + '{:02x}'.format(positionValueLow) + " " + '{:02x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        #time.sleep(0.2)
        
    def _update_LEDs(self, lednum, red, green, blue, channel=0):
        if channel != 0:
            # update lednum according to offset for selected channel number
            lednum += self.controller.get_lednum_offset_for_channel(channel)
        if self.controller.mobaledlib_version == 1:
            message = "#L" + '{:02x}'.format(lednum) + " " + '{:02x}'.format(red) + " " + '{:02x}'.format(green) + " " + '{:02x}'.format(blue) + " " + '{:02x}'.format(1) + "\n"
        else:
            message = "#L " + '{:04x}'.format(lednum) + " " + '{:02x}'.format(red) + " " + '{:02x}'.format(green) + " " + '{:02x}'.format(blue) + " " + '{:02x}'.format(1) + "\n"
        self.controller.send_to_ARDUINO(message)
        #time.sleep(0.2)            

    


