from vb2py.vbfunctions import *
from vb2py.vbdebug import *
import ExcelAPI.XLA_Application as P01

"""Build 026
***************************************************************************

 Authors:  JKP Application Development Services, info@jkp-ads.com, https://www.jkp-ads.com
           Peter Thornton, pmbthornton@gmail.com

 (c)2013-2015, all rights reserved to the authors

 You are free to use and adapt the code in these modules for
 your own purposes and to distribute as part of your overall project.
 However all headers and copyright notices should remain intact

 You may not publish the code in these modules, for example on a web site,
 without the explicit consent of the authors
***************************************************************************
-------------------------------------------------------------------------
 Module    : clsNode
 Company   : JKP Application Development Services (c)
 Author    : Jan Karel Pieterse (www.jkp-ads.com)
 Created   : 15-01-2013
 Purpose   : Holds all information of a node of the tree
-------------------------------------------------------------------------
 Changes made by Hardi are marked with 'Hardi'
 Second label for comments
 Hardi
 PT checkbox tristate boolean 0/-1 or 1 for null
 PT order added to Treeview's mcolNodes, won't change
 PT the visible order in the current view, changes with expand/collapse
 PT string name or numeric index as icon Key for the Image collection
 PT ditto for expanded icon
 PT number of icons availabel for this node 0, 1 or 2
 PT autosized text width before the node is widened beyond the frame
 PT
 PT
 PT
 Second label for comments
 Hardi
 PT editbox
 PT checkbox
 PT vertical line, only the first child node with children will have a vertical line
 PT horizontal line
 PT separate icon image control
# VB2PY (CheckDirective) VB directive took path 1 on mac
*********************
* Public Properties *
*********************
*****************************
* Public subs and functions *
*****************************
*************************************************************************
*    Friend Properties, Subs & Funtions                                 *
*    ** these procedures are visible throughout the project but should  *
*    ** only be used to communicate with the TreeView, ie clsTreeView   *
*************************************************************************
Friend Sub EditBox(bEnterEdit As Boolean)
  PT new in 006PT2 ,,move to clsTreView?
'-------------------------------------------------------------------------
' Procedure : moCtl_Click
' Author    : Peter Thornton
' Created   : 20-01-2013
' Purpose   : Enter/exit Editmode, show/hide the edit textbox
'-------------------------------------------------------------------------
    On Error Resume Next
    Set moEditBox = moTree.TreeControl.Controls("EditBox")
    On Error GoTo 0

    If bEnterEdit Then

        If moEditBox Is Nothing Then
            Set moEditBox = moTree.TreeControl.Controls.Add("forms.textbox.1", False)
            moEditBox.Name = "EditBox"
        End If

        With moEditBox
            .Left = Control.Left - 3
            .Top = Control.Top - 1.5
            .AutoSize = True
            .BorderStyle = fmBorderStyleSingle
            .Text = Caption
            Control.Visible = False
 hide the node label while editing
            .ZOrder 0
            .Visible = True
            .SelStart = 0
            .SelLength = Len(.Text)
            .SetFocus
        End With

    ElseIf Not moEditBox Is Nothing Then

 exit editmode
        If Not moEditBox Is Nothing Then

 error if moEditBox has already been removed
            On Error Resume Next
            moEditBox.Visible = False
            moEditBox.Text = ""
            Set moEditBox = Nothing
        End If
        Control.Visible = True

    End If
End Sub
******************************
* Private subs and functions *
******************************
***********************
*   Node Events       *
***********************
-------------------------------
-----------------------------------------------------------------------
"""


# Enumeration 'ndSortOrder'
ndAscending = 1
ndDescending = 2
# Enumeration 'ndCompareMethod'
ndBinaryCompare = 0
ndTextCompare = 1
# Enumeration 'ndMouse'
ndDown = 1
ndUp = 2
ndMove = 3
ndBeforeDragOver = 4
ndBeforeDropOrPaste = 5
mcFullWidth = 800
moLabSizer = MSForms.Label()
mcBreak = '¶ '

def ImageUpdate():
    bFullWidth = Boolean()

    vKey = Variant()

    Pic = StdPicture()
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if Me.hasIcon(vKey):
        #  error if Icon or Control is not yet created, silent abort, it'll update in the next BuildRoot
        if moTree.GetNodeIcon(vKey, Pic, bFullWidth):
            if bFullWidth:
                Me.Icon.Picture = Pic
            else:
                Me.Control.Picture = Pic
        elif bFullWidth:
            Me.Icon.Picture = None
        else:
            Me.Control.Picture = None
    return
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ndOrder=ndAscending - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: ndCompare=ndTextCompare - ByVal 
def Sort(ndOrder=ndAscending, ndCompare=ndTextCompare):
    global ChildNodes
    _fn_return_value = False
    sCaptions = vbObjectInitialize(objtype=String)

    lStart = Long()

    lLast = Long()

    i = Long()

    colNodes = Collection()

    bIsUnSorted = Boolean()
    # PT Sorts the child nodes,
    #    returns True if the order has changed to flag Refresh should be called
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    lStart = 1
    lLast = ChildNodes.Count
    # error if no childnodes to sort
    if lLast == 1:
        # nothing to sort
        return _fn_return_value
    idx = vbObjectInitialize(((lStart, lLast),), Long)
    sCaptions = vbObjectInitialize(((lStart, lLast),), String)
    for i in vbForRange(lStart, lLast):
        idx[i] = i
        sCaptions[i] = ChildNodes.item(i).Caption
    if ndOrder != ndAscending:
        ndOrder = - 1
    # descending
    if ndCompare != ndTextCompare:
        ndCompare = ndBinaryCompare
    BinarySortIndexText(sCaptions(), lStart, lLast, idx, ndOrder, ndCompare)
    for i in vbForRange(lStart, lLast - 1):
        if idx(i) != idx(i + 1) - 1:
            bIsUnSorted = True
            break
    if bIsUnSorted:
        for i in vbForRange(lStart, lLast):
            colNodes.Add(ChildNodes(idx(i)))
        ChildNodes = colNodes
        _fn_return_value = True
    #   Probably(?) any error was because there were no childnodes, no need to raise an error
    return _fn_return_value

