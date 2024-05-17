
import unittest
from vb2py.test_at_scale import file_tester


class Test_VykosX(file_tester.FileTester):

	def test0(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/VykosX/Forms/frmAbout.frm')

	def test1(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/VykosX/Class Modules/CEventHandler.cls')

	def test2(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/VykosX/Modules/modGeneral.bas')

	def test3(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/VykosX/Modules/modIcons.bas')

	def test4(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/VykosX/Modules/modClipboard.bas')

	def test5(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/VykosX/Modules/modProjectExplorer.bas')


if __name__ == '__main__':
	unittest.main()
