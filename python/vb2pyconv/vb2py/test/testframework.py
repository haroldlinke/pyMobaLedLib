#
# Turn off logging in extensions (too loud!)
import vb2py.extensions
vb2py.extensions.disableLogging()

import unittest
from unittest import main
from vb2py.vbparser import convertVBtoPython
import vb2py.vbfunctions as vbfunctions
import vb2py.vbclasses as vbclasses
import vb2py.vbfunctions
import vb2py.parserclasses

#
# Import script testing
try:
    from . import scripttest
except ImportError:
    scripttest = None

#
# Private data hiding may obscure some of the testing so we turn it off
import vb2py.config
import vb2py.parserclasses
Config = vb2py.config.VB2PYConfig()
Config.setLocalOveride("General", "RespectPrivateStatus", "No")
Config.setLocalOveride("General", "ReportPartialConversion", "No")

tests = []

def BasicTest():
    """Return a new class - we do it this way to allow this to work properly for multiple tests"""
    class _BasicTest(unittest.TestCase):
        """Holder class which gets built into a whole test case"""
        dialect = 'VB6'
        container = vb2py.parserclasses.VBModule

    return _BasicTest

# << Test functions >> (1 of 2)
def getTestMethod(vb, result, test_code=None, config=None):
    """Create a test method"""
    def testMethod(self):
        local_dict = {"convertVBtoPython": convertVBtoPython,
                      "vbfunctions": vbfunctions,
                      "vbclasses": vbclasses,
                      }
        #
        if config:
            for section, name, value in config:
                Config.setLocalOveride(section, name, value)
        # << Parse VB >>
        try:
            python = convertVBtoPython(
                vb.replace("\r\n", "\n"),
                dialect=self.dialect,
                container=self.container()
            )
        except Exception as err:
            self.fail("Error while parsing (%s)\n%s" % (err, vb))

        try:
            if test_code is None:
                python_test_code = ''
            else:
                python_test_code = convertVBtoPython(
                test_code.replace("\r\n", "\n"),
                dialect=self.dialect,
            )
        except Exception as err:
            self.fail("Error while parsing test code (%s)\n%s" % (err, test_code))

        # -- end -- << Parse VB >>
        # << Execute the Python code >>
        try:
            exec("from vb2py.vbfunctions import *", local_dict)
            exec(python, local_dict)
            if python_test_code:
                exec(python_test_code, local_dict)
        except Exception as err:
            if "FAIL" not in result:
                self.fail("Error (%s):\n%s\n....\n%s\n%s" % (err, vb, python, python_test_code))
        else:
            if "FAIL" in result:
                self.fail("Should have failed:%s\n\n%s\n%s" % (vb, python, python_test_code))
        # -- end -- << Execute the Python code >>
        # << Work out what is expected >>
        expected = {}
        exec("", expected)
        expected.update(result)
        expected["convertVBtoPython"] = convertVBtoPython
        expected["vbfunctions"] = vbfunctions

        # Variables which we don't worry about
        skip_variables = ["vbclasses", "logging", "logger"]
        # -- end -- << Work out what is expected >>
        # << Check for discrepancies >>
        reason = ""
        for key in local_dict:
            if not (key.startswith("_") or hasattr(vb2py.vbfunctions, key) or key == "MyClass"):
                try:
                    if expected[key] != local_dict[key]:
                        reason += "%s (exp, act): '%s' <> '%s'\n" % (key, expected[key], local_dict[key])
                except KeyError:
                    if key not in skip_variables:
                        reason += "Variable didn't exist: '%s'\n" % key
        # -- end -- << Check for discrepancies >>
        #
        self.assertTrue(reason == "", "Failed: %s\n%s\n\n%s\n%s" % (reason, vb, python, python_test_code))

    return testMethod
# << Test functions >> (2 of 2)
def getScriptTestMethod(vb):
    """Create a test method using the script testing method"""
    if scripttest is None:
        raise ImportError("Could not import script test - must be run on Windows with win32com support")
    def testMethod(self):
        scripttest.testCode(vb)
    return testMethod
# -- end -- << Test functions >>

#
# Add tests to main test class
def addTestsTo(TestClassFactory, tests, dialect='VB6', container=None):
    """Add all the tests to the test class"""
    TestClass = TestClassFactory()
    TestClass.dialect = dialect
    if dialect == 'vb.net':
        TestClass.container = vb2py.parserclasses.VBDotNetModule
    if container:
        TestClass.container = container
    #
    for idx in range(len(tests)):
        setattr(TestClass, "test%d" % idx, getTestMethod(*tests[idx]))
    return TestClass

#
# Add tests to main test class using script testing
def addScriptTestsTo(TestClassFactory, tests):
    """Add all the tests to the test class"""
    TestClass = TestClassFactory()
    for idx in range(len(tests)):
        setattr(TestClass, "test%d" % idx, getScriptTestMethod(tests[idx]))
    return TestClass
