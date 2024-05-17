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
import pattgen.Select_GotoNr_Form
import pattgen.Select_COM_Port_UserForm
import pattgen.MainMenu_Form
import pattgen.StatusMsg_UserForm
import pattgen.Select_from_Sheet_Form
import pattgen.Examples_UserForm



#***************************
#* UserForms
#***************************

StatusMsg_UserForm = None
Select_COM_Port_UserForm = None
Select_GotoNr_Form = None
MainMenu_Form = None
Select_from_Sheet_Form = None
Examples_UserForm = None

def init_UserForms():
    global StatusMsg_UserForm,  Select_COM_Port_UserForm, Select_GotoNr_Form,MainMenu_Form, Select_from_Sheet_Form, Examples_UserForm
    
    #Select_COM_Port_UserForm = D08.CSelect_COM_Port_UserForm()
    #StatusMsg_UserForm = D09.CStatusMsg_UserForm()
   
    Select_GotoNr_Form = pattgen.Select_GotoNr_Form.CSelect_GotoNr_Form(PG.global_controller)
    MainMenu_Form = pattgen.MainMenu_Form.CMainMenu_Form(PG.global_controller)
    Select_COM_Port_UserForm = pattgen.Select_COM_Port_UserForm.CSelect_COM_Port_UserForm(PG.global_controller)
    StatusMsg_UserForm = pattgen.StatusMsg_UserForm.CStatusMsg_UserForm(PG.global_controller)
    Select_from_Sheet_Form = pattgen.Select_from_Sheet_Form.CSelect_from_Sheet_Form(PG.global_controller)
    Examples_UserForm = pattgen.Examples_UserForm.CExamples_UserForm(PG.global_controller)