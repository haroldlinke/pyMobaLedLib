from vb2py.test.testframework import *
import vb2py.vbparser

tests.append(("""
#If 1 Then
a = 1
#Else
a = 2
#End If

""", {'a': 1}))

tests.append(("""
#If 0 Then
a = 1
#Else
a = 2
#End If

""", {'a': 2}, None, [('Directives', 'Path', 2)]))

tests.append(("""
'VB2PY-Set: Directives.Path = 2
#If 0 Then
a = 1
#Else If 1
a = 2
#Else
a = 3
#End If

""", {'a': 2}, None, [('Directives', 'Path', 2)]))

tests.append(("""
#If 0 Then
a = 1
#ElseIf 0
a = 2
#Else
a = 3
#End If

""", {'a': 3}, None, [('Directives', 'Path', 3)]))

tests.append(("""
#If Something  = 1 Then
a = 1
#Else If Something = 2
a = 2
#Else
a = 3
#End If

""", {'a': 1}, None, [('Directives', 'Path', 1)]))

tests.append(("""
#If Something  = 1 Then
a = 1
#Else If Something = 2
a = 2
#Else
a = 3
#End If

""", {'a': 2}, None, [('Directives', 'Path', 2)]))

tests.append(("""
#If Something  = 1 Then
a = 1
#Else If Something = 2
a = 2
#Else
a = 3
#End If

""", {'a': 3}, None, [('Directives', 'Path', 3)]))

tests.append(("""
#If Something  = 1 Then
Function _x(V)
#Else
Function _x(V, W)
#End If
_x = 123
End Function

a = _x(1)

""", {'a': 123}, None, [('Directives', 'Path', 1)]))

tests.append(("""
#If Something  = 1 Then
Function _x(V)
#Else
Function _x(V, W)
#End If
_x = 123
End Function

a = _x(1, 2)

""", {'a': 123}, None, [('Directives', 'Path', 2)]))

tests.append(("""
a = 0
b = 0
#If Something  = 1 Then
a = 1
#End If
#If Something = 2 Then
b = 1
#End IF

""", {'a': 1, 'b': 1}, None, [('Directives', 'Path', 1)]))

tests.append(("""
a = 0
b = 0
#If Something  = 1 Then
a = 1
#End If
#If Something = 2 Then
b = 1
#End IF

""", {'a': 0, 'b': 0}, None, [('Directives', 'Path', 2)]))



# vb2py.vbparser.log.setLevel(0)
TestClass = addTestsTo(BasicTest, tests)

if __name__ == "__main__":
    main()
