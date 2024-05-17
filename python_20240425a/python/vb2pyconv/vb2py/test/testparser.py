# -*- coding: latin-1 -*-

#
# Turn off logging in extensions (too loud!)
import vb2py.extensions
vb2py.extensions.disableLogging()

from vb2py.vbparser import buildParseTree, VBParserError

#
# Set some config options which are appropriate for testing
import vb2py.config
Config = vb2py.config.VB2PYConfig()
Config.setLocalOveride("General", "ReportPartialConversion", "No")

import unittest


tests = []
vb_dot_net_tests = []


# Simple assignments
tests.append("""
a = 10
b = 20+30
c = "hello there"
oneVal = 10
twoVals = Array(10,20)
functioncall = myfunction.mymethod(10)
a = this._30that
""")


# Set type assignments
tests.append("""
Set a = myobject
Set b = myobject.subobject
Set obj = function(10, 20, 30+40)
""")


# Set type assignments with "New" objects
tests.append("""
Set a = New myobject
Set b = New myobject.subobject
""")

# Assignments with tough parenthesis
tests.extend([
        "d=(((4*5)/2+10)-10)",
])

# Assignments with tough string quotes
tests.extend([
        'd="g""h""j"""',
])

# Assignments with tough strings in general
tests.extend([
        r'a="\"',  # The single slash is a killer
])

# Simple expressions
tests.extend([
'a = 10',
'a = 20+30',
'a = "hello there"',
'a = 10',
'a = Array(10,20)',
'a = myfunction.mymethod(10)',
'a = &HFF',
'a = &HFF00000L',
'a = &HFF&',
'a = #1/10/2000#',
'a = #1/10/2000 11:59#',
'a = #1/10/2000 11:59:12#',
'a = #1/10/2000 11:59:12 PM#',
'a = #1/10/2000 11:59:12 AM#',
'a = #11:59:12 AM#',
'a = #11:59:12#',
'a = #1/10#',
'a = 1#',
'a = 1.#',
'a = 1.2#',
'a = 10 Mod 2',
'a = 1000!',
'a = "12!12"',
'a = "=VLOOKUP(RC[-4],[Temp2.xlsx]Sheet1!C3C55,38,0)"',
'Range("X1").Select\nActiveWorkbook.Names.Add Name:="scrollx1", RefersToR1C1:="=OFFSET(All_logs!R2C19:R120C19,All_logs!R1C22,0,All_logs!R1C24,1)"',
])


# Nested expressions
tests.extend(["a = 10+(10+(20+(30+40)))",
              "a = (10+20)+(30+40)",
              "a = ((10+20)+(30+40))",
])

# Conditional expressions
tests.extend(["a = a = 1",
              "a = a <> 10",
              "a = a > 10",
              "a = a < 10",
              "a = a <= 10",
              "a = a >= 10",
              "a = a = 1 And b = 2",
              "a = a = 1 Or b = 2",
              "a = a Or b",
              "a = a Or Not b",
              "a = Not a = 1",
              "a = Not a",
              "a = a Xor b",
              "a = b Is Nothing",
              "a = b \ 2",
              "a = b Like c",
              'a = "hello" Like "goodbye"',
              'a = x Imp b',
])


# Things that failed
tests.extend([
            "a = -(x*x)",
            "a = -x*10",
            "a = 10 Mod 6",
            "Set NewEnum = mCol.[_NewEnum]",
            "a = 10 ^ -bob",
])

# Functions
tests.extend([
            "a = myfunction",
            "a = myfunction()",
            "a = myfunction(1,2,3,4)",
            "a = myfunction(1,2,3,z:=4)",
            "a = myfunction(x:=1,y:=2,z:=4)",
            "a = myfunction(x:=1,y:=2,z :=4)",
            "a = myfunction(b(10))",
])

# String Functions
tests.extend([
            'a = Trim$("hello")',
            'a = Left$("hello", 4)',
])			

# Things that failed
tests.extend([
            "a = -(x*x)",
            "a = -x*10",
            "a = 10 Mod 6",
])

# Address of
tests.extend([
        "a = fn(AddressOf fn)",
        "a = fn(a, b, c, AddressOf fn)",
        "a = fn(a, AddressOf b, AddressOf c, AddressOf fn)",
        "a = fn(a, AddressOf b.m.m, AddressOf c.k.l, AddressOf fn)",
        "a = AddressOf b",
        "DoIt AddressOf b",
        "DoIt AddressOf b, That",
        "DoIt This, AddressOf b",
])

# Type of
tests.extend([
        "a = fn(TypeOf fn)",
        "a = fn(a, b, c, TypeOf fn)",
        "a = fn(a, TypeOf b, TypeOf c, TypeOf fn)",
        "a = fn(a, TypeOf b.m.m, TypeOf c.k.l, TypeOf fn)",
        "a = TypeOf Control Is This",
        "a = TypeOf Control Is This Or TypeOf Control Is That",])

# Using ByVal and ByRef in a call or expression
tests.extend([
'a = fn(ByVal b)',
'a = fn(x, y, z, ByVal b)',
'a = fn(x, y, z, ByVal b, 10, 20, 30)',
'a = fn(ByVal a, ByVal b, ByVal c)',
'a = fn(ByRef b)',
'a = fn(x, y, z, ByRef b)',
'a = fn(x, y, z, ByRef b, 10, 20, 30)',
'a = fn(ByRef a, ByRef b, ByRef c)',
'fn ByVal b',
'fn x, y, z, ByVal b',
'fn x, y, z, ByVal b, 10, 20, 30',
'fn ByVal a, ByVal b, ByVal c',
'fn ByRef b',
'fn x, y, z, ByRef b',
'fn x, y, z, ByRef b, 10, 20, 30',
'fn ByRef a, ByRef b, ByRef c',
])

# Using New in a call
tests.extend([
    'fn(New A)',
    'fn(a, b, New C, New D)',
    'a = fn(New A)',
    'b = fn(a, b, New C, New D)',
])

# One line comments
tests.append("""
a = 10
' b = 20+30
' c = "hello there"
' oneVal = 10
twoVals = Array(10,20)
' functioncall = myfunction.mymethod(10)
""")

# One line comments with Rem
tests.append("""
a = 10
Rem b = 20+30
Rem not needed c = "hello there"
Rem opps oneVal = 10
twoVals = Array(10,20)
Rem dont do this anymore functioncall = myfunction.mymethod(10)
""")
tests.append('REM')
tests.append('1 REM')

# In-line comments
tests.append("""
a = 10
b = 20+30 ' comment
c = "hello there" ' another comment
oneVal = 10 ' yet another comment
twoVals = Array(10,20)
functioncall = myfunction.mymethod(10)
""")

# In-line comments with Rem
tests.append("""
a = 10
b = 20+30 Rem comment
c = "hello there" Rem another comment
oneVal = 10 Rem yet another comment
twoVals = Array(10,20)
functioncall = myfunction.mymethod(10)
""")

# Things which aren't comments
tests.append("""
a = "hello, this might ' look like ' a comment ' "
b = "wow there are a lot of '''''''' these here"
""")

# tough inline comments
tests.extend([
    "Public a As Integer ' and a comment"
])

# comments and colons in awkward places
tests.extend([
"""
If Len(l0022) = 0 Then Beep: Exit Sub
""",

"""
If a =0 Then ' nasty comment
    b=1
End If ' other nasty comment
""",

"""
While a<0 ' nasty comment
    b=1
Wend ' other nasty comment
""",

"""
While A = 1
    Exit While
End While
""",

"""
Select Case a ' nasty comment
Case 10 ' oops
    b=1
Case Else ' other nasty comment
    b = 2
End Select ' gotcha
""",

"""
For i = 0 To 100 ' nasty comment
    b=1
Next i ' other nasty comment
""",

"""
Sub a() ' nasty comment
    b=1
End Sub ' other nasty comment
""",

"""
Function f() ' nasty comment
    b=1
End Function ' other nasty comment
""",

"""
Sub a():
    b=1
End Sub 
""",


"""
Sub a()
    b=1
End Sub: 
""",

"""
Sub a
    b=12
End Sub 
""",


"""
Function a
    b=1
End Function
""",

])

