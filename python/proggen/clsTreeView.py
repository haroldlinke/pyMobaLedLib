from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as P01
import proggen.clsExtensionParameter

"""Build 026.4
***************************************************************************

 Authors:  JKP Application Development Services, info@jkp-ads.com, https://www.jkp-ads.com
           Peter Thornton, pmbthornton@gmail.com

 (c)2013-2017, all rights reserved to the authors

 You are free to use and adapt the code in these modules for
 your own purposes and to distribute as part of your overall project.
 However all headers and copyright notices should remain intact

 You may not publish the code in these modules, for example on a web site,
 without the explicit consent of the authors
***************************************************************************
-------------------------------------------------------------------------
 Module    : clsTreeView
 Company   : JKP Application Development Services (c)
 Author    : Jan Karel Pieterse (www.jkp-ads.com)
 Created   : 15-01-2013
 Purpose   : Creates a VBA Treeview control in a frame on your UserForm
-------------------------------------------------------------------------
 Changes made by Hardi are marked with 'Hardi'
 Set to true to use the same font color for the description like the name
 Number of nodes to show the HourGlassCursor (Old:400)
 Hardi
 Print the Caption2 of the root nodes in bold
 Hardi
 Print the Caption2 of nodes which have childs in bold
 Hardi
# VB2PY (CheckDirective) VB directive took path 2 on HostProject = "Access"
'-----------------------------------------------------------
 MouseAction generic example for all mouse events. See notes in NodeEventRouter
 Hardi: Uncommented
# VB2PY (CheckDirective) VB directive took path 1 on mac
 don't compile the APIs in Mac
 Mac displays at 72 pixels per 72 points (1 pt / pixel) vs 96/72  or 0.75 pt / pixel in most Windows systems
 The respective constants help size and position node controls appropriatelly in for Mac 1 and Win 0.75
 However sizing may not adapt correctly in Windows OS with Large Fonts, contact for support
# VB2PY (CheckDirective) VB directive took path 1 on mac
***************************
*    Public Properties    *
***************************
# VB2PY (CheckDirective) VB directive took path 2 on HostProject = "Access"
Public Property Get EnableLabelEdit(Optional bAutoSort As Boolean) As Boolean  del
    EnableLabelEdit = mbLabelEdit
    bAutoSort = mbAutoSort
End Property

Public Property Let EnableLabelEdit(Optional bAutoSort As Boolean, ByVal bLabelEdit As Boolean)
 PT
' optional bAutoSort: automatically resort siblings after a manual edit
    mbLabelEdit = bLabelEdit
    mbAutoSort = bAutoSort
End Property
Public Property Get MultiSelect() As Boolean
    MultiSelect = mbMultiSelect
End Property
Public Property Let MultiSelect(mbMultiSelect As Boolean)
    mbMultiSelect = MultiSelect
End Property
***********************************
*    Public functions and subs    *
***********************************
***********************************************************************************************
*    Friend properties, functions and subs                                                    *
*    although visible throughout the project these are only intended to be called by clsNodes *
***********************************************************************************************
*********************************************************************************************
*    Private events    *
**********************************************************************************************
************************************
*    Private functions and subs    *
************************************
"""

HostProject = 'Excel'
Internidiate_Description_same_Color = False
Show_HourGlassCursor_Cnt = 0
Root_Caption2_Bold = True
ParentCaption2_Bold = True
TreeControl = MSForms.Frame()
mbInActive = Variant()
mbAlwaysRedesign = Boolean()
mbAutoSort = Boolean()
mbChanged = Boolean()
mbCheckboxes = Boolean()
mbLabelEdit = Boolean()
mbTriState = Boolean()
mbCheckboxImage = Boolean()
mbEditMode = Boolean()
mbFullWidth = Boolean()
mbGotIcons = Boolean()
mbExpanderImage = Boolean()
mbKeyDown = Boolean()
mbMove = Boolean()
mbMultiLine = Boolean()
mbRedesign = Boolean()
mbRootButton = Boolean()
mbShowExpanders = Boolean()
mbShowLines = Boolean()
mlBackColor = Long()
mlForeColor = Long()
mlLabelEdit = Long()
mlLineColor = Long()
mlNodesCreated = Long()
mlNodesDeleted = Long()
mlVisCount = Long()
mlVisOrder = vbObjectInitialize(objtype=Long)
msAppName = String()
msngChkBoxPad = Single()
msngChkBoxSize = Single()
msngIndent = Single()
msngLineLeft = Single()
msngNodeHeight = Single()
msngRootLine = Single()
msngTopChk = Single()
msngTopExpB = Single()
msngTopExpT = Single()
msngTopHV = Single()
msngTopIcon = Single()
msngTopLabel = Single()
msngVisTop = Single()
msngMaxWidths = vbObjectInitialize(objtype=Single)
moActiveNode = clsNode()
moEditNode = clsNode()
moMoveNode = clsNode()
moRootHolder = clsNode()
mcolIcons = Collection()
mcolNodes = Collection()
moCheckboxImage = vbObjectInitialize(((- 1, 1),), StdPicture)
moExpanderImage = vbObjectInitialize(((- 1, 0),), StdPicture)
moForm = MSForms.UserForm()
# Enumeration 'tvMouse'
tvClick = 1
tvDblClick = 2
tvDown = 3
tvMove = 4
tvUp = 5
# Enumeration 'tvTreeRelationship'
tvFirst = 0
tvLast = 1
tvNext = 2
tvPrevious = 3
tvChild = 4
# VB2PY (UntranslatedCode) Event Click(cNode As clsNode)
# VB2PY (UntranslatedCode) Event MouseAction(cNode As clsNode, Action As Long, Button As Integer, Shift As Integer, X As Single, Y As Single)
# VB2PY (UntranslatedCode) Event NodeCheck(cNode As clsNode)
# VB2PY (UntranslatedCode) Event AfterLabelEdit(ByRef Cancel As Boolean, NewString As String, cNode As clsNode)
# VB2PY (UntranslatedCode) Event KeyDown(cNode As clsNode, ByVal KeyCode As MSForms.ReturnInteger, ByVal Shift As Integer)
class POINTAPI:
    def __init__(self):
        self.X = Long()
        self.Y = Long()

