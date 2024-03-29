from vb2py.vbfunctions import *
from vb2py.vbdebug import *

""" Revision History:
 ~~~~~~~~~~~~~~~~~
 23.10.18: - Incremented FixedBytes to 11 per macro Update_All_FixedBytes
 24.10.18: - Checking the number of channels (Max: 765)
           - Checking the Flash Usage (Max 2000)
 02.05.19: - Started saving and loading example sheets
 07.05.19: - Started the graphical display of the LED states
 14.05.19: - Goto grafik finished
 15.05.19: - Added menue to save, load, delete sheets
 20.05.19: - Corrected the Trend Grafic if 8 bits per value are used. Here "Wert Min/Max" are not used.
           - Text constants could be used in the LED table if 8 bits per value are used
 21.05.19: - Moved the LED table to the right to be able to change the column width of the LED columns
 22.05.19: - Adapt the column with to the duartion if "D" is added to the "Grafische Anzeige" field
 03.06.19: - Corrected "Set_LED_Val_8_Bit()" in case of empty cells
 07.06.19: => Ver. 0.7.6
           - Using the directory "Eigene Dokumente\MyPattern_Config_Examples" to store the files
 19.06.19: - Support for Englisch added. Most of the Outputs are automatically shown in Englisch or German
             depending of the Language settings in Excel and Windows.
 24.06.19: - Still some messages which are not adapted to the language. They are marked with "ToDo: Language"
 25.06.19: => Ver. 0.7.6
           - Message that the columns with is limmited is cleared if no longer valid
 26.06.19: - Translated some missing messages
 27.06.19: - Finished the Example description
 29.06.19: => Ver. 0.77
           - Adapted to the different the decimal separators (Error loading Examples if german "," was used)
 02.07.19: - Corrected the loading of pictures if a comma is used as decimal separator (German)
             Checked all other lines in the MLL_pcf file for decimal points (LED_Attr, msoTextBox, msoPicture)
 15.09.19: - Incremented the number of Duration entries from 20 to 30.
           - Changed 'InNr' to 'InCh' in the geneated macro
 19.10.19: - Corrected the loading of "Bold" the attribute in "Load_Textbox()"
           - Save/Load buttons and ForeColor to the example file
           - Added the morse code from Lorenz
           - Support for 64 Bit office
           => Ver. 0.78
 21.10.19: - Corrected the loading of buttons if the german comma is used
           => Ver. 0.79
 29.10.19: - Corrected comment in "Ergebnis" line: '\\' => '//'
           => Ver. 0.82
 03.11.19: - Pictures are loaded in addition from the MLL_pcf directory if the don't exist in the exampled directory.
           => Ver. 0.83
 15.11.19: - Started the exchange function to the Prog_Generator
 17.11.19: - Added Parameter line "Goto Aktivierung:". Attention a lot of constants have been adapted
           - New Button "Programm Generator"
           - Added a version number to the MLL_pcf file to be able to move the position of
             grafical elements (text box, grafic, button) if an old version was loaded
           => Ver. 0.84
 22.11.19: - Add and Del columns buttons finished
           - Fixed Problem with new LastFilledColumn2() function
             - Result is ok again after loading examples
           - Adapted the MorseCode to the changed line adresses
 25.11.19: - New methode to save the pictures. Now they are saved directly from excel without the "Paint" hack
             - Pictures are always written as jpg to save disk space (Old: png)
             - Pictures are saved to the same directory as the .MLL_cfg file
             - All other pictures are hidden when the user is asked to enter the picture name.
             - Old .png files are still loaded
             - Programm tries to load the picture from the .MLL_cfg directory.
               If this fails the examples directory is used.
 28.11.19: - Import of Pattern lines from the Program_Generator is working
 02.12.19: => Ver. 0.85
           - Excel 2010 doesn't support the "IstFormel()" command ;-(
             => It's replaced by the own function "Ist_Formel()"
 07.12.19: - Copy the program to the DestDir_All directory and generate a desktop link
 31.12.19: - Improved the Get_USB_Ports() function because the "find" function didn't work on Norberts compuer for some reasons
 01.01.20: - Test mode for the Charieplexing
 07.01.20: - Programming of the Charliplexing ATTiny and the Tiny_UniProg finished
 08.01.20: - Added also the Servo prog. to the Main menu
           - Checked the "Goto Aktivierung" Modes "Counter", "RandomButton" and "RandomTime"
 09.01.20: - An "S" in the first column of the "Goto Tabelle" is ignored because in this case the first column is adressed with 0 and 1
           => Ver. 0.90
 11.01.20: - Check the duration row added
           - Corrected the row of the "Duration" entry in the Languages sheet. Has been forgotten when the
             Charliplexing was added. => The "Duration" was not saved to the MLL_pcf file ;-(
 15.01.20: - Checking the Duration column and set "PF_SLOW" if the time is > 65 Sec
             If wrong entries are detected an error message is when the pattern is send to Prog_Generator / ATTiny
 16.01.20: - Corrected refference to InStrR
           => Ver. 0.91   uploaded to GitHub Library Version V1.0.1
 18.01.20: - Added "PtrSafe" to all external function declarations in module M57_modCOMM"
           => Ver. 0.92   uploaded to GitHub
 22.01.20: - Added Dutch languages
           - Corrected the language switching
           => Ver. 0.93   uploaded to GitHub in the developper directory
 24.01.20: - Started adding the dialog translations from Misha
 31.01.20: - Hopefully finished the translation to English
           - Sending the Pattern Data to all channels of the Charliplexing module in Send_LED_PWM()
             because the R and G pins of the SMD version of the WS32811 may be wrong connected on the PCB ;-(
           => Ver. 0.94
 12.02.20: - Started functions to read/write the translations in the examples
           => Ver. 0.95
 13.02.20: - Corrected the loading of the examles. "| " was not handeled correctly
           - Skipping the wrong buttons "Update_Grafik" and "New_Sheet" when loading example files.
             This buttons habe beeen aded by mistake by an old version of the program.
 07.03.20: - Checked langauges by Misha and Christian
           - Corrected startup to prevent crash when the program is started the first time
             after a download.
           => Ver. 0.96
 18.04.20: => Ver. 0.97
           - Copied modules from Prog_Gen:
             - M12_Copy_Prog      => Icon
             - M35_Mouse_Scroll
           -> Send to Armin, Dominik, Frank, Juergen, Karl, Rolf, Michael (Link to GitHub)
 26.04.20: - Hopefully saved the MouseHook problem by storing the MouseHook to the Worksheet "Main" in the range X1
           => Ver. 0.98
 30.05.20: - Using the Sketchbook Path for the working directory
 31.05.20: - Improved the switching to the Prog_Generator. Now the minimized state is detected correctly
             Prior the window was always set to "Normal". Now this is only done if the window was minimized.
 04.06.20: - Added Mishas Testbuttons
           -> Send to Misha
           - Synchroniced the Language modules with the Prog_Generator
 05.06.20: - Using the same USB detection like the Prog_Generator
           - Ignoring the "First RGB entry" for Charlieplexing because the ATTiny could no longer be programmed
             if "First RGB entry" is set to an other value than 0 ;-(
             In this case the EEPROM had to be cleared by setting "EEPROM not retained" in the Arduino IDE and
             writing the bootloader.
           - Hiding the debug messages when compiling & uploading
             - the Tiny_UniProg program
             - the ATTiny Servo program
             - the Charliepleying program
           - Checking if the Arduino could be programmed and is not blocked by an other programm in Compile_and_Upload
             This is used for programming the TinyUniProg, Servo and Charliplexing
             - Printing message at the end of the programming
           => Ver. 0.99b
              Uploaded to Github Beta
 07.06.20: - Corrected the detection of the data sheet in Delete_Shapes()
           - Translated some missing lines
           - Added the link to the Wiki in the Macros sheet
           => Ver. 0.99d
           -> Send to Misha
 09.06.20: - Splitted the examples in several groups which could be loaded separately
           - Using also the background color to define a RGB LED group for thr LED simulation from Misha
           - Added Mishas changes from 10.06.20
           => Ver. 0.99e
           -> Send to Misha
 13.06.20: - New check box "RGB LED" in the data sheets which is used instead of the "same names" or "same color" method
             - Adapted all examples
           - Corrected some wrong languages in the dialogs (Dutch and english instead of german)
 14.06.20: => Ver. 1.9.4
              Uploaded to Github Beta
           - Corrected crash when loading all examples
           - Copy also the Prog_Generator an create link
 15.06.20: - Don't clear the background of the LED Number row when the LED animation is shown in the Multiplexer sheet
 23.06.20: - Corrected language and translation problems
 30.06.20: => Uploaded to Github
 07.07.20: - Corrected "Unic_SheetName()" because it generates an endless loop with "KS_Hauptsignal_Zs3_Zs 6_Zs1_RGB"
 12.07.20: - Highlighting and centering the picture when asking for a picture name when saving a sheet
 14.07.20: - The new button "Insert Picture" from Misha is always visible because it's good if pictures are
             always iserted in this way. In this case the picture is automatically named and copied to the
             examples dir if not already there.
 15.07.20: => Ver. 1.9.5
              Uploaded to Github for Misha
 20.07.20: => Ver. 1.9.6
           - Changed the destination directory to "\MobaLedLib\Ver_..." to be able to set one
             exclusion in the virus scan program for all versions
 24.07.20: - Corrected the final fuse setting. Unfortunately the Flash has been erased in this step
             => The Servo program didn't exist at the end ;-(
 25.07.20: - Ask the user if the Servo pins shold be corrected (WS2811 SMD and platine Ver. 1.0)
 27.07.20: - Corrected problems with german decimal separator in "Load_msoShapeOval()"
 04.08.20: - Adapted the Sevo build process to use 16MHz CPU frequency
           => Ver. 1.9.6 D  Uploaded to Github Beta
 07.08.20: - Improved the ATTiny program
           - Improved the Servo and the Charlieplexing programming
           => Ver. 1.9.6 E  Uploaded to Github Beta
 15.10.20: - Extracted the compiler call in "Compile_and_Upload_to_ATTiny85.cmd"
             into "Compile_and_Upload_to_ATTiny85_Sub.cmd"
             to be able to check the error code. Prior the Find command has overwritten
             the result => Errors have not been detected ;-(
             This has been changed in the Servo and the Charlieplexing directory
 16.10.20: - Increased the number of Time entries from 30 to 64 and corrected the entries 24-30
           - New Charliplexing software which supports the 64 time channels
           => Ver. 1.9.6 K  Uploaded to Github Beta
 18.10.20: => Ver. 2.0.0 Uploaded to Github Beta
 27.10.20: - Disabling the Event which is called when Enter is pressed when the workbook is colosed
             Hopefully this solves the problem that the Pattern_Config is opened sometimes unintentionally
           => Ver. 2.0.0 B Uploaded to Github Beta
 01.11.20: - Corrected the support for 64 time entries. Unfortunately the prior changes have been made in
             the wrong worksheet and not in the Main sheet => They have been lost when the release
             version was build ;-(
 02.11.20:
           => Ver. 2.1.0 Uploaded to Github Beta
 02.12.20:
           => Ver. 2.1.2 Uploaded to Github Beta
 19.01.21: - Added the Signals_3D examples to the dialog
           - Jürgen corrected the translation macro
           => Ver. 2.1.3 Uploaded to Github Beta
 10.02.21: - Added Mishas changes
           => Ver. 2.1.3 E Uploaded to Github Beta
 20.03.21: - Fix problem with nonprintables in %userprofile% when uploading special modules
           => Ver. 2.1.3 K
 10.04.21: - Juergen: adapt ATTIny configuration download to new FarbTest protocol
           => Ver. 2.1.3 M
 21.04.21: - deploy Release 3.0.0
 23.04.21: ubit: Added ATTiny Program 03.ATTiny85_Sound for ServoMP3 serial programming of sound modules
 07.10.21: - Corrected the spelling of PM_SEQUENCE_W_RESTART => PM_SEQUENZ_W_RESTART in the Languages sheet (Hint from Theo)
             In addition the correct english spelling has been added to the MobaLedLib.h to be able to
             use both ways
 15.11.21: - Juergen: fix issue #6938
 21.11.21: - Juergen: Add Excel version check
 28.11.21: - change release to 3.1.0
           - publish release
 05.01.22: - Juergen: fix problem 'hang while load examples' #7425, #7428

 ToDo:
 ~~~~~
 - Aus irgend einem Grund wird die "Private Sub Workbook_Open()" funktion gerade nicht mehr
   aufgerufen ?!?
   Im Internet habe ich nichts brauchbares gefunden. Es gib Leute die den selben Fehler haben,
   aber es ist keine vernünftige Lösung zu finden.
   Immer wenn ich es ein paar mal probiert habe, dann geht es irgend wann wieder ?!?
   Vielleicht merkt sich Excel wenn ich das Laden der Beispiele abbreche und startet datum die Funktion
   Beim nächsten mal nicht mehr. Erst wenn ich wieder was am Programm ändere vergisst es das??
   Das ist mir schon mal aufgefallen. Das führt auch zu dem Folgenden Problem:
   - Manchmal funktioniert das laden der Beispiele und das kopieren in das User Verzeichniss nicht.
     Evtl. passiert das dann wenn ein anderes Excel Sheet offen ist.
 - Heute (10.04.20) ist das Progaram beim update der Sprache auf der letzten Seite abgestürtzt in der Function "Load_Textbox()".
   weil das Sheet "Charlie_But_Bin" geschützt war obwohl in der Routine vorher in "Translate_Standard_Description_Box()"
   ActiveSheet.Unprotect aufgerufen wurde.
   Als ich dann den Blatschutz deaktiviert habe und das Programm fortgesetzt habe ist die Standard Beschreibung über die
   Spezielle Beschreibung kopiert worden.
   Der Fehler ist bei jeden Start des Programmes aufgetreten. Als ich das Programm dann neu gespeichert habe ist
   das Problem verschwunden ?!? Aber dann wurde auch "Workbook_Open()" nicht gestartet ;-(
   Wenn ich jetzt "Update_Language_in_All_Pattern_Config_Sheets()" von Hand Starte geht es.
   - Dann habe ich die Addins "Charttools" und "Team Foundation Add-in" deaktiviert => Immer noch kein "Workbook_Open()"
   - Auch nach eienm Windows Neustart kein "Workbook_Open()"
   - Nachdem ich die Beispiele gelöscht geht es wieder ? Die Datei ist jetzt nur noch 6.58MB anstelle von 7.33MB?
   - Dann habe ich die Fehlerhafte Datei umbenannt in Pattern_Configurator_Autostart_geht_nicht_mehr.xlsm gestartet
     und jetzt wurden nach den Sicherheitsabfragen "Datei aus dem Internett..." die "Workbook_Open()" Funktion wieder gestartet.
     Aber nach dem ich die neue Datei in ..._Neu umbenannt hatte und das "_Autostart_geht_nicht_mehr" entfernt hatte
     und wieder zurück umbenannt hatt egeht das "Workbook_Open()" schon wieder nicht in der neuen Datei.
 - Icons einbinden
 - Zum Arduino schicken wie im Prog_Generaror
 - Manchmal wird Workbook_Open() nicht gestartet ?!?
 - EWMA Bibliothek für Charlieplexing
   => Wird in "02.CharlieplexTiny\Compile_and_Upload_to_ATTiny85.cmd"
      installiert => Gerald fragen
 - Sprachen:
   - Sheet: Special_Mode_Dlg und Par_Description
   - Beschriftung der Buttons: "Zum Modul schicken", ...
   - Beschriftung der Tabs im Main Menu "Beispiele", ...
   - Hotkeys der Buttons anpassen
 - Wenn Alle Seiten gelöscht werden, dann zuckt die Überschrift des VB Editors ;-(
   Läuft da noch was im Hintergrund ?
 - Die "Ist_Formel()" Funktion soll nur bei älterem Excel verwendet werden.
   Ich habe aber nicht herausgefunfen wie man per #if prüft ob Excel <= 2010 verwendet wird
 - Bilder sollen "Nur von Cellposition abhängig" sein damit sie mit verschoben werden wenn man
   - die Spaltenbreite verändert (Grafische Anzeige "D")
   - Den Goto oder Spezial Mode einschaltet
 - Goto Aktivierung:
   - Dialog soll so aktiviert werden wie bei der "RGB Modul Nummer"
     => Weiß nicht was besser ist. Die "Goto Aktivierung muss zwingend ausgefüllt werden.
        Darum ist es o.K. wenn der Dialog immer kommt
 - Zwei Eingänge in Counter Funktion für Up/Down oder enable
 - ArduinoISP2 untersuchen: https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/master/ArduinoISP
   Quarz pin Simmulation https://www.kollino.de/arduino/yikes-invalid-device-signature-da-brennen-mir-die-sicherungen-durch/
   Die Clock Leitung wird anscheinend schon vom Tiny_UniProg Programm im HV Reset Modus unterstützt. Zuminsest ist der
   Pin 2 des ATTiny angeschlossen.
 - Ich bin mir nicht sicher ob die "Global_On_Enter_Proc" für Stabilitätsprobleme sorgt
   Es scheint so als würde die Kiste jetzt öfters abstürtzen.
   Evtl. macht sie das Programm auch deutlich langsamer
   Man könnte die Dialoge auch NUR über einen Doppelklick und die Eingabe von "?" aufrufen.
 - Wie soll die Eingabe von Feldern gemacht werden in denen ein Dialog verwendet wird
   Es soll möglichst komfotabel sein.
   - Wenn man weiß was eingegeben werden muss, dann nerft der Dialog
   - Wenn ein Text erwartet wird, dann soll das Programm den Eingegebenen Test auswerten und entsprechend erweietrn
     "c" => Charliplexing, "A" => An/Aus
   - Das sollte Einheitlich sein
   Ich habe verschiedene Varianten implementiert:
   - Doppelklick mit der Maus: Prog_Generator/Makro Spalte
   - Automatisch öffen wenn der Cursor darin steht: Goto Aktivierung, Prog_Generator/Eingabe Typ
   - Enter oder ? Enter: RGB Modul Nummer

 - Zeitangaben wie "1 Min + 15.3 Sec" in Get_Duration() bearbeiten (Siehe Test_PWM_Data_send.xlsm)
 - "PatternTE" unterstützen in Decode_Pattern_String(). Nicht so wichtig weil "PatternTE" momentan (?)
   nicht vom Pattern_Configurator erzeugt wird (Untersuchen).
 - Neue Texte übersetzen und in Languages eintragen
 - Man könnte eine Zusätzliche Kommentar Zeile einbauen welche dann anstelle das Makro Names an
   den Prog_Generator übertragen wird
 - Überprüfung der GotoAction in "Check_Table_before_Copy()" einbauen bevor Makro zum
   Prog_Gernerator geschickt wird.
   Die Anzahl der Goto Ziele muss <= der möglichen Ausgänge der GotoAct Funktion sein
   Problem: Die "InCh_to_TmpVar()" Funktion unterstützt nur 8 Eingänge.
   Die Überprüfung ist bereits in den Auswahldialog eingebaut. Aber die Anzahl der Start
   Punkte kann sich verändert haben.
 - Wenn der HSV Mode verwendet wird, dann Hinweis geben oder Fragen ob New_HSV_Group() verwendet werden soll.
 - Die KS Signale sind unterschiedlich skalliert. Es sieht so aus als würde in Ronnys original die selbe Signaldatei auf
   verschiedenen Seiten mit unterschiedlichen skallierungen verwende.
   => Untersuchen. Evtl. muss der Skalierungsfaktor mit in der Datei abgelegt werden.
 - Kann es sein, dass "Last_LEDsCol" an einigen stellen zu groß ist? Die Dauer Tabelle kann maximal 30 Einträge fassen
 - Angaben in Prozent und nicht als Zahl in der Tabelle und bei "Wert Min" und "Wert Max" Vorschlag von Mark: (Mail 10.11.19)
   => Das ist nicht so einfach weil
      - Bei manchen Mustern die Zahlen beibehalten werden sollten (z.B. bei LocalVar Sound)
      - Sollen "Wert Min/Max" auch in Prozent angegeben werden?
      - Bei einer änderung von "Wert Min/Max" müssten die Prozente verändert werden oder sollen
        sich die Angaben Min und Max nicht berücksichigen.
      - Die Zahlen an verschiedenen Stellen benutzt werden
        - Erzeugen der Bytes: CalculatePattern()
        - Analog Trend Linie: Get_Avg_LED_Val()
        Beide Stellen benutzen Get_LED_Val(). Bei der Grafik muss allerdings noch der
        Offset wegen "Wert Min" berücksichtigt werden
      - Mit Range.NumberFormat kann man prüfen ob die Zahl als Prozent formatiert ist:
          instr(Range.NumberFormat, "%") > 0 and instr(Range.NumberFormat, """") = 0
        Private Sub Test_Get_Format()
          If InStr(ActiveCell.NumberFormat, "%") > 0 And InStr(ActiveCell.NumberFormat, """") = 0 Then
             Debug.Print "Ist Prozent:" & ActiveCell.Value
          End If
          Debug.Print ActiveCell.NumberFormat
        End Sub
 - Auswahl der Farbe über Dialog (Vorschlag von Mark: (Mail 10.11.19))
"""


