#!/usr/bin/python
# vim: ai et sw=4 ts=4
#
# This file contains all the custom dialogs (each based on CustomDialog) used
# by standaloneBuilder
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright (C)2003 Phil Edwards, phil@linux2000.com
# vim: ts=4 sw=4 ai et

# standard Python imports
import os
import sys
import time
import string
from md5 import md5
import copy

# PythonCard & wxPython imports
from PythonCard import dialog, resource, graphic, model
from PythonCard.model import CustomDialog
import wx
from wx.lib import dialogs


def dirSize(start, follow_links, my_depth, max_depth):
    # work out how much space a directory is taking up, another handy one from the
    # ASPN website, http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/86554
    total = 0L

    try:
        dir_list = os.listdir(start)
    except:
        if os.path.isdir(start): print 'Cannot list directory %s' % start
        return 0

    for item in dir_list:
        path = '%s/%s' % (start, item)
        try:
            stats = os.stat(path)
        except:
            print 'Cannot stat %s' % path
            continue
        total += stats[6]
        if os.path.isdir(path) and (follow_links or (not follow_links and not os.path.islink(path))):
                bytes = dirSize(path, follow_links, my_depth + 1, max_depth)
                total += bytes

    return total

def wrap_string(str, max, para = "\n\n"):
    paras = string.split(str, para)
    outStr = ""

    for paragraph in paras:
        paragraph = paragraph.replace("\n", " ")
        words = string.split(paragraph)
        outLine = ""
        lineCount = wordCount = 0

        for i in range(len(words)):
            if (len(outLine) + len(words[i])) > max:
                if lineCount:
                    outStr += "\n"
                outStr += outLine
                outLine = words[i]
                lineCount += 1
                wordCount = 1
            else:
                if wordCount:
                    outLine += " "
                outLine +=  words[i]
                wordCount += 1

        if lineCount:
            outStr += "\n"
        outStr += outLine
        outStr += para

    return outStr
    
# supplemental function used when doing a recursive import
def walkTree(arg, dirname, names):
    for item in names:
        file, ext = os.path.splitext(item)
        if ext.lower() == '.jpg' or ext.lower() == '.jpeg' and file[:1] != '.':
            arg.append(os.path.join(dirname,item))
            
class versionDialog(CustomDialog):
    """Displays a dialog for the next release version number"""

    def __init__(self, aBg, currentVersion):
        path = os.path.join(aBg.application.applicationDirectory, 'versionDialog')
        aDialogRsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        self.parent = aBg
        
        vstring = string.split(currentVersion, '.')
        self.components.majorVersion.value = int(vstring[0])
        self.components.minorVersion.value = int(vstring[1])
        self.components.fixLevel.value = int(vstring[2]) + 1
        
    def getVersion(self):
        vstring = []
        vstring.append(str(self.components.majorVersion.value))
        vstring.append(str(self.components.minorVersion.value))
        vstring.append(str(self.components.fixLevel.value))
        return vstring

    def on_btnOK_mouseClick(self, event):
        event.Skip()

    def on_btnCancel_mouseClick(self, event):
        event.Skip()

class HTMLHelp(CustomDialog):
    """Displays an HTML based about box"""

    def __init__(self, aBg, links=None):
        path = os.path.join(aBg.application.applicationDirectory, 'helpAbout')
        aDialogRsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        self.parent = aBg
        #self.components.versionText.text = 'Version %s' % self.parent.pimpversion

        # links is a 3-element list giving the HTML files to use for the About, Author
        # and License buttons
        if links is None: links = ['doc/about.html', 'doc/author.html', 'doc/license.html']
        self.links = links

        self.components.HtmlWindow.text = self.links[0]

    def on_btnOK_mouseClick(self, event):
        event.Skip()

    def on_AboutBtn_mouseClick(self, event):
        self.components.HtmlWindow.text = self.links[0]

    def on_AuthorBtn_mouseClick(self, event):
        self.components.HtmlWindow.text = self.links[1]

    def on_LicenseBtn_mouseClick(self, event):
        self.components.HtmlWindow.text = self.links[2]