def AddChild(sKey=VBMissingArgument, vCaption=VBMissingArgument, vImageMain=VBMissingArgument, vImageExpanded=VBMissingArgument, vCaption2=VBMissingArgument):
    global ImageMain, ImageExpanded, Caption, Caption2, Checked, Tree, ParentNode
    _fn_return_value = False
    bTriState = Boolean()

    cChild = clsNode()
    # VB2PY (UntranslatedCode) On Error GoTo errH
    cChild = clsNode()
    _with15 = moTree.Nodes
    if Len(sKey):
        _with15.Add(cChild, sKey)
        cChild.Key = sKey
    else:
        _with15.Add(cChild)
    cChild.Index = _with15.Count
    if mcolChildNodes is None:
        mcolChildNodes = Collection()
    mcolChildNodes.Add(cChild)
    _with16 = cChild
    if not IsMissing(vImageMain):
        if Len(vImageMain):
            _with16.ImageMain = vImageMain
    if not IsMissing(vImageExpanded):
        if Len(vImageExpanded):
            _with16.ImageExpanded = vImageExpanded
    _with16.Caption = vCaption
    _with16.Caption2 = vCaption2
    # Hardi
    if mlChecked == - 1:
        # -1 = true, +1 = mixed
        if moTree.CheckBoxes(bTriState):
            if bTriState:
                _with16.Checked = True
    _with16.Tree = moTree
    _with16.ParentNode = Me
    _fn_return_value = cChild
    return _fn_return_value
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1
    if Erl == 100 and Err.Number == 457:
        Err.Raise(vbObjectError + 1, 'clsNode.AddChild', 'Duplicate key: \'' + sKey + '\'')
    else:
        Err.Raise(Err.Number, 'clsNode.AddChild', Err.Description)
    return _fn_return_value

def ChildIndex(sKey):
    _fn_return_value = False
    cNode = clsNode()

    lCt = Long()
    #-------------------------------------------------------------------------
    # Procedure : ChildIndex
    # Company   : JKP Application Development Services (c)
    # Author    : Jan Karel Pieterse (www.jkp-ads.com)
    # Created   : 15-01-2013
    # Purpose   : Returns the index of a childnode using its key
    #-------------------------------------------------------------------------
    for cNode in mcolChildNodes:
        lCt = lCt + 1
        if sKey == cNode.Key:
            _fn_return_value = lCt
            cNode = None
            return _fn_return_value
    cNode = None
    return _fn_return_value

def FullPath():
    _fn_return_value = False
    s = String()

    cNode = clsNode()
    # PT, get all the grand/parent keys
    # assumes use of key
    # VB2PY (UntranslatedCode) On Error GoTo errDone
    s = Me.Key
    cNode = Me
    while Err.Number == 0:
        cNode = cNode.ParentNode
        s = cNode.Key + '\\' + s
    _fn_return_value = s
    return _fn_return_value

def GetChild(vKey):
    global mcolChildNodes
    _fn_return_value = False
    cNode = clsNode()

    lIdx = Long()
    #-------------------------------------------------------------------------
    # Procedure : GetChild
    # Company   : JKP Application Development Services (c)
    # Author    : Jan Karel Pieterse (www.jkp-ads.com)
    # Created   : 15-01-2013
    # Purpose   : Returns a childnode using its key
    #-------------------------------------------------------------------------
    if P01.VarType(vKey) == vbString:
        for cNode in mcolChildNodes:
            if vKey == cNode.Key:
                _fn_return_value = cNode
                cNode = None
                return _fn_return_value
    elif not mcolChildNodes is None:
        lIdx = vKey
        if lIdx == - 1:
            lIdx = mcolChildNodes.Count
        if lIdx > 0:
            _fn_return_value = mcolChildNodes(lIdx)
        else:
            mcolChildNodes = None
    cNode = None
    return _fn_return_value

def CheckTriStateParent():
    global mlChecked
    alChecked = vbObjectInitialize(((- 1, 1),), Long)

    cChild = clsNode()
    # PT set triState value of parent according to its childnodes' values
    if not ChildNodes is None:
        for cChild in ChildNodes:
            alChecked[cChild.Checked] = alChecked(cChild.Checked) + 1
        if alChecked(1):
            alChecked[1] = 1
        elif alChecked(- 1) == ChildNodes.Count:
            alChecked[1] = - 1
        elif alChecked(0) == ChildNodes.Count:
            alChecked[1] = 0
        else:
            alChecked[1] = 1
        if mlChecked != alChecked(1):
            mlChecked = alChecked(1)
            UpdateCheckbox()()
    if not Me.Caption == 'RootHolder':
        if not ParentNode.ParentNode is None:
            ParentNode.CheckTriStateParent()

def CheckTriStateChildren(lChecked):
    global mlChecked
    cChild = clsNode()
    # PT, make checked values of children same as parent's
    #     only called if triState is enabled
    if mlChecked != lChecked:
        mlChecked = lChecked
        UpdateCheckbox()()
    if not ChildNodes is None:
        for cChild in ChildNodes:
            cChild.CheckTriStateChildren(lChecked)

def hasIcon(vKey):
    _fn_return_value = False
    # PT get the appropriate icon key/index, if any
    if mlIconCnt == 2 and mbExpanded:
        vKey = mvIconExpandedKey
        _fn_return_value = True
    elif mlIconCnt:
        vKey = mvIconMainKey
        _fn_return_value = True
    return _fn_return_value

