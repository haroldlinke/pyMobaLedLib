
import unittest
from vb2py.test_at_scale import file_tester


class Test_wqweto(file_tester.FileTester):

	def test0(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/wqweto/Sample2/Form1.frm')

	def test1(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/wqweto/Src/mdGlobals.bas')

	def test2(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/wqweto/Src/cVszStream.cls')

	def test3(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/wqweto/Src/cVszArchive.cls')

	def test4(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/wqweto/Src/cVszDummy.cls')


if __name__ == '__main__':
	unittest.main()
