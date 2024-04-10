Python Source Code Editor

The codeEditor sample in PythonCard is focused on being a simple to use Python source code editor. It is not intended to be a generic editor or replace vi(m), Emacs, etc. If you are already happy with your existing editing environment for Python source code, there is no particular reason you have to switch. codeEditor and the resourceEditor and shell will be more tightly integrated as the project progresses so that the user has a simple Integrated Development Environment (IDE) for building desktop applications without needing to use an external program for editing.

Based on textEditor sample, but using wxStyledTextCtrl (wxSTC)

For more information, see:

PythonCard Editor (codeEditor) wiki page
http://wiki.wxpython.org/index.cgi/PythonCardEditor

wxStyledTextCtrl documentation
http://wiki.wxpython.org/index.cgi/wxStyledTextCtrl

If you use this sample as a real text editor then you should be careful to always work on backup copies of documents in case there are bugs that might corrupt your text.

You can change the style used to display the source code; the style is also used by the PythonCard shell.

The last position and size of the window will be saved in a user.config.txt file.

The About dialog displays the current filename, character, word, and line count.

Scriptlets
See the following message in the archive for more info.
http://aspn.activestate.com/ASPN/Mail/Message/PythonCard/1181106



Associating Python files with codeEditor on Windows

These instructions are for Windows 2000. They may be slightly different on other versions of Windows.

1. Open the Explorer and choose "Folder Options..." under the "Tools" menu
2. Click on the "File Types" tab
3. Scroll down in the "Registered file types" list and select extension "PY  Python File"
4. Click on the "Advanced" button
4a. You should be looking at an "Edit File Type" dialog with a list of Actions such as Edit and Open. Open is probably in bold since it is the default action usually associated with .py files.
5. Click on the "New..." button
5a. You should be looking at a "New Action" dialog
6. In the "Action:" field type in a label such as "Edit with PythonCard". This is the label that will show up in the context menu when you right-click on a .py file in the Explorer
7. in the "Application used to perform action:" field you need to specify the path to the Python executable as well as the location of the codeEditor.py file. On a Python 2.3.3 installation using the default installer this will look like:

C:\Python23\pythonw.exe C:\Python23\Lib\site-packages\PythonCard\tools\codeEditor\codeEditor.py "%1"

Substitute your own paths for the ones above and put quotes (") around the paths with spaces in them, if any. If you want a console when codeEditor.py runs, then use python.exe instead of pythonw.exe

8. Click "OK"
8a. You should now have an "Edit with PythonCard" item in your "Edit File Type" dialog
8b. The item in bold is the default action; Open will be the default if nothing is showing up in bold. Whether you want to "Edit with PythonCard" or "Open" (run) a script when you double-click a file in the Explorer is of course a personal preference. If you want "Edit with PythonCard" as the default action, then select "Edit with PythonCard" in the list, and click the "Set Default" button.
9. Click "OK"
10. Click "Close" in the "Folder Options" dialog
11. Open a directory in the explorer that contains a .py file, then right-click on the file and choose "Edit with PythonCard" and the file should be opened with codeEditor.py
11a. If it doesn't work, double-check the steps above
12. Repeat the process for .pyw files, using the same name and path.