def EditBox(bEnterEdit):
    global moEditBox, moLabSizer, mctlControl
    wd = Single()

    ht = Single()
    #  PT new in 006PT2 ,,move to clsTreView?
    #-------------------------------------------------------------------------
    # Procedure : moCtl_Click
    # Author    : Peter Thornton
    # Created   : 20-01-2013. Ammended 026 to resize/reposition the editbox within the confines of the frame container
    # Purpose   : Enter/exit Editmode, show/hide the edit textbox
    #-------------------------------------------------------------------------
    # VB2PY (UntranslatedCode) On Error Resume Next
    moEditBox = moTree.TreeControl.Controls('EditBox')
    moLabSizer = moTree.TreeControl.Controls('LabSizer')
    # VB2PY (UntranslatedCode) On Error GoTo 0
    if bEnterEdit:
        if moEditBox is None:
            moEditBox = moTree.TreeControl.Controls.Add('forms.textbox.1', 'EditBox')
            moLabSizer = moTree.TreeControl.Add('forms.Label.1', 'LabSizer')
            moLabSizer.left = moTree.TreeControl.left
            moLabSizer.top = moTree.TreeControl.top - 12
            moLabSizer.WordWrap = False
            moLabSizer.AutoSize = True
            moLabSizer.Visible = False
        _with17 = moEditBox
        _with17.left = mctlControl.left - 3
        _with17.top = mctlControl.top - 1.5
        _with17.AutoSize = False
        _with17.Width = moTree.TreeControl.Width
        _with17.BorderStyle = fmBorderStyleSingle
        if Len(Me.Caption):
            _with17.Text = Me.Caption
        else:
            moEditBox_Change()
        wd = _with17.Width
        ht = _with17.Height
        _with17.ZOrder(0)
        _with17.Visible = True
        mctlControl.Visible = False
        _with17.SelStart = 0
        _with17.SelLength = Len(_with17.Text)
        _with17.setFocus()
        _with17.Width = wd
        _with17.Height = ht
    elif not moEditBox is None:
        # exit editmode
        if not moEditBox is None:
            # error if moEditBox has already been removed
            # VB2PY (UntranslatedCode) On Error Resume Next
            moEditBox.Visible = False
            moEditBox.Text = ''
            #            If Len(moEditBox.Tag) Then
            #                moTree.TreeControl.ScrollTop = CSng(moEditBox.Tag)
            #                moEditBox.Tag = ""
            #            End If
            moEditBox = None
            moLabSizer = None
        mctlControl.Visible = True

def RemoveChild(cNode, bReverse=VBMissingArgument):
    global mcolChildNodes
    _fn_return_value = False
    lCt = Long()

    i = Long()

    cTmp = clsNode()
    #PT remove a node from the collection,
    #   note, this is only one part of the process of removing a node
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if bReverse:
        for i in vbForRange(mcolChildNodes.Count, 1, - 1):
            cTmp = mcolChildNodes(i)
            if mcolChildNodes(i) is cNode:
                mcolChildNodes.Remove(i)
                _fn_return_value = True
                break
    else:
        for cTmp in mcolChildNodes:
            lCt = lCt + 1
            if cTmp is cNode:
                mcolChildNodes.Remove(lCt)
                _fn_return_value = True
                break
    if mcolChildNodes.Count == 0:
        mcolChildNodes = None
        Me.Expanded = False
    return _fn_return_value
    Err.Raise(vbObjectError, 'RemoveChild', Err.Description)
    return _fn_return_value

def RemoveNodeControls():
    cChild = clsNode()
    if not ChildNodes is None:
        for cChild in ChildNodes:
            cChild.RemoveNodeControls()
    DeleteNodeControls(False)

def TerminateNode(bDeleteNodeControls=VBMissingArgument):
    global Index, mcolChildNodes, moTree
    cChild = clsNode()
    #-------------------------------------------------------------------------
    # Procedure : TerminateNode
    # Company   : JKP Application Development Services (c)
    # Author    : Jan Karel Pieterse (www.jkp-ads.com)
    # Created   : 15-01-2013
    # Purpose   : Terminates the class instance
    #-------------------------------------------------------------------------
    #Instead of the Terminate event of the class we use this public
    #method so it can be explicitly called by parent classes.
    #This is done because to break the two way or circular references
    #between the parent child classes.
    #The most important call in this routine is to destroy the reference
    #between this node class and the parent treeview class -
    #    < Set moTree = Nothing >
    #Once all the moTree references to have been destroyed everything else will
    # 'tear down' normally
    if not ChildNodes is None:
        for cChild in ChildNodes:
            # recursively drill down to all child nodes in this branch
            cChild.TerminateNode(bDeleteNodeControls)
    # If deleting individual nodes while the treeview is running we also want to
    # remove all associated controls as well as removing references
    if bDeleteNodeControls:
        DeleteNodeControls(True)
        if bDeleteNodeControls:
            Index = - 1
    mcolChildNodes = None
    moTree = None

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lStart - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: lEnd - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: idx - ByRef 
def BinarySortIndexText(sCaptions, lStart, lEnd, idx, ndOrder, ndCompare):
    lSmall = Long()

    lLarge = Long()

    sMid = String()

    lTmp = Long()
    # PT sorts the index array based on the string array
    lSmall = lStart
    lLarge = lEnd
    sMid = sCaptions(idx(( lSmall + lLarge )  / 2))
    while lSmall <= lLarge:
        while ( StrComp(sCaptions(idx(lSmall)), sMid, ndCompare) == - ndOrder and lSmall < lEnd ):
            lSmall = lSmall + 1
        while ( StrComp(sCaptions(idx(lLarge)), sMid, ndCompare) == ndOrder and lLarge > lStart ):
            lLarge = lLarge - 1
        if lSmall <= lLarge:
            lTmp = idx(lSmall)
            idx[lSmall] = idx(lLarge)
            idx[lLarge] = lTmp
            lSmall = lSmall + 1
            lLarge = lLarge - 1
    if lStart <= lLarge:
        BinarySortIndexText(sCaptions(), lStart, lLarge, idx, ndOrder, ndCompare)
    if lSmall <= lEnd:
        BinarySortIndexText(sCaptions(), lSmall, lEnd, idx, ndOrder, ndCompare)