tests.append('If A Then\nDoIt\nElse:\nDoOther\nEnd If')
tests.append('If A Then:\nDoIt\nElse:\nDoOther\nEnd If')
tests.append('If A Then\nDoIt\nElse:\nDoOther\nEnd If:')


# Directives
tests.extend([
    "' VB2PY-Set General.Blah = Yes",
    "' VB2PY-Set General.Blah = ___",
    "' VB2PY-Unset General.Blah",
    "' VB2PY-Add: General.Option = 10",
])

# Two line continuations
tests.append("""
a = _
10 + 20 + 30
b = 10/ _
25
c = (one + _
     two + three)
""")

# Milti-line continuations
tests.append("""
a = _
      10 + 20 + 30 _
    * 10/ _
      25
c = (one + _
     two + three) * _
     four.five()
""")

tests.extend(["""
Private Declare Function GetTempPathA Lib "kernel32" _
 (ByVal nBufferLength As Long, ByVal lpBuffer As String) As Long
""",
"""
Function GetTempPathA _
(ByVal nBufferLength As Long, ByVal lpBuffer As String) As Long
End Function
""",

])

# Continuation before a comma
tests.append('Private A, B _\n , C as String')

# Simple dims
tests.extend([
        "Dim A",
        "Dim B As String",
        "Dim variable As Object.OtherObj",
        "Dim Var As Variant",
        "Dim A As String * 100",
        "Dim A (10)",
])

# Dims with New
tests.extend([
        "Dim A As New Object",
        "Dim B As New Collection",
])

# Multiple dims on one line
tests.extend([
        "Dim A, B, C, D, E, F",
        "Dim A ,B As Collection",
        "Dim B As String, B As Long, B As Integer, B As String, B As String",
        "Dim variable As Object.OtherObj, B, C, D, E",
        "Dim Var As Variant",
        "Dim A, B, C As New Collection",
        "Dim E As New Collection, F As New Object, F, G",
        "Dim H As New Object, G As New Object",
])

# Array type dims
tests.extend([
        "Dim A()",
        "Dim B(10, 20, 30) As String",
        "Dim variable() As Object.OtherObj",
        "Dim Var(mysize) As Variant",
])

# Scoped dims
tests.extend([
        "Public A",
        "Private B As String",
        "Private A, B, C, D, E, F",
        "Private B As String, B As Long, B As Integer, B As String, B As String",
        "Private variable As Object.OtherObj, B, C, D, E",
        "Public Var As Variant",
])

# Static dims
tests.extend([
        "Static A",
        "Static B As String",
        "Static A, B, C, D, E, F",
        "Static B As String, B As Long, B As Integer, B As String, B As String",
        "Static variable As Object.OtherObj, B, C, D, E",
        "Static Var As Variant",
])

# Arrays
tests.extend([
    "Dim a(10)",
    "Dim a(0)",
    "Dim a(0), b(20), c(30)",
    "Dim a(10+20)",
    "Dim a(10+20, 1+3)",
    "Dim a(1 To 10)",
    "Dim a(1 To 10, 5 To 20)",
])

# Redims
tests.extend([
    "ReDim a(10)",
    "ReDim a(0)",
    "ReDim Preserve a(20)",
    "ReDim a(0), b(20), c(30)",
    "ReDim Preserve a(20), b(20)",
    "ReDim a(10+20)",
    "ReDim a(10+20, 1+3)",
    "ReDim a(1 To 10)",
    "ReDim a(1 To 10, 5 To 20)",
])


# Define in dim statements
tests.extend([
    "Dim A = 1234",
])
# Complex examples
tests.extend([
"""
With Obj
    ReDim .Child(10)
End With
""",
"Dim A(10).B(10)",
"Dim A(10).B.C(10) As Object",
])

# Constants with different types
tests.extend([
    "Const a = 10",
    'Const a = "Hello"',
    "Const a = &HA1",
    "Const a = 1#",
    "Const a = 1%",
    "Const a = 1&",
    "Const a = 1@",
    "Const a = 0.01@ + 0.02@",
    "#Const a = 123",
    "Public Const a = 10",
    'Public Const a = "Hello"',
    "Public Const a = &HA1",
    "Public Const a = 1#",
    "Public Const a = 1%",
    "Public Const a = 1&",
    "Private Const a = 10",
    'Private Const a = "Hello"',
    "Private Const a = &HA1",
    "Private Const a = 1#",
    "Private Const a = 1%",
    "Private Const a = 1&",
    "Private Const a! = 1",
])

# Constants
tests.extend([
        "Const A = 20",
        'Const B = "one"',
        "Private Const A = 1234.5 + 20",
        "Const a=10, b=20, c=30",
        "Private Const a=10, b=20, d=12345",
])

# Typed Constants
tests.extend([
        "Const A As Long = 20",
        'Const B As String = "one"',
        "Private Const A As Single = 1234.5 + 20",
        'Const a As Integer = 10, b As String = "hello", c As String * 10 = 43',
        'Private Const a As Integer = 10, b As String = "hello", c As String * 10 = 43',
])

# Odds and ends
tests.extend([
"Private WithEvents A As Button",
])

# Bare calls
tests.extend([
        "subr",
        "object.method",
        "object.method.method2.method",
])

# Explicit bare calls
tests.extend([
        "Call subr",
        "Call object.method",
        "Call object.method.method2.method",
])

# Bare calls with arguments
tests.extend([
        "subr 10, 20, 30",
        "object.method a, b, c+d, e",
        'object.method.method2.method 10, "hello", "goodbye" & name',
])

# Explicit Bare calls with arguments
tests.extend([
        "Call subr 10, 20, 30",
        "Call object.method a, b, c+d, e",
        'Call object.method.method2.method 10, "hello", "goodbye" & name',
])

# Explicit calls with arguments
tests.extend([
        "Call subr(10, 20, 30)",
        "Call object.method(a, b, c+d, e)",
        'Call object.method.method2.method(10, "hello", "goodbye" & name)',
        "Call subr()",
])

# Bare calls with arguments and functions
tests.extend([
        "subr 10, 20, 30",
        "object(23).method a, b, c+d, e",
        'object.method(5, 10, 20).method2.method 10, "hello", "goodbye" & name',
])

# Bare calls with named arguments and functions
tests.extend([
        "subr 10, 20, z:=30",
        "object(23).method one:=a, two:=b, three:=c+d, four:=e",
        'object.method(5, 10, 20).method2.method 10, "hello", two:="goodbye" & name',
])

# Bare calls with ommitted arguments
tests.extend([
        "subr 10, , 30",
        "subr ,,,,0",
        "subr 10, , , , 5",
])

# Subroutines and functions with ParamArray
tests.append('''
Sub A(X, Y, ParamArray Z() As String)
    DoIt(Z)
End Sub
''')

tests.append('''
Sub A(X, Y, ParamArray Z() As Integer)
    DoIt(Z)
End Sub
''')

tests.append('''
Sub A(X, Y, ByVal ParamArray Z() As Integer)
    DoIt(Z)
End Sub
''')

tests.append('''
Function A(X, Y, ByVal ParamArray Z() As Integer)
    DoIt(Z)
End Function
''')

# labels
tests.extend([
    "label:",
    "label20:",
    "20:",
    "label: a=1",
    "20: a=1",
    "101: doit",
    "101:\ndoit",
    "102: doit now",
    "103: doit now, for, ever",
])

