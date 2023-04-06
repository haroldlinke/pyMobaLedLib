# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
# *  
# * https://github.com/Hardi-St/MobaLedLib
# *
# * MobaLedCheckColors is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * MobaLedCheckColors is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************
from vb2py.vbfunctions import *
from vb2py.vbdebug import *
from vb2py.vbconstants import *

import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
# fromx PIL import Image, ImageTk
import uuid
import proggen.Prog_Generator as PG

import proggen.M02_Public as M02
import proggen.M03_Dialog as M03
import proggen.M06_Write_Header as M06
import proggen.M06_Write_Header_LED2Var as M06LED
import proggen.M06_Write_Header_Sound as M06Sound
import proggen.M06_Write_Header_SW as M06SW
import proggen.M07_COM_Port as M07
import proggen.M08_ARDUINO as M08
import proggen.M09_Language as M09
import proggen.M09_Select_Macro as M09SM
import proggen.M09_SelectMacro_Treeview as M09SMT
import proggen.M10_Par_Description as M10
import proggen.M20_PageEvents_a_Functions as M20
import proggen.M25_Columns as M25
import proggen.M27_Sheet_Icons as M27
import proggen.M28_divers as M28
import proggen.M30_Tools as M30
import proggen.M31_Sound as M31
import proggen.M37_Inst_Libraries as M37
import proggen.M60_CheckColors as M60
import proggen.M70_Exp_Libraries as M70
import proggen.M80_Create_Mulitplexer as M80
import proggen.Prog_Generator as PG

#import proggen.D09_StatusMsg_Userform as D09

import ExcelAPI.XLW_Workbook as P01

from ExcelAPI.XLC_Excel_Consts import *

STD_FONT = ("SANS_SERIF",10)

