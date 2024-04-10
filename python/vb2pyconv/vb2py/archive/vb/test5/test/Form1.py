# Created by Leo from: C:\Development\Python23\Lib\site-packages\vb2py\vb2py.leo

"""The main form for the application"""

from vb2py.PythonCardPrototype import model

# Allow importing of our custom controls
import vb2py.PythonCardPrototype.res
vb2py.PythonCardPrototype.res.APP_COMPONENTS_PACKAGE = "vb2py.targets.vb2py.PythonCard.vbcontrols"

class Background(model.Background):

    def __getattr__(self, name):
        """If a name was not found then look for it in components"""
        return getattr(self.components, name)


    def __init__(self, *args, **kw):
        """Initialize the form"""
        model.Background.__init__(self, *args, **kw)
        # Call the VB Form_Load
        # TODO: This is brittle - depends on how the private indicator is set
        if hasattr(self, "_MAINFORM__Form_Load"):
            self._MAINFORM__Form_Load()
        elif hasattr(self, "Form_Load"):
            self.Form_Load()


from vb2py.vbfunctions import *
from vb2py.vbdebug import *

class MAINFORM(Background):


    def on_Command1_mouseClick(self, *args):
        #
        self.Timer1.Interval = 500
        print self.Timer1.Enabled
        self.Timer1.Enabled = True
        #

    def on_Command2_mouseClick(self, *args):
        Form2.Show()

    def Timer1_Timer(self):
        #
        if Screen.ActiveControl is Nothing:
            Debug.Print('No active control')
        else:
            Debug.Print('Active control:', Screen.ActiveControl.Name)
        Debug.Print('Active form:', Screen.ActiveForm.Name)
        Debug.Print('Font count', Screen.FontCount)
        Debug.Print('Font 5:', Screen.Fonts(5))
        Debug.Print('Height:', Screen.Height)
        Debug.Print('Mouse icon Height:', Screen.MouseIcon.Height)
        Debug.Print('Mouse pointer:', Screen.MousePointer)
        Debug.Print('Twips per pixel x and y:', Screen.TwipsPerPixelX, Screen.TwipsPerPixelY)
        Debug.Print('Width:', Screen.Width)
        #

    # VB2PY (UntranslatedCode) Attribute VB_Name = "Form1"
    # VB2PY (UntranslatedCode) Attribute VB_GlobalNameSpace = False
    # VB2PY (UntranslatedCode) Attribute VB_Creatable = False
    # VB2PY (UntranslatedCode) Attribute VB_PredeclaredId = True
    # VB2PY (UntranslatedCode) Attribute VB_Exposed = False



if __name__ == '__main__':
    app = model.vb2py.PythonCardApp(MAINFORM)
    app.MainLoop()
