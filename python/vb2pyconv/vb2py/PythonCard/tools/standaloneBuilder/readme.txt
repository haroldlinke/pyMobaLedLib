standaloneBuilder tool version 0.2.0

This version of standaloneBuilder ought to be quite stable and usable in
most circumstances. There are still some limitations:

1. The MacOS platform is not currently supported. As I don't own a Mac, this
   will have to be addressed by someone else!

2. You can only create projects in subdirectories of the main projects
   directory specified in your preferences. This is annoying, and will be
   fixed in the next release.
   
3. The online manual feature has not yet been implemented.

4. The program is not able to manage non-PythonCard projects.

5. The build mechanism is still relatively simple-minded - a number of the
   more advanced features of pyInstaller and py2exe are not fully
   supported.
   
6. At the time of writing (May 2006) the current stable version of pyInstaller
   is version 1.1 - this version has a bug which leads to executables being
   corrupted when a Win32 Icon resource is inserted into the .EXE file. This
   means it will be necessary to install the unstable development snapshot of
   pyInstaller until such time as version 1.2 is released.
   
7. The program does not work too well when trying to use external programs
   other than the regular PythonCard tools, i.e. code editor and resource 
   editor.

Please refer to the changelog.txt file for a full list of changes made in this
release. Feedback or bug reports can be sent to the PythonCard users mailing
list, https://lists.sourceforge.net/lists/listinfo/pythoncard-users

Useful links:

PythonCard main website: http://pythoncard.sourceforge.net/

pyInstaller website: http://pyinstaller.hpcf.upr.edu/cgi-bin/trac.cgi

py2exe website: http://www.py2exe.org/

Inno Setup website: http://www.jrsoftware.org/isinfo.php


