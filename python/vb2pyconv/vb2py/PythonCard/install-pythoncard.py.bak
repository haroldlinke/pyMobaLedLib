
"""
__version__ = "$Revision: 1.9 $"
__date__ = "$Date: 2006/01/13 22:01:29 $"
"""

# THIS FILE IS ONLY FOR USE WITH MS WINDOWS
# It is run as parts of the bdist_wininst installer
# Be sure to build the installer with
# 'python setup.py --install-script=install-pythoncard.py'
# or insert this into setup.cfg:
# [bdist_wininst]
# install-script=install-pythoncard.py

import sys, os
from distutils.sysconfig import get_python_lib

if not sys.platform.startswith('win'):
    sys.exit()

try:
    prg = get_special_folder_path("CSIDL_COMMON_PROGRAMS")
except OSError:
    try:
        prg = get_special_folder_path("CSIDL_PROGRAMS")
    except OSError, reason:
        # give up - cannot install shortcuts
        print "cannot install shortcuts: %s" % reason
        sys.exit()

lib_dir = get_python_lib(plat_specific=1)

dest_dir = os.path.join(prg, "PythonCard")

pythonw = os.path.join(sys.prefix, "pythonw.exe")

if __name__ == '__main__':
    if "-install" == sys.argv[1]:

        try:
            os.mkdir(dest_dir)
            directory_created(dest_dir)
        except OSError:
            pass

        # create_shortcut(target, description, filename[, arguments[, \
        #                 workdir[, iconpath[, iconindex]]]])
        
        # file_created(path)
        #  - register 'path' so that the uninstaller removes it
        
        # directory_created(path)
        #  - register 'path' so that the uninstaller removes it
        
        # get_special_folder_location(csidl_string)

        target = os.path.join(lib_dir,
                              "PythonCard\\samples\\samples.pyw")
        path = os.path.join(dest_dir, "Sample Launcher.lnk")

        create_shortcut(target, "Sample Launcher", path)
        file_created(path)


        path = os.path.join(dest_dir, "Layout Editor.lnk")
        arguments = os.path.join(lib_dir,
             "PythonCard\\tools\\resourceEditor\\layoutEditor.py")
        create_shortcut(pythonw, "Layout Editor", path, arguments)
        file_created(path)

        path = os.path.join(dest_dir, "Resource Editor.lnk")
        arguments = os.path.join(lib_dir,
             "PythonCard\\tools\\resourceEditor\\resourceEditor.py")
        create_shortcut(pythonw, "Resource Editor", path, arguments)
        file_created(path)


        path = os.path.join(dest_dir, "Code Editor.lnk")
        arguments = os.path.join(lib_dir,
             "PythonCard\\tools\\codeEditor\\codeEditor.py")

        create_shortcut(pythonw, "Code Editor", path, arguments)
        file_created(path)

        path = os.path.join(dest_dir, "Tabbed Code Editor.lnk")
        arguments = os.path.join(lib_dir,
             "PythonCard\\tools\\oneEditor\\tabcodeEditor.py")

        create_shortcut(pythonw, "Tabbed Code Editor", path, arguments)
        file_created(path)


        path = os.path.join(dest_dir, "Find Files.lnk")
        arguments = os.path.join(lib_dir,
             "PythonCard\\tools\\findfiles\\findfiles.py")

        create_shortcut(pythonw, "Find Files", path, arguments)
        file_created(path)


        target = os.path.join(lib_dir,
                              "PythonCard\\docs\\html\\index.html")
        path = os.path.join(dest_dir, "Documentation.lnk")

        create_shortcut(target, "Documentation", path)
        file_created(path)


        target = os.path.join(sys.prefix, "RemovePythonCard.exe")
        path = os.path.join(dest_dir, "Uninstall PythonCard.lnk")
        arguments = "-u " + os.path.join(sys.prefix,
                                         "PythonCard-wininst.log")

        create_shortcut(target, "Uninstall PythonCard",
                        path, arguments)
        file_created(path)

        print "See the shortcuts installed in the PythonCard Programs Group"

    elif "-remove" == sys.argv[1]:
        pass