# Label begining with loop
tests.append('''
Do
LoopAgain:
a = 1
Loop
''')


# Goto's
tests.extend([
    "GoTo Label",
    "GoTo 20",
    "GoTo Label:",
    "GoTo 20:",
])

# Structures with labels
tests.extend([
"""
101: If a < 10 Then
102:		b=1
103: End If
""",

"""
101: While a < 0
102:		b=1
103: Wend
""",

"""
101: Select Case a
102:		Case 10
103:			b= 1
104:		Case Else
105:			b=2
103: End Select
""",

"""
101: For i = 0 To 100
102:		b=1
103: Next i
""",

"""
101: Sub a()
102:		b=1
103: End Sub
""",

])

# Numeric labels don't even need a ':' ... aarg!
tests.extend([
"""
101 If a < 10 Then
102		b=1
103 End If
""",

"""
101 While a < 0
102		b=1
103 Wend
""",

"""
101 Select Case a
102		Case 10
103			b= 1
104		Case Else
105			b=2
103 End Select
""",

"""
101 For i = 0 To 100
102		b=1
103 Next i
""",

"""
101 Sub a()
102		b=1
103 End Sub
""",

])

# simple multi-line statements
tests.extend([
    "a = 10: b = 20",
    "a = 10: b = 20: c=1: d=1: e=2",
    "a=10:",
    "a=10: b=20:",
])

# Blocks on a line
tests.extend([
    "For i = 0 To 10: b=b+i: Next i",
    "If a > b Then a = 10: b = 20"
])

# For with something on the line and a block following
tests.append("""
For i = 1 To 10: DoIt
    DoIt2 = 1
Next i
""")


# Bug #809979 - Line ending with a colon fails 
tests.extend([
    "a = 10:\nb = 20",
    "a = 10: b = 20:\nc=1: d=1: e=2",
    "a=10:\nb=20:\nc=1",
])

# open statements
tests.extend([
    "Open fn For Output As 12",
    "Open fn For Output As #12",
    "Open fn For Input As 12",
    "Open fn For Input As #12",
    "Open fn.gk.gl() For Input As #NxtChn()",
    "Open fn For Append Lock Write As 23",
    "Open fn For Random As 23 Len = 1234",
    "Close 1",
    "Close #1",
    "Close channel",
    "Close #channel",
    "Close",
    "Close\na=1",
    "Closet = 10",
])


# Bug #810968 Close #1, #2 ' fails to parse 
tests.extend([
    "Close #1, #2, #3, #4",
    "Close 1, 2, 3, 4",
    "Close #1, 2, #3, 4",
    "Close #one, #two, #three, #four",
    "Close one, two, three, four",
    "Close #1,#2,#3,#4",
    "Close   #1   ,   #2   ,   #3   ,   #4   ",
])

# print# statements
tests.extend([
    "Print 10",
    "Print #1, 10",
    "Print 10, 20, 30;",
    "Print #1, 10, 20, 30;",
    "Print #1, 10; 20; 30;",
    "Print #1, 10; 20; 30; 40, 50, 60, 70; 80; 90",
    "Print 10, 20, 30,",
    "Print 10, 20, 30",
    "Print",
    "Print ;;;",
    "Print ,,,",
    "Print 1,,,2,,,3,,,;",
    "Print #3,",
    "Print #3,;;;",
    "Print #3,,,",
    "Print #3,1,,,2,,,3,,,;",
])

# get# statements
tests.extend([
    "Get #1, a, b",
    "Get #1, , b",
])

# input # statements
tests.extend([
    "Input #1, a, b",
    "Input #1, b",
    "a = Input(20, #3)",
    "a = Input(20, #id)",
])

# line input # statements
tests.extend([
    "Line Input #1, b",
])


# Seek
tests.extend([
    "Seek #filenum, value",
    "10: Seek #filenum, value",
    "10: Seek #filenum, value ' comment",
    "Seek #filenum, value ' comment",
    "Seek filenum, value",
    "10: Seek filenum, value",
    "10: Seek filenum, value ' comment",
    "Seek filenum, value ' comment",
])

tests.extend([
    'Private Declare Function FileTimeToSystemTime Lib "kernel32" (ftFileTime As FILETIME, stSystemTime As SYSTEMTIME) As Long',
    'Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)',
    'Private Declare Function GetFileAttributes Lib "kernel32" Alias "GetFileAttributesA" (ByVal lpFileName As String) As Long',
    'Private Declare Function GetFileAttributes Lib "kernel32" _ \n(ByVal lpFileName As String) As Long',
    'Private Declare Function GetFileAttributes Lib "kernel32" _ \n(ByVal lpFileName As String, A) As Long',
    'Private Declare Function GetFileAttributes Lib "kernel32" _ \n(ByVal lpFileName As String , A) As Long',
    'Private Declare Function GetFileAttributes Lib "kernel32" _ \n(ByVal lpFileName As String ) As Long',
])

# General on error goto
tests.extend([
    "On Error GoTo 100",
    "On Error GoTo ErrTrap",
    "On Error GoTo 100 ' comment",
    "On Error GoTo ErrTrap ' comment",
    "100: On Error GoTo 100",
    "label: On Error GoTo ErrTrap",
    "100: On Error GoTo 100 ' comment",
    "label: On Error GoTo ErrTrap ' comment",
])

# General on error resume next
tests.extend([
    "On Error Resume Next",
    "On Error Resume Next ' comment",
    "100: On Error Resume Next",
    "label: On Error Resume Next",
    "100: On Error Resume Next ' comment",
    "label: On Error Resume Next ' comment",
])

# General on error goto - 
tests.extend([
    "On Error GoTo 0",
    "On Error GoTo 0 ' comment",
    "100: On Error GoTo 0",
    "100: On Error GoTo 0 ' comment",
])


# On something goto list 
tests.extend([
    "On var GoTo 20",
    "On var GoTo 10,20,30,40",
])

# Resume
tests.extend([
    "label: Resume Next",
    "Resume Next",
    "label: Resume Next ' Comment",
    "label: Resume 7",
    "Resume 7",
    "label: Resume 7 ' Comment",
    "label: Resume",
    "Resume\na=1",
    "label: Resume' Comment",
])

# General on local error resume next
tests.extend([
    "On Local Error Resume Next",
    "On Local Error Resume Next ' comment",
    "100: On Local Error Resume Next",
    "label: On Local Error Resume Next",
    "100: On Local Error Resume Next ' comment",
    "label: On Local Error Resume Next ' comment",
])

# Bug #809979 - On Error with : after the label fails 
tests.extend([
    "On Error GoTo 0:\na=1",
    "On Error GoTo 0: ' comment",
    "100: On Error GoTo 0:\na=1",
    "100: On Error GoTo 0: ' comment",
    "On Error GoTo lbl:\na=1",
    "On Error GoTo lbl: ' comment",
    "100: On Error GoTo lbl:\na=1",
    "100: On Error GoTo lbl: ' comment",
])

# Lines
tests.extend([
        "Line (10,20)-(30,40), 10, 20",
        "obj.Pset (10, 20), RGB(1,2,2)",
])

# Move
tests.extend([
        "Move (Screen.Width - Width) / 2, (Screen.Height - Height) / 2",
])

# General name test (rename a file)
tests.extend([
        "Name file As otherfile",
        "Name file & extension As otherfile",
        "Name file & extension As otherfile & otherextension",
        'Name path & "\origname.txt" As path & "\knewname.txt"',
])

# Attributes at the head of a file
tests.extend([
    'Attribute VB_Name = "frmMain"',
    'Attribute VB_GlobalNameSpace = False',
    'Attribute VB_Creatable = False',
    'Attribute VB_PredeclaredId = True',
    'Attribute VB_Exposed = False',
    'Attribute Me.VB_Exposed = False',
    'Attribute Me.VB_Exposed = False, 1, 2, 3, 4',
    'Attribute Me.VB_Exposed = False, "1", "2, 3,", 4',
])

