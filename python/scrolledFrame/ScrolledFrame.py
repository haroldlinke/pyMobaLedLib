from tkinter import *   # from x import * is bad practice
from tkinter import ttk
import logging

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=True)
        self.canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)
        self.focused = False

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)
        
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        
        #def _on_mousewheel(event):
        #    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        #self.interior.bind_all("<MouseWheel>", _on_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())
    

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            #logging.debug("Configure_Canvas: set canvas width= %s",self.canvas.winfo_width())  
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

        def _on_leave(event):
            self.focused = False
        self.interior.bind('<Leave>', _on_leave)
        def _on_enter(event): 
            self.focused = True
        self.interior.bind("<Enter>", _on_enter)
        def _on_mousewheel(event):
            if(self.focused):
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.interior.bind_all("<MouseWheel>", _on_mousewheel)

    def move_canvas(self,value):
        self.canvas.yview_moveto(value)    




class HorizontalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=True)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        xscrollcommand=hscrollbar.set)
        self.canvas.pack(side=TOP, fill=BOTH, expand=TRUE)
        hscrollbar.config(command=self.canvas.xview)
        self.focused = False

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)
        
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        
        #def _on_mousewheel(event):
        #    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        #self.interior.bind_all("<MouseWheel>", _on_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        #logging.debug("Configure_interior: %s",size)
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canvas.config(height=self.interior.winfo_reqheight())
            #logging.debug("Configure_Interior: set canvas width= %s",self.interior.winfo_reqwidth())
    

    def _configure_canvas(self, event):
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        #logging.debug("Configure_Canvas: %s",size)           
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, height=self.canvas.winfo_height())

        def _on_leave(event):
            self.focused = False
        self.interior.bind('<Leave>', _on_leave)
        def _on_enter(event): 
            self.focused = True
        self.interior.bind("<Enter>", _on_enter)

    def move_canvas(self,value):
        self.canvas.xview_moveto(value)    




class ScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        #vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        vscrollbar.grid(row=0,column=1,sticky="ns")
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        #hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)        
        hscrollbar.grid(row=1,column=0,sticky="ew")        
        self.canvas = Canvas(self, bd=0, highlightthickness=0,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set )
        #self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        #self.canvas.pack(side=TOP,fill=BOTH, expand=TRUE)
        self.canvas.grid(row=0,column=0,sticky="nesw")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)
        self.focused = False

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior,anchor=NW)
        
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        
        self.interior.bind('<Leave>', self._on_leave)
        self.interior.bind("<Enter>", self._on_enter)
        
        #def _on_mousewheel(event):
        #    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        #self.interior.bind_all("<MouseWheel>", _on_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
    def _configure_interior(self,event):
        # update the scrollbars to match the size of the inner frame
        
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        #logging.debug("Configure_interior: %s",size)
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            #logging.debug("Configure_Interior: set canvas width= %s",self.interior.winfo_reqwidth())
            self.canvas.config(width=self.interior.winfo_reqwidth())
        
        if self.interior.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas's width to fit the inner frame
            #logging.debug("Configure_Interior: set canvas height= %s",self.interior.winfo_reqheight())
            self.canvas.config(height=self.interior.winfo_reqheight())
        pass
    

    def _configure_canvas(self,event):
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        #logging.debug("Configure_Canvas: %s",size)            
        if self.interior.winfo_reqwidth() < self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            #logging.debug("Configure_Canvas: set canvas width= %s",self.canvas.winfo_width())      
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())
        
        if self.interior.winfo_reqheight() < self.canvas.winfo_height():
            #logging.debug("Configure_Canvas: set canvas height= %s",self.canvas.winfo_height())      
            # update the inner frame's height to fill the canvas
            self.canvas.itemconfigure(self.interior_id, height=self.canvas.winfo_height())
        pass
    

    def _on_leave(self,event):
        self.focused = False
    
    def _on_enter(self,event): 
        self.focused = True
    

if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)


            self.frame = ScrolledFrame(root)
            self.frame.grid(row=0,column=0)
            self.frame.grid_columnconfigure(0,weight=1)
            self.frame.grid_rowconfigure(0,weight=1)
            self.grid_columnconfigure(0,weight=1)
            self.grid_rowconfigure(0,weight=1)            
            
            self.label = Label(text="Shrink the window to activate the scrollbar.")
            self.label.grid(row=1,column=0)
            buttons = []
            for i in range(100):
                buttons.append(Button(self.frame.interior, text="Button                                                                                   " + str(i)))
                buttons[-1].pack()
                
    format = "%(asctime)s: %(message)s"

    logging.basicConfig(format=format, level=logging.DEBUG,datefmt="%H:%M:%S")

    app = SampleApp()
    app.mainloop()