def DeleteNodeControls(bClearIndex):
    global mctlControl, mctlHLine, mctlIcon, mctlControl2, mctlExpander, mctlExpanderBox, mctlVLine, moEditBox, mctlCheckBox
    #PT Delete all controls linked to this node
    # VB2PY (UntranslatedCode) On Error GoTo errH
    _with18 = moTree.TreeControl.Controls
    if not mctlControl is None:
        _with18.Remove(mctlControl.Name)
        mctlControl = None
        if not mctlHLine is None:
            _with18.Remove(mctlHLine.Name)
            mctlHLine = None
        if not mctlIcon is None:
            _with18.Remove(mctlIcon.Name)
            mctlIcon = None
        if not mctlIcon is None:
            _with18.Remove(mctlIcon.Name)
            mctlIcon = None
    if not mctlControl2 is None:
        # Hardi
        _with18.Remove(mctlControl2.Name)
        mctlControl2 = None
    if not mctlExpander is None:
        _with18.Remove(mctlExpander.Name)
        mctlExpander = None
    if not mctlExpanderBox is None:
        _with18.Remove(mctlExpanderBox.Name)
        mctlExpanderBox = None
    if not mctlVLine is None:
        _with18.Remove(mctlVLine.Name)
        mctlVLine = None
    if not moEditBox is None:
        _with18.Remove(moEditBox.Name)
        moEditBox = None
    if not mctlCheckBox is None:
        _with18.Remove(mctlCheckBox.Name)
        mctlCheckBox = None
    if not Me.ParentNode is None:
        # if Me is the last child delete parent's expander and VLine (if it has one)
        if FirstSibling is LastSibling:
            if not Me.ParentNode.VLine is None:
                _with18.Remove(Me.ParentNode.VLine.Name)
                Me.ParentNode.VLine = None
            if not Me.ParentNode.ExpanderBox is None:
                _with18.Remove(Me.ParentNode.ExpanderBox.Name)
                Me.ParentNode.ExpanderBox = None
            if not Me.ParentNode.Expander is None:
                _with18.Remove(Me.ParentNode.Expander.Name)
                Me.ParentNode.Expander = None
            Me.ParentNode.Expanded = False
    if bClearIndex:
        Me.Index = - 1
        # flag this node to be removed from mcolNodes in NodeRemove
    return
    # Stop
    # VB2PY (UntranslatedCode) Resume Next

def UpdateCheckbox():
    global Caption, ForeColor
    _fn_return_value = False
    Pic = StdPicture()
    if not mctlCheckBox is None:
        _with19 = mctlCheckBox
        if moTree.GetCheckboxIcon(mlChecked, Pic):
            _with19.Picture = Pic
        else:
            _with19.Caption = IIf(mlChecked, 'a', '')
            if ( mlChecked == 1 )  !=  ( _with19.ForeColor == rgb(180, 180, 180) ) :
                _with19.ForeColor = IIf(mlChecked == 1, rgb(180, 180, 180), vbWindowText)
    moTree.NodeEventRouter(Me, 'Checkbox', 1)
    return _fn_return_value

def UpdateExpanded(bControlOnly):
    global Caption
    bFullWidth = Boolean()

    vKey = Variant()

    Pic = StdPicture()
    #-------------------------------------------------------------------------
    # Procedure : UpdateExpanded
    # Author    : Peter Thornton
    # Created   : 27-01-2013
    # Purpose   : Called via an Expander click or arrow keys
    #             Updates the Expanded property and changes +/- caption
    #-------------------------------------------------------------------------
    if not bControlOnly:
        _with20 = Me.Expander
        if moTree.GetExpanderIcon(mbExpanded, Pic):
            _with20.Picture = Pic
        else:
            if mbExpanded:
                _with20.Caption = '-'
            else:
                _with20.Caption = '+'
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    if Me.hasIcon(vKey):
        if moTree.GetNodeIcon(vKey, Pic, bFullWidth):
            if bFullWidth:
                Me.Icon.Picture = Pic
                # potential error if Icon is nothing, let error abort
            else:
                Me.Control.Picture = Pic

def mctlCheckBox_Click():
    global moTree, Checked
    # PT new in 006PT2
    #-------------------------------------------------------------------------
    # Procedure : moCtl_Click
    # Author    : Peter Thornton
    # Created   : 20-01-2013
    # Purpose   : Event fires when a Checkbox label is clicked
    #-------------------------------------------------------------------------
    if moTree.EditMode(Me):
        # exit editmode if in editmode
        moTree.EditMode[Me] = False
    if mlChecked == 0:
        Checked = - 1
    else:
        Checked = 0
    if not moTree.ActiveNode is Me:
        moTree.ActiveNode = Me
        moTree.NodeEventRouter(Me, 'Caption', 1)
        # share the checkbox click event

def mctlControl_Click():
    global moLastActiveNode, moTree
    bFlag = Boolean()
    #-------------------------------------------------------------------------
    # Procedure : mctlControl_Click
    # Company   : JKP Application Development Services (c)
    # Author    : Jan Karel Pieterse (www.jkp-ads.com)
    # Created   : 15-01-2013
    # Purpose   : Event fires when a treebranch is clicked
    #-------------------------------------------------------------------------
    # PT the call to NodeClick will raise the click event to the form
    if not moLastActiveNode is None:
        moLastActiveNode.Control.BorderStyle = fmBorderStyleNone
        moLastActiveNode = None
        bFlag = True
    if moTree.ActiveNode is None:
        moTree.ActiveNode = Me
        bFlag = True
    elif not bFlag:
        bFlag = mctlControl.BorderStyle != fmBorderStyleNone
    if not moTree.ActiveNode is Me or bFlag:
        # only raise the event the first time the node is activated
        moTree.NodeEventRouter(Me, 'Caption', 1)
        # tvClick
        # if preferred the click event is always raised to the form (even if the
        # node was previously active) simply comment or remove this If/EndIf check