# Attributes at the head of a file
tests.extend([
"""
Enum thing
    _one = 1
    _two = 2
    _three = 3
    _four = 4
End Enum
""",
"""
Enum thing
    _one
    _two
    _three
    _four
End Enum
""",
"""
Public Enum Stats
xStrength = 1
Endurance
xIntelligence
Agility
Spirit
Stat_count
End Enum
""",
    """
Public Enum Stats As Integer
xStrength = 1
Endurance
xIntelligence
Agility
Spirit
Stat_count
End Enum
"""
])

# Types
tests.extend([
"""
Private Type ShellFileInfoType
 hIcon As Long
 iIcon As Long
 dwAttributes As Long
 szDisplayName As String * 260
 szTypeName As String * 80
End Type
"""
])

# The Option statement
tests.extend([
"Option Base 0",
"Option Base 1",
"Option Explicit",
"Option String Compare",
"Option String Compare Text",
])

# The End statement
tests.extend([
"10: End",
"End",
"End ' wow this is it",
"10: End ' this is the end",
])

# If with an 'End' in there
tests.append("""
If a = 10 Then
    End
End If
""")

# If without a then
tests.append("""
If some_logical_construct 
    b = 10
End If
""")

# If block with an inline in there too
tests.append("""
If some_logical_construct 
    b = 10
    ElseIf b = 2 Then x = 3
End If
""")

# The very odd Then else
tests.append('If IsBadCodePtr(lngMethod) = 0 Then Else A = 1')
tests.append('''
If A = 1 Then Else
    B = 1
End If
''')

tests.append("""
If A Or Not (B = 1) Then C = 1
""")

tests.append("""
If c = 2 Then ' bottom centered

ElseIf c = 5 Then ' comment
    a = 1
End If
""")

tests.append("""
If c = 2 Then ' bottom centered

ElseIf c = 5 Then D
End If
""")

# Sub with an 'End' in there
tests.append("""
Sub doit()
 End
End Sub
""")

# Fn with an 'End' in there
tests.append("""
Function doit()
 End
End Function
""")

# With with an 'End' in there
tests.append("""
With obj
 End
End With
""")

# The Event statement
tests.extend([
"Event doit()",
"Public Event doit()",
"Private Event doit()",
"Public Event doit(a, b, c, e)",
"Public Event doit(a As Integer, b As Long, c(), e As Command.Button)",
])

# The Debug.Print statement
tests.extend([
"Debug.Print",
"Debug.Print a",
"Debug.Print a,b",
"Debug.Print a;b",
"Debug.Print a+10;b+20",
"Debug.Print a+20, b-20",
"Debug.Print a;b;",
])

# Recordset notation
tests.extend([
"RS!diskID = DriveID",
"RS!diskID = DriveID+10",
'RS!diskID = "DriveID"',
"nice_view_water release & ![schema], nFileNum, ![schema_short]",
])

# Implicit Range identifiers
tests.extend([
"Worksheet.[A1].Select",
"A = Worksheet.[A1].Value",
"A = Worksheet.[1:10].Value",
"Worksheet.[value]",
"With worksheet\n\t.[1:10] = 5\nEnd With",
])

# Unicode
tests.extend([
'cIÅ  = 10',
'a = cIÅ + 30',
'a = "cIÅ there"',

])

# Unicode sub
tests.append("""
Sub cIÅ()
a=10
n=20
c="hello"
End Sub
""")

# Simple If
tests.append("""
If a = 10 Then
    b = 20
End If
If c < 1 Then
    d = 15
End If
""")

# Empty If
tests.append("""
If a = 10 Then
End If
""")

# Empty If with comments
tests.append("""
If a = 10 Then ' comment here
End If
""")

# If with no spaces
tests.append("""
If(a = 10) Then ' comment here
End If
""")
tests.append('If(A=1) Then DoIt')

# Simple If with And/Or
tests.append("""
If a = 10 And k = "test" Then
    b = 20
End If
If c < 1 Or d Then
    d = 15
End If
""")

# Simple If with compount And/Or expression
tests.append("""
If (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    b = 20
End If
If (c < 1) Or d And e = "hello" Or e < "wow" Then
    d = 15
End If
""")

#  If Not
tests.append("""
If Not a = 10 Then
    b=2
End If
""")

#  If With labels and comment
tests.append("""
10: If Not a = 10 Then 'heres a comment
20:   	b=2  ' antoher here
30: End If ' here too
""")

# Simple If/Else
tests.append("""
If a = 10 Then
    b = 20
Else
    b = 10
End If
If c < 1 Then
    d = 15
Else
    d = -12
End If
""")

# Empty If/Else
tests.append("""
If a = 10 Then
Else
End If
""")

# Simple If with And/Or
tests.append("""
If a = 10 And k = "test" Then
    b = 20
Else
    b = 1234
End If
If c < 1 Or d Then
    d = 15
Else
    e = "hello"
End If
""")

# Simple If with compount And/Or expression
tests.append("""
If (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    b = 20
Else
    g = 12
End If
If (c < 1) Or d And e = "hello" Or e < "wow" Then
    d = 15
Else
    h = 1234
End If
""")

# Simple If/Else
tests.append("""
If a = 10 Then
    b = 20
ElseIf a < 10 Then
    b = 10
End If
If c < 1 Then
    d = 15
ElseIf c = 1 Then
    d = -12
End If
""")


# Simple If with And/Or
tests.append("""
If a = 10 And k = "test" Then
    b = 20
ElseIf b = -102 Then
    b = 1234
End If
If c < 1 Or d Then
    d = 15
ElseIf e = Myfunction Then
    e = "hello"
End If
""")

# Simple If with compount And/Or expression
tests.append("""
If (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    b = 20
ElseIf (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    g = 12
End If
If (c < 1) Or d And e = "hello" Or e < "wow" Then
    d = 15
ElseIf k < 43 Then
    h = 1234
End If
""")

# Simple If/Else
tests.append("""
If a = 10 Then
    b = 20
ElseIf a < 10 Then
    b = 10
Else
    b = 1111
End If
If c < 1 Then
    d = 15
ElseIf c = 1 Then
    d = -12
Else
    d = "wow"
End If
""")


# Simple If with And/Or
tests.append("""
If a = 10 And k = "test" Then
    b = 20
ElseIf b = -102 Then
    b = 1234
Else
    b = 4321
End If
If c < 1 Or d Then
    d = 15
ElseIf e = Myfunction Then
    e = "hello"
Else
    g = 1
End If
""")

# Simple If with compount And/Or expression
tests.append("""
If (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    b = 20
ElseIf (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    g = 12
Else
    k = 3234
End If
If (c < 1) Or d And e = "hello" Or e < "wow" Then
    d = 15
ElseIf k < 43 Then
    h = 1234
Else
    doIt
End If
""")

# Simple Nested If
tests.append("""
If a = 10 Then
    b = 20
    If c < 1 Then
        d = 15
    End If
End If
""")


# Complex nested If
tests.append("""
If (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    b = 20
ElseIf (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    If (c < 1) Or d And e = "hello" Or e < "wow" Then
        d = 15
    ElseIf k < 43 Then
        h = 1234
    Else
        If (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
            b = 20
        End If
        If (c < 1) Or d And e = "hello" Or e < "wow" Then
            d = 15
        End If
    End If
Else
    k = 3234
End If
""")

# And Not
tests.append("a = This And Not (That)")
tests.append("a = This And Not (That Or Other)")

