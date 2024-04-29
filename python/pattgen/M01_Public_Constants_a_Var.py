from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as X02
import proggen.M02_Public as M02


""" Debug Events
 30.05.20:
# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
 06.12.19: Old: "\\libraries\\MobaLedLib\\examples\\23_B.LEDs_AutoProg"
 20.07.20: All Versions are located in "\\MobaLedLib\\Ver_..." to be able to set one exclusion in the virus scan program for all versions
 14.06.20:
 Version of the MLL_pcf file    17.11.19:
 ??
                     (29.12.19: Old E16)
                     (29.12.19: Old E18)
                     (29.12.19: Old D2:D18)
 Column D
                     (29.12.19: Old 20)
 Column E
 Column E
 Column F
                     (29.12.19: Old E46)
                     (29.12.19: Old E46:EW300)
                     (29.12.19: Old F46:EF300)
                     (29.12.19: Old 46)
 Column F
 Column EW
 We just check the attributes of the first x LED columns
                     (29.12.19: Old F24:AI24)
                     (29.12.19: Old 24)
 Column F
                     (29.12.19: Old F43:EW43)
                     (29.12.19: Old 43)
 Column F
 Proportional column width display in Adjust_Column_With_to_Duration()
 The quotiont Max_t / Min_t define the minimal column width.
 If the quotient is below the normal column width (NormColWidth) is used for the small columns
 If the quotient id greater the small columns are limmited to Min_ColWidth. In between the with is adapted proportional
 Normal column width. Also used in Normal_Column_With
 Minimal width
 Could be set to true to regenerate all pictures
 OEM char(MultiEdit): >>   Win: upperline (Line on top of the characters)
 This text is added to the Description in the Prog_Generator as a hint for automatic generated entry which could be replaced automatically
 Contains the sheet name which is used to read WertMin and WertMax, ... from
Public Button_Init_Proc_Finished As Boolean
 05.01.22: Juergen call init function synchronous
 Sheet names:
 COM Port:
 Column where the com port for the Left Arduino on the Main Board is stored
 Column where the com port for the Right Arduino on the Main Board is stored (Not used in this project)
 Column where the com port for programming the Tinys is stored
 Column where the build options for programming the Tinys is stored
 This row contains some sheet specific varaibles. The text uses white color => It' not visible
 This page is used to store the MouseHook. There must be a named range called "MouseHook" (X1).
---------------------------------------------------------------------
----------------------------------------------
# VB2PY (CheckDirective) VB directive took path 1 on USE_SKETCHBOOK_DIR
"""

Exp_Prog_Gen_Version = M02.Lib_Version_Nr
DEBUG_CHANGEEVENT = False
USE_SKETCHBOOK_DIR = True
SrcDirInLib = '\\libraries\\MobaLedLib\\extras\\'
DestDir_All = '\\MobaLedLib\\Ver_' + M02.Lib_Version_Nr + '\\'
AppLoc_Ardu = '\\AppData\\Local\\Arduino15\\'
INTPROGNAME = 'Pattern_Configurator'
DSKLINKNAME = 'MobaLedLib Pattern_Configurator'
DefaultIcon = 'Icons\\05_Gerald_Patt.ico'
SECOND_PROG = 'Prog_Generator_MobaLedLib'
SECOND_LINK = 'Prog_Generator MobaLedLib'
SECOND_ICON = 'Icons\\05_Gerald_Prog.ico'
WikiPg_Icon = 'Icons\\WikiMLL_v5.ico'
WikiPg_Link = 'https://wiki.mobaledlib.de/'
Env_USERPROFILE = 'USERPROFILE'
ACT_MLL_pcf_Version = 1
MacEnab_Rng = 'E1'
LED_Cnt_Rng = 'E5'
BitsVal_Rng = 'E6'
WertMin_Rng = 'E7'
WertMax_Rng = 'E8'
AnaFade_Rng = 'E11'
GrafDsp_Rng = 'E14'
ErgebnisRng = 'E20'
Macro_N_Rng = 'E22'
PARAMETER_RANGE = 'D2:D22'
PARAMETER_Col = 4
PARAMETER_Ro11 = 2
PARAMETER_Ro1N = 24
Goto_Txt_col = 5
LED_Text_Col = 5
GotoModeRow = 12
GrafDsp_Row = 14
GrafDsp_Col = 6
TableEmptyMsgRng = 'F44'
FirstLEDTabRANGE = 'E50'
LEDsRANGE = 'E50:EW304'
LEDs__TAB = 'F50:EW304'
LED_NR_ROW = 49
LEDsTAB_R = 50
LEDsTAB_C = 6
Last_LEDsCol = 153
Last_LEDs_ChkAttrCol = 27
Dauer_Rng = 'F28:AI28'
Dauer_Row = 28
Dauer_Col1 = 6
Dauer__Cnt = 30
GoTo_RNG = 'F47:EW47'
GoTo_Row = 47
GoTo_Col1 = 6
NormWidth_MM = 4*49/6.71
Min_Width_MM = 50*49/6.71
NormColWidth = 49 #was 6.71
Min_ColWidth = 0.8*49/6.71
Transp_Start_Graph = 0.7*49/6.71
ExampleDir = 'Pattern_Config_Examples'
MyExampleDir = 'MyPattern_Config_Examples'
OVERWRITE_EXISTING_PIC = False
pcfSep = 175
FROM_PAT_CONFIG_TXT = ' (pc)'
WertMinMaxValid = String()
WertMin = Integer()
WertMax = Integer()
BitsVal = Integer()
LED_Scale = Double()
LED_Offset = Double()
StartMax = Double()
StartMin = Double()
SaveDirCreated = Boolean()
ExampleName = String()
StdDescStart = 'Mit diesem Blatt kann die Konfiguration'
StdDescEdges = '497;0;767.4421;142.8818'
MAIN_SH = 'Main'
LANGUAGES_SH = 'Languages'
PAR_DESCRIPTION_SH = 'Par_Description'
GOTO_ACTIVATION_SH = 'Goto_Activation_Entries'
SPECIAL_MODEDLG_SH = 'Special_Mode_Dlg'
ComPortfromOnePage = MAIN_SH
Page_ID = 'DCC'
COMPort_COL = 30
COMPrtR_COL = 31
COMPrtT_COL = 32
BuildOT_COL = 33
SH_VARS_ROW = 1
BOARD_NANO_OLD = '--board arduino:avr:nano:cpu=atmega328old'
BOARD_NANO_NEW = '--board arduino:avr:nano:cpu=atmega328'
BOARD_UNO_NORM = '--board arduino:avr:uno'
AUTODETECT_STR = 'AutoDet'
DEFARDPROG_STR = '--pref programmer=arduino:arduinoisp'
MouseHook_Store_Page = 'Main'
Sketchbook_Path = String()