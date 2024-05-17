code_samples = [
    ["general", "", """
Dim A as Integer
B = 20

Sub DotIt(X as Double)
    Select Case A
        Case 1
            B = B + X
        Case 2
            B = B - X
        Case Else
            B = 0
    End Select
End Sub

Function GetHalfB() As Integer
    GetHalfB = B / 2
End Function
    """],
    [None, None, None],
    ["if", "", """

'
' Multi-line and singe-line ifs are converted to blocks in Python
If A = 10 Then
    DoSomething()
ElseIf B = 20 Then
    DoSomethingElse()
Else
    OtherCase()
If B = 20 Then C = 0 Else C = 1
End If
    """],
    ["with", "", """

'
' With statements allow quick access to properties and methods
' of an object. These will be translated into explicit calls to
' a temporary object (in case of side-effects)
With Container.Member
    .Init
    .IncrementCounter 43
    With .ChildItem
        .Refresh
    End With
End With
    """],
    ["select", "", """

'
' Selects are converted to If blocks with a temporary variable to
' hold the tested variables (in case of side-effects). Case ranges
' and options are handled as additional clauses for the if
Select Case A
    Case 1
        B = B + X
    Case 2
        B = B - X
        Select Case B
            Case 0 to 10
                C = 1
            Case 11, 12
                C = 2
        End Select
    Case Else
        B = 0
End Select
    """],
    ["for", "", """

'
' Numeric for loops use a helper function to create the underlying
' sequence to be iterated over
For I = 1 To 10
    B = B + 1
    For J = 10 To 0 Step -1
        If B = 20 Then Exit For
    Next J
Next I

'
' For Each relies on the underlying object supporting the iteration
' protocol (which might not be the case!)
For Each Child in Parent
    Child.CleanUp
Next
    """],
    ["while", "", """

'
' While and Do loops are converted to a Python while
' block.
While Something %3C%3E 10
    Something = Something + 1
Wend

'
' A starting until clause reverses the condition
Do Until Something = 5
    Something = Something - 1
Loop

'
' A final Until clause will generate an If with a break
Do
    Something = Something - 1
Loop Until Something = 0
    """],
    ["dim", "", """
'
' Dim statements define the types of variables and perform initialisation
' and so are mapped to helper functions which create python objects that
' try to behave like the VB equivalents
Dim A
Dim B as Integer, C As String
A = 10: B = 30: C = "Hello World"

'
' Where arrays are defined these use a helper function which creates
' a variant of a list which has initial values
Dim D(10) As String, E(10, 2, 3) As MyClass

D(5) = "Hello"
E(1, 1, 2) = New MyClass(20)

'
' ReDim statements use the helper function to resize the underlying list
' objects while retaining the size
ReDim Preserve D(5)
ReDim C(20)

    """],

        ["try", "", """
'
' Try ... Catch statements are converted to try ... except blocks
Try
    a = 1 / 0
Catch ZeroDivisionError As Err
    a = 1000
Finally
    b = 1
End Try

'
' If an Exit Try is found then an additional try ... except is created
' to allow breaking out of the current Except clause
Try
    a = 1 / 0
Catch
    a = 1000
    Exit Try
    b = 2000
Finally
    b = 1
End Try

'
' If there is a "When" clause then this is implemented as an If block 
' However, the behaviour is not likely to be identical in Python in the
' current implementation
a = 1
Try
    a = 1 / 0
Catch ZeroDivisionError When a = 1
    a = 1000
    b = 2000
Finally
    b = 1
End Try

    """],

    [None, None, None],

    ["sub", "", """
'
' Subroutines are converted to Python functions and can
' include optional parameters with defaults
'
' An optional parameter with no default uses the helper
' object VBMissingArgument and the helper function IsMissing
Sub MySub(X, Optional Y, Optional Z=20)
    Dim subLocal
    If IsMissing(Y) Then Y = 12
    subLocal = X + Y + Z + moduleGlobal
End Sub

MySub 1, 2
MySub 1, Z:=10

'
' Passing by Value converts but behaves differently for
' immutable types in Python.
Sub DoIt(x, ByVal y)
    x = x + 1
    y = y + 1
End Sub

x = 0
y = 0
DoIt x, y
' x is now 1, y is still 0
    """],
    ["fn", "", """
'
' Functions use a variable to store the result of the
' function during its execution
Function MyFunc(X, Optional Y, Optional Z=20)
    Dim subLocal
    subLocal = X + Y + Z
    MyFunc = subLocal*10
End Function

a = MyFunc(1, 2)
a = MyFunc(1, Z:=10)
    """],
    [None, None, None],
    ["type", "", """
'
' Types create classes with properties to store the
' values of the types
Type Point
    X As Single
    Y As Single
End Type
'
Type Line2D
    Start As Point
    Finish As Point
End Type
'
Dim p1 As Point, p2 As Point
p1.X = 10
p1.Y = 20
p2.X = 30
p3.Y = 40
'
Dim l1 As Line2D
l1.Start = p1
l1.Finish = p2

    """],
    ["enum", "", """
'
' Enums create variables with the same names
Enum Number
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Ten = 10
    Hundred = 100
End Enum

Enum Day
    Mon
    Tue
    Wed
    Thu
    Fri
End Enum
    """],
    [None, None, None],
    ["properties", "class", """
'
' In class modules you can use properties to provide
' accessor functions. These are converted to the Python
' equivalent
Dim myValue = 0

Property Let PriceToPublic(Value As Integer)
    myValue = myValue - Value
    If myValue %3C 0 Then myValue = 0
End Property

Property Get PriceToPublic()
    PriceToPublic = 2 * myValue
End Property

    """],
    ["class", "class", """

'
' In the context of a class module, dimensioned variables
' are converted to attributes of the class and any
' subroutines and functions are converted to methods
' of the class.
Dim A as Integer
Dim B = 20

Sub DotIt(X as Double)
    Select Case A
        Case 1
            B = B + X
        Case 2
            B = B - X
        Case Else
            B = 0
    End Select
End Sub

Function GetHalfB() As Integer
    GetHalfB = B / 2
End Function
    """],
    ["open", "", """
'
' File operations using #channels are mapped to a helper
' function that keeps track of the open files
Open "myfile.txt" For Input as #1
Line Input #1, aLine
Close #1

'
' This also handles the writing of files
Open "myOtherFile.txt" For Append as #2
Print #2, "Hello World"
Seek #2, 1
Print #2, "Here at the begining"
Close #2
    """],
    ["using", "", """
'
' Using blocks are mapped to with blocks.
Using A As Object.Value
    b = A.Result()
End Using
    """],
]
