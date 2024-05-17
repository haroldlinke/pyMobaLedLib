
"""
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2006/03/03 10:07:21 $"
"""

import wx

SPACES = '    '

def colorDescription(color):
    if isinstance(color, str):
        return "'%s'" % color
    else:
        return "%s" % str(color)

# this is a complete hack job in order to avoid
# outputting defaults
def widgetAttributes(background, aWidget):
    # this might be overly aggressive
    # it could be that the normal default of white might be different on these
    # various widgets rather than being the same, so the wxTextCtrl is
    # not a good comparison
    flds = ['TextField', 'PasswordField', 'TextArea']
    txtWidgets = ['TextField', 'PasswordField', 'TextArea', 'Choice',
                  'List', 'Calendar', 'ComboBox']
    imgWidgets = ['Image', 'ImageButton']
    comp = background.propertyEditorWindow.components
    dFgC = comp.wUpdate.foregroundColor.Get()
    dBgC = comp.wUpdate.backgroundColor.Get()
    dFont = repr(comp.wUpdate.font)
    dTextBgC = comp.wField.backgroundColor.Get()
    
    # make sure these primary attributes show up
    # at the beginning of the listing
    # the remaining ones will be in alphabetical order
    dStr = "{'type':'%s', \n" % aWidget.__class__.__name__
    
    # KEA 2002-03-24
    # only save the special ids
    if background.editingDialog and aWidget.__class__.__name__ == 'Button':
        if aWidget.id in [wx.ID_OK, wx.ID_CANCEL, wx.ID_YES, wx.ID_NO]:
            dStr += "    'id':%d, \n" % aWidget.id            

    dStr += "    'name':'%s', \n" % aWidget.name
    dStr += "    'position':%s, \n" % str(aWidget.position)

    # try and determine default sizes        
    width, height = aWidget.size
    if aWidget.__class__.__name__ in imgWidgets:
        width, height = aWidget._size
    elif aWidget.__class__.__name__ not in ['BitmapCanvas', 'HtmlWindow', 'IEHtmlWindow', 'Gauge', 'StaticBox']:
        bestWidth, bestHeight = aWidget.GetBestSize()
        if bestWidth == width:
            width = -1
        if bestHeight == height:
            height = -1
    if width != -1 or height != -1:
        dStr += "    'size':(%d, %d), \n" % (width, height)

        
    #for key in aWidget._getAttributeNames():
    attributes = aWidget._spec.getAttributes().keys()
    attributes.sort()
    for key in attributes:
        if key in ['id', 'bitmap', 'name', 'position', 'selection', 'size']:
            pass
        elif getattr(aWidget, key) is not None:
            #print aWidget.__class__.__name__, key, getattr(aWidget, key)
            value = getattr(aWidget, key)
            if key == 'file' and aWidget.__class__.__name__ in imgWidgets and value == '':
                dStr += "    'file':'', \n"
                continue

            if key == 'alignment' and \
                aWidget.__class__.__name__ in ['StaticText', 'PasswordField', 'TextField', 'TextArea'] \
                and value == 'left':
                continue
            if key == 'border' and aWidget.__class__.__name__ in txtWidgets and value == '3d':
                continue
            if key == 'backgroundColor' and \
               aWidget.__class__.__name__ in txtWidgets and \
               value.Get() == dTextBgC:
                continue
            if key == 'foregroundColor' and value.Get() == dFgC:
                continue
            if key == 'backgroundColor' and value.Get() == dBgC:
                continue
            if key == 'font' and repr(value) == dFont:
                continue
            # KEA 2002-07-07
            # what other Unicode strings do we need to deal with above?
            #print key, value, type(value)
            if isinstance(value, (str, unicode)):
                # if isinstance(value, unicode):
                #     value = value.encode('ascii', 'ignore')
                # need to escape strings
                #pprint.pprint(value)
                if value != '':
                    dStr += """    %s:%s, \n""" % (repr(key), repr(value))
            else:
                if (key in ['editable', 'enabled', 'visible'] and value == True) or \
                    (key in ['checked', 'default', 'horizontalScrollbar'] and value == False):
                    # don't include default values
                    pass
                else:
                    dStr += "    '%s':%s, \n" % (key, value)
    dStr += '    },\n'
    return dStr


def resourceMenuItemAttributes(menuItem):
    desc =  SPACES * 4 + "  {'type':'MenuItem',\n"
    desc += SPACES * 4 + "   'name':'%s',\n" % menuItem.name
    desc += SPACES * 4 + """   'label':%s,\n""" % repr(menuItem.label)
    try:
        if menuItem.command is not None:
            desc += SPACES * 4 + "   'command':'%s',\n" % menuItem.command
    except:
        pass
    try:
        if not menuItem.enabled:
            desc += SPACES * 4 + "   'enabled':0,\n"
    except:
        pass
    try:
        if menuItem.checkable:
            desc += SPACES * 4 + "   'checkable':1,\n"
        if menuItem.checked:
            desc += SPACES * 4 + "   'checked':1,\n"
    except:
        pass
    desc += SPACES * 4 + "  },\n"
    return desc