class SelectMacrosTreeform:
    def __init__(self):
        self.title = M09.Get_Language_Str("Auswahl des Makros")
        self.label1_txt = M09.Get_Language_Str("Makroauswahl:")
        self.label2_txt = M09.Get_Language_Str("Filter")
        #self.label3_txt = ""
        self.controller = PG.get_global_controller()
        self.IsActive = False
        self.button1_txt = M09.Get_Language_Str("Abbrechen")
        self.button2_txt = M09.Get_Language_Str("Ok")
        self.res = False
        self.SelectMame = ""
        self.SelectRow = 0
        self.Last_SelectedNr_Valid = False
        self.Last_SelectedNr = 0
        self.SelectMacro_Res = "" 
        self.ActKey = ""
        self.ActiveNode = None

 
    def ok(self, event=None):
        self.IsActive = False
        self.Select_Button_Click()
        #self.Userform_res = ""
        self.top.destroy()
        self.res = True
 
    def cancel(self, event=None):
        self.UserForm_res = '<Abort>'
        self.IsActive = False
        self.top.destroy()
        self.res = False

    def Start(self):
        Debug.Print("Start")
        self.entry1_input = tk.StringVar(self.controller)
        self.top = tk.Toplevel(self.controller)
        self.top.transient(self.controller)
        self.entry1_input.set("")
        
        self.std_font = Font(
            family = 'Tahoma',
            size = 11,
            weight = 'bold'            
        )
        
        self.entry1 = tk.Entry(self.top,width=10,textvariable=self.entry1_input)
        self.ActLanguage = M09.Get_ExcelLanguage()
       
        
        
        self.top.resizable(False, False)  # This code helps to disable windows from resizing
        
        window_height = 700
        window_width = 1400
        
        winfo_x = PG.global_controller.winfo_x()
        winfo_y = PG.global_controller.winfo_y()
        
        screen_width = PG.global_controller.winfo_width()
        screen_height = PG.global_controller.winfo_height()
        
        x_cordinate = winfo_x+int((screen_width/2) - (window_width/2))
        y_cordinate = winfo_y+int((screen_height/2) - (window_height/2))
        
        self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))             
        
        if len(self.title) > 0: self.top.title(self.title)
        self.label1 = ttk.Label(self.top, text=self.label1_txt,wraplength=window_width,font=("Tahoma", 11))
        self.label2 = ttk.Label(self.top, text=self.label2_txt,wraplength=window_width,font=("Tahoma", 11),foreground="#0000FF")
        #self.label3 = ttk.Label(self.top, text=self.label3_txt,wraplength=window_width,font=("Tahoma", 11))
        
        self.description = tk.StringVar()
        self.description.set("var1")
        self.label4 = ttk.Label(self.top, text="test1",wraplength=window_width,font=("Tahoma", 11),textvariable=self.description,relief=tk.SUNKEN,borderwidth=1)
        self.detail = tk.StringVar()
        self.detail.set("var2")
        self.label5 = ttk.Label(self.top, text="Test2",wraplength=window_width,font=("Tahoma", 11),textvariable=self.detail,relief=tk.SUNKEN,borderwidth=1)
        self.label1.grid(row=0,column=0,columnspan=1,sticky="nesw",padx=10,pady=10)
        self.label2.grid(row=0,column=1,columnspan=1,rowspan=1,sticky="nesw",padx=10,pady=10)
        #self.label3.grid(row=3,column=0,columnspan=1,sticky="nesw",padx=10,pady=10)
        
        self.macrotree = self.create_treeframe(self.top)
        self.macrotree.grid(row=1,column=0,columnspan=3,rowspan=1,sticky="nesw",padx=10,pady=10)
        
        self.label4.grid(row=2,column=0,columnspan=3,rowspan=1,sticky="nesw",padx=10,pady=10)
        self.label5.grid(row=3,column=0,columnspan=3,rowspan=1,sticky="nesw",padx=10,pady=10)
        self.entry1.grid(row=0,column=2)
        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)            
        self.button_frame = ttk.Frame(self.top)
        
        self.b_cancel = tk.Button(self.button_frame, text=self.button1_txt, command=self.cancel,width=10,font=("Tahoma", 11))
        self.b_ok = tk.Button(self.button_frame, text=self.button2_txt, command=self.ok,width=10,font=("Tahoma", 11))

        self.b_cancel.grid(row=0,column=0,sticky="e",padx=10,pady=10)
        self.b_ok.grid(row=0,column=1,sticky="e",padx=10,pady=10)
        
        self.button_frame.grid(row=4,column=1,sticky="e")
        
        self.IsActive = True

        return
    
    def CreateMacroTree(self, Tree, Parent, Filter, Dictionary):
        Debug.Print("CreateMacroTree")
        #self.__InitializeTreeFrom_Lib_Macros_Sheet(Parent,Filter)  #Filter)
        #return
    
        for key in Dictionary :
            if key[0]!="*":
                uid = uuid.uuid4()
                if isinstance(Dictionary[key], dict):
                    subdict = Dictionary[key]
                    value = subdict.get("*"+key,"")
                    description = value[0]
                    icon=value[1]
                    row = value[2]
                    if icon:
                        Tree.insert(Parent, 'end', uid, text=key,value=(description,str(row)),image=icon,tags=("node"))
                    else:
                        Tree.insert(Parent, 'end', uid, text=key,value=(description,str(row)),tags=("node"))
                    key_width = self.std_font.measure(key+"      ")
                    self.max_key_width = max(key_width, self.max_key_width)                
                    self.CreateMacroTree(Tree, uid, Filter, Dictionary[key])
                elif isinstance(Dictionary[key], list):
                    Tree.insert(Parent, 'end', uid, text=key + '[]')
                    key_width = self.std_font.measure(key+"      ")
                    self.max_key_width = max(key_width, self.max_key_width)                          
                    self.CreateMacroTree(Tree,uid, Filter, dict([(i, x) for i, x in enumerate(Dictionary[key])]))
                else:
                    value = Dictionary[key]
                    description = value[0]
                    icon=value[1]
                    row=value[2]
                    value_width = self.std_font.measure(description+"      ")
                    self.max_value_width = max(value_width, self.max_value_width)
                    if icon:
                        Tree.insert(Parent, 'end', uid, text=key, value=(description,str(row)),image=icon,tags=(str(row)))
                    else:
                        Tree.insert(Parent, 'end', uid, text=key, value=(description,str(row)),tags=(str(row)))
                
    def selectItem(self,a):
        Debug.Print("selectItem")
        curItem = self.tree.focus()
        selectedItem_dict = self.tree.item(curItem)
        if selectedItem_dict != {}:
            item = self.tree.item(curItem)
            #record = item['description']
            # show a message
            #print("selectedItem:",item)
        
    
    def clickItem(self,a):
        Debug.Print("clickItem")
        curItem = self.tree.focus()
        item = self.tree.item(curItem)
        #record = item['#0']
        # show a message
        #print("click item:",item)
        Sh = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
        Key = item["values"][1] #val(Split(with_8.key, ' ')(0))
        self.ActKey = Key
        Row = P01.val(Split(Key, ' ')(0))
        Desc = Replace(Sh.Cells(Row, M02.SM_DetailCOL + self.ActLanguage * M02.DeltaCol_Lib_Macro_Lang), '|', vbLf)
        if IsNumeric(Key):
            if Desc == '':
                Desc = Replace(Sh.Cells(Row, M02.SM_ShrtD_COL + self.ActLanguage * M02.DeltaCol_Lib_Macro_Lang), '|', vbLf)
            self.Set_Description(Desc)
            self.detail.set(M30.Replace_Multi_Space(Sh.Cells(Row, M02.SM_Macro_COL)))
        else:
            if Desc != '':
                self.Set_Description(Desc)
            else:
                self.Display_Navigation_Keys()
            self.Detail = Replace(Sh.Cells(Row, M02.SM_Group_COL).Value, '|', ' > ') 
        self.top.update()
       
    
    def create_treeframe(self,parent):
        Debug.Print("create_treeframe")
        # Setup Data
        self.max_value_width = 0
        self.max_key_width = 0
        
        # Setup the Frames
        TreeFrame = ttk.Frame(parent, padding="3",borderwidth=3)
        #TreeFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.tree = ScrollableTV(TreeFrame, height=20, columns=("description"),show="tree") #ttk.Treeview(TreeFrame, columns=('Values'))
        #style = ttk.Style()
        #style.configure("Treeview", font=ttk.STD_FONT)
        self.tree.heading("description", text=M09.Get_Language_Str("Beschreibung"), anchor="w")
        #self.tree.heading("dummy", text="dummy", anchor="w")
         
        #tree.column("#0", width=200, stretch=False)
        #tree.column("value", minwidth=2500, width=1000, stretch=True)
        self.tree.grid(padx=8, pady=(8,0),sticky="nesw")

        self.filter = ""
        
        self.__InitializeTreeFrom_Lib_Macros_Sheet(self.tree, self.filter)

        self.CreateMacroTree(self.tree, '', self.filter, self.macro_dict)
        
        TreeFrame.grid_columnconfigure(0,weight=1)
        TreeFrame.grid_rowconfigure(0,weight=1)
        verscrlbar = ttk.Scrollbar(TreeFrame,  
                                   orient =tk.VERTICAL,  
                                   command = self.tree.yview)
        verscrlbar.grid(row=0,column=1,sticky="ns") 
        # Configuring treeview 
        self.tree.configure(yscrollcommand = verscrlbar.set)             
        horscrlbar = ttk.Scrollbar(TreeFrame,  
                                   orient =tk.HORIZONTAL,  
                                   command = self.tree.xview)
        horscrlbar.grid(row=1,column=0,sticky="we",padx=8, pady=(0,8)) 
        # Configuring treeview 
        self.tree.configure(xscrollcommand = horscrlbar.set)
        self.tree.column("#0", width=self.max_key_width, stretch=True)
        self.tree.column("#1",width=1000,stretch=True)
        
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        children_list = self.tree.get_children()
        first_child_id = children_list[0]
        
        self.tree.focus_set()
        
        self.tree.selection_set(first_child_id)
        
        self.tree.item(first_child_id,open=True)
        
        self.tree.focus(first_child_id)
        
        #self.tree.bind('<Button-1>', self.clickItem)
        #self.tree.bind('<Double-1>', self.selectItem)
        return TreeFrame 
    
    
    
    def item_selected(self,event):
        Debug.Print("item_selected")
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            #record = item['#0']
            # show a message
            #print("item_selected:",item)
            #showinfo(title='Information', message=','.join(record))
            
            Sh = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
            
            Key = item["values"][1] #val(Split(with_8.key, ' ')(0))
            self.ActKey = Key
            Row = P01.val(Split(Key, ' ')(0))
            Desc = Replace(Sh.Cells(Row, M02.SM_DetailCOL + self.ActLanguage * M02.DeltaCol_Lib_Macro_Lang), '|', vbLf)
            if IsNumeric(Key):
                if Desc == '':
                    Desc = Replace(Sh.Cells(Row, M02.SM_ShrtD_COL + self.ActLanguage * M02.DeltaCol_Lib_Macro_Lang), '|', vbLf)
                self.Set_Description(Desc)
                self.detail.set(M30.Replace_Multi_Space(Sh.Cells(Row, M02.SM_Macro_COL)))
            else:
                if Desc != '':
                    self.Set_Description(Desc)
                else:
                    self.Display_Navigation_Keys()
                self.detail.set(Replace(Sh.Cells(Row, M02.SM_Group_COL).Value, '|', ' > '))
                
            self.top.update()        

    def __UserForm_Initialize(self):
        Debug.Print("__UserForm_Initialize")
        self.__InitializeTreeView()
    
    def __userform_terminate(self):
        ## VB2PY (CheckDirective) VB directive took path 1 on DebugMode = 1
        gFormTerm = gFormTerm + 1
        self.ClassCounts()   
    
    def __Add_Node(self,c):
        Debug.Print("__Add_Node")

        #-------------------------------
        Sh = c.Parent
        Row = c.Row
        ## VB2PY (CheckDirective) VB directive took path 1 on USE_LNAME
        Name = M09SM.Get_Language_Text(Row, M02.SM_LName_COL, self.ActLanguage)
        if Name == '':
            Name = c.Value
        with_3 = Sh
        GroupNames = M09SM.Get_Language_Text(Row, M02.SM_Group_COL, self.ActLanguage)
        Description = M09SM.Get_Language_Text(Row, M02.SM_ShrtD_COL, self.ActLanguage)
        if GroupNames == '':
            GroupNames = 'Not grouped'
        GroupNArr = Split(GroupNames, '|')
        #print("Find Child",Row)
        PicNamesArrInp = Split(with_3.Cells(Row, M02.SM_Pic_N_COL).Value, '|')
        PicNamesArr = vbObjectInitialize((UBound(GroupNArr) + 1,), Variant)
        for i in vbForRange(0, UBound(PicNamesArrInp)):
            if i > UBound(GroupNArr) + 1:
                break
            PicNamesArr[i] = M30.NoExt(Trim(PicNamesArrInp(i)))
        iconimagename = PicNamesArrInp[len(PicNamesArrInp)-1]
        if iconimagename !="":
            iconfilename = PG.ThisWorkbook.pyProgPath + '/' + "icons/"+Trim(iconimagename)+".png"
            #pic1 = Image.open(iconfilename)           # Open the image like this first
            Debug.Print("MacroTree-addNode - iconFilename:"+iconfilename)
            self.pic2 = tk.PhotoImage(file=iconfilename)      # Then with PhotoImage. NOTE: self.root_pic2 =     and not     root_pic2 =
            Debug.Print("MacroTree-addNode - iconFilename:"+iconfilename+" -OK-")
        else:
            self.pic2=None
        
        if Name == "":
            cur_dict = self.macro_dict
            for group in GroupNArr:
                group=Trim(group)
                cur_dict_group = cur_dict.get(group,None)
                if cur_dict_group==None:
                    cur_dict_group=cur_dict
                    cur_dict[group]={"*"+group: (Description,self.pic2,str(0))}
                    break
                else:
                    cur_dict = cur_dict_group
        else:
            cur_dict = self.macro_dict
            Level = 0
            for group in GroupNArr:
                group=Trim(group)
                cur_dict_group = cur_dict.get(group,None)
                if cur_dict_group == None:
                    cur_dict[group]={"*"+group: (Description,self.pic2,str(Row))}
                    cur_dict = cur_dict.get(group,None)
                    break
                else:
                    cur_dict = cur_dict_group
                Level = Level +1
                    
            if cur_dict != None:
                Name=Trim(Name)
                cur_dict[Name] = (Description,self.pic2,str(Row))

    
    def __InitializeTreeFrom_Lib_Macros_Sheet(self,Parent,Filter):
        Debug.Print("__InitializeTreeFrom_Lib_Macros_Sheet")
        fn_return_value = None
        
        self.macro_dict ={}

        #-----------------------------------------------------------------------------
        # Add elements to the Treeview and return the number of the listbox entry which matches with the given string
        #ShowHourGlassCursor(True)
        #if not self.Visible:
        #P01.StatusMsg_UserForm.ShowDialog('Initialisiere Dialog...', '')
        #else:
        #    Please_Wait.Visible = True
        #    DoEvents()
        #if not __mcTree is None:
        #    __mcTree.NodesClear()
            #Some Treeview properties are retained for another session
        ListDataSh = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
        Debug_Language = -1 #ListDataSh.Range('Test_Language')
        if Debug_Language == - 1:
            self.ActLanguage = M09.Get_ExcelLanguage()
        else:
            self.ActLanguage = Debug_Language
            Debug.Print('Using Debug_Language:' + Debug_Language)
        #Debug.Print "InitializeTreeFrom_Lib_Macros_Sheet(" & Filter & "," & TextBoxFilter.Text & ")" ' Debug
        fn_return_value = - 1
        with_5 = ListDataSh
        #r = with_5.Range(with_5.Cells(M02.SM_DIALOGDATA_ROW1, M02.SM_Name__COL), with_5.Cells(M30.LastUsedRowIn(ListDataSh), M02.SM_Name__COL))
        # VB2PY (UntranslatedCode) On Error GoTo ErrMsg
        Cnt = 0
        for Row in range(M02.SM_DIALOGDATA_ROW1,ListDataSh.LastUsedRow):
            #If c.Row = 80 Then
            #   Debug.Print "Row " & c.Row
            #End If
            c = ListDataSh.Cells(Row,M02.SM_Name__COL)
            Expert_CheckBox = True #*HL
            #print("Initialize Tree:",Row,M02.SM_Name__COL,c.Value, c.Row)
            if ( c.Value != '' or with_5.Cells(c.Row, M02.SM_ShrtD_COL) != '' or with_5.Cells(c.Row, M02.SM_DetailCOL) != '' )  and  ( with_5.Cells(c.Row, M02.SM_Mode__COL) == '' or Expert_CheckBox ) :
                Found = False
                if Trim(Filter) == '':
                    Found = True
                elif InStr(1, c.Value, Filter) > 0:
                    Found = True
                elif InStr(1, with_5.Cells(c.Row, M02.SM_Group_COL + self.ActLanguage * M02.DeltaCol_Lib_Macro_Lang).Value, Filter) > 0:
                    Found = True
                elif InStr(1, with_5.Cells(c.Row, M02.SM_LName_COL + self.ActLanguage * M02.DeltaCol_Lib_Macro_Lang).Value, Filter) > 0:
                    Found = True
                elif InStr(1, with_5.Cells(c.Row, M02.SM_ShrtD_COL + self.ActLanguage * M02.DeltaCol_Lib_Macro_Lang).Value, Filter) > 0:
                    Found = True
                
                if Found:
                    self.__Add_Node(c)
                    Cnt = Cnt + 1
        if Cnt > 0:
            pass
            #__mcTree.Refresh()
            #if Trim(TextBoxFilter.Text) == '':
            #    __mcTree.ExpandToLevel(0)
            #    __mcTree.RootNodes[1].Expanded = True
            #__mcTree.Refresh()
        #Please_Wait.Visible = False
        #if not Me.Visible:
        #P01.Unload(P01.StatusMsg_UserForm)
        #ShowHourGlassCursor(False)
        return fn_return_value
    
    
    def __InitializeTreeView():
        Debug.Print("__InitializeTreeView")

        #-------------------------------------------------------------------------
        # Procedure : Initialize
        # Company   : JKP Application Development Services (c)
        # Author    : Jan Karel Pieterse (www.jkp-ads.com)
        # Created   : 15-01-2013
        # Purpose   : Initializes the userform,
        #             adds the VBA treeview to the container frame on the userform
        #             and populates the treeview.
        #-------------------------------------------------------------------------
        #__mcTree = clsTreeView()
        # VB2PY (UntranslatedCode) On Error GoTo errH
        #with_6 = __mcTree
        #with_6.TreeControl = Me.frTreeControl
        #with_6.AppName = Me.AppName
        #Add some tree properties:
        #with_6.CheckBoxes = False
        #with_6.RootButton = True
        #with_6.EnableLabelEdit[bAutoSort= False, bMultiLine= False] = False
        #with_6.FullWidth = True
        #with_6.Indentation = 12
        #with_6.NodeHeight = 12
        #with_6.ShowLines = True
        #with_6.ShowExpanders = True
        #with_6.Images = Me.frmImageBox
        self.Display_Navigation_Keys()
        self.__InitializeTreeFrom_Lib_Macros_Sheet() #(TextBoxFilter.Value)
        return
    
        ## VB2PY (CheckDirective) VB directive took path 1 on DebugMode = 1
        Stop()
        # VB2PY (UntranslatedCode) Resume
        #if not __mcTree is None:
        #    MsgBox(Err.Description, VBGetMissingArgument(MsgBox, 1), AppName)
        #    __mcTree.NodesClear()
        #    __mcTree.TerminateTree()
    
    def __GetIcons(self,colImages, ImageNames=[]):
        Debug.Print("__GetIcons")
        fn_return_value = None
        v = Variant()
    
        img = MSForms.Image()
        #-------------------------------------------------------------------------
        # Procedure : GetIcons
        # Company   : -
        # Author    : Peter Thornton
        # Created   : 28-01-2013
        # Purpose   : Creates a collection of StdPicture objects from images in the frame frmImageBox
        #-------------------------------------------------------------------------
        colImages = Collection()
        if IsMissing(ImageNames):
            # get all available images
            for img in Me.frmImageBox.Controls:
                colImages.Add(img.Picture, img.Name)
        else:
            # only get specified images
            for v in ImageNames:
                colImages.Add(Me.frmImageBox.Controls(v).Picture, v)
        fn_return_value = colImages.Count
        return fn_return_value
    
    def __frTreeControl_Enter(self):
        if not __mcTree is None:
            __mcTree.EnterExit(False)
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByVal 
    def __frTreeControl_Exit(Cancel):
        if not __mcTree is None:
            __mcTree.EnterExit(True)
    
    def Set_Description(self,Txt):
        Debug.Print("Set_Description")
        #ActFocus = Variant()
        #-----------------------------------------
        # VB2PY (UntranslatedCode) On Error Resume Next
        #ActFocus = Me.ActiveControl
        # VB2PY (UntranslatedCode) On Error GoTo 0
        self.description.set(Txt)
        #with_7 = Description
        #with_7.setFocus()
        #with_7.SelStart = 0
        #if not ActFocus is None:
        #    ActFocus.setFocus()
    
    def Display_Navigation_Keys(self):
        #------------------------------------
        self.Set_Description(M09.Get_Language_Str('Tasten:' + vbCr + 'Pfeiltasten Auf/Ab, Seite Auf/Ab, Home/Ende zum Navigieren.' + vbCr + 'Pfeiltasten links/rechts zum Ein-/Ausklappen.' + vbCr + 'Zifferntasten 0 bis 9 zum Auf- und Zuklappen auf eine Ebene.' + vbCr + 'Buchstaben zum aktivieren des Filters.'))
    
    def __mcTree_Click(cNode):
        #-----------------------------------------
        #Debug.Print "mcTree_Click " & cNode.Key
        with_8 = cNode
        Sh = PG.ThisWorkbook.Sheets(LIBMACROS_SH)
        __ActKey = with_8.key
        Row = val(Split(with_8.key, ' ')(0))
        Desc = Replace(Sh.Cells(Row, SM_DetailCOL + __ActLanguage * DeltaCol_Lib_Macro_Lang), '|', vbLf)
        if IsNumeric(with_8.key):
            if Desc == '':
                Desc = Replace(Sh.Cells(Row, SM_ShrtD_COL + __ActLanguage * DeltaCol_Lib_Macro_Lang), '|', vbLf)
            __Set_Description(Desc)
            Me.Detail = Replace_Multi_Space(Sh.Cells(Row, SM_Macro_COL))
        else:
            if Desc != '':
                __Set_Description(Desc)
            else:
                __Display_Navigation_Keys()
            Me.Detail = Replace(Sh.Cells(Row, SM_Group_COL).Value, '|', ' > ')
    
    def __mcTree_MouseAction(cNode, Action, Button, Shift, X, Y):
        #------------------------------------------------------------------------------------------------------------------------------
        # Activated by a double click
        # See: NodeEventRouter
        #Debug.Print "mcTree_DblClick:" & cNode.Key & " Action:" & Action
        #If IsNumeric(cNode.key) Then Select_Button_Click
        if IsNumeric(cNode.key) and InStr(cNode.key, ' ') == 0:
            __Select_Button_Click()
            # 15.1.21 Juergen workaround for Excel 2007 isNumericBug
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
    def __Send_Letters_to_TextBoxFilter(KeyCode, Shift):
        fn_return_value = None
        #------------------------------------------------------------------------------------------------------------------
        if (Asc('A') <= KeyCode <= Asc('Z')):
            if Shift < 2:
                TextBoxFilter.setFocus()
                if Shift == 0:
                    KeyCode = KeyCode + 32
                    # Convert to lower case
                TextBoxFilter = TextBoxFilter + Chr(KeyCode)
            elif Shift == 4 and KeyCode == Asc('F'):
                TextBoxFilter.setFocus()
            fn_return_value = True
            #Case Else: Debug.Print "KeyCode: " & KeyCode.Value & " chr: " & Chr(KeyCode.Value) & " Shift:" & Shift
        return fn_return_value
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
    def __mcTree_KeyDown(cNode, KeyCode, Shift):
        bMove = Boolean()
    
        sMsg = String()
    
        cSource = clsNode()
        #-----------------------------------------------------------------------------------------------------------
        #This gets fired when a key is pressed down
        if __Send_Letters_to_TextBoxFilter(KeyCode, Shift):
            return
        if (KeyCode == vbKeyUp) or (KeyCode == vbKeyDown) or (KeyCode == vbKeyLeft) or (KeyCode == vbKeyRight) or (48 <= KeyCode <= 57) or (96 <= KeyCode <= 105) or (KeyCode == vbKeyF2) or (KeyCode == 20) or (KeyCode == 93) or (KeyCode == vbKeyPageUp) or (KeyCode == vbKeyPageDown) or (KeyCode == vbKeyHome) or (KeyCode == vbKeyEnd):
            # these keys are already trapped in clsTreeView for navigation, expand/collapse, edit mode
            ## VB2PY (CheckDirective) VB directive took path 1 on 0
            pass
        elif (Asc('A') <= KeyCode <= Asc('Z')):
            if Shift < 2:
                TextBoxFilter.setFocus()
                if Shift == 0:
                    KeyCode = KeyCode + 32
                    # Convert to lower case
                TextBoxFilter = TextBoxFilter + Chr(KeyCode)
            elif Shift == 4 and KeyCode == Asc('F'):
                TextBoxFilter.setFocus()
        elif (KeyCode == vbKeyReturn):
            __Select_Button_Click()
            #Case Else: Debug.Print "KeyCode: " & KeyCode.Value & " chr: " & Chr(KeyCode.Value) & " Shift:" & Shift
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyAscii - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
    def __Expert_CheckBox_KeyUp(KeyAscii, Shift):
        __Send_Letters_to_TextBoxFilter(KeyAscii, Shift)
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyAscii - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
    def __Abort_Button_KeyUp(KeyAscii, Shift):
        __Send_Letters_to_TextBoxFilter(KeyAscii, Shift)
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyAscii - ByVal 
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
    def __Select_Button_KeyUp(KeyAscii, Shift):
        __Send_Letters_to_TextBoxFilter(KeyAscii, Shift)
    
    def Calc_SelectMacro_Res(self):
        Res = String()
    
        Row = int()
        #---------------------------------
        # Return the name and the row number in the ListDataSheet
        if self.ActKey != '' and IsNumeric(self.ActKey):
            Row = P01.val(self.ActKey)
            with_9 = PG.ThisWorkbook.Sheets(M02.LIBMACROS_SH)
            Res = with_9.Cells(Row, M02.SM_Name__COL) + ',' + str(Row)
            self.Last_SelectedNr_Valid = True
            self.Last_SelectedNr = Row
            self.SelectMacro_Res = Res
        else:
            self.SelectMacro_Res = ''
    
    def __Abort_Button_Click():
        Debug.Print("__Abort_Button_Click")
        #-------------------------------
        UnhookFormScroll()
        Me.Hide()
        SelectMacro_Res = ''
        #Enable_Listbox_Changed = False
    
    def Select_Button_Click(self):
        Debug.Print("Select_Button_Click")
        #--------------------------------
        #UnhookFormScroll()
        self.Calc_SelectMacro_Res()
        if self.SelectMacro_Res == '':
            #Show_Status_for_a_while Get_Language_Str "Please selec
            M31.BeepThis2('Windows Balloon.wav')
        else:
            #Me.Hide()
            #Debug.Print('Result: ' + SelectMacro_Res)
            pass
    
    def __Expert_CheckBox_Click():
        #----------------------------------
        if not __InitializeTreeFrom_Activ:
            __InitializeTreeFrom_Lib_Macros_Sheet(TextBoxFilter.Value)
            M28.Set_String_Config_Var('Expert_Mode_aktivate', IIf(Expert_CheckBox, '1', '0'))
    
    def Update_TextBoxFilter():
        #---------------------------------
        if not __InitializeTreeFrom_Activ:
            __InitializeTreeFrom_Lib_Macros_Sheet(TextBoxFilter.Value)
    
    def __TextBoxFilter_Change():
        #---------------------------------
        if not __InitializeTreeFrom_Activ:
            ## VB2PY (CheckDirective) VB directive took path 1 on DELAYED_FILTER_FUNCTION
            if __StartTime_Update_TextBox != 0:
                # VB2PY (UntranslatedCode) On Error Resume Next
                Application.OnTime(__StartTime_Update_TextBox, 'Update_TextBoxFilter_onTime', Schedule=False)
            __StartTime_Update_TextBox = 1000 #Now + TimeValue('00:00:01')
            Application.OnTime(__StartTime_Update_TextBox, 'Update_TextBoxFilter_onTime')
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lngRotation - ByVal 
    def MouseWheel(lngRotation):
        #-----------------------------------------------
        # Process the mouse wheel changes
        #Debug.Print "MouseWheel " & lngRotation & " " & Me.frTreeControl.ScrollTop
        if Description is Me.ActiveControl:
            ActiveNode = __mcTree.ActiveNode
            with_10 = Description
            with_10.setFocus()
            if lngRotation < 0:
                Application.SendKeys('{HOME}{DOWN}{DOWN}{DOWN}')
            else:
                if with_10.SelStart > 0:
                    Application.SendKeys('{HOME}{UP}{UP}{UP}')
            # Problem beim Scrollen in der Description box:
            # Wenn der Cursor ganz oben ist, dann verliert die Box den Focus und die Simulierten Tasten werden von dem TreeView
            # verarbeitet. Das führt dazu, dass ein anderer Eintrag ausgewählt wird.
            # Das wird mit dem folgenden Block abgefangen
            for i in vbForRange(1, 7):
                DoEvents()
                Sleep(10)
            if not Description is Me.ActiveControl:
                #mcTree.ScrollToView ActiveNode, 0
                __mcTree.NodeEventRouter(ActiveNode, 'Caption', 1)
                with_10.setFocus()
        else:
            with_11 = Me.frTreeControl
            if lngRotation > 0:
                if with_11.ScrollTop > 0:
                    if with_11.ScrollTop > Step:
                        with_11.ScrollTop = with_11.ScrollTop - Step
                    else:
                        with_11.ScrollTop = 0
            else:
                with_11.ScrollTop = with_11.ScrollTop + Step
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: key - ByVal 
    def __Find_Node(self,key):
        Debug.Print("__Find_Node")
        
        fn_return_value = None
        #---------------------------------------------------------
        # VB2PY (UntranslatedCode) On Error GoTo ErrProc
        
        fn_return_value = self.searchTree(key)
        #fn_return_value = __mcTree.Nodes(key)
        return fn_return_value
        #Debug.Print('Not Found ' + key + ' ;-(')
        #return fn_return_value
    
    def searchTree(self,searchvalue):
        Debug.Print("searchTree")

        selections = self.tree.tag_has(str(searchvalue))
        print(searchvalue, selections)
        
        #for child in self.tree.get_children():
            #print(self.tree.item(child)['values'])
        #    if searchvalue in self.tree.item(child)['values']:
                #print(self.tree.item(child)['values'])
        #        selections.append(child)
        #print('search completed')
        self.tree.selection_set(selections)
        return selections
    
    def open_child(self,child):
        Debug.Print("Open_child")
        self.tree.item(child, open=True)  # open
        parent = self.tree.parent(child)
        if parent !="":
            self.tree.item(parent, open=True) 
            self.open_child(parent)
    
    # VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: SelectName - ByVal 
    def Show_SelectMacros_TreeView(self,SelectName):
        Debug.Print("Show_SelectMocros_TreeView")

        #Row = int()
        #----------------------------------------------------------------
        # Use this function to show the dialog.
        # Selct the node by Selectname
        if SelectName != '':
            Row = M09SM.Find_Macro_in_Lib_Macros_Sheet(SelectName)
            if Row > 0:
                self.ActiveNode = self.__Find_Node(Row)
                if self.ActiveNode is None and TextBoxFilter != '':
                    TextBoxFilter = ''
                    self.ActiveNode = self.__Find_Node(Row)
                if self.ActiveNode is None and Expert_CheckBox == False:
                    self.__InitializeTreeFrom_Activ = True
                    TextBoxFilter = ''
                    self.__InitializeTreeFrom_Activ = False
                    Expert_CheckBox = True
                    self.ActiveNode = self.__Find_Node(Row)
        # Selct the node Last_SelectedNr
        if self.ActiveNode is None and self.Last_SelectedNr_Valid and self.Last_SelectedNr > 0:
            Row = self.Last_SelectedNr
            self.ActiveNode = self.__Find_Node(Row)
        if not self.ActiveNode is None:
            #self.tree.selection_set(self.ActiveNode)
            self.open_child(self.ActiveNode)
            self.tree.selection_set(self.ActiveNode)
            pass
            #__mcTree.NodeEventRouter(ActiveNode, 'Caption', 1)
            #__mcTree.ScrollToView(ActiveNode, 0)
        #HookFormScroll(Me, 'frTreeControl')
        #frTreeControl.setFocus()
        self.controller.wait_window(self.top) # Me.Show()
        P01.ActiveSheet.Redraw_table()
        return self.SelectMacro_Res
        
    
    def Get_Icon(vKey, Pic):
        fn_return_value = None
        bFullWidth = Boolean()
        #-----------------------------------------------------------
        fn_return_value = __mcTree.GetNodeIcon(vKey, Pic, bFullWidth)
        return fn_return_value
    
    # VB2PY (UntranslatedCode) Option Explicit
    

        
# subclass treeview for the convenience of overriding the column method
class ScrollableTV(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.columns=[]
    # column now records the name and details of each column in the TV just before they're added
    def column(self, column, **kw):
        if column not in [column[0] for column in self.columns]:
            self.columns.append((column, kw))
        super().column(column, **kw)
