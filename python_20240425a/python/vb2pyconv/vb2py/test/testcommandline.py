"""Test of the Command Line version"""

import unittest
import shutil
import glob
import os
import sys

import vb2py.utils
import vb2py.projectconverter


OUTPUT_FOLDER = os.path.join('/', 'tmp', 'vb2py_cl')


class TestCommandLine(unittest.TestCase):
    """Test of the CommandLine class"""

    def setUp(self):
        """Set up the tests"""
        if os.path.isdir(OUTPUT_FOLDER):
            shutil.rmtree(OUTPUT_FOLDER)
        os.mkdir(OUTPUT_FOLDER)
        if OUTPUT_FOLDER not in sys.path:
            sys.path.append(OUTPUT_FOLDER)

    def tearDown(self):
        """Tear down the tests"""

    def _testProject(self, folder, project_file):
        """Run the command line on a project file"""
        sys.argv = [
            'converter.py',
            os.path.join(folder, project_file),
            OUTPUT_FOLDER
        ]
        vb2py.projectconverter.main()
        #
        # Check files
        expected_files = glob.glob(os.path.join(folder, '*.frm'))
        expected_files.extend(glob.glob(os.path.join(folder, '*.cls')))
        expected_files.extend(glob.glob(os.path.join(folder, '*.bas')))
        #
        for file in expected_files:
            self.assertTrue(os.path.isfile(file))

    def _getFormFile(self, filename):
        """Get some elements from the form file"""
        namespace = {}
        global_namespace = {
            'sys': sys,
        }
        folder, file = os.path.split(filename)
        form_name = os.path.splitext(file)[0]
        with open(os.path.join(OUTPUT_FOLDER, folder, '{}.py'.format(form_name)), 'r') as f:
            text = f.read()
            exec(text, global_namespace, namespace)
        #
        return namespace[form_name], namespace['FormControls_{}'.format(form_name)]

    def testTest1(self):
        """testTest1: test 1 project"""
        self._testProject(vb2py.utils.relativePath('test', 'projects', 'test1'), 'test1.vbp')
        main, c = self._getFormFile('frmMain.frm')
        #
        # Some control properties
        self.assertEqual('Test form in VB', c.Caption)
        self.assertEqual('Factorial', c.FormControls_cmdFactorial.Caption)
        self.assertEqual(375, c.FormControls_Command1.Height)
        #
        # Some class attributes
        self.assertTrue(hasattr(main, '_frmMain__Command1_Click'))
        self.assertTrue(hasattr(main, '_frmMain__btnZeroIt_Click'))

    def testTest3(self):
        """testTest3: test 3 project"""
        self._testProject(vb2py.utils.relativePath('test', 'projects', 'test3'), 'Main Test.vbp')
        main, c = self._getFormFile('frmSettings.frm')
        #
        # Some control properties
        self.assertEqual('Settings', c.Caption)
        self.assertEqual('Main', c.FormControls_txtSection.Text)
        self.assertEqual(3480, c.FormControls_cmdGetAll.Left)
        #
        # Some class attributes
        self.assertTrue(hasattr(main, '_frmSettings__cmdGetAll_Click'))
        self.assertTrue(hasattr(main, '_frmSettings__cmdSet_Click'))


if __name__ == '__main__':
    unittest.main()