class newProjectWizard(CustomDialog):
    """Displays a wizard for creating a new project"""

    def __init__(self, aBg):
        baseResourceName = 'newProjectWizard'
        path = os.path.join(aBg.application.applicationDirectory, baseResourceName)
        aDialogRsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        
        self.parent = aBg
        
        self.addWizardPage(baseResourceName, 'Page1')
        self.addWizardPage(baseResourceName, 'Page2')
        self.addWizardPage(baseResourceName, 'Page3')
        self.addWizardPage(baseResourceName, 'Page4')
        self.maxPages = 4
        
        self.pgCnt = 0
        self.accepted = False
        self.setPage(self.pgCnt)
        
    def addWizardPage(self, basename, pageref):
        r = basename + pageref
        resName = model.internationalResourceName(r)
        fd = open(resName, 'r')
        res = eval(fd.read())
        for comp in res['components']:
            if comp.has_key('userdata') and comp['userdata'] == pageref.lower():
                compname = comp['name']
                self.components[compname] = comp
        
    def setPage(self, cnt, flag=True):
        # set the currently displayed page
        groupname = 'page' + str(cnt)
        
        for compname in self.components.keys():
            if groupname in self.components[compname].userdata:
                self.components[compname].enabled = flag
                self.components[compname].visible = flag
            elif self.components[compname].userdata != '':
                self.components[compname].enabled = not(flag)
                self.components[compname].visible = not(flag)
        
        self.setButtons()
            
    def setButtons(self):
        # enable the 'next' button if we have enough information to move
        # on to the next page
        
        # back button is (almost) always enabled
        self.components.backBtn.enabled = True
        
        if self.pgCnt == 0:
            # initial page - the back button is always disabled, the next
            # button is always enabled
            self.components.nextBtn.enabled = True
            self.components.backBtn.enabled = False
            
        if self.pgCnt == 1:
            # first page - next button is enabled if we have something in the
            # project name field, back button is always enabled
            self.components.backBtn.enabled = True
            if self.components.projectName.text == '':
                self.components.nextBtn.enabled = False
            else:
                self.components.nextBtn.enabled = True
            self.components.projectName.SetFocus()
                
        if self.pgCnt == 2:
            # second page - next button is enabled if we have something in
            # the project descrption
            if self.components.projectDesc.text == '':
                self.components.nextBtn.enabled = False
            else:
                self.components.nextBtn.enabled = True
            self.components.projectDesc.SetFocus()
                
        if self.pgCnt == 3:
            # third page - next button is enabled if we have something in
            # the base directory
            if self.components.baseDir.text == '':
                self.components.nextBtn.enabled = False
            else:
                self.components.nextBtn.enabled = True
            self.components.baseDir.SetFocus()
                
        if self.pgCnt == self.maxPages:
            self.components.nextBtn.label = 'Create'
        else:
            self.components.nextBtn.label = 'Next >'
        self.components.nextBtn.SetFocus()
            
    def on_backBtn_mouseClick(self, event):
        # got to previous page
        self.pgCnt -= 1
        self.setPage(self.pgCnt)
        
    def on_nextBtn_mouseClick(self, event):
        # go to next page
        if self.pgCnt < self.maxPages:
            self.pgCnt += 1
            self.setPage(self.pgCnt)
        else:
            self.accepted = True
            self.Close()
                    
    def on_projectName_keyUp(self, event):
        # can't move on to the next page until something is typed into the
        # project name
        if self.components.projectName.text != '':
            self.components.nextBtn.enabled = True
        else:
            self.components.nextBtn.enabled = False
        event.Skip()
        
    def on_projectDesc_keyUp(self, event):
        if self.components.projectDesc.text != '':
            self.components.nextBtn.enabled = True
        else:
            self.components.nextBtn.enabled = False
        event.Skip()
        
    def on_baseDir_keyUp(self, event):
        if self.components.baseDir.text != '':
            self.components.nextBtn.enabled = True
        else:
            self.components.nextBtn.enabled = False
        event.Skip()
            
    def on_baseDirBtn_mouseClick(self, event):
        title = 'Select project base directory'
        basepath = str(self.parent.cfg.get('ConfigData', 'projects'))
        result = dialog.directoryDialog(self, title, basepath, wx.DD_NEW_DIR_BUTTON)
        if result.accepted:
            # need an error here if the directory selected is not a subdirectory
            # of basepath...
            plist = []
            plist.append(basepath)
            plist.append(str(result.path))
            if os.path.commonprefix(plist) != basepath:
                title = 'Invalid project base directory'
                txt = 'This version of standaloneBuilder does not allow creation '
                txt += 'of projects which reside outside of the projects directory '
                txt += 'specified in your preferences. This issue will be addressed '
                txt += 'in the next version. Yes, it\'s lame - sorry! :-('
                bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
                self.components.baseDir.SetFocus()
            else:
                self.components.baseDir.text = result.path
                self.components.nextBtn.enabled = True
            
    def getResult(self):
        d = dialogs.DialogResults
        d.accepted = self.accepted
        d.projectName = self.components.projectName.text
        d.projectDesc = self.components.projectDesc.text
        d.baseDir = self.components.baseDir.text
        return d
        
    def on_cancelBtn_mouseClick(self, event):
        event.Skip()
            