# Inline ifs
tests.extend([
        "If a = 10 Then b = 20",
        "If a = 20 And b = 5 Then d = 123",
        "If a = 12 Then d = 1 Else g = 5",
        "If a = 10 Then doit",
        "If a = 10 Then doit 10, 20, 30",
        "If a = 10 Then doit Else dont",
        "If a = 10 Then doit 10, 20, 30 Else dont",
        "If a = 10 Then doit 10, 20, 30 Else dont 5, 10, 15",
        "If a = 10 Then Exit Function",
        "If a = 10 Then Exit Function Else DoIt",
        "If a = 10 Then Exit Function Else DoIt=1",
        "If a = 10 Then Exit Function Else DoIt 1, 2, 3",
        "If a = 10 Then DoIt Else Exit Function",
        "If a = 10 Then DoIt=1 Else Exit Function",
        "If a = 10 Then DoIt 1,2,34 Else Exit Function",
        "If a = 10 Then Remove X",
        "If ip Then i1 = ip: b = 1  Else i1 = 0",
        "If ip Then DoIt: Else DontDoIt",
        "If ip Then a = 1: Else DontDoIt",
        "If ip Then DoIt: Else A = 2",
])

# Weird inline if followed by assignment that failed once
tests.extend([
        "If a = 10 Then b a\nc=1",
])

# #If
tests.append("""
#If a = 10 Then
    b = 20
#Else
    c=2
#End If
#If c < 1 Then
    d = 15
#Else
    c=2
#End If
""")

# Empty #If
tests.append("""
#If a = 10 Then
#Else
    c=2
#End If
""")

# Empty #If with comments
tests.append("""
#If a = 10 Then ' comment here
#Else
    c=2
#End If
""")

# Simple #If with And/Or
tests.append("""
#If a = 10 And k = "test" Then
    b = 20
#Else
    c=2
#End If
#If c < 1 Or d Then
    d = 15
#Else
    c=2
#End If
""")

# If with comments at end
tests.append('''
#If Debug
    DoIt
#End If     ' 
''')

# Problematic if
tests.append("""
if a = 1 Then
        iFile = xFreeFile
End if
""")

# Simple #If with compount And/Or expression
tests.append("""
#If (a = 10 And k = "test") And (c Or b Or e = 43.23) Then
    b = 20
#Else
    c=2
#End If
#If (c < 1) Or d And e = "hello" Or e < "wow" Then
    d = 15
#Else
    c=2
#End If
""")

#  #If Not
tests.append("""
#If Not a = 10 Then
    b=2
#Else
    c=2
#End If
""")

# simple sub
tests.append("""
Sub MySub()
a=10
n=20
c="hello"
End Sub
""")

# Sub and functions on a line
tests.append('Sub A(): End Sub')
tests.append('Public Sub A(): End Sub')
tests.append('Function A(): End Function')
tests.append('Public Function A(): End Function')

# simple sub with exit
tests.append("""
Sub MySub()
a=10
n=20
Exit Sub
c="hello"
End Sub
""")


# simple sub with scope
tests.extend(["""
Private Sub MySub()
a=10
n=20
c="hello"
End Sub""",
"""
Public Sub MySub()
a=10
n=20
c="hello"
End Sub
""",
"""
Friend Sub MySub()
a=10
n=20
c="hello"
End Sub
""",
"""
Private Static Sub MySub()
a=10
n=20
c="hello"
End Sub
""",
])

# simple sub with gap in ()
tests.append("""
Sub MySub(   )
a=10
n=20
c="hello"
End Sub
""")

# simple sub
tests.append("""
Sub MySub(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Sub
""")


# simple sub with exit
tests.append("""
Sub MySub(x, y, z, a, b, c)
a=10
n=20
Exit Sub
c="hello"
End Sub
""")


# simple sub with scope
tests.append("""
Private Sub MySub(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Sub
Public Sub MySub(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Sub
""")

# simple sub
tests.append("""
Sub MySub(x As Single, y, z As Boolean, a, b As Variant, c)
a=10
n=20
c="hello"
End Sub
""")


# simple sub with exit
tests.append("""
Sub MySub(x As Single, y, z As Object, a, b As MyThing.Object, c)
a=10
n=20
Exit Sub
c="hello"
End Sub
""")


# simple sub with scope
tests.append("""
Private Sub MySub(x, y As Variant, z, a As Boolena, b, c As Long)
a=10
n=20
c="hello"
End Sub
Public Sub MySub(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Sub
""")

# simple sub
tests.append("""
Sub MySub(x As Single, y, z As Boolean, a, Optional b As Variant, c)
a=10
n=20
c="hello"
End Sub
""")


# simple sub with exit
tests.append("""
Sub MySub(x() As Single, y, z As Object, Optional a, b As MyThing.Object, Optional c)
a=10
n=20
Exit Sub
c="hello"
End Sub
""")


# simple sub with scope
tests.append("""
Private Sub MySub(x, Optional y As Variant, Optional z, a As Boolena, b, c As Long)
a=10
n=20
c="hello"
End Sub
Public Sub MySub(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Sub
""")

# simple sub with optional arguments and defaults
tests.append("""
Sub MySub(x As Single, y, z As Boolean, a, Optional b = 10, Optional c="hello")
a=10
n=20
c="hello"
End Sub
""")

# simple sub with optional arguments and defaults
tests.append("""
Sub MySub(x As Single, y, z As Boolean, a, Optional b = 10, Optional c As String = "hello")
a=10
n=20
c="hello"
End Sub
""")

# ByVal, ByRef args
tests.append("""
Sub MySub(ByVal a, ByRef y)
a=10
n=20
c="hello"
End Sub
""")

tests.append("""
Sub MySub(a, ByRef y)
a=10
n=20
c="hello"
End Sub
""")

tests.append("""
Sub MySub(ByVal a, y)
a=10
n=20
c="hello"
End Sub
""")

tests.append("""
Sub MySub(ByVal a As Single, y)
a=10
n=20
c="hello"
End Sub
""")

# 852166 Sub X<spc>(a,b,c) fails to parse 
tests.append("""
Sub MySub (ByVal a, ByRef y)
a=10
n=20
c="hello"
End Sub
""")

# 880612 Continuation character inside call  
tests.append("""
Sub MySub _
(ByVal a, ByRef y)
a=10
n=20
c="hello"
End Sub
""")

# Continuation using a comment
tests.append("' This is a comment a _\n= 1 /")
tests.append("B = 10 ' This is a comment a _\n= 1 /")

# Continuation with a blank line
tests.append("a = 1 _\n\nb = 2")

# Continuation within a with
tests.append('''
With A
  If LenB(contntMD5) <> 0 Then _
   .setRequestHeader "Content-MD5", contntMD5
End With
''')

# simple fn
tests.append("""
Function MyFn()
a=10
n=20
c="hello"
MyFn = 20
End Function
""")


# simple fn with exit
tests.append("""
Function MyFn()
a=10
n=20
MyFn = 20
Exit Function
c="hello"
End Function
""")


# simple sub with scope
tests.extend(["""
Private Function MyFn()
a=10
n=20
c="hello"
MyFn = 20
End Function""",
"""
Public Function MyFn()
a=10
n=20
c="hello"
MyFn = 20
End Function
""",
"""
Friend Function MyFn()
a=10
n=20
c="hello"
MyFn = 20
End Function
""",
])

# simple fn with gap in ()
tests.append("""
Function MyFn(  )
a=10
n=20
c="hello"
MyFn = 20
End Function
""")

# simple sub
tests.append("""
Function MySub(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Function
""")


# simple sub with exit
tests.append("""
Function MySub(x, y, z, a, b, c)
a=10
n=20
Exit Sub
c="hello"
End Function
""")


# simple sub with scope
tests.append("""
Private Function MySub(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Function
Public Function fn(x, y, z, a, b, c)
a=10
n=20
c="hello"
End Function
""")

