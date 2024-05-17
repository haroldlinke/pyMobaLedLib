import bundlebuilder
import os

# I set this to make adding subfolders into the package easier
# KEA 2004-07-22
# rather than hard-coding the path
# we'll just get the path from this module
##packageroot = "/Users/kevino/oss/eclass/eclass_builder"
packageroot = os.path.abspath(os.path.dirname(__file__))
# for the purposes of building the standalone
# change to the directory the build script is in to simplify imports
os.chdir(packageroot)

myapp = bundlebuilder.AppBuilder(verbosity=1)
myapp.mainprogram = os.path.join(packageroot, "minimal.py")
myapp.standalone = 1
myapp.name = "Minimal"

# minimal.rsrc.py is read in at runtime, but
# not using import, so can it just be placed
# in the directory of the standalone?
myapp.resources.append(os.path.join(packageroot, "minimal.rsrc.py"))

myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.dylib")
myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd-2.5.2.rsrc")
myapp.libs.append("/usr/local/lib/wxPython-2.5.2.8/lib/libwx_macd_stc-2.5.2.dylib")

myapp.setup()
myapp.build()