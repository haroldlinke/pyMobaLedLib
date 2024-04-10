
import unittest
from vb2py.test_at_scale import file_tester


class Test_tonamalu(file_tester.FileTester):

	def test0(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Studentbook.frm')

	def test1(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/member_details.frm')

	def test2(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/MDIlibrary.frm')

	def test3(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Member_full_details.frm')

	def test4(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Library1.frm')

	def test5(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/entire_book_details1.frm')

	def test6(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Fine.frm')

	def test7(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/entire_book_details.frm')

	def test8(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/changepass.frm')

	def test9(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Member.frm')

	def test10(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Book1.frm')

	def test11(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Book_Details.frm')

	def test12(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/librarian.frm')

	def test13(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Students.frm')

	def test14(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Member_full_details2.frm')

	def test15(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Login.frm')

	def test16(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/library.bas')

	def test17(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/tonamalu/Fine_details.frm')


if __name__ == '__main__':
	unittest.main()
