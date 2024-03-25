# -*- coding: utf-8 -*-
#
#         Calc Worksheet
#
# * Version: 4.02
# * Author: Harold Linke
# * Date: January 7, 2022
# * Copyright: Harold Linke 2021
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *  
# * https://github.com/Hardi-St/MobaLedLib
# *
# * MobaLedCheckColors is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * MobaLedCheckColors is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************

#------------------------------------------------------------------------------
# CHANGELOG:
# 2021-12-23 v4.01 HL: - Inital Version converted by VB2PY based on MLL V3.1.0
# 2022-01-07 v4.02 HL: - Else:, ByRef check done, first PoC release

import pattgen.M30_Tools as M30
import pattgen.M02_Main as M02
import ExcelAPI.XLW_Workbook as X02

funcvars=globals()

def getCellValuebyName(ws,name,valtype=str):
    cell = ws.find_RangeName(name)
    return valtype(cell)

def setCellValuebyName(ws,name,value):
    cell = ws.find_RangeName(name)
    cell.Value=value
    
def IF(condition,true_val,false_val):
    if condition:
        return true_val
    else:
        return false_val
    
def OR(*arguments):
    for cond in arguments:
        if cond==True:
            return True
    return False

def AND(*arguments):
    for cond in arguments:
        if cond==False:
            return False
    return True

def ISNUMBER(value):
    valstr=str(value)
    if valstr.isnumeric():
        return True
    else:
        return False
    
def CONCATENATE(*arguments):
    resulttext=""
    for text in arguments:
        if type(text)!=str:
            text=str(text)
        resulttext=resulttext+text
    return resulttext
        
def COUNTIF(rangelist,testval):
    count=0
    for i in rangelist:
        if i == testval:
            count+=1
    return count

def DEC2BIN(value,places=None):
    res="{0:08b}".format(value)
    return res

def LEFT(s, amount):
    s=str(s)
    return s[:amount]
    
def RIGHT(s, amount):
    #if not isinstance(s,str):
    s=str(s)    
    return s[-amount:]

def MID(s, offset, amount):
    #if not isinstance(s,str):
    s=str(s)    
    return s[offset-1:offset-1+amount]

def LEN(text):
    if isinstance(text,X02.CRange):
        text=str(text)
    return len(text)

def SUBSTITUTE(text,old_text,new_text=None,count=None):
    if new_text==None:
        new_text=""
    if count == None:
        res=text.replace(old_text,new_text)
    else:
        res=text.replace(old_text,new_text,count)
    return res
    

def COUNTA(rangelist):
    count=0
    for i in rangelist:
        if i != "":
            count+=1
    return count