mcCheckboxFont = 13
mcCheckboxPad = 19
mcCheckboxPadImg = 15
mcChkBoxSize = 13
mcExpanderFont = 13
mcExpButSize = 15
mcExpBoxSize = 12
mcFullWidth = 800
mcIconPad = 17
mcIconSize = 16
mcTLpad = 4
mcLineLeft = mcTLpad + 10
mcPtPxl = 1
mcSource = 'clsTreeView'

def ExpandNode(cNode):
    cTmp = clsNode()
    cTmp = cNode.ParentNode
    while not cTmp.Caption == 'RootHolder':
        cTmp.Expanded = True

def ImageAdd(Pic, sName):
    global mbGotIcons
    # PT
    # added v026
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if mcolIcons is None:
        mcolIcons = Collection()
        mbGotIcons = True
    mcolIcons.Add(Pic, sName)
    # error if sName is not a unique key
    return
    Err.Raise(Err.Number, 'ImageAdd', 'Error in ImageAdd' + vbNewLine + Err.Description)

def AddRoot(sKey=VBMissingArgument, vCaption=VBMissingArgument, vImageMain=VBMissingArgument, vImageExpanded=VBMissingArgument, vCaption2=VBMissingArgument):
    global moRootHolder
    _fn_return_value = False
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if moRootHolder is None:
        moRootHolder = clsNode()
        moRootHolder.ChildNodes = Collection()
        moRootHolder.Tree = Me
        moRootHolder.Caption = 'RootHolder'
        if mcolNodes is None:
            mcolNodes = Collection()
    _fn_return_value = moRootHolder.AddChild(sKey, vCaption, vImageMain, vImageExpanded, vCaption2= vCaption2)
    return _fn_return_value
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1
    Err.Raise(Err.Number, 'AddRoot', Err.Description)
    return _fn_return_value

def CheckboxImage(picFalse, picTrue, picTriState=VBMissingArgument):
    global moCheckboxImage, mbCheckboxImage
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    moCheckboxImage[0] = picFalse
    moCheckboxImage[- 1] = picTrue
    if not IsMissing(picTriState):
        moCheckboxImage[1] = picTriState
    mbCheckboxImage = True

def EnterExit(bExit):
    global mbInActive
    #PT WithEvents can't trap Enter/Exit events, if we need them here they can be
    #   called from the TreeControl's Enter/Exit events in the form
    mbInActive = bExit
    SetActiveNodeColor(bExit)
    # apply appropriate vbInactiveCaptionText / vbHighlight

def ExpanderImage(picMinus, picPlus):
    global moExpanderImage, mbExpanderImage
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    moExpanderImage[0] = picPlus
    moExpanderImage[- 1] = picMinus
    mbExpanderImage = True

def ExpandToLevel(lExpansionLevel, bReActivate=True):
    global ActiveNode
    cTmp = clsNode()
    # PT call SetTreeExpansionLevel and reactivates the closest expanded parent if necessary
    #    eg, if activeNode.level = 4 and lExpansionLevel = 2, the activenode's grandparent will be activated
    SetTreeExpansionLevel(lExpansionLevel - 1)
    if bReActivate:
        if ActiveNode.Level > lExpansionLevel:
            cTmp = ActiveNode.ParentNode
            while cTmp.Level > lExpansionLevel:
                cTmp = cTmp.ParentNode
            ActiveNode = cTmp

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: vAfter=VBMissingArgument - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: bShowError=VBMissingArgument - ByVal 
def Copy(cSource, cDest, vBefore=VBMissingArgument, vAfter=VBMissingArgument, bShowError=VBMissingArgument):
    global MoveCopyNode
    lParentChecked = Long()
    MoveCopyNode[False] = None
    if mbTriState:
        lParentChecked = cDest.Checked
    Clone(cDest, cSource, vBefore, vAfter)
    if lParentChecked == - 1 and cDest.Checked == 0:
        cDest.Checked = - 1
    SetActiveNodeColor()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: vAfter=VBMissingArgument - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: bShowError=VBMissingArgument - ByVal 
