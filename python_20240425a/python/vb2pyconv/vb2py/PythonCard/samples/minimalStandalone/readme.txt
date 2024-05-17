minimalStandalone is a copy of the minimal sample with the import line
already uncommented and the necessary scripts for building a standalone
version of the minimal sample with py2exe and Gordon McMillan's installer
supplied. It also contains a French version of the resource file.

minimal is about  the smallest PythonCard program possible. Refer to
walkthrough1.html in the PythonCard documentation directory for an
example of copying and modifying minimal.py as your first PythonCard
program.

When you create standalone executable versions of a PythonCard
application using either py2exe or Gordon McMillan's Installer, you end up
with a folder with multiple files, incuding an exe file whose name is identical
to the main Python script  name you supply as the primary source file. To
distribute your application, you must supply the user with all of the contents
of the folder indicated in the directions below. Note that Installer 
creates two
temporary folders called "build" and "buildminimal" that you need *not*
distribute.


py2exe
======

You can build a standalone Windows executable using py2exe,
available at:
  http://py2exe.sourceforge.net/

Use the following command-line to build the minimal.exe file.
   python setup.py py2exe --excludes=Image

The results ofthe build are placed in the
minimalStandAlone\dist\minimal directory.

The --windows or -w option should be used to build a windows application, 
similar to running the script with pythonw.exe or using a .pyw extension.
See the py2exe page for other options.


Gordon McMillan's Installer
===========================

You can also build a standalone Windows or Linux executable using
Gordon McMillan's Installer, available at 
  http://www.mcmillan-inc.com/install1.html.

Place Installer in its own folder in your Python directory's lib/site-packages
directory.

Use the following comand-line to build the minimal standalone with Installer:

python Build.py minimal.spec

The results of the build are placed in the minimalStandAlone\distminimal
directory.


Mac OS X bundlebuilder.py
=========================

You can build a standalone on Mac OS X using the macbuild.py script.

Use the following comand-line to build the minimal standalone with Installer:

/usr/local/bin/python macbuild.py

For more information, see the mailing list post I made in July 2003:

  http://aspn.activestate.com/ASPN/Mail/Message/1746353


International and localization issues
=====================================

The minimal.fr.rsrc.py file is the French version of minimal.rsrc.py. If
the locale setting on the users machine indicates French (fr) as the
language, that resource will automatically be used.