def mctlControl2_Click():
    # Hardi
    #-------------------------------
    mctlControl_Click()

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByVal 
def mctlControl_DblClick(Cancel):
    global moTree
    bDummy = Boolean()
    # PT  a node label has been double-clicked, enter edit-mode if manual editing is enabled
    if moTree.EnableLabelEdit(bDummy):
        moTree.EditMode[Me] = True
        EditBox(bEnterEdit=True)
    else:
        mctlExpander_Click()
        # Hardi: Added to open/close an child with a double click
        moTree.NodeEventRouter(Me, 'Caption', tvDblClick)
        # Hardi: Uncommented to be able to use the double click event

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Cancel - ByVal 
def mctlControl2_DblClick(Cancel):
    # 12.10.21: Hardi
    #-----------------------------------------------------------------------
    mctlControl_DblClick(Cancel)

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Button - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: X - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Y - ByVal 
def mctlControl_MouseDown(Button, Shift, X, Y):
    global moLastActiveNode, moTree
    bFlag = Boolean()
    #PT temporarily activate and highlight the MouseDown node and a grey border to the previous activenode
    #   MouseUp and Click events will confirm the action or reset the previous active node
    if moTree.ActiveNode is Me:
        bFlag = Me.Control.BackColor == vbHighlight
        # bFlag = bFlag Or Me.Control.BorderStyle = fmBorderStyleSingle
        # in Access this should be uncommented
    if not bFlag:
        moLastActiveNode = moTree.ActiveNode
        moTree.ActiveNode = Me
        if not moLastActiveNode is None:
            moLastActiveNode.Control.BorderStyle = fmBorderStyleSingle
            moLastActiveNode.Control.BorderColor = rgb(200, 200, 200)
    if moTree.EditMode(Me):
        # if any node is in edit mode exit edit mode
        moTree.EditMode[Me] = False
    # moTree.NodeEventRouter Me, "Caption", tvDown, Button, Shift, X, Y

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Button - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: X - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Y - ByVal 
def mctlControl_MouseUp(Button, Shift, X, Y):
    global moLastActiveNode, moTree
    bFlag = Boolean()

    bMouseIsOver = Boolean()

    bMoveCopy = Boolean()
    # PT MouseUp fires before the Click event, at this point we don't know 100% if user
    #    definately wants to activate the MouseDown node. If user drags the mouse off the MouseDown node the
    #    Click event will not fire which means user wants to cancel and revert to the previous activenode.
    #
    #    If MouseUp occurs with the cursor not over the node reset the original activenode
    if not moLastActiveNode is None:
        _with21 = Me.Control
        # is the mouse over the node or within a pixel of it
        bMouseIsOver = ( X >= - 1 and X <= _with21.Width + 1 )  and  ( Y >= - 1 and Y <= _with21.Height + 1 )
        if not bMouseIsOver:
            # if the last-activenode was marked for MoveCopy we will need to reset it
            bFlag = moLastActiveNode is moTree.MoveCopyNode(bMoveCopy)
            # reset the original activenode
            moLastActiveNode.Control.BorderStyle = fmBorderStyleNone
            moTree.ActiveNode = moLastActiveNode
            if bFlag:
                moTree.MoveCopyNode[bMoveCopy] = moLastActiveNode
            moLastActiveNode = None
        elif Button == 2:
            # the click event doesn't fire with right click so explicitly call it
            mctlControl_Click()
    # moTree.NodeEventRouter Me, "Caption", tvUp, Button, Shift, X, Y

def mctlExpander_Click():
    global Expanded, moTree
    #
    Expanded = not Expanded
    if moTree.EditMode(Me):
        # if any node is in edit mode exit edit mode
        moTree.EditMode[Me] = False
    moTree.NodeEventRouter(Me, 'Expander', 1)

def moEditBox_Change():
    global Caption, moTree
    i = Long()

    Ub = Long()

    lSelSt = Long()

    lRows = Long()

    ht = Single()

    wd = Single()

    sngMaxW = Single()

    sngMaxHt = Single()

    sngMaxR = Single()

    sngVisR = Variant()

    sngIdealL = Variant()

    sngIdealTop = Single()

    sEdit = String()

    splt = Variant()

    v = Variant()

    splt2 = Variant()

    bExit = Boolean()

    cPad = 6
    # PT resize horizontally & vertically to accommodate the changed text but restrict size to a bit less than the container frame
    #    Autosize is good for width only if multiline=false, but it's problematic to size both width & height to text without this fix
    if bExit:
        return
    # VB2PY (UntranslatedCode) On Error GoTo errH
    _with22 = moTree.TreeControl
    sngMaxW = _with22.InsideWidth - cPad
    sngMaxHt = IIf(_with22.ScrollHeight, _with22.ScrollHeight, _with22.InsideHeight) - cPad
    sngMaxR = IIf(_with22.ScrollWidth > _with22.InsideWidth, _with22.ScrollWidth, _with22.InsideWidth) - cPad
    sngVisR = _with22.ScrollLeft + _with22.InsideWidth
    sngIdealL = mctlControl.left - 1.5
    sngIdealTop = mctlControl.top - 1.5
    sEdit = moEditBox
    if InStr(1, sEdit, vbNewLine):
        splt = Split(sEdit, vbNewLine)
    elif InStr(1, sEdit, vbCr):
        splt = Split(sEdit, vbCr)
    elif InStr(1, sEdit, vbLf):
        splt = Split(sEdit, vbLf)
    else:
        splt = vbObjectInitialize((0,), Variant)
        splt[0] = sEdit
    Ub = UBound(splt)
    _with23 = moLabSizer
    _with23.Caption = 'A'
    ht = _with23.Height
    _with23.Caption = ''
    lRows = 1
    for i in vbForRange(0, Ub):
        splt2 = Split(splt(i), ' ')
        for v in splt2:
            _with23.Caption = _with23.Caption + v + ' '
            _with23.AutoSize = True
            if _with23.Width > sngMaxW - 9:
                lRows = lRows + 1
                _with23.Caption = v + ' '
                if _with23.Width > wd:
                    wd = _with23.Width
                    if _with23.Width > sngMaxW:
                        lRows = lRows + 1
            elif _with23.Width > wd:
                wd = _with23.Width
        if i < Ub:
            lRows = lRows + 1
            _with23.Caption = ''
    if _with23.Width > wd:
        wd = _with23.Width
    if wd + 15 > sngMaxW:
        wd = sngMaxW
    else:
        wd = wd + 15
    bExit = True
    _with24 = moEditBox
    if lRows > 1:
        _with24.AutoSize = True
        _with24.MultiLine = True
        lSelSt = _with24.SelStart
        _with24.SelStart = 0
        _with24.SelStart = lSelSt
        if ht * lRows + 9 > sngMaxHt:
            _with24.Height = sngMaxHt - 3
        else:
            _with24.Height = ht * lRows + 9
        if sngIdealTop + _with24.Height > sngMaxHt - 3:
            _with24.top = sngMaxHt - _with24.Height + 3
        else:
            _with24.top = sngIdealTop
        _with24.Width = wd
    else:
        _with24.MultiLine = False
        _with24.AutoSize = True
        _with24.MultiLine = True
        _with24.top = mctlControl.top - 1.5
    if sngIdealL + _with24.Width > sngMaxR:
        _with24.left = sngMaxR - _with24.Width + 3
    else:
        _with24.left = sngIdealL
    sngVisR = ( _with24.left + _with24.Width )  - sngVisR
    if sngVisR > 0:
        moTree.TreeControl.ScrollLeft = moTree.TreeControl.ScrollLeft + sngVisR
    bExit = False
    return
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1
    EditBox(False)
    # VB2PY (UntranslatedCode) Resume done

# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: KeyCode - ByVal 
# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: Shift - ByVal 
def moEditBox_KeyDown(KeyCode, Shift):
    global mvCaption, mctlControl, TextWidth, Control, moTree
    bCancel = Boolean()

    bSort = Boolean()

    bMultiLine = Boolean()

    sNewText = String()
    # PT Textbox key events to Enter or Esc the Editbox,   006PT2
    # PT ammended 026 to resize/reposition the editbox within the confines of the frame container
    #    remove any CR & LF to ensure the node label is a single line but retain line breaks in the property if bMultiLine
    if KeyCode == vbKeyReturn and Shift == 0:
        sNewText = moEditBox
        if sNewText == Me.Caption:
            KeyCode = vbKeyEscape
        else:
            # note: sNewText could be parsed where the RaiseAfterLabelEdit is received
            bCancel = moTree.RaiseAfterLabelEdit(Me, sNewText)
            if not bCancel:
                bCancel = moTree.EnableLabelEdit(bSort, bMultiLine)
                if InStr(1, sNewText, vbCr) or InStr(1, sNewText, vbLf):
                    ## VB2PY (CheckDirective) VB directive took path 1 on mac
                    #' Mac doesn't seem to use vbCrLf/vbNewLine, only vbCr or vbLf (?)
                    if bMultiLine:
                        Me.Caption = Replace(Replace(sNewText, vbCr, mcBreak), vbLf, mcBreak)
                    else:
                        Me.Caption = Replace(Replace(sNewText, vbCr, '  '), vbLf, '  ')
                    if bMultiLine:
                        # Drectly write the original multiline to the Caption, but don't use Let-Caption Property
                        mvCaption = sNewText
                else:
                    Me.Caption = sNewText
                mctlControl.WordWrap = False
                mctlControl.AutoSize = True
                TextWidth = mctlControl.Width
                if TextWidth < mcFullWidth and moTree.FullWidth:
                    Control.Width = mcFullWidth
                moTree.Changed = True
                if bSort:
                    if Me.ParentNode.Sort:
                        moTree.Refresh()
                moTree.SetScrollbars(True)
                # replaced moTree.SetScrollbars in 026
            EditBox(False)
    if KeyCode == vbKeyEscape:
        moTree.EditMode[Me] = False
        EditBox(False)

def class_initialize():
    global mbExpanded
    # default properties
    mbExpanded = True
    # default
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1

def __del__():
    global moTree
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1
    moTree = None


def setBackColor(lColor):
    global mlBackColor, mctlControl
    #PT if lColor is written as 0/black, change it to 1 as 0 means default
    mlBackColor = lColor
    if mlBackColor == 0:
        mlBackColor = 1
    if not mctlControl is None:
        mctlControl.BackColor = lColor

def getBackColor():
    global BackColor
    _fn_return_value = False
    _fn_return_value = mlBackColor
    # if zero the treecaller will apply the frame container's backcolor
    return _fn_return_value
BackColor = property(fset=setBackColor, fget=getBackColor)


def setBold(bBold):
    global mbBold, mctlControl
    mbBold = bBold
    if not mctlControl is None:
        mctlControl.Font.Bold = mbBold

def getBold():
    global Bold
    _fn_return_value = False
    _fn_return_value = mbBold
    return _fn_return_value
Bold = property(fset=setBold, fget=getBold)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: vCaption - ByVal 
def setCaption(vCaption):
    global mvCaption, mctlControl, msngTextWidth
    sngWd = Single()
    mvCaption = vCaption
    if not mctlControl is None:
        mctlControl.Caption = CStr(vCaption)
        if mctlControl.AutoSize:
            msngTextWidth = mctlControl.Width
        else:
            sngWd = mctlControl.Width
            mctlControl.AutoSize = True
            msngTextWidth = mctlControl.Width
            mctlControl.AutoSize = False

def getCaption():
    global Caption
    _fn_return_value = False
    _fn_return_value = mvCaption
    return _fn_return_value
Caption = property(fset=setCaption, fget=getCaption)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: vCaption - ByVal 
def setCaption2(vCaption):
    global mvCaption2, mctlControl2
    sngWd = Single()
    # Hardi
    mvCaption2 = vCaption
    if not mctlControl2 is None:
        mctlControl2.Caption = CStr(vCaption)
        ## VB2PY (CheckDirective) VB directive took path 2 on False

def getCaption2():
    global mvCaption2, Caption2
    _fn_return_value = False
    # Hardi
    if mvCaption2 == '':
        mvCaption2 = ' '
        # Otherwise the textbox is shown as "__" for some reasons
    _fn_return_value = mvCaption2
    return _fn_return_value
Caption2 = property(fset=setCaption2, fget=getCaption2)


def setChecked(vChecked):
    global mlChecked, moTree
    bFlag = Boolean()

    bTriState = Boolean()

    lChecked = Long()

    cChild = clsNode()
    # PT
    # Checked values are -1 true, 0 false, +1 mixed
    # if vChecked is a boolean Checked will coerce to -1 or 0
    # if vChecked is Null Checked is set as +1
    if P01.VarType(vChecked) == vbBoolean:
        lChecked = vChecked
    elif IsNull(vChecked):
        lChecked = 1
    elif vChecked >= - 1 and vChecked <= 1:
        lChecked = vChecked
    bFlag = lChecked != mlChecked
    mlChecked = lChecked
    if not mctlCheckBox is None and bFlag:
        moTree.Changed = True
        UpdateCheckbox()()
    if not moTree is None:
        # eg during clone
        bFlag = moTree.CheckBoxes(bTriState)
        if bTriState:
            if ParentNode.Caption != 'RootHolder':
                ParentNode.CheckTriStateParent()
            if not ChildNodes is None:
                for cChild in ChildNodes:
                    cChild.CheckTriStateChildren(mlChecked)