def Move(cSource, cDest, vBefore=VBMissingArgument, vAfter=VBMissingArgument, bShowError=VBMissingArgument):
    global MoveCopyNode, mbAlwaysRedesign
    sErrDesc = String()

    bIsParent = Boolean()

    bRemoveReverseOrder = Boolean()

    lParentChecked = Long()

    idx = Long()

    cNode = clsNode()

    cSourceParent = clsNode()
    # PT Move source node + children to destination node
    #    cannot move the Root and cannot move to a descendant
    #   vBefore/vAfter work as for normal collection; error if invalid, eg a new collection, after the last item, etc
    #
    MoveCopyNode[False] = None
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if cSource is None or cDest is None or cSource is cDest:
        # Or cSource Is Root
        return
    cNode = cDest
    bIsParent = False
    while 1:
        cNode = cNode.ParentNode
        bIsParent = cNode is cSource
        if cNode is None or bIsParent:
            break
    if bIsParent:
        Err.Raise(vbObjectError + 110)
    if cDest.ChildNodes is None:
        # the child becomes a parent for the first time
        cDest.ChildNodes = Collection()
        # expander & VLine will get created automatically if necessary
    if cDest is cSource.ParentNode:
        # changing order in the original parent
        for cNode in cDest.ChildNodes:
            idx = idx + 1
            if cNode is cSource:
                break
        if not IsMissing(vBefore):
            bRemoveReverseOrder = P01.val(vBefore) < idx
        elif not IsMissing(vAfter):
            bRemoveReverseOrder = P01.val(vAfter) < idx
        elif cSource is cSource.LastSibling:
            return
            # no point to move to the same place
    AddNodeToCol(cDest.ChildNodes, cSource, False, vBefore, vAfter)
    cSourceParent = cSource.ParentNode
    _with0 = cSourceParent
    _with0.RemoveChild(cSource, bRemoveReverseOrder)
    # if the old parent has no more children remove its expander & VLine
    if _with0.ChildNodes is None:
        if not _with0.Expander is None:
            Me.TreeControl.Controls.Remove(_with0.Expander.Name)
            _with0.Expander = None
        if not _with0.ExpanderBox is None:
            Me.TreeControl.Controls.Remove(_with0.ExpanderBox.Name)
            _with0.ExpanderBox = None
        if not _with0.VLine is None:
            Me.TreeControl.Controls.Remove(_with0.VLine.Name)
            _with0.VLine = None
        _with0.Expanded = False
    cSource.ParentNode = cDest
    cDest.Expanded = True
    if mbTriState:
        lParentChecked = cDest.Checked
        cDest.CheckTriStateParent()
        cSourceParent.CheckTriStateParent()
        if lParentChecked == - 1 and cDest.Checked == 0:
            cDest.Checked = - 1
    SetActiveNodeColor()
    mbAlwaysRedesign = True
    # ensure Left's get recalc'd during next refresh
    return
    _select0 = Err.Number
    if (_select0 == vbObjectError + 110):
        sErrDesc = 'Cannot cut and move a Node to a descendant node'
    else:
        sErrDesc = 'Move: ' + Err.Description
    if bShowError:
        P01.MsgBox(sErrDesc, VBGetMissingArgument(P01.MsgBox, 1), AppName)
    else:
        Err.Raise(Err.Number, mcSource, 'Move: ' + sErrDesc)

def NodeAdd(vRelative=VBMissingArgument, vRelationship=VBMissingArgument, sKey=VBMissingArgument, vCaption=VBMissingArgument, vImageMain=VBMissingArgument, vImageExpanded=VBMissingArgument):
    _fn_return_value = False
    i = Long()

    cNode = clsNode()

    cRelative = clsNode()

    cParent = clsNode()

    cTmp = clsNode()
    #  As tvTreevRelationship
    #PT, similar to the ocx treeview's nodes.add method
    #    main difference is vRelative can be a Node object as well as a key or index
    #    see also clsNode.AddChild
    #    tvFirst = 0  tvlast = 1 tvNext = 2 tvprevious = 3  tvChild = 4
    if IsMissing(vRelative):
        _fn_return_value = Me.AddRoot(sKey, vCaption, vImageMain, vImageExpanded)
        return _fn_return_value
    else:
        # VB2PY (UntranslatedCode) On Error Resume Next
        cRelative = vRelative
        if cRelative is None:
            cRelative = mcolNodes(vRelative)
        # VB2PY (UntranslatedCode) On Error GoTo errH
        if cRelative is None:
            Err.Raise(vbObjectError + 100, 'NodeAdd', 'vRelative is not a valid node or a node.key')
    if IsMissing(vRelationship):
        vRelationship = tvTreeRelationship.tvNext
        # default
    if vRelationship == tvChild or cRelative is cRelative.Root:
        cParent = cRelative
    else:
        cParent = cRelative.ParentNode
    cNode = clsNode()
    if Len(sKey):
        mcolNodes.Add(cNode, sKey)
    else:
        mcolNodes.Add(cNode)
    if cParent.ChildNodes is None:
        cParent.ChildNodes = Collection()
    _with1 = cParent.ChildNodes
    if _with1.Count == 0:
        _with1.Add(cNode)
    else:
        i = 0
        if vRelationship == tvNext or vRelationship == tvPrevious:
            for cTmp in cParent.ChildNodes:
                i = i + 1
                if cTmp is cRelative:
                    break
        _select1 = vRelationship
        if (_select1 == tvFirst):
            _with1.Add(cNode, VBGetMissingArgument(_with1.Add, 1), 1)
        elif (_select1 == tvLast):
            _with1.Add(cNode, after=_with1.Count)
        elif (_select1 == tvNext):
            _with1.Add(cNode, after=i)
        elif (_select1 == tvPrevious):
            _with1.Add(cNode, before=i)
        elif (_select1 == tvChild):
            _with1.Add(cNode)
    _with2 = cNode
    _with2.Key = sKey
    _with2.Caption = CStr(vCaption)
    _with2.ImageMain = vImageMain
    _with2.ImageExpanded = vImageExpanded
    _with2.Index = mcolNodes.Count
    _with2.ParentNode = cParent
    _with2.Tree = Me
    cNode.Tree = Me
    # do this after let key = skey
    _fn_return_value = cNode
    return _fn_return_value
    if mcolNodes is None:
        mcolNodes = Collection()
        # VB2PY (UntranslatedCode) Resume
    if Erl == 100 and Err.Number == 457:
        Err.Raise(vbObjectError + 1, 'clsNode.AddChild', 'Duplicate key: \'' + sKey + '\'')
    else:
        ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1
        Err.Raise(Err.Number, 'clsNode.AddChild', Err.Description)
    return _fn_return_value