def resourceMenuAttributes(menu):
    desc =  SPACES * 3 + " {'type':'Menu',\n"
    desc += SPACES * 3 + " 'name':'%s',\n" % menu.name
    desc += SPACES * 3 + """ 'label':%s,\n""" % repr(menu.label)
    desc += SPACES * 3 + " 'items': [\n"
    
    for m in menu.items:
        desc += resourceMenuItemAttributes(m)
        
    desc += SPACES * 3 + "  ]\n"
    desc += SPACES * 3 + " },\n"
    return desc

def resourceMenubarAttributes(menubar):
    desc =  SPACES * 2 + "'menubar': {'type':'MenuBar',\n"
    desc += SPACES * 2 + " 'menus': [\n"

    for m in menubar.menus:
        desc += resourceMenuAttributes(m)
    
    desc += SPACES * 2 + " ]\n"
    desc += SPACES + " },\n"
    return desc

def resourceBackgroundAttributes(background, bg):
    desc =  "    {'type':'Background',\n"
    desc += "          'name':'%s',\n" % bg.name
    desc += """          'title':%s,\n""" % repr(bg.title)
    # KEA 2004-10-04
    # need a more sophisticated way of specifying an optional position
    # but just saving the position the user is editing the window at
    # is bad, so turn it off for now
##    desc += "          'position':%s,\n" % str(background.GetPositionTuple())
    desc += "          'size':%s,\n" % str(background.GetSizeTuple())
    
    if bg.statusBar is not None and bg.statusBar:
        desc += "          'statusBar':1,\n"
    if bg.foregroundColor is not None:
        desc += "          'foregroundColor':" +  colorDescription(bg.foregroundColor) + ",\n"
    if bg.backgroundColor is not None:
        desc += "          'backgroundColor':" + colorDescription(bg.backgroundColor) + ",\n"
    if bg.icon is not None: 
        desc += "          'icon':'%s',\n" % bg.icon
    if bg.image is not None:
        desc += "          'image':'%s',\n" % bg.image
    if bg.tiled:
        desc += "          'tiled':1,\n"
    if not bg.visible:
        desc += "          'visible':0,\n"
    if bg.style != []:
        desc += "          'style':%s,\n" % str(bg.style)
    desc += "\n"

    try:
        desc += resourceMenubarAttributes(bg.menubar)
    except:
        pass

    # KEA 2002-05-15
    # strings
    if bg.strings != {}:
        desc += "         'strings': {\n"
        for s in bg.strings.__dict__:
            desc += """         %s:%s,\n""" % (repr(s), repr(bg.strings.__dict__[s]))
        desc += "         },\n\n"
    
    desc += "         'components': [\n\n"
    return desc

def resourceStackAttributes(background):
    if background.rsrc is None:
        print "no rsrc"
        # we should probably blow up here

    desc =  "{'application':{'type':'Application',\n"
    desc += "          'name':'%s',\n" % background.rsrc.application.name
    desc += "    'backgrounds': [\n"
    desc += resourceBackgroundAttributes(background, background.rsrc.application.backgrounds[0])
    
    return desc

def resourceDialogAttributes(background, bg):
    desc =  "{'type':'CustomDialog',\n"
    desc += "    'name':'%s',\n" % bg.name
    desc += "    'title':'%s',\n" % bg.title
    desc += "    'position':%s,\n" % str(background.GetPositionTuple())
    desc += "    'size':%s,\n" % str(background.GetSizeTuple())
    #if bg.statusBar is not None and bg.statusBar:
    #    desc += "          'statusBar':1,\n"
    #desc += "\n"
    #if bg.foregroundColor is not None:
    #    desc += "         'foregroundColor':" +  colorDescription(bg.foregroundColor) + ",\n"
    #if bg.backgroundColor is not None:
    #    desc += "         'backgroundColor':" + colorDescription(bg.backgroundColor) + ",\n"
    #if bg.image is not None:
    #    desc += "         'image':'%s',\n" % bg.image
    #if bg.tiled != 0:
    #    desc += "         'tiled':1,\n"

    # KEA 2002-09-12
    # strings
    if bg.strings != {}:
        desc += "\n    'strings': {\n"
        for s in bg.strings.__dict__:
            desc += """        %s:%s,\n""" % (repr(s), repr(bg.strings.__dict__[s]))
        desc += "    },\n\n"

    desc += "    'components': [\n\n"
    return desc

def resourceAttributes(background):
    # KEA 2002-03-24
    """
    editingDialog = 0
    try: 
        name = background.rsrc.application.name
    except:
        editingDialog = 1
    """

    if background.editingDialog:
        desc = resourceDialogAttributes(background, background.rsrc)
        for w in background.components.order:
            if w not in background.sizingHandleNames:
                desc += widgetAttributes(background, background.components[w]) + "\n"

        desc += "] # end components\n"
        desc += "} # end CustomDialog\n"
    else:
        desc = resourceStackAttributes(background)
        for w in background.components.order:
            if w not in background.sizingHandleNames:
                desc += widgetAttributes(background, background.components[w]) + "\n"

        desc += "] # end components\n"
        desc += "} # end background\n"
        desc += "] # end backgrounds\n"
        desc += "} }\n"
        
    return desc