# simple sub
tests.append("""
Function fn(x As Single, y, z As Boolean, a, b As Variant, c) As Single
a=10
n=20
c="hello"
End Function
""")


# simple sub with exit
tests.append("""
Function fc(x As Single, y, z As Object, a, b As MyThing.Object, c) As Object.Obj
a=10
n=20
Exit Function
c="hello"
End Function
""")


# simple sub with scope
tests.append("""
Private Function MySub(x, y As Variant, z, a As Boolena, b, c As Long) As Variant
a=10
n=20
c="hello"
End Function
Public Function MySub(x, y, z, a, b, c) As String
a=10
n=20
c="hello"
End Function
""")

# function returning an array
tests.append("""
Function fn(x As Single, y, z As Boolean, a, b As Variant, c) As Single()
a=10
n=20
c="hello"
End Function
""")

# simple sub
tests.append("""
Function fn(x As Single, y, z As Boolean, a, Optional b As Variant, c) As Single
a=10
n=20
c="hello"
End Function
""")

# Function with some spaces
tests.append('''
Public Function CreateFile(pathOfFile$ , Optional fileContnts$ ) As String

End Function
''')

# simple sub with exit
tests.append("""
Function MySub(x() As Single, y, z As Object, Optional a, b As MyThing.Object, Optional c) As Integer
a=10
n=20
Exit Function
c="hello"
End Function
""")


# simple sub with scope
tests.append("""
Private Function MySub(x, Optional y As Variant, Optional z, a As Boolena, b, c As Long) As Long
a=10
n=20
c="hello"
End Function
Public Function MySub(x, y, z, a, b, c) As Control.Buttons.BigButtons.ThisOne
a=10
n=20
c="hello"
End Function
""")

# simple fn with optional arguments and defaults
tests.append("""
Function MySub(x As Single, y, z As Boolean, a, Optional b = 10, Optional c="hello")
a=10
n=20
c="hello"
End Function
""")

# simple fn with optional arguments and defaults
tests.append("""
Function MySub(x As Single, y, z As Boolean, a, Optional b = 10, Optional c As String = "hello")
a=10
n=20
c="hello"
End Function
""")

# ByVal, ByRef args
tests.append("""
Function MySub(ByVal a, ByRef y)
a=10
n=20
c="hello"
End Function
""")

tests.append("""
Function MySub(a, ByRef y)
a=10
n=20
c="hello"
End Function
""")

tests.append("""
Function MySub(ByVal a, y)
a=10
n=20
c="hello"
End Function
""")

tests.append("""
Function MySub(ByVal a As Single, y)
a=10
n=20
c="hello"
End Function
""")

# Simple property let/get/set
tests.extend(["""
Property Let MyProp(NewVal As String)
 a = NewVal
 Exit Property
End Property
""",
"""
Property Get MyProp() As Long
 MyProp = NewVal
 Exit Property
End Property
""",
"""
Property Set MyProp(NewObject As Object) 
 Set MyProp = NewVal
 Exit Property
End Property
"""
"""
Public Property Let MyProp(NewVal As String)
 a = NewVal
End Property
""",
"""
Public Property Get MyProp() As Long
 MyProp = NewVal
End Property
""",
"""
Public Property Set MyProp(NewObject As Object) 
 Set MyProp = NewVal
End Property
""",
"""
Public Property Get MyProp(   ) As Long
 MyProp = NewVal
End Property
""",
])

# Simple property let/get/set with labels
tests.extend(["""
1: Property Let MyProp(NewVal As String)
1:  a = NewVal
1: End Property
""",
"""
1: Property Get MyProp() As Long
1:  MyProp = NewVal
1: End Property
""",
"""
1: Property Set MyProp(NewObject As Object) 
1:  Set MyProp = NewVal
1: End Property
"""
])

# Simple property let/get/set with labels and comment
tests.extend(["""
1: Property Let MyProp(NewVal As String) ' comment
1:  a = NewVal  ' comment
1: End Property  ' comment
""",
"""
1: Property Get MyProp() As Long  ' comment
1:  MyProp = NewVal  ' comment
1: End Property  ' comment
""",
"""
1: Property Set MyProp(NewObject As Object)   ' comment
1:  Set MyProp = NewVal  ' comment
1: End Property  ' comment
"""
])

# Property all on one line
tests.append("Property Get Position() As Long: Position = Loc(mFileNumber): End Property")
tests.append("""
Property Get Position() As Long: Position = Loc(mFileNumber)
End Property
""")
tests.append("""
Property Get Position() As Long
Position = Loc(mFileNumber): End Property
""")


# Simple case
tests.append("""
Select Case x
Case "one"
    y = 1
Case "two"
    y = 2
Case "three"
    z = 3
End Select
""")

# Simple case with else
tests.append("""
Select Case x
Case "one"
    y = 1
Case "two"
    y = 2
Case "three"
    z = 3
Case Else
    z = -1
End Select
""")

# Simple case with else and trailing colons
tests.append("""
Select Case x
Case "one":
    y = 1
Case "two":
    y = 2
Case "three":
    z = 3
Case Else:
    z = -1
End Select
""")

# Multiple case with else
tests.append("""
Select Case x
Case "one"
    y = 1
Case "two"
    y = 2
Case "three", "four", "five"
    z = 3
Case Else
    z = -1
End Select
""")

# Single line case with else
tests.append("""
Select Case x
Case "one": y = 1
Case "two": y = 2
Case "three", "four", "five": z = 3
Case Else: z = -1
End Select
""")

# Single line case with colon at the end
tests.append("""
Select Case x:
End Select
""")

# Range case 
tests.append("""
Select Case x
Case "a" To "m"
    z = 1
Case "n" To "z"
    z = 20
End Select
""")

# Range case with Is and Like
tests.append("""
Select Case x
Case Is < "?", "a" To "m"
    z = 1
Case "n" To "z", Is > 10, Is Like "*blah"
    z = 20
End Select
""")

# Multiple Range case 
tests.append("""
Select Case x
Case "a" To "m", "A" To "G", "K" To "P"
    z = 1
Case "n" To "z", 10 To this.that(10,20)
    z = 20
End Select
""")

# Empty case
tests.append("""
    Select Case a
    Case 10
    Case 20
    End Select
""")

# Case with comments
tests.append("""
Select Case x
' Here is a nasty comment

Case "one"
    y = 1
Case "two"
    y = 2
Case "three"
    z = 3
End Select
""")

# Simple for
tests.append("""
For i = 0 To 1000
  a = a + 1
Next i
""")

# Simple for
tests.append("""
For i=0 To 1000
  a = a + 1
Next i
""")

# Empty for
tests.append("""
For i = 0 To 1000
Next i
""")

# Simple for with unnamed Next
tests.append("""
For i = 0 To 1000
  a = a + 1
Next
""")

# For with step
tests.append("""
For i = 0 To 1000 Step 2
  a = a + 1
Next i
""")

# For with exit
tests.append("""
For i = 0 To 1000
  a = a + 1
  Exit For
Next i
""")

# Nested for
tests.append("""
For i = 0 To 1000
  a = a + 1
  For j = 1 To i
     b = b + j
  Next j
Next i
""")

# Dotted names - what does this even mean?
tests.append("""
For me.you = 0 To 1000 Step 2
  a = a + 1
Next me.you
""")

# Simple for
tests.append("""
For Each i In coll
  a = a + 1
Next i
""")

# Empty for
tests.append("""
For Each i In coll
Next i
""")

# Simple for with unnamed Next
tests.append("""
For Each i In coll
  a = a + 1
Next
""")


# For with exit
tests.append("""
For Each i In coll
  a = a + 1
  Exit For
Next i
""")

# Nested for
tests.append("""
For Each i In coll
  a = a + 1
  For Each j In coll
     b = b + j
  Next j
Next i
""")