def Calc_Worksheet(ws,cell=None):
    global funcvars
    
    def createcellvariable(ws,name):
        global funcvars
        cellvalue = getCellValuebyName(ws,name)
        if cellvalue.isnumeric():
            funcvars.__setitem__(name,int(cellvalue))
        else:
            funcvars.__setitem__(name,cellvalue)
   
    def setcellfromvariable(ws,name,variable=None):
        global funcvars
        if variable == None:
            variable=funcvars.get(name,None)
        if variable == None:
            createcellvariable(ws,name)
            variable=funcvars.get(name,None)
        
        setCellValuebyName(ws, name, variable)
        return
    
    if cell!=None:
        WS_Conditional_Formating(ws, cell)
        
    Kanaele = getCellValuebyName(ws, "E5",int)
    Start = getCellValuebyName(ws, "E34")
    Bits_pro_Wert = getCellValuebyName(ws, "E6",int)
    ErsteRGBLED = getCellValuebyName(ws, "E2",int)
    StCh_FreeBits_BpC = getCellValuebyName(ws, "E6",int)
    InputCh = getCellValuebyName(ws, "E35")
    Ende = getCellValuebyName(ws, "E42")
    Makro_Name = getCellValuebyName(ws, "E22")
    InNrStr = getCellValuebyName(ws, "H35")
    FreeBits_BpC = getCellValuebyName(ws, "E37",int)
    InNrStr2 = getCellValuebyName(ws, "J35")
    Zeiten = getCellValuebyName(ws, "E31")
    Mode = getCellValuebyName(ws, "E10")
    Analoges_Überblenden = getCellValuebyName(ws, "E11")
    Analog = getCellValuebyName(ws, "E33")
    Goto_Mode = getCellValuebyName(ws, "E12")
    SchalterNr = getCellValuebyName(ws, "E4")
    Startkanal = getCellValuebyName(ws, "E3",int)
    FreeBits = getCellValuebyName(ws, "E39",int)
    Pattern_u_FreeBits = getCellValuebyName(ws, "E38")
    Wert_Min = getCellValuebyName(ws, "E7")
    Wert_Max = getCellValuebyName(ws, "E8")
    Wert_ausgeschaltet = getCellValuebyName(ws, "E9")
    Mode16 = getCellValuebyName(ws, "E32")
    Pattern_Bytes = getCellValuebyName(ws, "E40")
    Goto_Bytes = getCellValuebyName(ws, "E41")
    TimerBytes = getCellValuebyName(ws, "H44")
    DataBytes = getCellValuebyName(ws, "K44")
    
    funcvars=globals()
    
    #copy Timevalue from row 28 to row 29 shifted by one col left
    cell_list=X02.Range("F28:EW28")
    for cell in cell_list:
        target_cell=X02.Cells(29, cell.Column-1)
        target_cell.Value = cell.Value
    
    #* "F2" <f>IF(E2="","<= Bitte erste RGB LED des Musters eingeben","")</f>
    createcellvariable(ws, "E2")
    F2=IF(E2=="","<= Bitte erste RGB LED des Musters eingeben","")
    setcellfromvariable(ws, "F2",F2)
    
    #* "F3" <f>IF(OR(AND(E3 <>"",E3=0),E3=1,E3=2),"","<= Bitte Startkanal innerhalb der RGB LED angeben")</f>
    createcellvariable(ws, "E3")
    F3=IF(OR(AND(E3 !="",E3==0),E3==1,E3==2),"","<= Bitte Startkanal innerhalb der RGB LED angeben")
    setcellfromvariable(ws, "F3", F3)

    #* "F4" <f>IF(E4="","<= Bitte Nummer des Schalters eingeben","")</f>
    createcellvariable(ws, "E4")
    F4=IF(E4=="","<= Bitte Nummer des Schalters eingeben","")
    setcellfromvariable(ws, "F4",F4)
    
    #* "F5" <f>IF(AND(ISNUMBER(Kanaele),Kanaele>0,Kanaele<=100),"","<- Bitte Anzahl der Kanäle eingeben(1..100)")</f>
    #F5=IF(AND(ISNUMBER(Kanaele),Kanaele>0,Kanaele<=100),"","<- Bitte Anzahl der Kanäle eingeben(1..100)")
    if ISNUMBER(Kanaele):
        F5=IF(AND(Kanaele>0,Kanaele<=100),"","<- Bitte Anzahl der Kanäle eingeben(1..100)")
    else:
        F5="<- Bitte Anzahl der Kanäle eingeben(1..100)"
    setcellfromvariable(ws, "F5",F5)
    
    #* "F6" <f>CONCATENATE(" => ",2^Bits_pro_Wert," Helligkeitsstufen (0..",2^Bits_pro_Wert-1,")")</f>
    F6=CONCATENATE(" => ",2**Bits_pro_Wert," Helligkeitsstufen (0..",2**Bits_pro_Wert-1,")")
    setcellfromvariable(ws, "F6",F6)
    
    #* "F7" <f>IF(OR(E7="",E7<0,E7>255),"<= Bitte Wert für nicht aktive LED angeben (0..255)","")</f>
    createcellvariable(ws, "E7")
    F7=IF(OR(E7=="",E7<0,E7>255),"<= Bitte Wert für nicht aktive LED angeben (0..255)","")
    setcellfromvariable(ws, "F7",F7)

    #* "F8" <f>IF(OR(E8="",E8<0,E8>255),"<= Bitte Wert für aktive LED angeben (0..255)","")</f>
    createcellvariable(ws, "E8")
    F8=IF(OR(E8=="",E8<0,E8>255),"<= Bitte Wert für aktive LED angeben (0..255)","")
    setcellfromvariable(ws, "F8",F8)
    
    #* "F9" <f>IF(OR(E9="",E9<0,E9>255),"<= Bitte LED Wert angeben wenn Schalter aus ist","")</f>
    createcellvariable(ws, "E9")
    F9=IF(OR(E9=="",E9<0,E9>255),"<= Bitte LED Wert angeben wenn Schalter aus ist","")
    setcellfromvariable(ws, "F9",F9)
    
    #* "E31" <f>Calc_TimesStr(F28:BQ28,Mode)</f> -> Zeiten
    E31=M02.Calc_TimesStr(X02.Range("F28:BQ28"),Mode)
    Zeiten=E31
    setcellfromvariable(ws, "E31",E31)
    

    #* "E32" WENN(ODER(Analoges_Überblenden="";Analoges_Überblenden=0;Analoges_Überblenden="N";Analoges_Überblenden="n");"";WENN(Analoges_Überblenden="X";"X";"A"))
    E33 = IF (OR(Analoges_Überblenden=="",Analoges_Überblenden=="0",Analoges_Überblenden=="N"), "", IF(Analoges_Überblenden=="X","X","A") ) 
    Analog = E33
    setcellfromvariable(ws, "E33",E33)
        
    #* "E34" <f>CONCATENATE(Analog,"PatternT",64-COUNTIF(E29:BP29,""),"(")</f> -> Start
    E34=CONCATENATE(Analog,"PatternT",64-COUNTIF(X02.Range("E29:BP29"),""),"(")
    Start=E34
    setcellfromvariable(ws, "E34",E34)  

    #* "E35" <f>IF(Goto_Mode=1,"SI_LocalVar",SchalterNr)</f> -> InputCh
    E35=IF(Goto_Mode=="1","SI_LocalVar",SchalterNr)
    InputCh=E35
    setcellfromvariable(ws, "E35",E35)
    
    #* "H35" <f>IF(Goto_Mode=1,"",",InCh")</f> -> InChStr
    H35=IF(Goto_Mode=="1","",",InCh")
    InChStr=H35
    setcellfromvariable(ws, "H35",H35)
    
    #* "J35" <f>IF(Goto_Mode=1,"SI_LocalVar","InCh")</f> -> InNrStr2
    J35=IF(Goto_Mode=="1","SI_LocalVar","InCh")
    InNrStr2=J35
    setcellfromvariable(ws, "J35",J35)
    
    #* "E36" <f>Startkanal+(Bits_pro_Wert-1)*4+FreeBits*32</f> -> StCh_FreeBits_BpC
    E36=Startkanal+(Bits_pro_Wert-1)*4+FreeBits*32
    StCh_FreeBits_BpC=E36
    setcellfromvariable(ws, "E36",E36)
    
    #* "F36" <f>DEC2BIN(E36,8)</f>
    F36=DEC2BIN(E36,8)
    setcellfromvariable(ws, "F36",F36)
    
    #* "E37" <f>(Bits_pro_Wert-1)*4+FreeBits*32</f> ->FreeBits_BpC
    E37=(Bits_pro_Wert-1)*4+FreeBits*32
    FreeBits_BpC=E37
    setcellfromvariable(ws, "E37",E37)
    E6 = getCellValuebyName(ws, "E6",int)
    E38=M02.CalculatePattern(Kanaele,E6,X02.Range("F50:EW304"))
    Pattern_u_FreeBits=E38
    setcellfromvariable(ws, "E38",E38)

    #* "E39" <f>LEFT(Pattern_u_FreeBits,1)</f>
    E39=LEFT(Pattern_u_FreeBits,1)
    FreeBits=E39
    setcellfromvariable(ws, "E39",E39)

    #* "E40" <f>MID(Pattern_u_FreeBits,3,LEN(Pattern_u_FreeBits))</f> -> Pattern_Bytes
    E40=MID(Pattern_u_FreeBits,3,LEN(Pattern_u_FreeBits))
    Pattern_Bytes=E40
    setcellfromvariable(ws, "E40",E40)

    #* "E41" <f>Calculate_Goto(Kanaele,E12,F47:EW47,F50:EW304)</f> -> Goto_Bytes
    createcellvariable(ws, "E12")
    E41=M02.Calculate_Goto(Kanaele,E12,X02.Range("F47:EW47"),X02.Range("F50:EW304"))
    Goto_Bytes=E41
    setcellfromvariable(ws, "E41",E41)
    
    #* "E42" <f>CONCATENATE(Kanaele,",",Wert_Min,",",WertMax,",",Wert_ausgeschaltet,",",Mode16,Zeiten,Pattern_Bytes,Goto_Bytes,")")</f> -> Ende
    E42=CONCATENATE(Kanaele,",",Wert_Min,",",Wert_Max,",",Wert_ausgeschaltet,",",Mode16,Zeiten,Pattern_Bytes,Goto_Bytes,")")
    Ende=E42
    setcellfromvariable(ws, "E42",E42)

    #* "E43" <f>CONCATENATE("#define ",Makro_Name,"(LED,NStru,InCh) ",Start,"LED,NStru,InCh,",Ende)</f>
    E43=CONCATENATE("#define ",Makro_Name,"(LED,NStru,InCh) ",Start,"LED,NStru,InCh,",Ende)
    setcellfromvariable(ws, "E43",E43)

    #* "H44" <f>2*(64-COUNTIF(E29:BP29,""))</f> -> TimerBytes
    H44=2*(64-COUNTIF(X02.Range("E29:BP29"),""))
    TimerBytes=H44
    setcellfromvariable(ws, "H44",H44)

    #* "K44" <f>LEN(Pattern_Bytes)-LEN(SUBSTITUTE(Pattern_Bytes,",",))</f> -> DataBytes
    K44=LEN(Pattern_Bytes)-LEN(SUBSTITUTE(Pattern_Bytes,",",))
    DataBytes=K44
    setcellfromvariable(ws, "K44",K44)

    #* "E46" <f>E44+TimerBytes+DataBytes</f> -> FlashUsage
    createcellvariable(ws, "E44")
    E46=E44+TimerBytes+DataBytes
    FlashUsage=E46
    setcellfromvariable(ws, "E46",E46)
    
    #* "F48" <f>IF(COUNTA(F50:AM57)=0,"Bitte Tabelle ausfüllen. Positionen an denen die LEDs leuchten sollen werden mit einem Zeichen (z.B. x) markiert. Bei einer leeren Zellen ist die LED aus.","")</f>
    F48=IF(COUNTA("F50:AM57")==0,"Bitte Tabelle ausfüllen. Positionen an denen die LEDs leuchten sollen werden mit einem Zeichen (z.B. x) markiert. Bei einer leeren Zellen ist die LED aus.","")
    setcellfromvariable(ws, "F48",F48)    
    
    #* "E20" <f>CONCATENATE(Start,ErsteRGBLED,",",StCh_FreeBits_BpC,",",InputCh,",",Ende," // ",Makro_Name)</f>
    E20=CONCATENATE(Start,ErsteRGBLED,",",StCh_FreeBits_BpC,",",InputCh,",",Ende," // ",Makro_Name)
    setcellfromvariable(ws, "E20",E20)
    
    #* "E23" <f>CONCATENATE("#define ",IF(Makro_Name="","Makro_Name",Makro_Name),"(LED",InNrStr,") ",Start,"LED,",StCh_FreeBits_BpC,",",InNrStr2,",",Ende)</f> -> Macro_Range
    E23=CONCATENATE("#define ",IF(Makro_Name=="","Makro_Name",Makro_Name),"(LED",InNrStr,") ",Start,"LED,",StCh_FreeBits_BpC,",",InNrStr2,",",Ende)
    Macro_Range=E23
    setcellfromvariable(ws, "E23",E23)
    
    #* "E25" <f>CONCATENATE("#define ",IF(Makro_Name="","Makro_Name",Makro_Name),"_StCh(LED,StCh",InNrStr,") ",Start,"LED,","StCh+",FreeBits_BpC,",",InNrStr2,",",Ende)</f>
    E25=CONCATENATE("#define ",IF(Makro_Name=="","Makro_Name",Makro_Name),"_StCh(LED,StCh",InNrStr,") ",Start,"LED,","StCh+",FreeBits_BpC,",",InNrStr2,",",Ende)
    setcellfromvariable(ws, "E25",E25)
    
    #* "D28" <f>IF(Zeiten="","Bitte Dauer eintragen =>","")</f>
    D28=IF(Zeiten=="","Bitte Dauer eintragen =>","")
    setcellfromvariable(ws, "D28",D28)
    
    #* "E29" <f>IF(AND(Ist_Formel(F28),F29=""),"",IF(F28<>"",F28,""))</f>
    #* until "BP29"
    #*

    #* "E32" <f>IF(Mode="",IF(myInStr(Zeiten,"/16")>0,"PF_SLOW","PM_NORMAL"),IF(AND(myInStr(Zeiten,"/16")>0,myInStr("X"&Mode,"PF_SLOW")=0),"PF_SLOW|"&Mode,Mode))</f> -> Mode16
    E32=IF(Mode=="",IF(M30.myInStr(Zeiten,"/16")>0,"PF_SLOW","PM_NORMAL"),IF(AND(M30.myInStr(Zeiten,"/16")>0,M30.myInStr("X"+Mode,"PF_SLOW")==0),"PF_SLOW|"+Mode,Mode))
    Mode16=E32
    setcellfromvariable(ws, "E32",E32)
    