class prefsDialog(CustomDialog):
    """Displays a preferences dialog"""

    def __init__(self, aBg, cfgfile):
        path = os.path.join(aBg.application.applicationDirectory, 'prefsDialog')
        aDialogRsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        self.parent = aBg
        self.CONFIG_FILE = cfgfile
        #if sys.platform.startswith('win'): self.fitToComponents(10,10)
        self.components.resEditPath.text = self.parent.cfg.get('ConfigData', 'reseditor')
        self.components.srcEditPath.text = self.parent.cfg.get('ConfigData', 'codeeditor')
        self.components.txtEditPath.text = self.parent.cfg.get('ConfigData', 'texteditor')
        self.components.pixmapEditPath.text = self.parent.cfg.get('ConfigData', 'pixmapeditor')
        self.components.installerPath.text = self.parent.cfg.get('ConfigData', 'installerpath')
        self.components.buildTool.stringSelection = self.parent.cfg.get('ConfigData', 'buildtool')
        
        if self.components.buildTool.stringSelection == 'py2exe':
            self.components.installerPath.enabled = False
            self.components.installerPathBtn.enabled = False
            self.components.installerPathHelpBtn.enabled = False
        else:
            self.components.installerPath.enabled = True
            self.components.installerPathBtn.enabled = True
            self.components.installerPathHelpBtn.enabled = True
            
        self.components.compilerPath.text = self.parent.cfg.get('ConfigData', 'compilerpath')
        self.components.appPublisher.text = self.parent.cfg.get('ConfigData', 'publisher')
        self.components.projectsPath.text = self.parent.cfg.get('ConfigData', 'projects')
        
    def on_buildTool_select(self, event):
        if self.components.buildTool.stringSelection == 'py2exe':
            try:
                from distutils.core import setup as wibble
            except ImportError:
                title = '*** ERROR ***'
                txt = 'You do not appear to have a copy of the distutils '
                txt += 'package installed. This is required in order to allow '
                txt += 'building with py2exe.'
                bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
                self.components.buildTool.stringSelection = 'pyInstaller'
            else:
                try:
                    import py2exe as wibble
                except ImportError:
                    title = '*** ERROR ***'
                    txt = 'You do not appear to have a '
                    txt += 'copy of the py2exe package installed. Please install '
                    txt += 'the package and then re-configure your preferences.'
                    bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
                    self.components.buildTool.stringSelection = 'pyInstaller'
                else:
                    self.components.installerPath.text = ''
                    self.components.installerPath.enabled = False
                    self.components.installerPathBtn.enabled = False
                    self.components.installerPathHelpBtn.enabled = False
        else:
            self.components.installerPath.enabled = True
            self.components.installerPathBtn.enabled = True
            self.components.installerPathHelpBtn.enabled = True
            # see if we can find pyInstaller
            # C:\Python23\pyInstaller\Build.py
            want = os.path.join('pyInstaller', 'Build.py')
            installer = self.parent.lookFor(want)
            #self.parent.cfg.set('ConfigData', 'installerpath', installer)
            self.components.installerPath.text = installer
        
    def on_btnOK_mouseClick(self, event):
        if self.components.buildTool.stringSelection == 'pyInstaller':
            if self.components.installerPath.text == '':
                title = 'Preferences not saved!'
                txt = 'You must specify the directory where the pyInstaller components can be found'
                bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
                return
        if self.components.compilerPath.text == '' and sys.platform.startswith('win'):
            title = 'Preferences not saved!'
            txt = 'You must specify the directory where the Inno Setup compiler can be found'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            return
        if self.components.projectsPath.text == '':
            title = 'Preferences not saved!'
            txt = 'You must specify your base projects directory'
            bull = dialog.alertDialog(self, wrap_string(txt, 60), title)
            return
        self.parent.cfg.set('ConfigData', 'reseditor', self.components.resEditPath.text)
        self.parent.cfg.set('ConfigData', 'codeeditor', self.components.srcEditPath.text)
        self.parent.cfg.set('ConfigData', 'texteditor', self.components.txtEditPath.text)
        self.parent.cfg.set('ConfigData', 'pixmapeditor', self.components.pixmapEditPath.text)
        self.parent.cfg.set('ConfigData', 'installerpath', self.components.installerPath.text)
        self.parent.cfg.set('ConfigData', 'buildtool', self.components.buildTool.stringSelection)
        self.parent.cfg.set('ConfigData', 'compilerpath', self.components.compilerPath.text)
        self.parent.cfg.set('ConfigData', 'publisher', self.components.appPublisher.text)
        self.parent.cfg.set('ConfigData', 'projects', self.components.projectsPath.text)
        fd = open(self.CONFIG_FILE, 'w')
        self.parent.cfg.write(fd)
        fd.close()
        event.Skip()
        
    def on_btnCancel_mouseClick(self, event):
        event.Skip()
        
    def on_resEditPathBtn_mouseClick(self, event):
        result = dialog.fileDialog(self, self.components.StaticText3.text, self.components.resEditPath.text)
        if result.accepted:
            self.components.resEditPath.text = result.paths[0]
        
    def on_resEditPathHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.resEditPath.userdata, self.components.StaticText3.text)
        
    def on_srcEditPathBtn_mouseClick(self, event):
        result = dialog.fileDialog(self, self.components.StaticText4.text, self.components.srcEditPath.text)
        if result.accepted:
            self.components.srcEditPath.text = result.paths[0]
        
    def on_srcEditPathHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.srcEditPath.userdata, self.components.StaticText4.text)
        
    def on_pixmapEditPathBtn_mouseClick(self, event):
        result = dialog.fileDialog(self, self.components.StaticText5.text, self.components.pixmapEditPath.text)
        if result.accepted:
            self.components.pixmapEditPath.text = result.paths[0]
        
    def on_pixmapEditPathHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.pixmapEditPath.userdata, self.components.StaticText5.text)
        
    def on_installerPathBtn_mouseClick(self, event):
        result = dialog.fileDialog(self, self.components.StaticText1.text, self.components.installerPath.text)
        if result.accepted:
            self.components.installerPath.text = result.paths[0]
        
    def on_installerPathHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.installerPath.userdata, self.components.StaticText1.text)
        
    def on_buildToolHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.buildTool.userdata, self.components.StaticText1.text)
        
    def on_compilerPathBtn_mouseClick(self, event):
        result = dialog.fileDialog(self, self.components.StaticText7.text, self.components.compilerPath.text)
        if result.accepted:
            self.components.compilerPath.text = result.paths[0]
        
    def on_compilerPathHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.compilerPath.userdata, self.components.StaticText7.text)
        
    def on_appPublisherHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.appPublisher.userdata, self.components.StaticText6.text)
        
    def on_projectsPathBtn_mouseClick(self, event):
        result = dialog.directoryDialog(self, self.components.StaticText2.text, self.components.projectsPath.text)
        if result.accepted:
            self.components.projectsPath.text = result.path
        
    def on_projectsPathHelpBtn_mouseClick(self, event):
        self.showHelp(self.components.projectsPath.userdata, self.components.StaticText2.text)
        
    def showHelp(self, text, label):
        text = string.replace(text, '\\n', '\n')
        #dlg = wx.MessageDialog(self, wrap_string(text, 50), label, wx.OK|wx.ICON_INFORMATION)
        dlg = wx.MessageDialog(self, wrap_string(text, 60), label, wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
            
class propertiesDialog(CustomDialog):
    """Displays the project properties dialog"""

    def __init__(self, aBg):
        path = os.path.join(aBg.application.applicationDirectory, 'propertiesDialog')
        aDialogRsrc = resource.ResourceFile(model.internationalResourceName(path)).getResource()
        CustomDialog.__init__(self, aBg, aDialogRsrc)
        self.parent = aBg
        
        #try:
        self.components.buildPath.text = self.parent.pathJoin(self.parent.project.get('Project', 'buildfilespath'))
        self.components.distPath.text = self.parent.pathJoin(self.parent.project.get('Project', 'distfilespath'))
        self.components.pixmapsPath.text = self.parent.pathJoin(self.parent.project.get('Project', 'pixmapspath'))
        self.components.tarballPath.text = self.parent.pathJoin(self.parent.project.get('Project', 'tarballspath'))
        self.components.appPublisher.text = self.parent.project.get('Project', 'publisher')
        self.components.appURL.text = self.parent.project.get('Project', 'appurl')
        self.components.appLicence.text = self.parent.pathJoin(self.parent.project.get('Project', 'applicence'))
        self.components.asciiChk.checked = self.parent.project.getboolean('Project', 'ascii')
        self.components.striplibsChk.checked = self.parent.project.getboolean('Project', 'striplib')
        self.components.consoleChk.checked = self.parent.project.getboolean('Project', 'console') # best to have a coonsole for new projects!
        self.components.optimizeChk.checked = self.parent.project.getboolean('Project', 'optimize')
        self.components.compressChk.checked = self.parent.project.getboolean('Project', 'compress')
        self.components.debugChk.checked = self.parent.project.getboolean('Project', 'debug')
        if self.parent.project.getboolean('Project', 'onedir'):
            self.components.buildType.stringSelection = 'Single directory'
        else:
            self.components.buildType.stringSelection = 'Single file'
        #except:
        #    pass
        
    def on_buildPathBtn_mouseClick(self, event):
        basepath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        basepath = os.path.join(basepath, self.components.buildPath.text)
        refpath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        
        title = 'Select path to project build directory'
        result = dialog.directoryDialog(self, title, basepath)
        
        if result.accepted:
            path = self.parent.getRelativePath(refpath, result.path)
            self.components.buildPath.text = path
        
    def on_distPathBtn_mouseClick(self, event):
        basepath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        basepath = os.path.join(basepath, self.components.distPath.text)
        refpath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        
        title = 'Select path to project distribution directory'
        result = dialog.directoryDialog(self, title, basepath)
        
        if result.accepted:
            path = self.parent.getRelativePath(refpath, result.path)
            self.components.distPath.text = path
        
    def on_pixmapsPathBtn_mouseClick(self, event):
        basepath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        basepath = os.path.join(basepath, self.components.pixmapsPath.text)
        refpath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        
        title = 'Select path to project pixmaps directory'
        result = dialog.directoryDialog(self, title, basepath)
        
        if result.accepted:
            path = self.parent.getRelativePath(refpath, result.path)
            self.components.pixmapsPath.text = path
        
    def on_tarballsPathBtn_mouseClick(self, event):
        basepath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        basepath = os.path.join(basepath, self.components.tarballsPath.text)
        refpath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        
        title = 'Select path to project tarballs directory'
        result = dialog.directoryDialog(self, title, refpath)
        
        if result.accepted:
            path = self.parent.getRelativePath(refpath, result.path)
            self.components.tarballsPath.text = path
            
    def on_appLicenceBtn_mouseClick(self, event):
        basepath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        basepath = os.path.join(basepath, self.components.appLicence.text)
        refpath = os.path.join(self.parent.cfg.get('ConfigData', 'projects'), self.parent.components.baseDir.text)
        
        title = 'Select path to project licence file'
        result = dialog.openFileDialog(self, title, refpath)
        
        if result.accepted:
            path = self.parent.getRelativePath(refpath, result.paths[0])
            self.components.appLicence.text = path
        
    def on_btnOK_mouseClick(self, event):
        old = copy.deepcopy(self.parent.project)
        self.parent.project.set('Project', 'buildfilespath', self.parent.pathSplit(self.components.buildPath.text))
        self.parent.project.set('Project', 'distfilespath', self.parent.pathSplit(self.components.distPath.text))
        self.parent.project.set('Project', 'pixmapspath', self.parent.pathSplit(self.components.pixmapsPath.text))
        self.parent.project.set('Project', 'tarballspath', self.parent.pathSplit(self.components.tarballPath.text))
        self.parent.project.set('Project', 'publisher', self.components.appPublisher.text)
        self.parent.project.set('Project', 'appurl', self.components.appURL.text)
        self.parent.project.set('Project', 'applicence', self.parent.pathSplit(self.components.appLicence.text))
        self.parent.project.set('Project', 'ascii', str(int(self.components.asciiChk.checked)))
        self.parent.project.set('Project', 'striplib', str(int(self.components.striplibsChk.checked)))
        self.parent.project.set('Project', 'console', str(int(self.components.consoleChk.checked)))
        self.parent.project.set('Project', 'optimize', str(int(self.components.optimizeChk.checked)))
        self.parent.project.set('Project', 'compress', str(int(self.components.compressChk.checked)))
        self.parent.project.set('Project', 'debug', str(int(self.components.debugChk.checked)))
        if self.components.buildType.stringSelection == 'Single directory':
            self.parent.project.set('Project', 'onedir', '1')
        else:
            self.parent.project.set('Project', 'onedir', '0')
        if self.parent.project != old: self.parent.documentChanged = True
        event.Skip()
        
    def on_btnCancel_mouseClick(self, event):
        event.Skip()
