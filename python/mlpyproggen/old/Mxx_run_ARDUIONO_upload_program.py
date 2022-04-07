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

import subprocess

def start_ARDUINO_program_Run(self):
    result = subprocess.run(self.startfile, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    
    if result.returncode == 0:
        self.arduinoMonitorPage.add_text_to_textwindow("\n"+self.ARDUINO_message2+"\n*******************************************************\n",highlight="OK")
    else:
        self.arduinoMonitorPage.add_text_to_textwindow("\n******** "+self.ARDUINO_message3+" ********\n",highlight="Error")
        self.arduinoMonitorPage.add_text_to_textwindow("\n"+result.stdout,highlight="Error")
        self.arduinoMonitorPage.add_text_to_textwindow("\n*******************************************************\n\n\n",highlight="Error")

def write_stdout_to_text_window(self):
    if self.continue_loop:
        output = self.process.stdout.readline()

        if output != '' and self.continue_loop:
            try:
                self.arduinoMonitorPage.add_text_to_textwindow(output.decode('utf-8').strip())
            except BaseException as e:
                logging.debug(e)
                logging.debug("ERROR: Write_stdout_to_text_window: %s",output)
                pass            
        
        if self.process.poll() is not None:
            self.continue_loop=False
            self.rc = self.process.poll()
            if self.rc==1:
                self.arduinoMonitorPage.add_text_to_textwindow("\n******** "+self.ARDUINO_message3+" ********\n",highlight="Error")
            else:
                self.arduinoMonitorPage.add_text_to_textwindow("\n"+self.ARDUINO_message2+"\n*******************************************************\n",highlight="OK")

    if self.continue_loop:
        self.after(10,self.write_stdout_to_text_window)

        
def start_ARDUINO_program_Popen(self):
    try:
        self.process = subprocess.Popen(self.startfile, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin = subprocess.DEVNULL)
        self.continue_loop=True
        self.write_stdout_to_text_window()
    except BaseException as e:
        #logging.error("Exception in start_ARDUINO_program_Popen %s - %s",e,self.startfile[0])
        self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")
        self.arduinoMonitorPage.add_text_to_textwindow("\n* Exception in start_ARDUINO_program_Popen "+ e + "-" + self.startfile[0]+ "\n",highlight="Error")
        self.arduinoMonitorPage.add_text_to_textwindow("\n*****************************************************\n",highlight="Error")

def upload_to_ARDUINO(self,_event=None,arduino_type="LED",init_arduino=False):
# send effect to ARDUINO
    if self.controller.ARDUINO_status == "Connecting":
        tk.messagebox.showwarning(title="Zum ARDUINO Hochladen", message="PC versucht gerade sich mit dem ARDUINO zu verbinden, bitte warten Sie bis der Vorgang beendet ist!")
        return
    self.controller.disconnect()
    self.controller.set_connectstatusmessage("Kompilieren und Hochladen ...",fg="green")
    
    if arduino_type == "LED":
        self.create_ARDUINO_CMD(init_arduino=init_arduino)
            
    private_startfile = self.getConfigData("startcmdcb")
    
    macrodata = self.controller.MacroDef.data.get("ARDUINOMonitorPage",{})
    
    self.arduinoMonitorPage=self.controller.getFramebyName ("ARDUINOMonitorPage")
    self.arduinoMonitorPage.delete_text_from_textwindow()
    
    file_not_found = True
    
    system_platform = platform.platform()
    
    if not "Windows" in system_platform:
        private_startfile = True
    
    self.ARDUINO_message4=""
    
    if private_startfile == True:
        filename = self.getConfigData("startcmd_filename")
        logging.debug("upload_to_ARDUINO - Individual Filename: %s",filename)
        if filename == " " or filename == "":
            filename = "No Filename provided"
        logging.debug("send to ARDUINO - Platform: %s",platform.platform())
        
        macos = "macOS" in system_platform
        macos_fileending = "/Contents/MacOS/Arduino" 
        if macos:
            logging.debug("This is a MAC")
            if not filename.endswith(macos_fileending):
                filename = filename + "/Contents/MacOS/Arduino"
            file_not_found = False
        else:
            if os.path.isfile(filename):
                file_not_found = False
            if file_not_found:
                self.ARDUINO_message4 = macrodata.get("Message_4","") + filename

    else:
        file_not_found = True
        #check if arduino_debug.exe exists in the program dirs
        Win_ARDUINO_searchlist = macrodata.get("Win_ARDUINOIDE","")
        
        for IDE_filename in Win_ARDUINO_searchlist:
            if os.path.isfile(IDE_filename):
                file_not_found = False
                filename = IDE_filename
                break
        if file_not_found:
            self.ARDUINO_message4 = macrodata.get("Message_4","") + repr(Win_ARDUINO_searchlist)
    logging.debug("upload_to_ARDUINO - Filename: %s",filename)
    self.controller.showFramebyName("ARDUINOMonitorPage")
    self.controller.set_connectstatusmessage("Kompilieren und Hochladen ...",fg="green")
    self.update()
    
    if file_not_found:
        self.arduinoMonitorPage.add_text_to_textwindow("\n*******************************************************\n"+self.ARDUINO_message4+"\n*******************************************************\n")            
    else:
        serport = self.getConfigData("serportname")
        arduinotypenumber = self.getConfigData("ArduinoTypeNumber")
        ArduinoTypeNumber_config_dict = self.get_param_config_dict("ARDUINO Type")
        ArduinotypeList = ArduinoTypeNumber_config_dict["Values2Params"]
        ArduinoType = ArduinotypeList[arduinotypenumber]
        
        self.ARDUINO_message1 = macrodata.get("Message_1","")
        self.ARDUINO_message2 = macrodata.get("Message_2","")
        self.ARDUINO_message3 = macrodata.get("Message_3","")
        
        #h_filedir = os.path.dirname(filename)
        filedir = os.path.dirname(os.path.realpath(__file__))
        h_filedir1 = os.path.dirname(filedir)
        h_filedir = os.path.dirname(h_filedir1)            
        #os.chdir(h_filedir)
        os.chdir(self.controller.mainfile_dir)
        
        #filedirname = os.path.join(h_filedir, filename)
        #if platform.platform == "darwin":
        #    logging.debug("This is a MAC")
        #    filedirname = filename + "/Contents/MacOS/Arduino"
        #else:
        filedirname = filename
        
        if arduino_type=="DCC":
            ino_filename = self.controller.get_macrodef_data("StartPage","InoName_DCC") #"../../examples/23_A.DCC_Interface/23_A.DCC_Interface.ino"
        elif arduino_type=="Selectrix":
            ino_filename = self.controller.get_macrodef_data("StartPage","InoName_SX") #"../../examples/23_A.DCC_Interface/23_A.DCC_Interface.ino"
        elif arduino_type=="LED":
            ino_filename = self.controller.get_macrodef_data("StartPage","InoName_LED") #"LEDs_AutoProg.ino"
        
        if ArduinoType == " ":
            self.startfile = [filedirname,ino_filename,"--upload","--port",serport,"--pref","programmer=arduino:arduinoisp","--pref","build.path=../Arduino_Build_LEDs_AutoProg","--preserve-temp-files"]
        else:
            self.startfile = [filedirname,ino_filename,"--upload","--port",serport,"--board",ArduinoType,"--pref","programmer=arduino:arduinoisp","--pref","build.path=../Arduino_Build_LEDs_AutoProg","--preserve-temp-files"]
        
        logging.debug(repr(self.startfile))
        
        self.arduinoMonitorPage.add_text_to_textwindow("\n\n*******************************************************\n"+self.ARDUINO_message1+"\n*******************************************************\n\n")
        
        if arduino_type=="LED":
            self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*    Zum                                                                  *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*     PC                    Prog_Generator " + PROG_VERSION+ " by Harold    *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*      \\\\                                                                 *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*       \\\\                                                                *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*    ____\\\\___________________                                            *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  | [_] | | [_] |[oo]    |  Achtung: Es muss der LINKE               *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  Arduino mit dem PC verbunden             *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  sein.                                    *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  | LED | |     |        |                                           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  | Nano| |     |        |  Wenn alles gut geht, dann wird           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  hier eine Erfolgsmeldung angezeigt       *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |                                           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |_____| |_____| [O]    |                                           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |    [@] [@] [@]          |  Falls Probleme auftreten, dann werden    *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |__________________[:::]__|  die Fehler hier aufgelistet              *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*                                                                         *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")
        elif arduino_type=="DCC":
            self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*             Zum                                                         *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*              PC           Prog_Generator " + PROG_VERSION+ " by Harold    *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*              \\\\                                                         *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*               \\\\                                                        *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*    ____________\\\\____________                                           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  | [_] | | [_] |[oo]    |  Achtung: Es muss der RECHTE              *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  Arduino mit dem PC verbunden             *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  sein.                                    *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | | DCC |        |                                           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | | Nano|        |  Wenn alles gut geht, dann wird           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |  hier eine Erfolgsmeldung angezeigt       *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |     | |     |        |                                           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |  |_____| |_____| [O]    |                                           *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |    [@] [@] [@]          |  Falls Probleme auftreten, dann werden    *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*   |__________________[:::]__|  die Fehler hier aufgelistet              *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("*                                                                         *\n")
            self.arduinoMonitorPage.add_text_to_textwindow("***************************************************************************\n")                
        else:
            pass
        
        self.controller.showFramebyName("ARDUINOMonitorPage")
        start_with_realtime_logging = True
        use_start_cmd = False
        if use_start_cmd:
            filedir = os.path.dirname(os.path.realpath(__file__))
            h_filedir1 = os.path.dirname(filedir)
            h_filedir = os.path.dirname(h_filedir1)
            filename = "Start_Arduino.cmd"
            
            os.chdir(h_filedir)
            self.startfile = filename
            os.startfile(self.startfile)
        elif start_with_realtime_logging:
            self.after(500, self.start_ARDUINO_program_Popen)
        else:
            self.after(500, self.start_ARDUINO_program_Run)
