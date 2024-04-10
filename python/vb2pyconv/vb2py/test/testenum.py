from vb2py.test.testframework import *


# Simple test with missing
tests.append(("""
Enum thing
    _one 
    _two = 2
    _three 
    _four
End Enum

a = _one
b = _two
c = _three
d = _four
""", {"a":0, "b":2, "c":1, "d":3}))

# Simple test
tests.append(("""
Enum thing
    _one
    _two
    _three
    _four
End Enum

a = _one
b = _two
c = _three
d = _four
""", {"a":0, "b":1, "c":2, "d":3}))


# Simple test with values
tests.append(("""
Enum thing
    _one = 1
    _two = 2
    _three = 3
    _four = 4
End Enum

a = _one
b = _two
c = _three
d = _four
""", {"a":1, "b":2, "c":3, "d":4}))

tests.append(('''
Enum A
  _B = 1
  ' A comment
End Enum
a = _B

''', {"a": 1}))



# -- end -- << Enum tests >>

import vb2py.vbparser
vb2py.vbparser.log.setLevel(0) # Don't print all logging stuff
TestClass = addTestsTo(BasicTest, tests)

if __name__ == "__main__":
    main()