def convertCell2Excel(cell):
    #returns the Excel Cell Representation e.g. "E5"
    column=cell.Column
    col1 = column % 26
    col2 = int(column/26.0)
    cellstr=""
    if col2!=0:
        cellstr=chr(col2+ord("A")-1)
    cellstr = cellstr+chr(col1+ord("A")-1)
    cellstr = cellstr+str(cell.Row)
    return cellstr
    
def compareCells(cell,xcellstr):
    #compares Cell objects wit Excelcellstring e.g. "E1"
    pattern=re.compile("([A-Z]+)(\d+)")
    m = re.match(pattern,xcellstr)
    #print(rangestr,"->",m.groups())
    m_list = m.groups(0)
    col_str = m_list[0]
    named_range_col = 0
    for char in col_str:
        index = ord(char)-ord("A")+1
        named_range_col = named_range_col*26+index
    row_str = m_list[1]
    named_range_row = int(row_str)
    if cell.Row==named_range_row and cell.Column==named_range_col:
        return True
    else:
        return False
    
def WS_Conditional_Formating(ws,changedCell):
    #test=convertCell2Excel(changedCell)
    #print(test)
    if convertCell2Excel(changedCell)=="E5":
        #extend grid
        value=int(changedCell)
        ws.changeGrid(2,((48,3),(48+value+1,63)))
        

    
