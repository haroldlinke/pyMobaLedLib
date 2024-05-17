from vb2py.test.testframework import *

# << If tests >> (1 of 7)
# Test main branch of If
tests.append(
    ("""a = 10
        b = 0
        If a = 10 Then
            b = 1
        End If
     """,
     {"a" : 10, "b" : 1}
    ))

# Test else branch of If
tests.append(
    ("""a = 20
        b = 0
        If a = 10 Then
            b = 1
        End If
     """,
     {"a" : 20, "b" : 0}
    ))	

# Test main branch of If with not
tests.append(
    ("""a = 10
        b = 0
        If Not a = 10 Then
            b = 1
        End If
     """,
     {"a" : 10, "b" : 0}
    ))
tests.append(
    ("""a = 11
        b = 0
        If Not a = 10 Then
            b = 1
        End If
     """,
     {"a" : 11, "b" : 1}
    ))

# This test with the redundant parenthesis used to fail
tests.append(
    ("""a = 11
        b = 0
        If (Not a = 10) Then
            b = 1
        End If
     """,
     {"a" : 11, "b" : 1}
    ))
# << If tests >> (2 of 7)
# Test main branch of If
tests.append(
    ("""a = 10
        If a = 10 Then
            b = 1
        Else
            b = 0
        End If
     """,
     {"a" : 10, "b" : 1}
    ))

# Test else branch of If
tests.append(
    ("""a = 20
        If a = 10 Then
            b = 1
        Else
            b = 0
        End If
     """,
     {"a" : 20, "b" : 0}
    ))
# << If tests >> (3 of 7)
# Test main branch of If
tests.append(
    ("""a = 10
        If a = 10 Then
            b = 1
        ElseIf a = 20 Then
            b = 2
        Else
            b = 0
        End If
     """,
     {"a" : 10, "b" : 1}
    ))

# Test elseif branch of If
tests.append(
    ("""a = 20
        If a = 10 Then
            b = 1
        ElseIf a = 20 Then
            b = 2
        Else
            b = 0
        End If
     """,
     {"a" : 20, "b" : 2}
    ))	

# Test else branch of If
tests.append(
    ("""a = 30
        If a = 10 Then
            b = 1
        ElseIf a = 20 Then
            b = 2
        Else
            b = 0
        End If
     """,
     {"a" : 30, "b" : 0}
    ))
# << If tests >> (4 of 7)
# Test main branch of If
tests.append(
    ("""a = 10
        b = 0
        c = 20
        If a = 10 Then
            If c = 20 Then
                b = 1
            End If
        End If
     """,
     {"a" : 10, "b" : 1, "c" : 20}
    ))

# Test else branch of If
tests.append(
    ("""a = 10
        b = 0
        c = 20
        If a = 10 Then
            If c = 30 Then
                b = 1
            End If
        End If
     """,
     {"a" : 10, "b" : 0, "c" : 20}
    ))
# << If tests >> (5 of 7)
# Test main branch of If
tests.append(
    ("""a = 10
        b = 0
        c = 20
        If a = 10 Then
            If c = 20 Then
                b = 1
            Else
                b = 2
            End If
        Else
            b = 3
        End If
     """,
     {"a" : 10, "b" : 1, "c" : 20}
    ))

# Test else branch of If
tests.append(
    ("""a = 10
        b = 0
        c = 20
        If a = 10 Then
            If c = 25 Then
                b = 1
            Else
                b = 2
            End If
        Else
            b = 3
        End If
     """,
     {"a" : 10, "b" : 2, "c" : 20}
    ))	

tests.append(
    ("""a = 10
        b = 0
        c = 20
        If a = 15 Then
            If c = 25 Then
                b = 1
            Else
                b = 2
            End If
        Else
            b = 3
        End If
     """,
     {"a" : 10, "b" : 3, "c" : 20}
    ))
# << If tests >> (6 of 7)
# Test main branch of If
tests.append(
    ("""a = 10
        b = 0
        c = 20
        If a = 10 Then
            If c = 20 Then
                b = 1
            ElseIf c = 30 Then
                b = 4
            Else
                b = 2
            End If
        ElseIf a = 15 Then
            b = 5
        Else
            b = 3
        End If
     """,
     {"a" : 10, "b" : 1, "c" : 20}
    ))

# Test else branch of If
tests.append(
    ("""a = 10
        b = 0
        c = 30
        If a = 10 Then
            If c = 20 Then
                b = 1
            ElseIf c = 30 Then
                b = 4
            Else
                b = 2
            End If
        ElseIf a = 15 Then
            b = 5
        Else
            b = 3
        End If
     """,
     {"a" : 10, "b" : 4, "c" : 30}
    ))

# Test else branch of If
tests.append(
    ("""a = 15
        b = 0
        c = 30
        If a = 10 Then
            If c = 20 Then
                b = 1
            ElseIf c = 30 Then
                b = 4
            Else
                b = 2
            End If
        ElseIf a = 15 Then
            b = 5
        Else
            b = 3
        End If
     """,
     {"a" : 15, "b" : 5, "c" : 30}
    ))
# << If tests >> (7 of 7)
# Lots of inline ifs
tests.extend([
    ("a = 0\nIf 1 < 2 Then a = 10", {"a" : 10,}),	
    ("a = 0\nIf 2 < 1 Then a = 10", {"a" : 0,}),
    ("If 1 < 2 Then a = 10 Else a = 20", {"a" : 10,}),	
    ("If 1 > 2 Then a = 10 Else a = 20", {"a" : 20,}),	
])

# Bug #810401 python if statements may be missing a body 
tests.append((
"""
a = 0
If 1 < 2 Then Resume Next
a = 10
""", {"a" : 10,}))

# Inline if with multiple items
tests.append((
"""
_x = 0
If _x = 0 Then a = 1: b = 2: Else a = 10: b = 20
_x = 1
If _x = 0 Then c = 1: d = 2: Else c = 10: d = 20
""", {"a" : 1, "b": 2, "c": 10, "d": 20}))

# Inline if with no then
tests.append((
"""
_x = 1 = 1
_y = 1 = 2
a = 0
b = 0
If _x 
a = 1
End If
If _y
b = 1
End If
""", {"a" : 1, "b": 0,}))

# If block with an inline else
tests.append((
"""
_x = 0
_y = 1
a = 1
If _x Then
a = -1
ElseIf _y Then a = 2
End If
""", {"a": 2}
))

tests.append((
"""
_x = 0
_y = 0
a = 1
b = 1
If _x Or Not (_y = 1) Then a = 2
If _x Or Not (_y = 0) Then b = 2
""", {"a": 2, "b": 1}
))


# Very weird "Then Else"
tests.append((
"""
x = 0
y = 0
_a = 0
If _a = 0 Then Else x = 1
If _a = 1 Then Else y = 1
""", {"x": 0, "y": 1}
))
tests.append((
"""
x = 0
y = 0
_a = 0
If _a = 0 Then Else 
    x = 1
End If
If _a = 1 Then Else
    y = 1
End If
""", {"x": 0, "y": 1}
))


import vb2py.vbparser
vb2py.vbparser.log.setLevel(0) # Don't print all logging stuff
TestClass = addTestsTo(BasicTest, tests)

if __name__ == "__main__":
    main()
