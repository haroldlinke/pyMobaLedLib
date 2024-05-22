import tkinter as tk
from tkinter import ttk


class CanvasFrame(tk.Frame):
    def __init__(self, parent, canvas_height, canvas_width):
        global total_scalefactor
        self.tabClassName = "CanvasFrame"
        self.parent = parent
        self.canvas=None
        tk.Frame.__init__(self,parent)
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.frame=ttk.Frame(self,relief="ridge", borderwidth=1)
        self.frame.grid_columnconfigure(0,weight=1)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid(row=0,column=0,sticky="nesw")
        self.cv_frame=None
        self.define_key_bindings()
        self.canvas = self.create_canvas()
        self.scalefactorunit = 0.95
        self.total_scalefactor = 1
        self.old_scalefactor = 1
        self.firstcall = True
        self.block_Canvas_movement_flag = False
        self.canvas_init = True
 
    def create_canvas(self):
        if self.cv_frame:
            #self.cv_frame.destroy()
            pass
        else:
            self.cv_frame = ttk.Frame(self.frame)
        self.cv_frame.grid(row=0,column=0,sticky="nesw")
        self.cv_frame.grid_columnconfigure(0,weight=1)
        self.cv_frame.grid_rowconfigure(0,weight=1)
        if self.canvas and self.canvas != None:
            canvas = self.canvas
        else:
            canvas=tk.Canvas(self.cv_frame,width=self.canvas_width,height=self.canvas_height,scrollregion=(0,0,self.canvas_width,self.canvas_height),bg="white")
            hbar=tk.Scrollbar(self.cv_frame,orient=tk.HORIZONTAL)
            hbar.pack(side=tk.BOTTOM,fill=tk.X)
            hbar.config(command=canvas.xview)
            vbar=tk.Scrollbar(self.cv_frame,orient=tk.VERTICAL)
            vbar.pack(side=tk.RIGHT,fill=tk.Y)
            vbar.config(command=canvas.yview)
            canvas.config(width=self.canvas_width,height=self.canvas_height)
            canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
            canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        self.canvas = canvas
        self.canvas_bindings()
        return canvas
        
    def define_key_bindings(self):
        
        self.key_to_method_dict = { "<Home>"     : self.onRestoreZoom,
                                    "<Shift-Up>"    : self.onMoveCanvasUp,
                                    "<Shift-Down>"  : self.onMoveCanvasDown,
                                    "<Shift-Left>"  : self.onMoveCanvasLeft, 
                                    "<Shift-Right>" : self.onMoveCanvasRight,
                                    "<Control-Down>" : self.onZoomIn,
                                    "<Control-Up>" : self.onZoomOut,
                                    "<F5>"   : self.onRefreshCanvas
                                   }
 
        
    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        if self.block_Canvas_movement_flag:
            return
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        if self.block_Canvas_movement_flag:
            return        
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def onCtrlMouseWheel(self, event):
        scale = 1.0
        if event.delta == -120:
            scale *= self.scalefactorunit
        if event.delta == 120:
            scale /= self.scalefactorunit
        self.resize(scale, event.x, event.y)
    
    def onAltMouseWheel(self, event):
        pass
    
    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def onMoveCanvasUp(self, event):
        if event.keysym == "Up":
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(-1, "pages")
    
    def onMoveCanvasDown(self, event):
        if event.keysym == "Down":
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(1, "pages")
    
    def onZoomIn(self, event):
        scale = self.scalefactorunit
        self.resize(scale)
    
    def onZoomOut(self, event):
        scale = 1.0/self.scalefactorunit
        self.resize(scale)
    
    def onMoveCanvasLeft(self, event):
        self.canvas.xview_scroll(-1, "units")
    
    def onMoveCanvasRight(self, event):
        self.canvas.xview_scroll(1, "units")
    
    #def onPrior(self, event):
    #    self.canvas.xview_scroll(1, "pages")
    
    #def onNext(self, event):
    #    self.canvas.xview_scroll(-1, "pages")
    
    def onShiftMouseWheel(self, event):
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
    def onRefreshCanvas(self, event):
        pass
        # self.timetable_main.regenerate_canvas()
    
    def onRestoreZoom(self, event=None):
        if round(self.total_scalefactor,4)!=1:
            self.old_scalefactor = self.total_scalefactor
            #self.canvas_old_x, self.canavs_old_y = self.canvas.coords("all")
            #print(self.canvas_old_x, self.canavs_old_y)
            #self.canvas_old_x, self.canavs_old_y, x2, y2 = self.canvas.bbox("all")
            #print(self.canvas_old_x, self.canavs_old_y)
            self.resize(1/self.total_scalefactor)
            self.total_scalefactor = 1
        else:
            self.resize(self.old_scalefactor)
            self.old_scalefactor = 1
            #self.canvas.move("all",self.canvas_old_x, self.canavs_old_y)
            #self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        #self.resize(event, 1/self.total_scalefactor)
        #self.total_scalefactor = 1
   
    def scale_objects(self, scale):
        self.canvas.scale('all', 0, 0, scale, scale)
        
    def scale_canvas_arround_object(self, scale, objectid):
        if False: #objectid != -1:
            object_coords = self.canvas.coords(objectid)
            self.scaleshift_x0 = object_coords[0]
            self.scaleshift_y0 = object_coords[1]
        else:
            self.scaleshift_x0 = 0
            self.scaleshift_y0 = 0
        self.canvas.scale('all', self.scaleshift_x0, self.scaleshift_y0, scale, scale)        
        
    def resize(self, scale, x=0, y=0):
        self.total_scalefactor *= scale
        #print("Resize: Scale %s - total scalefactor %s", scale,self.total_scalefactor)
        if self.total_scalefactor > 1:
            self.canvas.itemconfigure("Background",fill="")#,outline="")
        else:
            self.canvas.itemconfigure("Background",fill="white")#,outline="")
        """
        if event == None:
            x=0
            y=0
        else:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
        """
        x1 = x #self.canvas.canvasx(x)
        y1 = y #self.canvas.canvasy(y)
        #self.scale_canvas_arround_object(scale, objectid)
        self.canvas.scale('all', 0, 0, scale, scale)
        #print("Canvas.bbox:", self.canvas.bbox('all'))
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
                
    def block_Canvas_movement(self,flag):
        self.block_Canvas_movement_flag = flag
        
    def canvas_bindings(self):
        self.canvas.bind('<Shift-ButtonPress-1>', self.move_from)
        self.canvas.bind('<Shift-B1-Motion>', self.move_to)
        self.canvas.bind("<Control-MouseWheel>", self.onCtrlMouseWheel, add="+")
        self.canvas.bind("<Alt-MouseWheel>", self.onAltMouseWheel, add="+")
        self.canvas.bind("<MouseWheel>", self.onMouseWheel, add="+")
        self.canvas.bind("<Shift-MouseWheel>", self.onShiftMouseWheel, add="+")
        self.canvas.bind("<Shift-MouseWheel>", self.onShiftMouseWheel, add="+")
        for key_str, action in self.key_to_method_dict.items():
            self.canvas.bind(key_str,action)
        return
    
    def canvas_unbind(self):
        self.canvas.unbind('<Shift-ButtonPress-1>')
        self.canvas.unbind('<Shift-B1-Motion>')
        self.canvas.unbind("<Control-MouseWheel>")
        self.canvas.unbind("<Alt-MouseWheel>")
        self.canvas.unbind("<MouseWheel>")
        self.canvas.unbind("<Shift-MouseWheel>")
        for key_str, action in self.key_to_method_dict.items():
            self.frame.unbind(key_str)
        return
    
    def get_key_for_action(self,action):
        return shortCutDict["Key"].get(action,None)
    