def NodeRemove(cNode):
    global moActiveNode, moEditNode, mlNodesCreated, mlNodesDeleted, mlVisCount
    lIdx = Long()

    lNodeCtlsOrig = Long()

    cParent = clsNode()

    cNodeAbove = clsNode()

    cNd = clsNode()
    # PT Remove a Node, its children and grandchildrem
    #    remove all associated controls and tear down class objects
    #    Call Refresh() when done removing nodes
    # VB2PY (UntranslatedCode) On Error GoTo errH
    cNodeAbove = NextVisibleNodeInTree(cNode, bUp= True)
    cParent = cNode.ParentNode
    cNode.TerminateNode(True)
    cParent.RemoveChild(cNode)
    cNode.Index = - 1
    # flag to get removed from mcolNodes in the loop below
    if ActiveNode is cNode:
        moActiveNode = None
    moEditNode = None
    lIdx = 0
    lNodeCtlsOrig = mlNodesCreated
    mlNodesCreated = 0
    for cNd in mcolNodes:
        lIdx = lIdx + 1
        if cNd.Index == - 1:
            mcolNodes.Remove(lIdx)
            lIdx = lIdx - 1
            # decrement the collection index
        else:
            mlNodesCreated = mlNodesCreated - CLng(not cNd.Control is None)
            cNd.Index = lIdx
    mlNodesDeleted = mlNodesDeleted + lNodeCtlsOrig - mlNodesCreated
    cNode = None
    # should terminate the class
    if mlNodesCreated:
        if not cNodeAbove is None:
            Me.ActiveNode = cNodeAbove
        elif mcolNodes.Count:
            Me.ActiveNode = mcolNodes(1)
    else:
        #all nodes deleted
        Erase(mlVisOrder)
        Erase(msngMaxWidths)
        mlVisCount = 0
        mlNodesCreated = 0
        mlNodesDeleted = 0
    return
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1

def NodesClear():
    global mlVisCount, mlNodesCreated, mlNodesDeleted, mbChanged
    i = Long()
    # PT,  similar to Treeview.Nodes.Clear
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if not TreeControl is None:
        _with3 = TreeControl
        for i in vbForRange(TreeControl.Controls.Count - 1, 0, - 1):
            TreeControl.Controls.Remove(i)
        _with3.ScrollBars = fmScrollBarsNone
        _with3.ScrollWidth = 0
        _with3.ScrollHeight = 0
        _with3.ScrollTop = 0
    Erase(mlVisOrder)
    Erase(msngMaxWidths)
    mlVisCount = 0
    mlNodesCreated = 0
    mlNodesDeleted = 0
    TerminateTree()
    mbChanged = False
    return
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1

def Refresh():
    global mlVisCount, mlNodesCreated, mlNodesDeleted, mbRedesign
    bInit = Boolean()
    # Create node controls as required the first time respective parent's Expanded property = true
    # hide or show and (re)position node controls as required
    # Call Refresh after changing any Treeview properties or after adding/removing/moving any nodes
    # or making any change that will alter placement of nodes in the treeview
    if Me.TreeControl is None:
        TerminateTree()
        # a Frame (container for the treeview) should have been referrenced to me.TreeControl
        Err.Raise(vbObjectError + 10, mcSource, 'Refresh: \'TreeControl\' frame is not referenced')
    elif moRootHolder is None:
        #
        Err.Raise(vbObjectError + 11, mcSource, 'Refresh: No Root nodes have been created')
    elif moRootHolder.ChildNodes is None:
        # nothing to do
        mlVisCount = 0
        mlNodesCreated = 0
        mlNodesDeleted = 0
        Erase(mlVisOrder)
        Erase(msngMaxWidths)
        return
    elif Me.TreeControl.Controls.Count == 0:
        # display the treeview for first time
        bInit = True
    else:
        # ensure all node properties are checked, eg after changing indentation or nodeheight during runtime
        mbRedesign = True
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    BuildRoot(bInit)
    return
    ShowHourGlassCursor(False)
    Err.Raise(Err.Number, mcSource, 'Error in BuildRoot: ' + Err.Description)

def ScrollToView(cNode=VBMissingArgument, Top1Bottom2=VBMissingArgument, bCollapseOthers=VBMissingArgument):
    bIsVisible = Boolean()

    bWasCollapsed = Boolean()

    lVisIndex = Long()

    sngTop = Single()

    sngBot = Single()

    sngVisHt = Single()

    sngScrollTop = Single()

    cTmp = clsNode()
    # PT scrolls the treeview to position the node in view
    # Top1Bottom2= 0 roughly 1/3 from the top
    # Top1Bottom2= 1 or -1 at the top
    # Top1Bottom2= 2 or -2 at the bottom
    if cNode is None:
        cNode = ActiveNode
    if bCollapseOthers:
        SetTreeExpansionLevel(0)
    cTmp = cNode.ParentNode
    while not cTmp.Caption == 'RootHolder':
        if not cTmp.Expanded:
            bWasCollapsed = True
            cTmp.Expanded = True
        cTmp = cTmp.ParentNode
    if bWasCollapsed:
        BuildRoot(False)
    lVisIndex = cNode.VisIndex
    sngBot = mcTLpad + lVisIndex * NodeHeight
    sngTop = sngBot - NodeHeight
    _with4 = TreeControl
    sngVisHt = _with4.InsideHeight
    if _with4.ScrollBars == fmScrollBarsBoth or _with4.ScrollBars == fmScrollBarsHorizontal:
        sngVisHt = sngVisHt - 15
        # roughly(?) width of a scrollbar
    bIsVisible = sngTop > _with4.ScrollTop and sngBot < _with4.ScrollTop + sngVisHt
    if not bIsVisible or Top1Bottom2 > 0:
        if Top1Bottom2 < 0:
            Top1Bottom2 = Top1Bottom2 * - 1
        if Top1Bottom2 == 0:
            # place about 1/3 from top
            sngScrollTop = lVisIndex * NodeHeight - _with4.InsideHeight / 3
        elif Top1Bottom2 == 1:
            # scroll to top
            sngScrollTop = sngTop - mcTLpad
        else:
            sngScrollTop = sngBot - sngVisHt + mcTLpad
            # scroll to bottom
        if sngScrollTop < 0:
            sngScrollTop = 0
        _with4.ScrollTop = sngScrollTop

