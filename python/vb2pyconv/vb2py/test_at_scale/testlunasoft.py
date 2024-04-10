
import unittest
from vb2py.test_at_scale import file_tester


class Test_lunasoft(file_tester.FileTester):

	def test0(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/UNIT_TEST.frm')

	def test1(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/Cancelation.cls')

	def test2(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/Authentication.cls')

	def test3(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/Issue.cls')

	def test4(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/Base64Coder.bas')

	def test5(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/basUtf8FromString.bas')

	def test6(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/Stamp.cls')

	def test7(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/Validate.cls')

	def test8(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/lunasoft/SW-Services/AccountBalance.cls')


if __name__ == '__main__':
	unittest.main()
