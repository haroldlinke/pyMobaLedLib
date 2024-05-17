"""
This is a simple script to run all unit tests in a directory and its subdirectories.
It simply searches for all modules ending in "Test", imports them all, calls suite()
on each one, composes all of those suites, and runs the resultant suite.

The easiest way to define a suite function in each of your test modules is to use
the pyunit module. Simply call pyunit.exportAllTests() after you have declared all
of your tests, and it will define a suite() function that will work.

This script can run with any test runner. Simply pass the module and classname on
the command line. It defaults to using pyunit.TextTestRunner.
"""
import os
import sys
import types
import re
import pyunit

def loadTheSuite(modName):
  try:
    mod = __import__(modName, globals(), locals(), [])
  except:
    print "Failed to import module %s while trying to locate tests." % modName
    return None
  attrs = mod.__dict__.values()
  attrs = filter(
    lambda obj: isinstance(obj, (type, types.ClassType))
      and issubclass(obj, pyunit.unittest.TestCase),
    attrs)
  return pyunit.unittest.TestSuite(map(pyunit.makeUsualSuite, attrs))
  
def getIgnorePattern():
  try:
    oldpath = sys.path
    sys.path = [os.getcwd()]
    if sys.modules.get('testIgnore', None):
      del sys.modules['testIgnore']
    import testIgnore
    sys.path = oldpath
    print 'Ignoring some files in %s, with pattern %s' \
      % (os.getcwd(), testIgnore.ignore)
    return testIgnore.ignore
  except Exception, e:
    return '^$'

def locateAllTestSuites():
  sys.path.append(".")
  testSuites = []
  for root, dirs, files in os.walk('.'):
    walkPos = os.getcwd()
    os.chdir(root)
    ignoredFiles = getIgnorePattern()
    testSuites.extend(
      map(
        lambda fileName: loadTheSuite(os.path.splitext(fileName)[0]),
        filter(
##          lambda x: re.match("[^.]*\.py$", x)
          lambda x: (not x.endswith('.rsrc.py') and x.endswith('.py') or x.endswith('.pyw'))
            and not re.match(ignoredFiles, x),
##            and x!= 'setup.py',
          files)))
    os.chdir(walkPos)
    if 'CVS' in dirs:
      dirs.remove('CVS')  # don't visit CVS directories
  testSuites = filter(
    lambda x: x != None,
    testSuites)
  return pyunit.TestSuite(testSuites)

def printUsage():
  print """
This script locates and runs all tests in test modules in the current directory
or any of its subdirectories. A test module is defined as any module which is
named *.py, and includes a function named suite().

Usage:
  python runAllTests.py
    - or -
  python runAllTests.py TestRunnerModule TestRunnerClassName

The first usage will result in all tests being run via the TextTestRunner. The
second usage allows you to specify which test runner should be used to collect
and output the results of the test. Any test runner may be used, as long as it
meets the requirements of the unittest module, and can be found on the python
include path.

"""

def selectTestRunner(argv):
  if(1 == len(argv)):
    return pyunit.TextTestRunner()
  else:
    if(3 == len(argv)):
      mod = __import__(argv[1], globals(), locals(), [])
      return getattr(mod, argv[2])()
    else:
      printUsage()
      raise IndexError("Please correct the script arguments to match above usage guidelines.")

def run(argv=[""]):
  pyunit.runTests(
    locateAllTestSuites(),
    selectTestRunner(argv))

if(__name__ == "__main__"):
  run(sys.argv)