def SetScrollbars(bRecalcWidths, bSetScrollDims=VBMissingArgument):
    i = Long()

    bars = Long()
    # PT set scrollbars as required to ensure all nodes are viewable
    #    called internally by BuildRoot
    #    call externally to reset scrollbars while resizing the Treeview container Frame with bSetScrollDims:=False
    #    or with bSetScrollDims:=True after changing or updating text in node captions
    if bRecalcWidths:
        RecalcMaxTextWidth()
        bSetScrollDims = True
    _with5 = Me.TreeControl
    if bSetScrollDims:
        _with5.ScrollWidth = MaxNodeWidth + mcTLpad
        _with5.ScrollHeight = mlVisCount * NodeHeight + mcTLpad
    for i in vbForRange(0, 1):
        bars = 0
        if _with5.InsideWidth < _with5.ScrollWidth:
            bars = fmScrollBarsHorizontal
        if _with5.InsideHeight < _with5.ScrollHeight:
            bars = bars + fmScrollBarsVertical
        if bars != _with5.ScrollBars:
            _with5.ScrollBars = bars
        else:
            break

def TerminateTree():
    global moMoveNode, moEditNode, moActiveNode, moRootHolder, mcolNodes
    cNode = clsNode()
    #-------------------------------------------------------------------------
    # Procedure : TerminateTree
    # Company   : JKP Application Development Services (c)
    # Author    : Jan Karel Pieterse (www.jkp-ads.com)
    # Created   : 15-01-2013
    # Purpose   : Terminates this class' instance
    #-------------------------------------------------------------------------
    #Instead of the terminate event of the class
    #we use this public method so it can be
    #explicitly called by parent classes
    #this is done because we'll end up having multiple circular references
    #between parent and child classes, which may cause the terminate events to be ignored.
    if not moRootHolder is None:
        if not moRootHolder.ChildNodes is None:
            for cNode in moRootHolder.ChildNodes:
                cNode.TerminateNode()
        moRootHolder.TerminateNode()
    moMoveNode = None
    moEditNode = None
    moActiveNode = None
    moRootHolder = None
    mcolNodes = None
    #** TerminateTree does NOT reset treeview properties or remove
    #** the TreeControl reference to the treeview's Frame control
    #
    #   If the form is being unloaded it's enough to call TerminateTree in it's close event,
    #   node controls will automatically unload with the form.
    #   However if the treeview is to be cleared or moved but the main form is not being unloaded
    #   call the NodesRemove method which will remove all node controls, then call TerminateTree

def GetExpanderIcon(bExpanded, Pic):
    _fn_return_value = False
    if mbExpanderImage:
        Pic = moExpanderImage(bExpanded)
        _fn_return_value = True
    return _fn_return_value

def GetCheckboxIcon(lChecked, Pic):
    _fn_return_value = False
    if mbCheckboxImage:
        Pic = moCheckboxImage(lChecked)
        _fn_return_value = True
    return _fn_return_value

def GetNodeIcon(vKey, Pic, bFullWidth):
    _fn_return_value = False
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    Pic = mcolIcons(vKey)
    _fn_return_value = True
    bFullWidth = mbFullWidth
    # after error in case no picture
    return _fn_return_value

def RaiseAfterLabelEdit(cNode, sNewText):
    _fn_return_value = False
    Cancel = Boolean()
    # PT called from moEditBox_KeyDown after vbKeyEnter
    #
    RaiseEvent(AfterLabelEdit(Cancel, sNewText, cNode))
    _fn_return_value = Cancel
    return _fn_return_value

def NodeEventRouter(cNode, sControl, lAction, Button=VBMissingArgument, Shift=VBMissingArgument, X=VBMissingArgument, Y=VBMissingArgument):
    global ActiveNode
    bFlag = Boolean()

    lngViewable = Long()

    cLastChild = clsNode()
    if sControl == 'Caption':
        if not ActiveNode is cNode:
            ActiveNode = cNode
        else:
            SetActiveNodeColor()
        if lAction == 1:
            # tvClick
            RaiseEvent(Click(cNode))
        else:
            # tvDblClick, tvDown, tvMove, tvUp
            # To enable DblClick, MouseDown and MouseUp events:
            #   uncomment moTree.NodeEventRouter in mctlControl_MouseDown, _MouseUp and _DblClick in clsNode
            #   add a mctlControl_MouseMove stub if MouseMove is required and adapt the call to NodeEventRouter with lAction = tvMove
            #   uncomment Event MouseAction in the declarations in this module
            #   uncomment RaiseEvent MouseAction below
            #   add the treeview_MouseAction stub in the main from that holds the reference to the treeview
            RaiseEvent(MouseAction(cNode, lAction, Button, Shift, X, Y))
    elif sControl == 'Expander':
        bFlag = not ActiveNode is cNode
        if bFlag:
            ActiveNode = cNode
        BuildRoot(False)
        if cNode.Expanded:
            if not cNode.ChildNodes is None:
                cLastChild = cNode.ChildNodes(cNode.ChildNodes.Count)
                if not NodeIsVisible(cLastChild, lngViewable):
                    if lngViewable > cNode.ChildNodes.Count:
                        ScrollToView(cLastChild, Top1Bottom2=2)
                    else:
                        ScrollToView(cNode, Top1Bottom2=1)
        if bFlag:
            # Skip unnecesary click event if user clicks the already active node,
            # only raise the click event if a new Node has just been made active.
            # Remove this If bFlag if always want to trap the click event
            RaiseEvent(Click(cNode))
    elif sControl == 'Checkbox':
        RaiseEvent(NodeCheck(cNode))

