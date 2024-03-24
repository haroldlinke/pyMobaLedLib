from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M06_Goto_Graph
import pattgen.M30_Tools as M30
import ExcelAPI.XLW_Workbook as X02
import pattgen.M01_Public_Constants_a_Var as M01

""" Different arangements:

   |     |  |         |   |  |  |     |    |  |    |
   |\____/  |         |   |  |  |     |    |  |    |
   \________/         \___\__/__/     \____/  \____/

----------------------------------------------------------------------------
UT-------------------------
"""

class GotoListEntry_t:
    def __init__(self):
        self.Start = Long()
        self.Ende = Long()
        self.Min = Long()
        self.Max = Long()
        self.Dist = Long()
        self.Inside_Cnt = Long()
        self.OutsideCnt = Long()


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: GotoArrowTab - ByVal 
def Calc_Height_GotoArrow(GotoArrowTab):
    _fn_return_value = None
    StrEnt = Variant()

    GotoList = vbObjectInitialize(objtype=GotoListEntry_t)

    StrArray = vbObjectInitialize(objtype=String)

    Nr = Long()

    a = Long()

    t = Long()

    Res = String()
    #----------------------------------------------------------------------------
    # Fill the array
    StrArray = Split(GotoArrowTab, ' ')
    GotoList = vbObjectInitialize((UBound(StrArray),), Variant)
    for StrEnt in StrArray:
        Cols = Split(StrEnt, ',')
        GotoList[Nr].Start = Val(Cols(0))
        GotoList[Nr].Ende = Val(Cols(1))
        if GotoList(Nr).Start < GotoList(Nr).Ende:
            GotoList[Nr].Min = GotoList(Nr).Start
            GotoList[Nr].Max = GotoList(Nr).Ende
        else:
            GotoList[Nr].Min = GotoList(Nr).Ende
            GotoList[Nr].Max = GotoList(Nr).Start
        GotoList[Nr].Dist = Abs(GotoList(Nr).Start - GotoList(Nr).Ende)
        Nr = Nr + 1
    # Calc Inside_Cnt and OutsideCnt
   
    for a in vbForRange(0, UBound(GotoList)):
        Min = GotoList(a).Min
        Max = GotoList(a).Max
        GotoList[a].Inside_Cnt=0
        GotoList[a].OutsideCnt=0        
        for t in vbForRange(0, UBound(GotoList)):
            if a != t:
                if GotoList(t).Min <= Min and GotoList(t).Max >= Max:
                    GotoList[a].OutsideCnt = GotoList(a).OutsideCnt + 1
                elif GotoList(t).Min >= Min and GotoList(t).Max <= Max:
                    GotoList[a].Inside_Cnt = GotoList(a).Inside_Cnt + 1
    for Nr in vbForRange(0, UBound(GotoList)):
        h = ( 1 + GotoList(Nr).Inside_Cnt )  /  ( GotoList(Nr).OutsideCnt + GotoList(Nr).Inside_Cnt + 1 )
        Res = Res + str(GotoList(Nr).Start) + ',' + str(GotoList(Nr).Ende) + ',' + str(int(h)) + ' '
    _fn_return_value = Left(Res, Len(Res) - 1)
    return _fn_return_value

def Test_GotoArrow():
    List_w_Height = String()
    #UT-------------------------
    List_w_Height = Calc_Height_GotoArrow('5,20 6,20 7,20 8,20 9,20 10,20 11,20 12,20 13,20 14,20 15,20 16,20 17,20 18,20 19,20')
    # LocalVar Sound
    pattgen.M06_Goto_Graph.Delete_Goto_Graph()
    Draw_GotoArrowTab(List_w_Height, M30.LastUsedColumnInRow(X02.ActiveSheet, M01.GoTo_Row))

# VB2PY (UntranslatedCode) Option Explicit
