
import os, sys
import bundlebuilder

# I set this to make adding subfolders into the package easier
# KEA 2004-07-22
# rather than hard-coding the path
# we'll just get the path from this module
##packageroot = "/Users/kevino/oss/eclass/eclass_builder"
packageroot = os.path.abspath(os.path.dirname(__file__))
# for the purposes of building the standalone
# change to the directory the build script is in to simplify imports
os.chdir(packageroot)

# Create the AppBuilder
myapp = bundlebuilder.AppBuilder(verbosity=1)

# Tell it where to find the main script - the one that loads on startup
myapp.mainprogram = os.path.join(packageroot, "findfiles.py")

myapp.standalone = 1
myapp.name = "FindFiles"

# includePackages forces certain packages to be added to the app bundle
##myapp.includePackages.append("encodings")
##myapp.includePackages.append("_xmlplus")

# KEA 2004-07-22
# force imports for components used in .rsrc.py file
#from PythonCard.components import button, checkbox, combobox, list, statictext, textfield

# Here you add supporting files and/or folders to your bundle
##myapp.resources.append(os.path.join(packageroot, "about"))
##myapp.resources.append(os.path.join(packageroot, "autorun"))
##myapp.resources.append(os.path.join(packageroot, "Graphics"))
myapp.resources.append(os.path.join(packageroot, "findfiles.rsrc.py"))

# bundlebuilder does not yet have the capability to detect what shared libraries
# are needed by your app - so in this case I am adding the wxPython libs manually
myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.dylib")
myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.rsrc")
myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_stc-2.5.2.dylib")

# Here we build the app!
myapp.setup()
myapp.build()
