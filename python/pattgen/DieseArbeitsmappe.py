from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M02_Main as M02a
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01
import pattgen.Pattern_Generator as PG

""" The constant "USE_SHAPE_MOVE_EVENT" has to be enabled in "Extras/Eigenschaften" in the VBA Editor
# VB2PY (CheckDirective) VB directive took path 2 on USE_SHAPE_MOVE_EVENT
--------------------------
--------------------------------------------------------------------------------------------------------------
# VB2PY (CheckDirective) VB directive took path 2 on USE_SHAPE_MOVE_EVENT
 USE_SHAPE_MOVE_EVENT
 06.07.20:
--------------------------------------------------
"""


def Workbook_Open():
    #--------------------------
    # For some reasons this macro is not allways called ;-(
    # Therefor we use the old Auto_Open() in addition which is located in "M02_Main"
    Debug.Print('Starting Workbook_Open() in \'DieseArbeitsmappe\'')
    M02a.Init()

def Enable_Events_again():
    X02.Application.EnableEvents = True

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Sh - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Target - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByRef 
def Workbook_SheetBeforeDoubleClick(Sh, Target, Cancel):
    #--------------------------------------------------------------------------------------------------------------
    if M01.DEBUG_CHANGEEVENT:
        Debug.Print('DieserArbeitsmappe: Workbook_SheetBeforeDoubleClick:' + Target.Row + ' Cancel=' + Cancel)
    M02a.Proc_DoubleCkick(Sh, Target, Cancel)
    #Cancel = True

def Workbook_BeforeClose(Cancel):
    # 27.10.20:
    #--------------------------------------------------
    X02.Application.OnKey('{Return}', '')
    Debug.Print(PG.ThisWorkbook.Name + ' Workbook_BeforeClose() called and \'Return\'-key event removed')

# VB2PY (UntranslatedCode) Option Explicit