def UniqueKey(sKey):
    _fn_return_value = False
    cNode = clsNode()
    for cNode in Nodes:
        if cNode.Key == sKey:
            Err.Raise(vbObjectError + 1, 'clsTreeView', 'Duplicate key: \'' + sKey + '\'')
    _fn_return_value = sKey
    return _fn_return_value

def TreeControl_Click():
    global EditMode
    # PT exit editmode if an empty part of the treeview is clicked
    EditMode[ActiveNode] = False

def class_initialize():
    global mbRootButton, mbShowExpanders, mbShowLines, mlLineColor, msngIndent, msngNodeHeight, msngRootLine, msAppName
    # default properties
    mbRootButton = True
    mbShowExpanders = True
    mbShowLines = True
    mlLineColor = vbScrollBars
    ## VB2PY (CheckDirective) VB directive took path 1 on mac
    msngIndent = 20
    msngNodeHeight = 16
    msngRootLine = msngIndent
    msAppName = 'TreeView'
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1

def __del__():
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1
    pass

def AddNodeToCol(colNodes, cAddNode, bTreeCol, vBefore=VBMissingArgument, vAfter=VBMissingArgument):
    _fn_return_value = False
    i = Long()

    sKey = String()

    cTmp = clsNode()

    Pos = Long()
    if bTreeCol:
        sKey = cAddNode.Key
    if Len(sKey):
        # VB2PY (UntranslatedCode) On Error Resume Next
        i = 0
        cTmp = colNodes(sKey)
        if not cTmp is None:
            Pos = InStr(1, sKey, '_copy:')
            if Pos:
                sKey = left(sKey, Pos - 1)
            sKey = sKey + '_copy:'
            while not cTmp is None:
                cTmp = None
                i = i + 1
                cTmp = colNodes(sKey + i)
            sKey = sKey + i
            if bTreeCol:
                cAddNode.Key = sKey
        # VB2PY (UntranslatedCode) On Error GoTo 0
        # error returns to caller
        if IsMissing(vBefore) and IsMissing(vAfter):
            colNodes.Add(cAddNode, sKey)
        elif IsMissing(vAfter):
            colNodes.Add(cAddNode, sKey, P01.val(vBefore))
        else:
            colNodes.Add(cAddNode, sKey, VBGetMissingArgument(colNodes.Add, 2), P01.val(vAfter))
    else:
        # no key
        if IsMissing(vBefore) and IsMissing(vAfter):
            colNodes.Add(cAddNode)
        elif IsMissing(vAfter):
            colNodes.Add(cAddNode, VBGetMissingArgument(colNodes.Add, 1), P01.val(vBefore))
        else:
            colNodes.Add(cAddNode, VBGetMissingArgument(colNodes.Add, 1), VBGetMissingArgument(colNodes.Add, 2), P01.val(vAfter))
    return _fn_return_value


def setActiveNode(oActiveNode):
    global MoveCopyNode, moActiveNode
    cTmp = clsNode()
    #-------------------------------------------------------------------------
    # Procedure : ActiveNode
    # Company   : JKP Application Development Services (c)
    # Author    : Jan Karel Pieterse (www.jkp-ads.com)
    # Created   : 17-01-2013
    # Purpose   : Setting the activenode also updates the node colors
    #             and ensures the node is scrolled into view
    #-------------------------------------------------------------------------
    if oActiveNode is MoveCopyNode(False):
        MoveCopyNode[False] = None
    if moActiveNode is oActiveNode:
        SetActiveNodeColor()
        return
    ResetActiveNodeColor(ActiveNode)
    if oActiveNode.Control is None:
        cTmp = oActiveNode.ParentNode
        while not cTmp.Caption == 'RootHolder':
            cTmp.Expanded = True
            cTmp = cTmp.ParentNode
        if mlNodesCreated:
            BuildRoot(False)
    moActiveNode = oActiveNode
    SetActiveNodeColor()

def getActiveNode():
    global ActiveNode
    _fn_return_value = False
    _fn_return_value = moActiveNode
    return _fn_return_value
ActiveNode = property(fset=setActiveNode, fget=getActiveNode)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: sAppName - ByVal 
def setAppName(sAppName):
    global msAppName
    msAppName = sAppName

def getAppName():
    global AppName
    _fn_return_value = False
    _fn_return_value = msAppName
    return _fn_return_value
AppName = property(fset=setAppName, fget=getAppName)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: bChanged - ByVal 
def setChanged(bChanged):
    global mbChanged
    # called after manual node edit and Checked change
    mbChanged = bChanged

def getChanged():
    global Changed
    _fn_return_value = False
    #PT user has edited node(s) and/or changed Checked value(s)
    _fn_return_value = mbChanged
    return _fn_return_value
Changed = property(fset=setChanged, fget=getChanged)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: bCheckboxes - ByVal 
def setCheckBoxes(bTriState=VBMissingArgument, bCheckboxes):
    global mbCheckboxes, mbTriState, msngChkBoxPad, msngNodeHeight, mbRedesign
    bOrig = Boolean()

    bOrigTriState = Boolean()
    # PT
    bOrig = mbCheckboxes
    mbCheckboxes = bCheckboxes
    bOrigTriState = mbTriState
    mbTriState = bTriState
    if bCheckboxes:
        msngChkBoxPad = mcCheckboxPad
        if msngNodeHeight < mcExpButSize:
            msngNodeHeight = mcExpButSize
    else:
        msngChkBoxPad = 0
    if not TreeControl is None:
        if TreeControl.Controls.Count and  ( bOrig != mbCheckboxes or bOrigTriState != mbTriState ) :
            # Checkboxes added changed after start-up so update the treeview
            mbRedesign = True
            Refresh()

