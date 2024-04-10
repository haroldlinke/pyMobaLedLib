"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2005/10/12 22:27:39 $"
"""

"""
Simple sizer for PythonCard

Uses a simple method for sizing:
    - each component type is defined to be fixed or stretchable 
    - uses GetBestSize() to get a min size for each component 
    - each component is placed by its centre point as laid out
    - centre locations are scaled by "current window size / min size"
    
This will adjust component sizes for differences between OS's, but will
not move components to make space.
"""

import wx

DEBUG = False
DEBUG1 = False

#----------------------------------------------------------------------

class simpleSizer(wx.PySizer):
    def __init__(self, minsize, border=0):
        wx.PySizer.__init__(self)
        self.minsize = minsize
        self.border = border
        
    #--------------------------------------------------
    def Add(self, item, option=0, flag=0, border=0,
            pos=None, size=None,  
            growX = False, growY = False
            ):

        if DEBUG: print("adding", item.name, pos, size, growX, growY)

        wx.PySizer.Add(self, item, option, flag, border,
                       userData=(pos, size, growX, growY))

    #--------------------------------------------------
    def CalcMin( self ):
        x,y = self.minsize
        return wx.Size(x, y)
        
    #--------------------------------------------------
    def RecalcSizes( self ):
        # save current dimensions, etc.
        curWidth, curHeight  = self.GetSize()
        px, py = self.GetPosition()
        minWidth, minHeight  = self.CalcMin()
        if DEBUG: print(minWidth, minHeight,  curWidth, curHeight)

        if minWidth == 0 or minHeight == 0: return
        
        scaleX = 100 * curWidth / minWidth
        scaleY = 100 * curHeight / minHeight
            
        # iterate children and set dimensions...
        for item in self.GetChildren():
            pos, size, growX, growY = item.GetUserData()
            if DEBUG: print("in recalc", pos, size, growX, growY)
            cx,cy = pos
            sx,sy = size
            cx = (cx * scaleX + sx*scaleX/2) / 100
            cy = (cy * scaleY + sy*scaleY/2) / 100
            
            if growX: 
                sx = sx * scaleX / 100
            if growY: 
                sy = sy * scaleY / 100
                
            self.SetItemBounds( item, cx-sx/2, cy-sy/2, sx, sy )

    #--------------------------------------------------
    def SetItemBounds(self, item, x, y, w, h):
        # calculate the item's actual size and position within
        # its grid cell
        ipt = wx.Point(x, y)
        isz = wx.Size(w,h)
        if DEBUG: print("in itembounds", x,y,w,h)
            
        item.SetDimension(ipt, isz)
#--------------------------------------------------



# AGT fill this list
heightGrowableTypes = ["BitmapCanvas", "CodeEditor", "HtmlWindow", \
                       "Image", "List", "MultiColumnList", 
                       "Notebook", \
                       "RadioGroup", "StaticBox", "TextArea", \
                       "Tree"]
widthGrowableTypes = ["BitmapCanvas", "CheckBox", "Choice", \
                      "CodeEditor", "ComboBox", "HtmlWindow", \
                      "Image", "List", "MultiColumnList", \
                      "Notebook", \
                      "PasswordField", "RadioGroup", "Spinner", \
                      "StaticBox", "StaticText", "TextArea", \
                      "TextField", "Tree"]
growableTypes = ["Gauge", "Slider", "StaticLine"]  

def autoSizer(aBg):
    winX, winY = aBg.size
    # make list of all components, make a simpleSizer to hold them
    complist = []
    for compName in aBg.components.keys():
        comp = aBg.components[compName]
        complist.append( comp )

    sizer = simpleSizer(aBg.panel.size)
    
    # add the components to the grid
    for comp in complist:
        tx, ty = comp.position
        dx, dy = comp.size
        
        # AGT Must be an easier way to get a component's type ??
        compType = comp._resource.__dict__['type']

        dx1, dy1 = comp.GetBestSize()
        if dx1 > dx: dx = dx1
        if dy1 > dy: 
            # hack to deal with the fact that GetBestSize() comes up with too 
            #  large heights for textareas.
            if compType != "TextArea": dy = dy1

        # AGT FUTURE this checks contents of the component's userdata
        #     extend resourceEditor to allow a way to set this
        if "HEIGHT_GROWABLE" in comp.userdata or \
            compType in heightGrowableTypes or \
            (compType in growableTypes and comp.layout == "vertical"):
                compGrowableY = True
        else: compGrowableY = False
        if "WIDTH_GROWABLE" in comp.userdata or \
            compType in widthGrowableTypes or \
            (compType in growableTypes and comp.layout == "horizontal"):
                compGrowableX = True
        else: compGrowableX = False

        sizer.Add(comp, pos=(tx,ty), size=(dx,dy), growX = compGrowableX, growY = compGrowableY )
        if DEBUG1: print("adding ", comp.name, (tx, ty), (dx, dy), compGrowableX, compGrowableY)
            
    sizer.SetSizeHints(aBg)
    aBg.panel.SetSizer(sizer)
    aBg.panel.SetAutoLayout(1)
    aBg.panel.Layout()
#--------------------------------------------------
