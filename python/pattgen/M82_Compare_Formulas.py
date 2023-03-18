from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLW_Workbook as X02

"""---------------------------------------"""


def Compare_Formulas_in_Sheets():
    c = Variant()

    Sh1 = X02.Worksheet()

    sh2 = X02.Worksheet()
    #---------------------------------------
    Sh1 = X02.Workbooks('Pattern_Configurator.xlsm~2020-10-16~11_16_38.xlsm').Sheets('Charlieplex.LED Test')
    sh2 = X02.Workbooks('Pattern_Configurator.xlsm').Sheets('Main')
    for c in Sh1.UsedRange:
        if c.Row == 36:
            if c.Column == 5:
                Debug.Print('')
        if c.HasFormula:
            if c.Formula != sh2.Cells(c.Row, c.Column).Formula:
                Debug.Print('Different Formulas:' + c.Row + ', ' + c.Column)
                Debug.Print(c.Formula)
                Debug.Print(sh2.Cells(c.Row, c.Column).Formula)
                Sh1.Activate()
                Sh1.Cells(c.Row, c.Column).Select()
                sh2.Activate()
                sh2.Cells(c.Row, c.Column).Select()
                Debug.Print('')

# VB2PY (UntranslatedCode) Option Explicit
