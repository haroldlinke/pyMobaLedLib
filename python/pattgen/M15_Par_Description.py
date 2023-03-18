from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M30_Tools as M30
import ExcelAPI.XLC_Excel_Consts as X01
import pattgen.M09_Language
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01

"""------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
UT----------------------------
"""

ParName_COL = 1
Par_Cnt_COL = 2
ParType_COL = 3
Par_Min_COL = 4
Par_Max_COL = 5
Par_Def_COL = 6
ParInTx_COL = 7
ParHint_COL = 8
FirstDatRow = 2

def Get_ParDesc_Row(Sh, Name):
    _fn_return_value = None
    r = X02.Range()

    f = Variant()
    #------------------------------------------------------------------------
    _with48 = Sh
    r = _with48.Range(_with48.Cells(1, ParName_COL), _with48.Cells(M30.LastUsedRowIn(Sh), ParName_COL))
    f = r.Find(What= Name, After= r.Cells(FirstDatRow, 1), LookIn= X01.xlFormulas, LookAt= X01.xlWhole, SearchOrder= X01.xlByRows, SearchDirection= X01.xlNext, MatchCase= True, SearchFormat= False)
    if f is None:
        X02.MsgBox(pattgen.M09_Language.Get_Language_Str('Fehler: Der Parameter Name \'') + Name + pattgen.M09_Language.Get_Language_Str('\' wurde nicht im Sheet \'') + Sh.Name + pattgen.M09_Language.Get_Language_Str('\' gefunden!'), vbCritical, pattgen.M09_Language.Get_Language_Str('Internal Error'))
        M30.EndProg()
    else:
        _fn_return_value = f.Row
    return _fn_return_value

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ParName - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Typ - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Min - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Max - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Def - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: InpTxt - ByRef 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Hint - ByRef 
def Get_Par_Data(ParName, Typ, Min, Max, Def, InpTxt, Hint):
    Row = Long()

    Sh = X02.Worksheet()
    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Sh = X02.Sheets(M01.PAR_DESCRIPTION_SH)
    Row = Get_ParDesc_Row(Sh, ParName)
    _with49 = Sh
    Typ = _with49.Cells(Row, ParType_COL)
    Min = _with49.Cells(Row, Par_Min_COL)
    Max = _with49.Cells(Row, Par_Max_COL)
    Def = _with49.Cells(Row, Par_Def_COL)
    InpTxt = _with49.Cells(Row, ParInTx_COL)
    if InpTxt == '':
        InpTxt = ParName
    Hint = _with49.Cells(Row, ParHint_COL)
    # Inserting a LF seames to be not possible ;-(   Test with: Replace(.Cells(Row, ParHint_COL), "|", vbCrLf)

def Test_Get_Par_Data():
    Typ = String()

    Min = String()

    Max = String()

    Def = String()

    InpTxt = String()

    Hint = String()
    #UT----------------------------
    Get_Par_Data('Duration', Typ, Min, Max, Def, InpTxt, Hint)
    Debug.Print('Typ:' + Typ, 'Min:' + Min + ' Max:' + Max + ' Def:' + Def + vbCr + 'InpTxt:' + InpTxt + vbCr + 'Hint:' + Hint)

# VB2PY (UntranslatedCode) Option Explicit
