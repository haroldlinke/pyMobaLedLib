from vb2py.test.testframework import *



# << Sub tests >> (1 of 5)
# Simple subroutine - use "global" to see results of the subroutine
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Value As String)
    _lst(Index) = Value
End Sub

_SetValue 5, "hello"
a = _lst(5)
""", {"a" : "hello"}))

# Simple subroutine with an exit
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Value1 As String, Value2 As String)
    _lst(Index) = Value1
    Exit Sub
    _lst(Index) = Value2
End Sub

_SetValue 5, "hello", "bye"
a = _lst(5)
""", {"a" : "hello"}))

# Simple sub calling a sub
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Value As String)
    _lst(Index) = Value
End Sub

Sub _SetFive(Value)
    _SetValue 5, Value
End Sub

_SetFive "hello"
a = _lst(5)
""", {"a" : "hello"}))

# Subroutine empty but for a comment - this can be a syntax error in Python
tests.append(("""
Sub _SetValue()
    ' Nothing to see here
End Sub
""", {}))
# << Sub tests >> (2 of 5)
# Recursive sub
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Value)
    _lst(Index) = Value
    If Index < 10 Then 
        _SetValue Index+1, Value+1
    End If
End Sub

_SetValue 1, 1
a = _lst(5)
""", {"a" : 5}))
# << Sub tests >> (3 of 5)
# Optional arguments
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Optional Value=10)
    _lst(Index) = Value
End Sub

_SetValue 5, "hello"
_SetValue 6
a = _lst(5)
b = _lst(6)
""", {"a" : "hello", "b" : 10}))

# Optional arguments
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Optional Value)
    If IsMissing(Value) Then Value = 10
    _lst(Index) = Value
End Sub

_SetValue 5, "hello"
_SetValue 6
a = _lst(5)
b = _lst(6)
""", {"a" : "hello", "b" : 10}))

# Optional arguments - failing parsing case, where the space before the bracket used to cause a problem
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Optional Value)
    If IsMissing (Value) Then Value = 10
    _lst(Index) = Value
End Sub

_SetValue 5, "hello"
_SetValue 6
a = _lst(5)
b = _lst(6)
""", {"a" : "hello", "b" : 10}))


# Optional arguments with hex numbers
tests.append(("""
Dim _lst(10) As Single
Sub _SetValue(Index As Integer, Optional Value=&HA)
    _lst(Index) = Value
End Sub

_SetValue 5, "hello"
_SetValue 6
a = _lst(5)
b = _lst(6)
""", {"a" : "hello", "b" : 10}))
# << Sub tests >> (4 of 5)
# Sub with named arguments
tests.append(("""
Dim _vals(10)
Sub _sum(Optional x=1, Optional y=2, Optional z=3)
    _vals(1) = x + y + z
End Sub

_sum 10, 20, 30
a = _vals(1)
_sum x:=10
b = _vals(1)
_sum z:=10 
c = _vals(1)
_sum
d = _vals(1)
_sum x:=10, y:=20, z:=30
f = _vals(1)
""", {"a" : 60, "b" : 15, "c" : 13, "d" : 6, "f" : 60}))
# << Sub tests >> (5 of 5)
# Implicit calling in the way that VBScript implements it
# VBScript allows calls like:
#     object.method()
#     object.method(10,20)
#
# These are illegal in VB 

tests.append(("""
Dim _vals(10)
Sub _sum(x, y)
    _vals(0) = x + y
End Sub

Sub _const()
     _vals(1) = 123
End Sub

_sum(10, 20)
_const()

a = _vals(0)
b = _vals(1)

""", {"a" : 30, "b" : 123}))


# Parameter arrays at the end
tests.append(("""
Dim a As Double
a = _calcSum(4, 3, 2, 1)
Dim b As Double
b = _calcSum()

Function _calcSum(ParamArray args() as Double) as Double
    _calcSum = 0
    sum = 0
    If UBound(args, 1) <= 0 Then Exit Function
    For i = 0 to UBound(args, 1) - 1
        sum = sum + args(i)
    Next i
    _calcSum = sum
End Function

""", {"a": 10, "b": 0}))
#
tests.append(("""
Dim a As Double
a = _calcSum(10, 4, 3, 2, 1)
Dim b As Double
b = _calcSum(10)

Function _calcSum(StartValue As Double, ParamArray args() as Double) as Double
    sum = StartValue
    _calcSum = sum
    If UBound(args, 1) <= 0 Then Exit Function
    For i = 0 to UBound(args, 1) - 1
        sum = sum + args(i)
    Next i
    _calcSum = sum
End Function

""", {"a": 20, "b": 10}))
#
tests.append(("""
Dim result(3) As Double
_calcSum(result, 4, 3, 2, 1)

Sub _calcSum(results() as Double, ParamArray args() as Double)
    If UBound(args, 1) <= 0 Then Exit Function
    For i = 0 to UBound(args, 1) - 1
        results(i) = args(i)
    Next i
End Sub

""", {"result": [4, 3, 2, 1]}))
#

# Test with explicit call with no brackets
tests.append(("""
Dim result(3) As Double
Call _calcSum result, 4, 3, 2, 1

Sub _calcSum(results() as Double, ParamArray args() as Double)
    If UBound(args, 1) <= 0 Then Exit Function
    For i = 0 to UBound(args, 1) - 1
        results(i) = args(i)
    Next i
End Sub

""", {"result": [4, 3, 2, 1]}))
#


# New keyword in the call
tests.append(("""

a = _ReturnLength(New list)

Function _ReturnLength(Item() As String) As Integer
    ReDim Item(1)
    Item(0) = 10
    _ReturnLength = Item(0)
End Function


""", {'a': 10}))

tests.append(("""

_ReturnLength(New list)

Sub _ReturnLength(Item() As String) 
    ReDim Item(1)
    Item(0) = 10
End Sub


""", {}))

# This one is not really VB but helps in the testing
tests.append(("""

Set a = _ReturnLength(New list)

Function _ReturnLength(Item() As String) as Object 
    Item.append(20)
    Set _ReturnLength = Item
End Function


""", {'a': [20]}))


tests.append(("""

Set a = _ReturnLength(New VBArray(0))

Function _ReturnLength(Item() As String) as Object 
    Item.append(20)
    Set _ReturnLength = Item
End Function


""", {'a': [20]}))

tests.append(("""

Dim a() as Integer 
_Dummy

Sub _Dummy 
   a.append(1)
End Sub


""", {'a': [0, 1]}))

import vb2py.vbparser
vb2py.vbparser.log.setLevel(0) # Don't print all logging stuff
TestClass = addTestsTo(BasicTest, tests)

if __name__ == "__main__":
    main()
