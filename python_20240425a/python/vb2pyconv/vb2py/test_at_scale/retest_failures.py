
from vb2py.test_at_scale import file_tester
import glob
import os
import unittest
import vb2py.extensions
from vb2py.utils import TextColours as T


vb2py.extensions.disableLogging()

def get_test(filename):
    def testMethod(self):
        print('%sTrying %s%s' % (T.OKBLUE, filename, T.ENDC))
        self._testFile(filename, store_failure=False)
        print('%sSucceeded - removing file %s%s' % (T.OKGREEN, filename, T.ENDC))
        os.remove(filename)
    return testMethod


class AllTests(file_tester.FileTester):
    """Base for all tests"""


if __name__ == '__main__':
    #
    # Create test
    files = glob.glob(os.path.join(file_tester.FAILURES_FOLDER, '*.cls'))
    for idx, file in enumerate(files):
        setattr(AllTests, ('test_%s' % idx), get_test(file))
    #
    unittest.main()