def getCheckBoxes(bTriState=VBMissingArgument):
    global CheckBoxes
    _fn_return_value = False
    # PT
    _fn_return_value = mbCheckboxes
    bTriState = mbTriState
    return _fn_return_value
CheckBoxes = property(fset=setCheckBoxes, fget=getCheckBoxes)


def setForm(frm):
    global moForm
    moForm = frm
Form = property(fset=setForm)


def setFullWidth(bFullWidth):
    global mbFullWidth
    mbFullWidth = bFullWidth

def getFullWidth():
    global FullWidth
    _fn_return_value = False
    _fn_return_value = mbFullWidth
    return _fn_return_value
FullWidth = property(fset=setFullWidth, fget=getFullWidth)


def setImages(objImages):
    global mcolIcons, mbGotIcons
    sDesc = String()

    Pic = stdole.StdPicture()

    obj = Object()
    # PT  objImages can be a collection of StdPicture objects
    #     a Frame containing only Image controls (or controls with an image handle)
    #     stdole.IPictureDisp or stdole.StdPicture  objects
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if proggen.clsExtensionParameter.TypeName(objImages) == 'Collection':
        mcolIcons = objImages
        for Pic in mcolIcons:
            # if not a valid picture let the error abort
            pass
    else:
        mcolIcons = Collection()
        ##If HostProject = "Access" Then
        #' if the frame is on an Access form include .Object
        #For Each obj In objImages.Object.Controls
        for obj in objImages.Controls:
            mcolIcons.Add(obj.Picture, obj.Name)
    # Flag we have a valid collection of images
    mbGotIcons = mcolIcons.Count >= 1
    return
    mcolIcons = None
    if Erl == 100:
        sDesc = 'The obImages collection includes an invalue StdPicture object'
    elif Erl == 200:
        sDesc = 'A control in objImages does not contain a valid Picture object'
    sDesc = sDesc + vbNewLine + Err.Description
    Err.Raise(Err.Number, 'Images', sDesc)
Images = property(fset=setImages)


def setIndentation(sngIndent):
    global msngIndent, msngRootLine, ActiveNode
    cNode = clsNode()

    sngOld = Single()
    sngOld = msngIndent
    ## VB2PY (CheckDirective) VB directive took path 1 on mac
    if sngIndent < 16:
        msngIndent = 16
        # min indent ?
    elif sngIndent > 80:
        msngIndent = 80
        # max indent
    else:
        msngIndent = Int(sngIndent)
    if mbRootButton:
        msngRootLine = msngIndent
    if not TreeControl is None and not  ( sngOld == msngIndent ) :
        # changed after start-up so update the treeview
        if TreeControl.Controls.Count:
            cNode = Me.ActiveNode
            Refresh()
            if not cNode is None:
                ActiveNode = cNode

def getIndentation():
    global Indentation
    _fn_return_value = False
    _fn_return_value = msngIndent
    return _fn_return_value
Indentation = property(fset=setIndentation, fget=getIndentation)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: bLabelEdit - ByVal 
def setEnableLabelEdit(bAutoSort=VBMissingArgument, bMultiLine=VBMissingArgument, bLabelEdit):
    global mbLabelEdit, mbAutoSort, mbMultiLine
    # PT
    #PT optional bAutoSort: automatically sort siblings after a manual edit
    #   optional bMultiLine: do not remove line breaks from manual edits
    mbLabelEdit = bLabelEdit
    mbAutoSort = bAutoSort
    mbMultiLine = bMultiLine

def getEnableLabelEdit(bAutoSort=VBMissingArgument, bMultiLine=VBMissingArgument):
    global EnableLabelEdit
    _fn_return_value = False
    _fn_return_value = mbLabelEdit
    bAutoSort = mbAutoSort
    bMultiLine = mbMultiLine
    return _fn_return_value
EnableLabelEdit = property(fset=setEnableLabelEdit, fget=getEnableLabelEdit)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: nLabelEdit - ByVal 
def setLabelEdit(bAutoSort=VBMissingArgument, nLabelEdit):
    global mlLabelEdit, mbLabelEdit, mbAutoSort
    # PT
    mlLabelEdit = nLabelEdit
    mbLabelEdit = ( nLabelEdit == 0 )
    mbAutoSort = bAutoSort

def getLabelEdit(bAutoSort=VBMissingArgument):
    global LabelEdit
    _fn_return_value = False
    # PT
    # PT,  equivalent to Treeview.LabelEdit
    # 0/tvwAutomatic nodes can be manually edited
    # optional bAutoSort: automatically resort siblings after a manual edit
    _fn_return_value = mlLabelEdit
    bAutoSort = mbAutoSort
    return _fn_return_value
LabelEdit = property(fset=setLabelEdit, fget=getLabelEdit)


def setLineColor(lColor):
    global mlLineColor
    if lColor <= vbInfoBackground or  ( lColor >= 0 and lColor <= vbWhite ) :
        mlLineColor = lColor
    else:
        # invalid input
        mlLineColor = vbScrollBars

def getLineColor():
    global LineColor
    _fn_return_value = False
    #default mlLineColor=vbScrollBars applied in initialize
    _fn_return_value = mlLineColor
    return _fn_return_value