# Simple while wend
tests.append("""
        a = 0
        While a < 10
            g = 10
            a = a + 1
        Wend
""")

tests.append("While A: Wend")

# Nested while wend
tests.append("""
        a = 0
        While a < 10
            g = 10
            a = a + 1
            While b < 40
                doit
            Wend
        Wend
""")

# Simple while wend with line numbers
tests.append("""
1:		a = 0
2:		While a < 10
3:			g = 10
4:			a = a + 1
5:		Wend
""")

# Simple do while loop
tests.append("""
        a = 0
        Do While a < 10
            g = 10
            a = a + 1
        Loop
""")

# Do While on a single line
tests.append('Do While A : A = A - 1 : Loop')
tests.append('Do : A = A - 1 : Loop')
tests.append('Do : A = A - 1 : Loop While A')
tests.append('Do Until A = 0 : A = A - 1 : Loop')

# Simple do while with exit
tests.append("""
        a = 0
        Do While a < 10
            g = 10
            a = a + 1
            Exit Do
        Loop
""")

# Nested do while loop
tests.append("""
        a = 0
        Do While a < 10
            g = 10
            a = a + 1
            Do While b < 40
                doit
            Loop
        Loop
""")

# Simple do  loop
tests.append("""
        a = 0
        Do  
            g = 10
            a = a + 1
        Loop
""")

# Empty Do's
tests.append("""
        Do  
        Loop
""")
tests.append("""
        Do Until A And B  
        Loop
""")
# Simple do  loop
tests.append("""
        Do  
        Loop Until A And B
""")

# Simple do  with exit
tests.append("""
        a = 0
        Do 
            g = 10
            a = a + 1
            Exit Do
        Loop
""")

# Nested do  loop
tests.append("""
        a = 0
        Do 
            g = 10
            a = a + 1
            Do 
                doit
            Loop
        Loop
""")

# Simple do  loop
tests.append("""
        a = 0
        Do  
            g = 10
            a = a + 1
        Loop While a < 10
""")

# Simple do  with exit
tests.append("""
        a = 0
        Do 
            g = 10
            a = a + 1
            Exit Do
        Loop While a <10
""")

# Nested do  loop
tests.append("""
        a = 0
        Do 
            g = 10
            a = a + 1
            Do 
                doit
            Loop While a <10
        Loop While a< 10
""")

# Simple do  loop
tests.append("""
        a = 0
        Do  
            g = 10
            a = a + 1
        Loop Until a < 10
""")

# Simple do  with exit
tests.append("""
        a = 0
        Do 
            g = 10
            a = a + 1
            Exit Do
        Loop Until a <10
""")

# Nested do  loop
tests.append("""
        a = 0
        Do 
            g = 10
            a = a + 1
            Do 
                doit
            Loop While a <10
        Loop Until a< 10
""")

# Simple do  loop
tests.append("""
        a = 0
        Do Until a < 10
            g = 10
            a = a + 1
        Loop 
""")

# Simple do  with exit
tests.append("""
        a = 0
        Do Until a <10
            g = 10
            a = a + 1
            Exit Do
        Loop 
""")

# Nested do  loop
tests.append("""
        a = 0
        Do Until a< 10
            g = 10
            a = a + 1
            Do While a <10
                doit
            Loop 
        Loop 
""")


# simple type
tests.append("""
Type myType
    A As Integer
    B As String
    C As MyClass.MyType
End Type
""")

# simple type with scope
tests.append("""
Public Type myType
    A As Integer
    B As String
    C As MyClass.MyType
End Type
""")

tests.append("""
Private Type myType
    A As Integer
    B As String
    C As MyClass.MyType
End Type
""")

# Type with keyword names
tests.append("""
Private Type myType
    To As Integer
    From As String
    Message As MyClass.MyType
End Type
""")

# With a comment inside
tests.append("""
Private Type myType
    A As Integer
    B As String
    ' Here is a comment
    C As MyClass.MyType
End Type
""")

# General with with just the structure
tests.append("""
With MyObject
    a = 10
End With
""")

# General with with some assignments
tests.append("""
With MyObject
    .value = 10
    .other = "Hello"
End With
""")

# General with with some assignments and expressions
tests.append("""
With MyObject
    .value = .other + 10
    .other = "Hello" & .name
End With
""")

# Nested With
tests.append("""
With MyObject
    a = 10
    With .OtherObject
        b = 20
    End With
End With
""")

# General with with just the structure and labels
tests.append("""
1: With MyObject
2: 	a = 10
3: End With
""")

# Empty with
tests.append("""
With MyObject
End With
""")


tests.append("""
With MyObject. _
    Other
End With
""")
tests.append("""
        With ActiveSheet.ListObjects.Add.Range("$A$1"). _
            QueryTable
        End With
""")

# Simple header found at the top of most class files
tests.append("""
VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
""")

# Simple enumeration
tests.append("""
Enum MyEnum
    one
    two
    three
    four
    five
End Enum
""")


# Scoped enumeration
tests.append("""
Public Enum MyEnum
    one
    two
    three
    four
    five
End Enum
""")

tests.append("""
Private Enum MyEnum
    one
    two
    three
    four
    five
End Enum
""")

# Enum with mulitple on a line
tests.append('''
Enum A
    Thing = 1:    That = 2
End Enum
'''
)

# Simple enumeration with comments
tests.append("""
Enum MyEnum ' yeah
    one ' this 
    two ' is 
    three
    four ' neat
    five
End Enum
""")

# Simple enumeration with whole line comments
tests.append("""
Enum MyEnum ' yeah
    one 
    ' this 
    two 
    ' is 
    three
    four 
    ' neat
    ' oh
    five
End Enum
""")

# If seems that some enums for registry items have [] in them
tests.append("""
Public Enum KeyRoot
[HKEY_CLASSES_ROOT] = &H80000000 'stores OLE class information and file associations
[HKEY_CURRENT_CONFIG] = &H80000005 'stores computer configuration information
[HKEY_CURRENT_USER] = &H80000001 'stores program information for the current user.
[HKEY_LOCAL_MACHINE] = &H80000002 'stores program information for all users
[HKEY_USERS] = &H80000003 'has all the information for any user (not just the one provided by HKEY_CURRENT_USER)
End Enum
""")



# Initialising arrays
tests.append('Public Shared A() as String = {"one", "two"}')
tests.append('Public Shared A() as String = ({"one", "two"})')
tests.append('Public Shared A() as Integer = {1, 2, 4, 5}')
tests.append('Public Shared A() as Integer = {}')




# Shared Dim
tests.append('Public SharedScriptSupport As New clsScriptSupportClass')



# Using statement
tests.append("""
Using client as New WebClient
    DoSomething()
End Using
""")
tests.append("""
Using client as New WebClient
    DoSomething()
    Using other_client as Something.Somethat()
        DoOtherThing client, other_client
    End Using 
End Using
""")


tests.append("If IsMissing (oDoc) Then oDoc = ThisComponent")
tests.append('If NOT oDoc.SupportsService ("com.sun.star.sheet.SpreadsheetDocument") Then Exit Function')
tests.append('If (iSheet>= oSheets.getCount ()) Then Exit Function')
tests.append('oSheet = oSheets.getByIndex (iSheet)')
tests.append('arrayOfString () = Split (tmpString, ";")')
tests.append('If UBound (arrayOfString) <( 3 + iSheet) Then Exit Function')
tests.append('''
If InStr (tmpString, "+")> 0 Then
       arrayOfString () = Split (tmpString, "+")
Else
 arrayOfString () = Split (tmpString, "/")
End If

''')


tests.append('''
For i = 1 To 10
Label:
Next
''')

