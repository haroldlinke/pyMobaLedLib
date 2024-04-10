#!/usr/bin/env python
# $Id: setup.py,v 1.22 2004/10/03 18:53:22 kasplat Exp $
# By R.Suzi rnd@onego.ru
# Extended and expanded by Andy Todd <andy47@halfcooked.com>

WIN_DEFAULT_COMMAND = "install"
APPLICATION_NAME = "PythonCard"
from distutils.core import setup
from distutils.command.install_data import install_data
import glob, os, sys
import __version__
if len(sys.argv) == 1 and sys.platform.startswith("win"):
    sys.argv.append(WIN_DEFAULT_COMMAND)

classifiers = """\
Development Status :: 4 - Beta
Environment :: MacOS X
Environment :: MacOS X :: Carbon
Environment :: Win32 (MS Windows)
Environment :: X11 Applications :: GTK
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: End Users/Desktop
Intended Audience :: Information Technology
Intended Audience :: Other Audience
Intended Audience :: Science/Research
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
Programming Language :: Python
Topic :: Software Development
Topic :: Software Development :: User Interfaces
"""

longdescription = "PythonCard is a GUI construction kit for building cross-platform " + \
"desktop applications on Windows, Mac OS X, and Linux, using the Python language."

"""
This script is setup.py of the PythonCard package.

You need to have wxPython to run PythonCard
"""

class smart_install_data(install_data):
    def run(self):
        #need to change self.install_dir to the actual library dir
        install_cmd = self.get_finalized_command('install')
        self.install_dir = getattr(install_cmd, 'install_lib')
        return install_data.run(self) 

def recurseDir(startDir):
    # This should all be replaced by calls to os.path.walk, but later
    listX=[startDir]
    for fyle in os.listdir(startDir):
        file=os.path.join(startDir,fyle)
        if os.path.isdir(file):
            listX.extend(recurseDir(file))
    return listX

def makeDataDirs(rootDir=APPLICATION_NAME, dataDirs=['.', 'docs','samples', 'tools']):
    "Construct a list of the data directories to be included"
    # This function will return a list of tuples, each tuple being of the form;
    #  ( <target_directory_name>, [<list_of_files>] )
    listX=[]
    results=[]
    for directory in dataDirs:
        directories=recurseDir(directory)
        results.extend(directories)
    for directory in results:
        if os.path.split(directory)[1]!='CVS':
            # Add this directory and its contents to list
            files=[]
            for file in os.listdir(directory):
                if file!='CVS' and file!='.cvsignore':
                    if os.path.isfile(os.path.join(directory, file)):
                        files.append(os.path.join(directory, file))
            listX.append((rootDir+'/'+directory, files))
    # list.append((rootDir, 'stc_styles.cfg'))
        
    return listX

setup(name=APPLICATION_NAME, 
      version=__version__.VERSION_STRING,
      description="PythonCard GUI-builder",
      author="PythonCard Developers",
      author_email="pythoncard-users@lists.sourceforge.net",
      url="http://pythoncard.sourceforge.net/",
      download_url="http://sourceforge.net/project/showfiles.php?group_id=19015",
      classifiers = filter(None, classifiers.split("\n")),
      long_description = longdescription,
      platforms = "Mac OS X, Windows, Linux",
      packages=[APPLICATION_NAME, APPLICATION_NAME + ".components", APPLICATION_NAME + ".templates", APPLICATION_NAME + ".templates.dialogs"],
      package_dir={APPLICATION_NAME: '.'},
      scripts=["install-pythoncard.py"],
      license="BSD",
      cmdclass = { 'install_data': smart_install_data},
      data_files=makeDataDirs(),
     )

# End of setup.py