shortCutDict =  { "MouseButton":
                     {"move_from"        : '<Shift-ButtonPress-1>',
                      "move_to"          : '<Shift-B1-Motion>',
                      "Activate_Min"     : "<Button-1>",
                      "Activate_Sec"     : "<Alt-1>",
                      "Motion_Min"       : "<B1-Motion>",
                      "Motion_Sec"       : "<Alt-B1-Motion>"                      
                      },
                  "MouseWheel" :
                     {"Zoom" : "<Control-MouseWheel>",
                      "onAltMouseWheel"  : "<Alt-MouseWheel>",
                      "onMouseWheel"     : "<MouseWheel>",
                      "onShiftMouseWheel":"<Shift-MouseWheel>"                      
                      },
                 "Key":
                     {"onRestoreZoom"         : "<Home>", 
                      "onMoveCanvasUp"        : "<Up>",
                      "onMoveCanvasDown"      : "<Down>",
                      "onMoveCanvasLeft"      : "<Left>", 
                      "onMoveCanvasRight"     : "<Right>",
                      "onZoomIn"              : "<Control-Down>",
                      "onZoomOut"             : "<Control-Up>",
                      "onRefreshCanvas"       : "<F5>",
                      "onTimeDecMinute"       : "-",
                      "onTimeIncMinute"       : "+",
                      "onNextStationTime"     : "8",
                      "onPreviousStationTime" : "2",                     
                      "onPreviousTrainTime"   : "4",
                      "onNextTrainTime"       : "6",                      
                     }
                   }    