LineColor = property(fset=setLineColor, fget=getLineColor)


def setMoveCopyNode(bMove=VBMissingArgument, lColor=VBMissingArgument, cNode):
    global mbMove, moMoveNode
    lOrigBackcolor = Long()
    mbMove = bMove
    if lColor == 0:
        if bMove:
            lColor = rgb(255, 231, 162)
        else:
            lColor = rgb(159, 249, 174)
    if not moMoveNode is None:
        moMoveNode.BackColor = lOrigBackcolor
        moMoveNode.Control.BackColor = lOrigBackcolor
        moMoveNode = None
    else:
    if not cNode is None:
        lOrigBackcolor = cNode.BackColor
        if lOrigBackcolor == 0:
            lOrigBackcolor = mlBackColor
        cNode.BackColor = lColor
        cNode.Control.BackColor = cNode.BackColor
        cNode.Control.ForeColor = cNode.ForeColor
        moMoveNode = cNode
    else:

def getMoveCopyNode(bMove=VBMissingArgument, lColor=VBMissingArgument):
    global MoveCopyNode
    _fn_return_value = False
    bMove = mbMove
    _fn_return_value = moMoveNode
    return _fn_return_value
MoveCopyNode = property(fset=setMoveCopyNode, fget=getMoveCopyNode)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: sngNodeHeight - ByVal 
def setNodeHeight(sngNodeHeight):
    global msngNodeHeight, msngRootLine, ActiveNode
    cNode = clsNode()

    sngOld = Single()
    sngOld = msngNodeHeight
    ## VB2PY (CheckDirective) VB directive took path 1 on mac
    if sngNodeHeight < 12:
        # height of expander-box is 12 in Mac
        msngNodeHeight = 12
    elif sngNodeHeight > 60:
        msngNodeHeight = 60
    else:
        msngNodeHeight = Int(sngNodeHeight)
    if mbRootButton:
        msngRootLine = msngIndent
    if not TreeControl is None and not  ( sngOld == msngNodeHeight ) :
        if TreeControl.Controls.Count:
            cNode = Me.ActiveNode
            Refresh()
            if not cNode is None:
                ActiveNode = cNode

def getNodeHeight():
    global msngNodeHeight, NodeHeight
    _fn_return_value = False
    if msngNodeHeight == 0:
        msngNodeHeight = 12
    _fn_return_value = msngNodeHeight
    return _fn_return_value
NodeHeight = property(fset=setNodeHeight, fget=getNodeHeight)


def getNodes():
    global Nodes
    _fn_return_value = False
    # Global collection of the nodes
    # *DO NOT USE* its Nodes.Add and Nodes.Remove methods
    # To add & remove nodes use clsNode.AddChild() or clsTreeView.NodeAdd and clsTeevView.NodeRemove()
    if mcolNodes is None:
        mcolNodes = Collection()
    _fn_return_value = mcolNodes
    return _fn_return_value
Nodes = property(fget=getNodes)


def setRootButton(lRootLeader):
    global mbRootButton, msngRootLine
    # PT The Root nodes have expanders and lines (if mbShowlines)
    mbRootButton = lRootLeader
    if mbRootButton:
        msngRootLine = msngIndent
    else:
        msngRootLine = 0
    if not Me.TreeControl is None:
        if not moRootHolder is None:
            if not moRootHolder.ChildNodes is None:
                Refresh()

def getRootButton():
    global RootButton
    _fn_return_value = False
    if mbRootButton:
        _fn_return_value = 1
    return _fn_return_value
RootButton = property(fset=setRootButton, fget=getRootButton)


def getRootNodes():
    global RootNodes
    _fn_return_value = False
    #PT returns the collection of Root-nodes
    # **should be treated as read only. Use AddRoot and NodeRemove to add/remove a root node**
    _fn_return_value = moRootHolder.ChildNodes
    return _fn_return_value
RootNodes = property(fget=getRootNodes)


def setShowExpanders(bShowExpanders):
    global mbShowExpanders
    mbShowExpanders = bShowExpanders
    if not TreeControl is None:
        if TreeControl.Controls.Count:
            Refresh()

def getShowExpanders():
    global ShowExpanders
    _fn_return_value = False
    _fn_return_value = mbShowExpanders
    return _fn_return_value
ShowExpanders = property(fset=setShowExpanders, fget=getShowExpanders)


def setShowLines(bShowLines):
    global mbShowLines
    bOrig = Boolean()
    # PT Show horizontal & vertical lines
    bOrig = mbShowLines
    mbShowLines = bShowLines
    if not TreeControl is None:
        if TreeControl.Controls.Count:
            if bOrig != mbShowLines:
                # ShowLines added after start-up so update the treeview
                Refresh()

def getShowLines():
    global ShowLines
    _fn_return_value = False
    _fn_return_value = mbShowLines
    return _fn_return_value
ShowLines = property(fset=setShowLines, fget=getShowLines)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: bEditMode - ByVal 
def setEditMode(cNode, bEditMode):
    global MoveCopyNode, mbEditMode, moEditNode
    # PT
    MoveCopyNode[False] = None
    mbEditMode = bEditMode
    if not moEditNode is None:
        moEditNode.EditBox(False)
    if bEditMode:
        moEditNode = cNode
    else:
        moEditNode = None

def getEditMode(cNode):
    global EditMode
    _fn_return_value = False
    # PT
    _fn_return_value = mbEditMode
    return _fn_return_value
EditMode = property(fset=setEditMode, fget=getEditMode)

# VB2PY (UntranslatedCode) Option Explicit
# VB2PY (ParserError) Parsing error: 0, 'Private Sub BuildRoot(bInit As Boolean)'
# VB2PY (ParserStop) Conversion of VB code halted
