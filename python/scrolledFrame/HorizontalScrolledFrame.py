from tkinter import *   # from x import * is bad practice
from tkinter import ttk

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

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
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canvas.config(height=self.interior.winfo_reqheight())
    

    def _configure_canvas(self, event):
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
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=TRUE)        
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set )
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        self.focused = False

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
        #def _on_mousewheel(event):
        #    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        #self.interior.bind_all("<MouseWheel>", _on_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            #if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
            #    canvas.config(width=interior.winfo_reqwidth())
            #if interior.winfo_reqheight() != canvas.winfo_height():
                # update the canvas's width to fit the inner frame
            #    canvas.config(height=interior.winfo_reqheight())
            pass
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            #if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
            #    canvas.itemconfigure(interior_id, width=canvas.winfo_width())
            #if interior.winfo_reqheight() != canvas.winfo_height():
                # update the inner frame's height to fill the canvas
            #    canvas.itemconfigure(interior_id, height=canvas.winfo_height())
            pass
        canvas.bind('<Configure>', _configure_canvas)

        def _on_leave(event):
            self.focused = False
        interior.bind('<Leave>', _on_leave)
        def _on_enter(event): 
            self.focused = True
        interior.bind("<Enter>", _on_enter)


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)


            self.frame = ScrolledFrame(root)
            self.frame.pack()
            self.label = Label(text="Shrink the window to activate the scrollbar.")
            self.label.pack()
            buttons = []
            for i in range(100):
                buttons.append(Button(self.frame.interior, text="Button                                                                                   " + str(i)))
                buttons[-1].pack()

    app = SampleApp()
    app.mainloop()