def getChecked():
    global Checked
    _fn_return_value = False
    # PT
    # Checked values are -1 true, 0 false, +1 mixed
    # If TriState is enabled be careful not to return a potential +1 to a boolean or it'll coerce to True
    _fn_return_value = mlChecked
    return _fn_return_value
Checked = property(fset=setChecked, fget=getChecked)


def getChild():
    global Child
    _fn_return_value = False
    # PT Returns a reference to the first Child node, if any
    # VB2PY (UntranslatedCode) On Error Resume Next
    _fn_return_value = mcolChildNodes(1)
    return _fn_return_value
Child = property(fget=getChild)


def setChildNodes(colChildNodes):
    global mcolChildNodes
    mcolChildNodes = colChildNodes

def getChildNodes():
    global ChildNodes
    _fn_return_value = False
    _fn_return_value = mcolChildNodes
    return _fn_return_value
ChildNodes = property(fset=setChildNodes, fget=getChildNodes)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: sControlTipText - ByVal 
def setControlTipText(sControlTipText):
    global msControlTipText, mctlControl
    msControlTipText = sControlTipText
    if not mctlControl is None:
        mctlControl.ControlTipText = msControlTipText

def getControlTipText():
    global ControlTipText
    _fn_return_value = False
    _fn_return_value = msControlTipText
    return _fn_return_value
ControlTipText = property(fset=setControlTipText, fget=getControlTipText)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: bExpanded - ByVal 
def setExpanded(bExpanded):
    global mbExpanded
    mbExpanded = bExpanded
    if not Me.Expander is None:
        UpdateExpanded(bControlOnly=False)
    elif not Me.Control is None:
        UpdateExpanded(bControlOnly=True)

def getExpanded():
    global Expanded
    _fn_return_value = False
    _fn_return_value = mbExpanded
    return _fn_return_value
Expanded = property(fset=setExpanded, fget=getExpanded)


def setForeColor(lColor):
    global mlForeColor, mctlControl
    #PT if lColor is written as 0/black, change it to 1 as 0 means default
    mlForeColor = lColor
    if mlForeColor == 0:
        mlForeColor = 1
    if not mctlControl is None:
        mctlControl.ForeColor = lColor

def getForeColor():
    global ForeColor
    _fn_return_value = False
    _fn_return_value = mlForeColor
    return _fn_return_value
ForeColor = property(fset=setForeColor, fget=getForeColor)


def getFirstSibling():
    global FirstSibling
    _fn_return_value = False
    if not moParentNode is None:
        # PT Root has no parent
        _fn_return_value = moParentNode.GetChild(1)
    return _fn_return_value
FirstSibling = property(fget=getFirstSibling)


def getLastSibling():
    global LastSibling
    _fn_return_value = False
    if not moParentNode is None:
        # PT Root has no parent
        _fn_return_value = moParentNode.GetChild(- 1)
        # -1 flags GetChild to return the last Child
    return _fn_return_value
LastSibling = property(fget=getLastSibling)


def setImageExpanded(vImageExpanded):
    global mvIconMainKey, mvIconExpandedKey, mlIconCnt
    # PT string name or numeric index for an expanded icon key
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    if not IsMissing(vImageExpanded):
        if not P01.IsEmpty(vImageExpanded):
            if Len(mvIconMainKey) == 0:
                mvIconMainKey = vImageExpanded
            mvIconExpandedKey = vImageExpanded
            mlIconCnt = 2

def getImageExpanded():
    global ImageExpanded
    _fn_return_value = False
    # PT string name or numeric index for the main icon key
    _fn_return_value = mvIconExpandedKey
    return _fn_return_value
ImageExpanded = property(fset=setImageExpanded, fget=getImageExpanded)


def setImageMain(vImageMain):
    global mvIconMainKey, mlIconCnt
    # PT string name or numeric index for the main icon key
    # VB2PY (UntranslatedCode) On Error GoTo errExit
    if not IsMissing(vImageMain):
        if not P01.IsEmpty(vImageMain):
            mvIconMainKey = vImageMain
            if mlIconCnt == 0:
                mlIconCnt = 1

def getImageMain():
    global ImageMain
    _fn_return_value = False
    # PT string name or numeric index for the main icon key
    _fn_return_value = mvIconMainKey
    return _fn_return_value
ImageMain = property(fset=setImageMain, fget=getImageMain)


# VB2PY (UntranslatedCode) Argument Passing Semantics / Decorators not supported: sKey - ByVal 
def setKey(sKey):
    global msKey
    bIsInMainCol = Boolean()

    i = Long()

    cTmp = clsNode()
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if Tree is None:
        msKey = sKey
        return
    elif msKey == sKey or Len(sKey) == 0:
        return
    # VB2PY (UntranslatedCode) On Error Resume Next
    cTmp = Tree.Nodes.item(sKey)
    # VB2PY (UntranslatedCode) On Error GoTo errH
    if not cTmp is None:
        Err.Raise(457)
        # standard duplicate key error
    # to change the Key, remove Me and add Me back where it was with the new key
    for cTmp in Tree.Nodes:
        i = i + 1
        if cTmp is Me:
            bIsInMainCol = True
            break
    if bIsInMainCol:
        _with12 = Tree.Nodes
        _with12.Remove(i)
        if i <= _with12.Count:
            _with12.Add(Me, sKey, i)
        else:
            _with12.Add(Me)
    else:
        # Let Key  called by via move/copy
        pass
    msKey = sKey
    return
    Err.Raise(Err.Number, 'Let Key', Err.Description)

def getKey():
    global Key
    _fn_return_value = False
    _fn_return_value = msKey
    return _fn_return_value
Key = property(fset=setKey, fget=getKey)