# Spaces in object calls
tests.append('a = b() .c')
tests.append('a = b () .c')
tests.append('a = b () . c')
tests.append('a = b ( ) . c')


# Imports statements
vb_dot_net_tests.extend([
    'Imports A',
    'Imports A.B.C',
    'Imports this = A',
    'Imports this = A.B.C',
])


# For and other statements with type declaration
vb_dot_net_tests.append('''
    For A As Integer = 1 To 10
    Next 
''')
vb_dot_net_tests.append('''
    For Each A As Microsoft.Thing In Some.Collection
    Next 
''')
vb_dot_net_tests.append('''
    Select Case X As Integer
    End Select 
''')
vb_dot_net_tests.append('''
    With Container.Member As Integer
    End With
''')


# Casting for lists
vb_dot_net_tests.append('Dim X as New List(Of String)')
vb_dot_net_tests.append('Dim X as New List(Of String.Thing)')


# Brackets and method calls in an expression
vb_dot_net_tests.append('a = (value).ToString')
vb_dot_net_tests.append('a = (value).ToString()')
vb_dot_net_tests.append('a = (value).ToString + "something else"')

# Complex explicit calls
vb_dot_net_tests.append('Do.It(10).Again()')
vb_dot_net_tests.append('Do.It(10, 10).Again(20)')

# Try statements
vb_dot_net_tests.append('''
Try
    a = 1
Catch
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
    Exit Try
    b = 2
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
    Exit Try
    b = 2
Catch OtherError
    b = 3
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch ValueError.ThisError As Err When B = 2
    a = 2
    Exit Try
    b = 2
Catch OtherError
    b = 3
Finally
    b = 4
End Try
''')

vb_dot_net_tests.append('''
Try
Catch ValueError.ThisError As Err When B = 2
Catch OtherError
Finally
End Try
''')

vb_dot_net_tests.append('''
Try
    a = 1
Catch    ValueError.ThisError   As    Err    When   B = 2  
    a = 2
    Exit    Try  
    b = 2
Catch    OtherError   
    b = 3
Finally
    b = 4
End     Try
''')

vb_dot_net_tests.append('''
Try
    Throw ValueError
Catch    ValueError.ThisError   As    Err    When   B = 2  
    a = 2
End     Try
''')

vb_dot_net_tests.append('''
Try
    Throw New ValueError
Catch    ValueError.ThisError   As    Err    When   B = 2  
    a = 2
End     Try
''')

vb_dot_net_tests.append('''
Try
    Throw New ValueError("this is an error")
Catch    ValueError.ThisError   As    Err    When   B = 2  
    a = 2
End     Try
''')

# Weird short circuiting
vb_dot_net_tests.extend([
    'a = 1 AndAlso 2',
    'If A AndAlso B Then C = 1',
    'a = 1 OrElse 2',
    'If A OrElse B Then C = 1',
])

# Nested do  loop with line numbers
vb_dot_net_tests.append("""
        a = 0
        Do Until a< 10
            g = 10
            a = a + 1
            Do While a <10
                doit = 1
112         Loop 
111        Loop 
""")


# String Array initialisation
vb_dot_net_tests.extend([
    'Dim cydiashsh As String() = New String() {","}',
])

# Using with an equals
vb_dot_net_tests.append('''
Using A = client.Open("asas")
End Using
''')

# Using with an equals
vb_dot_net_tests.append('''
Using A As Integer = client.Open("asas")
End Using
''')
vb_dot_net_tests.append('''
Using A As Integer = New client.Open("asas")
End Using
''')

# Implicit line continuations
vb_dot_net_tests.append(
    '''MessageBox(
    "This is on another line")
    '''
)
vb_dot_net_tests.append(
    '''MessageBox("This is on the same line",
    "This is on another line")
    '''
)
vb_dot_net_tests.append(
    '''MessageBox(   
    "This is on the same line",
    
    "This is on another line", b, 
    c, d+10, 
    e)
    '''
)


# Closures
vb_dot_net_tests.extend([
    'a = GetProcess().Any(Function(x) x.id = id)',
    'a = GetProcess().Any(Function(x) x.id = id, 10, Function() 123)',
    'Dim F = Function(x, y) x + y',
])

# Decorators
vb_dot_net_tests.append('''
    <System.This.That()> _
    Class MyThing
        Function X(Y)
        End Function
    End Class
''')
vb_dot_net_tests.append('''
    <System.This.That()> _
    Function X(Y)
    End Function
''')
vb_dot_net_tests.append('''
    <System.This.That()> _
    Class MyThing
        <DllImport("some dll.dll")> _
        Function X(Y)
        End Function
    End Class
''')
# With no continuation marker
vb_dot_net_tests.append('''
    <System.This.That()> 
    Class MyThing
        Function X(Y)
        End Function
    End Class
''')
vb_dot_net_tests.append('''
    <System.This.That()> 
    Function X(Y)
    End Function
''')
vb_dot_net_tests.append('''
    <System.This.That()> 
    Class MyThing
        <DllImport("some dll.dll")> 
        Function X(Y)
        End Function
    End Class
''')

# Using with an equals
vb_dot_net_tests.append('''
Sub X(a, <[In]()> b)
End Sub
''')
vb_dot_net_tests.append('''
Function X(a, <[In]()> b)
End Function
''')
vb_dot_net_tests.append('''
Function X(a, <[In](), Out()> b)
End Function
''')

# Inherits
vb_dot_net_tests.append('''
    Class MyThing
    Inherits This.That.Other
    
        Function X(Y)
        End Function
    End Class
''')
vb_dot_net_tests.append('''
    Class MyThing
    Inherits This.That.Other, Same, OneThing
    
        Function X(Y)
        End Function
    End Class
''')

# Protected and Overrides
vb_dot_net_tests.append('''
    Protected Overrides Sub DoIt()
    End Sub
''')
vb_dot_net_tests.append('''
    Protected  Sub DoIt()
    End Sub
''')
vb_dot_net_tests.append('''
     Overrides Sub DoIt()
    End Sub
''')

# AddressOf for .NET
vb_dot_net_tests.extend([
        "a = fn(AddressOf fn)",
        "a = fn(a, b, c, AddressOf fn)",
        "a = fn(a, AddressOf b, AddressOf c, AddressOf fn)",
        "a = fn(a, AddressOf b.m.m, AddressOf c.k.l, AddressOf fn)",
        "a = AddressOf b",
        "DoIt AddressOf b",
        "DoIt AddressOf b, That",
        "DoIt This, AddressOf b",
])

# Partial classes etc
vb_dot_net_tests.append('''
    Partial Class MyThing
        Function X(Y)
        End Function
    End Class
''')
vb_dot_net_tests.append('''
    Partial Friend Class MyThing
        Function X(Y)
        End Function
    End Class
''')
vb_dot_net_tests.append('''
    Friend Class MyThing
        Function X(Y)
        End Function
    End Class
''')

# Namespace
vb_dot_net_tests.append('''
    Namespace Bob.Evans
        Class A
        End Class
    End Namespace
''')


failures = [
]
# -- end -- << Parsing tests >>

class ParsingTest(unittest.TestCase):
    """Holder class which gets built into a whole test case"""


def getTestMethod(vb, dialect='VB6'):
    """Create a test method"""
    def testMethod(self):
        try:
            buildParseTree(vb, dialect=dialect)
        except VBParserError:
            raise Exception("Unable to parse ...\n%s" % vb)
    return testMethod


#
# Add tests to main test class
for idx in range(len(tests)):
    setattr(ParsingTest, "test%d" % idx, getTestMethod(tests[idx]))


for idx in range(len(vb_dot_net_tests)):
    setattr(ParsingTest, "dot_net_test%d" % idx, getTestMethod(vb_dot_net_tests[idx], dialect='vb.net'))


if __name__ == "__main__":
    unittest.main()
