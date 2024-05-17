#
# Turn off logging in extensions (too loud!)
import vb2py.extensions
import unittest
from unittest import main
vb2py.extensions.disableLogging()

from vb2py.vbparser import convertVBtoPython, VBClassModule, VBModule, VBFormModule, VBCodeModule, VBDotNetClass, VBDotNetModule
import vb2py.vbfunctions as vbfunctions
import vb2py.vbfunctions

tests = []

def BasicTest():
    """Return a new class - we do it this way to allow this to work properly for multiple tests"""
    class _BasicTest(unittest.TestCase):
        """Holder class which gets built into a whole test case"""
    return _BasicTest


def getTestMethod(container, vb, assertions):
    """Create a test method"""
    def testMethod(self):
        local_dict = {"convertVBtoPython" : convertVBtoPython,
                      "vbfunctions" : vbfunctions}
        # << Parse VB >>
        try:					  
            python = convertVBtoPython(vb, container=container, dialect=container.expected_dialect)
        except Exception as err:
            self.fail("Error while parsing (%s)\n%s" % (err, vb))
        # -- end -- << Parse VB >>
        # << Execute the Python code >>
        try:
            exec("from vb2py.vbfunctions import *", local_dict)
            exec(python, local_dict)
        except Exception as err:
            self.fail("Error (%s):\n%s\n....\n%s" % (err, vb, python))
        # -- end -- << Execute the Python code >>
        # << Check assertions >>
        reason = ""

        internal_dict = {"python" : python, "vb" : vb}

        for assertion in assertions:
            if assertion.startswith("$"):
                dct = internal_dict
                assertion = assertion[1:]
            else:
                dct = local_dict
            try:
                exec(assertion, dct)
            except Exception as err:
                reason += "%s (%s)\n" % (Exception, err)
        # -- end -- << Check assertions >>
        #print vb, "\n\n", python, "\n\n--------------------------------"
        #
        self.assertTrue(reason == "", "Failed: %s\n%s\n\n%s" % (reason, vb, python))

    return testMethod

#
# Add tests to main test class
def addTestsTo(TestClassFactory, tests):
    """Add all the tests to the test class"""
    TestClass = TestClassFactory()
    for idx in range(len(tests)):
        setattr(TestClass, "test%d" % idx, getTestMethod(*tests[idx]))
    return TestClass
