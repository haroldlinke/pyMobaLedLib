"""Tests that we know fail but are not within the scope of v0.2"""

import vb2py.vbparser
from vb2py.test import complexframework
from vb2py.test.testframework import *
vb2py.vbparser.log.setLevel(0)


# Simple function with ByRef argument which is changed
tests.append(("""
Function _square(x, y)
    _square = x*x
    y = y + 1
End Function
b = 0
a = _square(10, b)
""", {"a": 100, "b": 1}))

# Optional arguments
tests.append(("""
Sub _Change(ByVal x, ByRef y)
    x = x + 1
    y = y + 1
End Sub
a = 0
b = 0
_Change a, b
""", {"a": 0, "b": 1}))

# From testassignment.py
tests.extend([
("""
Dim _a As Object
If _a Is Nothing Then
    b = 1
Else
    b = 2
End If
""", {"b" : 1}),
])

# From testfiles.py
# Dir
tests.append((r"""
_path = "%s"
Open _path & "\origname.txt" For Output As #3
Close #3
a = Dir(_path & "\origname.txt")
Name _path & "\origname.txt" As _path & "\knewname.txt"
b = Dir(_path & "\origname.txt")
c = Dir(_path & "\knewname.txt")
""" % (vb2py.utils.relativePath("test")),
{
'a' : "origname.txt",
'b' : "",
'c' : "knewname.txt",
}))

# Dir
tests.append((r"""
_path = "%s"
Open _path & "\origcopy.txt" For Output As #3
Print #3, "original"
Close #3
a = Dir(_path & "\origcopy.txt")
b = Dir(_path & "\finalcopy.txt")
FileCopy _path & "\origcopy.txt", _path & "\finalcopy.txt"
c = Dir(_path & "\origcopy.txt")
d = Dir(_path & "\finalcopy.txt")
""" % (vb2py.utils.relativePath("test")),
{
'a' : "origcopy.txt",
'b' : "",
'c' : "origcopy.txt",
'd' : "finalcopy.txt",
}))

# Open with Random access
tests.append((r"""
Open "%s" For Random As #3 Len = 2
' !!!!Dont expect this to work!!!!
Input #3, a
Input #3, b
Input #3, c, d, e
Input #3, f, g
Close #3
""" % vb2py.utils.relativePath("test/testread.txt"), {'a' : 'This wont work!!!!'}))

# From testoperators.py
tests.append(
    ('a = "one" & "the" & "dog" Like "???dog"', {"a" : 0}),
)


# From testclassmethods.py
#
# Make sure class properties are not shared
complexframework.tests.append((
        complexframework.VBClassModule(),
        """
        Public arr(20)

        Public Sub DoIt(Value As Integer)
            arr(10) = Value
        End Sub
        """,
        ("A = MyClass()\n"
         "B = MyClass()\n"
         "A.DoIt(10)\n"
         "B.DoIt(20)\n"
         "assert A.arr[10] == 10, 'A.arr[10] was (%s)' % (A.arr[10],)\n"
         "assert B.arr[10] == 20, 'B.arr[10] was (%s)' % (B.arr[10],)\n",)
))


TestClass = addTestsTo(BasicTest, tests)
ComplexTestClass = complexframework.addTestsTo(complexframework.BasicTest, complexframework.tests)


# From testassignment.py
from vb2py.plugins.attributenames import TranslateAttributes

class TestAttributeNames(unittest.TestCase):

    def setUp(self):
        """Setup the tests"""
        self.p = TranslateAttributes()

    # << Tests >>
    def testAll(self):
        """Do some tests on the attribute"""
        names =(("Text", "text"),
                ("Visible", "visible"),)
        for attribute, replaced in names:
            for pattern in ("a.%s=b", ".%s=b", "b=a.%s", "b=.%s",
                            "a.%s.b=c", ".%s.c=b", "b=a.%s.c", "b=.%s.c",
                            "a.%s.b+10=c", ".%s.c+10=b", "b=a.%s.c+10", "b=.%s.c+10",):
                test = pattern % attribute
                new = self.p.postProcessPythonText(test)
                self.assertEqual(new, pattern % replaced)
        for attribute, replaced in names:
            for pattern in ("a.%slkjlk=b", ".%slkjlk=b", "b=a.%slkjl", "b=.%slkjl",
                            "a.%slkj.b=c", ".%slkj.c=b", "b=a.%slkj.c", "b=.%slkj.c",
                            "a.%slkj.b+10=c", ".%slkj.c+10=b", "b=a.%slkj.c+10", "b=.%slkj.c+10",):
                test = pattern % attribute
                new = self.p.postProcessPythonText(test)
                self.assertNotEqual(new, pattern % replaced)


if __name__ == "__main__":
    main()
