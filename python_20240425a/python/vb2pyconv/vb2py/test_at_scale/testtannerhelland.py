
import unittest
from vb2py.test_at_scale import file_tester


class Test_tannerhelland(file_tester.FileTester):

	def test0(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/Compression.bas')

	def test1(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/frmTest.frm')

	def test2(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressZLibNG.cls')

	def test3(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressLZMS.cls')

	def test4(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/VB_Hacks.bas')

	def test5(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressZThunk.cls')

	def test6(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressZLib.cls')

	def test7(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressXPressHuff.cls')

	def test8(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressLz4.cls')

	def test9(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressLz4HC.cls')

	def test10(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressXPress.cls')

	def test11(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressBrotli.cls')

	def test12(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/ICompress.cls')

	def test13(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressMSZip.cls')

	def test14(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressLibDeflate.cls')

	def test15(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tannerhelland/pdCompressZstd.cls')


if __name__ == '__main__':
	unittest.main()
