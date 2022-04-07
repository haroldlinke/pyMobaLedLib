# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.21
# * Author: Harold Linke
# * Date: January 1st, 2020
# * Copyright: Harold Linke 2020
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 10.03.2020 - Harold Linke - first release
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
from tkintertable.TableModels import TableModel
from mlpyproggen.T01_exceltable import set_globaltabelmodel



def Cells(row:int, column:int):
    return None

def Rows(row:int):
    return None

def Columns(col:int):
    return None

def val(txt: str) -> int:
    return int(txt)

def MsgBox(ErrorMessage:str, type:int, ErrorTitle:str):
    print(ErrorTitle,": ",ErrorMessage)

def init_tablemodel_DCC():
    data = {'rec1': {'A':"",'Aktiv': "DCC", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec2': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"LED auf dem Mainboard","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"Heartbeat LED","Beleuchtung, Sound, oder andere Effekte":"RGB_Heartbeat(#LED)","Start\nLEDNr":0,"LEDs":1,"InCnt":0,"Loc\nInCh":"","LED/\nSound\nKanal":0},
            'rec3': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec4': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec5': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec6': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec7': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec8': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec9': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec10': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec11': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec12': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec13': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""},
            'rec14': {'A':"",'Aktiv': "", 'Filter': "", 'Adresse oder Name': '',"Typ":"","Startwert":"","Beschreibug":"","Verteiler\n-Nummer":"","Stecker-\nNummer":"","Icon":"","Name":"","Beleuchtung, Sound, oder andere Effekte":"","Start\nLEDNr":"","LEDs":"","InCnt":"","Loc\nInCh":"","LED/\nSound\nKanal":""}

            }
    init_tablemodel = TableModel()
    init_tablemodel.importDict(data)
    return init_tablemodel


class CWorkbook:
    def __init__(self, path: str):
        self.Path = path
        tablemodel = init_tablemodel_DCC() #get_globaltabelmodel()
        set_globaltabelmodel(tablemodel)
        self.sheets = [CWorksheet("DCC",tablemodel)]
        
    def Sheets(self,name):
        for sheet in self.sheets:
            if sheet.Name == name:
                return sheet
        return None
    
    def add_sheets(self,sheets):
        self.sheets = sheets

class CWorksheet:
    def __init__(self,Name,tablemodel):
        self.UsedRange = None
        self.ProtectContents = False
        self.Name = Name
        self.tablemodel = tablemodel
        
    def Cells(self,row, col):
        print("Cells", self.Name, row, col)
        return self.tablemodel.getCellRecord(row-1, col-1)
    
    def Range(self,cell1,cell2):
        print("Range,cell1,cell2")
        return None
    
    def Unprotect(self):
        self.ProtectContents = False
        
    def Columns(col:int):
        print("Columns",col)
        return None
    
class CCell:
    def __init__(self):
        self.Value = ""
        
class CWorksheetFunction:
    def __init__(self):
        pass
    def RoundUp(v1,v2):
        print("RoundUp")
        return int(v1)
        
class CApplication:
    def __init__(self):
        self.StatusBar = ""
        self.EnableEvents = True
        
class SoundLines:
    def __init__(self):
        self.dict = {}
    
    def Exists(self,Channel:int):
        pass
    
    def Add(Channel, Pin_playerClass):
        pass
    
ActiveWorkbook = Workbook = ThisWorkbook = CWorkbook("dummy_path")

WorksheetFunction = CWorksheetFunction()

Application = CApplication()

P01.ActiveSheet = ActiveWorkbook.Sheets("DCC")

xlPart = 0
