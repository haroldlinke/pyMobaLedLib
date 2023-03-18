from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import pattgen.M01_Public_Constants_a_Var as M01
import ExcelAPI.XLW_Workbook as X02
import pattgen.M07_COM_Port
import pattgen.M55_PWM_Data_Send

"""UT----------------------------------------
----------------------------------
"""


def Test_Show_Select_GotoAct_Form():
    #UT----------------------------------------
    #  Debug.Print "Res= " & Select_from_Sheet_Form.Show_Form(SPECIAL_MODEDLG_SH, _
"Dialog Überschrift", "Überschrift", "Beschreibung", _
oDialog_Dat_ROW1:=Sheets(SPECIAL_MODEDLG_SH).Range("LED_Assignm_Head").Row + 1, _
oExp_Mode_COL:=1, _
oExpert_CheckBox:="Test Expert Mode", _
oExpert_CheckBox_Checked:=True, _
oLowerWin_COL:=3)
    Debug.Print('Res= ' + Select_from_Sheet_Form.Show_Form(M01.SPECIAL_MODEDLG_SH, 'Dialog Überschrift', 'Überschrift', 'Beschreibung', oDialog_Dat_ROW1= X02.Sheets(M01.SPECIAL_MODEDLG_SH).Range('Special_Mode_Head').Row + 1, oLowerWin_COL= 3))

def Test_Test_GotoNr_Form():
    PortId = Integer()
    #----------------------------------
    PortId = pattgen.M07_COM_Port.Get_USB_Port_with_Dialog()
    if PortId > 0:
        pattgen.M55_PWM_Data_Send.Open_Port_and_Show_Test_GotoNr_Form(PortId)

# VB2PY (UntranslatedCode) Option Explicit
