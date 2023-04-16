# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors ConfigFile
#
# * Version: 1.00
# * Author: Harold Linke
# * Date: December 25th, 2019
# * Copyright: Harold Linke 2019
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *
# * History of Change
# * V1.00 23.11.2019 - Harold Linke - first release
# *
# * MobaLedCheckColors supports the MobaLedLib by Hardi Stengelin
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
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# * MobaLedCheckColors is based on tkColorPicker by Juliette Monsel
# * https://sourceforge.net/projects/tkcolorpicker/
# *
# * tkcolorpicker - Alternative to colorchooser for Tkinter.
# * Copyright 2017 Juliette Monsel <j_4321@protonmail.com>
# *
# * tkcolorpicker is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * tkcolorpicker is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# * The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# * License: http://creativecommons.org/licenses/by-sa/3.0/
# ***************************************************************************


import os
import json
import logging

# ----------------------------------------------------------------
# Class ConfigFile
# ----------------------------------------------------------------
class ConfigFile():
    """ Configuration File """

    def __init__(self,default_config, filename,filedir=""):
        # type:
        """ Config Constructor Method (__init__)

        Arguments:
            default_config
            filename

        Raises:
            None
        """
        if filedir == "":
            filedir = os.path.dirname(os.path.realpath(__file__))
            
        filepath1 = os.path.join(filedir, filename)
        
        self.filepath = os.path.normpath(filepath1)

        try:
            jsondata={}
            file_not_found=True
            with open(self.filepath, "r", encoding='utf8') as read_file:
                file_not_found=False
                jsondata = json.load(read_file)
        except ValueError as err:
            logging.error ("ERROR: JSON Error in Config File %s",self.filepath)
            logging.error(err)
        except:
            if file_not_found:
                logging.warning ("Warning: Config File %s not found",self.filepath)
            else:
                logging.error ("ERROR: JSON Error in Config File %s",self.filepath)
                logging.error(jsondata)
                jsondata = {}
            
        try:
            self.data = default_config.copy()
            if True: #self.data == {}:
                self.data.update(jsondata)
            else:
                if all(elem in self.data.keys() for elem in jsondata.keys()):
                    self.data.update(jsondata)
                else:
                    logging.debug (self.data.keys())
                    logging.debug (jsondata.keys())
                    logging.error ("ERROR: JSON Error in Config File %s - wrong key in config-file",self.filepath)
                    logging.error(jsondata)
                    self.data.update(jsondata)

        except:
            logging.error ("Error in Config File %s",self.filepath)
            logging.error(self.data)
            self.data = default_config.copy()
        
        create_sorted=False
        
        sorted_dict = dict(sorted(self.data.items()))
        
        if create_sorted:
            with open(self.filepath+"sort", 'w', encoding='utf8') as outfile:
                json.dump(sorted_dict, outfile, ensure_ascii=False, indent=4)            

    def save(self):

        # Write JSON file
        with open(self.filepath, 'w', encoding='utf8') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False, indent=4)
        logging.debug("ConfigFile-Save:" + self.filepath)
        print("ConfigFile-Save:" + self.filepath, "Port:",self.data.get("serportname"))