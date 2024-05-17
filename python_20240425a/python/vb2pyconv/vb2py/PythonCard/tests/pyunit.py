"""
This is a simple uability extension for unittest. It only exports a subset of the names in that
module, making it simpler to see which ones matter. Futhermore, it extracts the boilerplate
involved in the most common method of unit testing, so that a test declaration module needs only
one import and one statement besides the definitions for the tests.

Any test module that uses pyunit will actually support two methods of running tests. The first is
to simply run it as a script. If you do, it will run all of its tests and return. The second method
is to load it and call its suite() method, which will then return a pyunit.TestSuite. Test suites
can be composed, and then run in a batch. This makes it easy to run all of your tests in a batch
as long as they all pass, then to drill down by just running the script for any test which is failing.

The most important symbols exported from the pyunit module are:

classes:
  TestCase
  TestSuite
  TextTestRunner
  TestRunner

functions:
  exportAllTests()
  runTests(TestSuite, [TestRunner])

To show how they are used, I have included a sample declaration of a test suite, and a sample
script for running a test suite.

Declaring tests:

import pyunit

class CallTests(pyunit.TestCase):
  def testEmpty(self):
    pass

class MoreTests(pyunit.TestCase):
  def testEmpty(self):
    pass
  def testFailing(self):
    assert 1 == 2

pyunit.exportAllTests()

That's it. Now for running tests in a few modules that you know the name of:

import MyTests, MyOtherTests, pyunit

suite = pyunit.TestSuite((MyTests.suite(), MyOtherTests.suite())
pyunit.runTests(suite)

# or, to use a special test runner
import FancyRunners
pyunit.runTests(suite, FancyRunners.XMLRunner())

Again, pretty simple. All of the work comes in finding the modules that you want
to run tests from. You may want to look at the script runAllTests.py for an
example: it runs all tests defined in modules of a certain name, in any subdirectory
of the directory in which it is run.
"""
import unittest
from unittest import TestCase, TestSuite, TextTestRunner

def makeUsualSuite(obj):
  return unittest.makeSuite(obj, 'test')

def suite(dictToExportFrom):
  import types
  tests = []
  for name in dictToExportFrom:
    obj = dictToExportFrom[name]
    if(isinstance(obj, (type, types.ClassType)) and
      issubclass(obj, unittest.TestCase)):
      tests.append(obj)
  return unittest.TestSuite(map(makeUsualSuite,tests))

def callersGlobals():
  """
  returns the globals dictionary active from the caller of the function that calls this one.
  """
  import sys
  try:
    raise Exception("dummy")
  except Exception:
    return sys.exc_info()[2].tb_frame.f_back.f_back.f_globals

def exportAllTests():
  """
  This function must be called from some other module. This function will do one of two
  things, depending on whether the calling module is the __main__ one or not.

  If the calling module is __main__, then it causes that module to immediately run
  any unit tests that it has declared. For this reason, it should always be called
  at top-level scope, as the last line in the file.

  If the caller is not __main__, then exportAllTests() causes that module to define
  a suite() function which exports all of its tests. It does this by mucking with the
  calling module's dictionaries.

  If you call this function from a module that already declares a function named suite,
  the old definition will be overwritten. This is defined to maximally reduce the number
  of lines of boilerplate that must be written in each testing file, not to honor
  encapsulation. You have been warned.
  """
  callingGlobals = callersGlobals()
  if(callingGlobals['__name__'] == '__main__'):
    runTests(suite(callingGlobals))
  else:
    callingGlobals['suite'] = lambda: suite(callingGlobals)

def runTests(testSuite, testRunner=unittest.TextTestRunner()):
  testRunner.run(testSuite)
