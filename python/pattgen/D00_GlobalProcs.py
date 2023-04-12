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
import mlpyproggen.Pattern_Generator as PG
import pattgen.M20_Morsecode as M20
import mlpyproggen.Pattern_Generator as PG
import pattgen.M02_Main as M02
import pattgen.Tabelle9 as PAT09

globalprocs= {"Make_Morsecode_Init"                    : M20.Make_Morsecode_Init,
              "Make_Morsecode"                         : M20.Make_Morsecode,
              "Add_Col_Button_Click"                   : PG.Add_Col_Button_Click,
              "Del_Col_Button_Click"                   : PG.Del_Col_Button_Click,
              "M02.Main_Menu"                          : M02.Main_Menu,
              "PAT09.Import_from_ProgGen_Button_Click" : PAT09.Import_from_ProgGen_Button_Click,
              "PAT09.Prog_Generator_Button_Click"      : PAT09.Prog_Generator_Button_Click,
              "PAT09.InsertPicture_Button_Click"       : PAT09.InsertPicture_Button_Click,
              "button_testen_cmd"                      : PG.button_testen_cmd,
              "button_aktualisieren_cmd"               : PG.button_aktualisieren_cmd,
              "button_newsheet_cmd"                    : PG.button_newsheet_cmd}



