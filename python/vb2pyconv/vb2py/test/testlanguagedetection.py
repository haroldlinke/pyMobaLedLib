"""Test of the language detection class"""

import unittest
import os
import re
from vb2py.conversionserver import detectLanguage
from vb2py.test_at_scale import file_tester


class TestLanguageDetection(unittest.TestCase):
    """Test of the LanguageDetection class"""

    def setUp(self):
        """Set up the tests"""

    def tearDown(self):
        """Tear down the tests"""

    @classmethod
    def addTests(cls, folder):
        """Add all tests from folder"""
        filenames = file_tester.scanForFiles(folder, ['.vb'])
        #filenames = [os.path.join(file_tester.BASE_FOLDER, 'submitted', '2019-09-11 14:54:49 code.vb')]
        #
        for idx, filename in enumerate(filenames):
            extn = os.path.splitext(filename)[1]
            name = os.path.split(filename)[1]
            name = name.replace(' ', '').replace('-', '').replace(':', '').replace('.', '')

            def get_fn(filename):
                """Return a test function"""
                def test_fn(self):
                    with open(filename, 'r') as f:
                        text = file_tester.FileTester.getFileText(filename)
                        if text.strip():
                            finder = re.match(r"'VB2PY-(\S+)", text)
                            if finder:
                                expect = finder.group(1)
                            else:
                                expect = 'VB.NET' if os.path.splitext(filename)[1].lower() == '.vb' else 'VB6'
                            language = detectLanguage(text)
                            self.assertEqual(expect, language)

                return test_fn
            #
            setattr(TestLanguageDetection, 'test_{}'.format(name), get_fn(filename))


#TestLanguageDetection.addTests(file_tester.BASE_FOLDER)
TestLanguageDetection.addTests(os.path.join(file_tester.BASE_FOLDER, 'submitted'))


if __name__ == '__main__':
    unittest.main()
