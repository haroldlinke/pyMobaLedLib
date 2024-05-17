from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import proggen.M20_PageEvents_a_Functions as M20

"""-------------------------------
-------------------------------
"""


def Start_Button_Click():
    #-------------------------------
    M20.Arduino_Button_StartPage()

def Worksheet_Activate():
    #-------------------------------
    M20.Global_Worksheet_Activate()

# VB2PY (UntranslatedCode) Option Explicit