def getLevel():
    global Level
    _fn_return_value = False
    lLevel = Long()

    cNode = clsNode()
    # VB2PY (UntranslatedCode) On Error GoTo errH
    lLevel = - 1
    cNode = Me.ParentNode
    while not cNode is None:
        lLevel = lLevel + 1
        cNode = cNode.ParentNode
    _fn_return_value = lLevel
    return _fn_return_value
    ## VB2PY (CheckDirective) VB directive took path 2 on DebugMode = 1
    return _fn_return_value
Level = property(fget=getLevel)


def getNextNode():
    global NextNode
    _fn_return_value = False
    i = Long()

    cNode = clsNode()
    # can't name this proc 'Next' in VBA
    # PT return the next sibling if there is one
    _with13 = Me.ParentNode
    for cNode in _with13.ChildNodes:
        i = i + 1
        if cNode is Me:
            break
    if _with13.ChildNodes.Count > i:
        _fn_return_value = _with13.ChildNodes(i + 1)
    return _fn_return_value
NextNode = property(fget=getNextNode)


def setParentNode(oParentNode):
    global moParentNode
    moParentNode = oParentNode

def getParentNode():
    global ParentNode
    _fn_return_value = False
    _fn_return_value = moParentNode
    return _fn_return_value
ParentNode = property(fset=setParentNode, fget=getParentNode)


def getPrevious():
    global Previous
    _fn_return_value = False
    i = Long()

    cNode = clsNode()
    # PT return the previous sibling if there is one
    _with14 = Me.ParentNode
    for cNode in Me.ParentNode.ChildNodes:
        i = i + 1
        if cNode is Me:
            break
    if i > 1:
        _fn_return_value = _with14.ChildNodes(i - 1)
    return _fn_return_value
Previous = property(fget=getPrevious)


def getRoot():
    global Root
    _fn_return_value = False
    cTmp = clsNode()
    cTmp = Me
    while not cTmp.ParentNode.ParentNode is None:
        cTmp = cTmp.ParentNode
    _fn_return_value = cTmp
    return _fn_return_value
Root = property(fget=getRoot)


def settag(vTag):
    global mvTag
    mvTag = vTag

def gettag():
    global tag
    _fn_return_value = False
    _fn_return_value = mvTag
    return _fn_return_value
tag = property(fset=settag, fget=gettag)


def setControl(ctlControl):
    global mctlControl
    mctlControl = ctlControl
    if not mctlControl is None:
        if not moTree is None:
            mctlControl.Font = moTree.TreeControl.Font
        else:
            Stop()

def getControl():
    global Control
    _fn_return_value = False
    _fn_return_value = mctlControl
    return _fn_return_value
Control = property(fset=setControl, fget=getControl)


def setControl2(ctlControl):
    global mctlControl2
    # Hardi
    mctlControl2 = ctlControl
    if not mctlControl2 is None:
        if not moTree is None:
            mctlControl2.Font = moTree.TreeControl.Font
            #mctlControl2.Font.Bold = True
            # 19.10.21: Hardi
        else:
            Stop()

def getControl2():
    global Control2
    _fn_return_value = False
    # Hardi
    _fn_return_value = mctlControl2
    return _fn_return_value
Control2 = property(fset=setControl2, fget=getControl2)


def setIndex(idx):
    global mnIndex
    # PT Index: the order this node was added to Treeview's collection mcolNodes
    #    Index will never increase but may decrement if previously added nodes are removed
    mnIndex = idx

def getIndex():
    global Index
    _fn_return_value = False
    # PT
    _fn_return_value = mnIndex
    return _fn_return_value
Index = property(fset=setIndex, fget=getIndex)


def setVisIndex(lVisIndex):
    global mlVisIndex
    mlVisIndex = lVisIndex

def getVisIndex():
    global VisIndex
    _fn_return_value = False
    # PT
    _fn_return_value = mlVisIndex
    return _fn_return_value
VisIndex = property(fset=setVisIndex, fget=getVisIndex)


def setTree(oTree):
    global moTree
    moTree = oTree

def getTree():
    global Tree
    _fn_return_value = False
    _fn_return_value = moTree
    return _fn_return_value
Tree = property(fset=setTree, fget=getTree)


def setCheckbox(oCtl):
    global mctlCheckBox
    mctlCheckBox = oCtl

def getCheckbox():
    global Checkbox
    _fn_return_value = False
    _fn_return_value = mctlCheckBox
    return _fn_return_value
Checkbox = property(fset=setCheckbox, fget=getCheckbox)


def setExpander(ctlExpander):
    global mctlExpander
    mctlExpander = ctlExpander

def getExpander():
    global Expander
    _fn_return_value = False
    _fn_return_value = mctlExpander
    return _fn_return_value
Expander = property(fset=setExpander, fget=getExpander)


def setExpanderBox(ctlExpanderBox):
    global mctlExpanderBox
    mctlExpanderBox = ctlExpanderBox

def getExpanderBox():
    global ExpanderBox
    _fn_return_value = False
    _fn_return_value = mctlExpanderBox
    return _fn_return_value
ExpanderBox = property(fset=setExpanderBox, fget=getExpanderBox)


def setHLine(ctlHLine):
    global mctlHLine
    mctlHLine = ctlHLine

def getHLine():
    global HLine
    _fn_return_value = False
    _fn_return_value = mctlHLine
    return _fn_return_value
HLine = property(fset=setHLine, fget=getHLine)


def setIcon(ctlIcon):
    global mctlIcon
    mctlIcon = ctlIcon

def getIcon():
    global Icon
    _fn_return_value = False
    _fn_return_value = mctlIcon
    return _fn_return_value
Icon = property(fset=setIcon, fget=getIcon)


def setTextWidth(sngTextWidth):
    global msngTextWidth
    msngTextWidth = sngTextWidth

def getTextWidth():
    global TextWidth
    _fn_return_value = False
    _fn_return_value = msngTextWidth
    return _fn_return_value
TextWidth = property(fset=setTextWidth, fget=getTextWidth)


def setVLine(ctlVLine):
    global mctlVLine
    mctlVLine = ctlVLine

def getVLine():
    global VLine
    _fn_return_value = False
    _fn_return_value = mctlVLine
    return _fn_return_value
VLine = property(fset=setVLine, fget=getVLine)

# VB2PY (UntranslatedCode) Option Explicit
