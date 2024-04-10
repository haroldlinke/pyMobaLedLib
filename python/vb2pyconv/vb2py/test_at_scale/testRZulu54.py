
import unittest
from vb2py.test_at_scale import file_tester


class Test_RZulu54(file_tester.FileTester):

	def test0(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Forms/frmChessX.frm')

	def test1(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Forms/DebugMain.frm')

	def test2(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Forms/Main.frm')

	def test3(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/UtilVBAbas.bas')

	def test4(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Board.bas')

	def test5(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/BitBoard32.bas')

	def test6(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Process.bas')

	def test7(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/CmdOutput.bas')

	def test8(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/clsBoardField.cls')

	def test9(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Eval.bas')

	def test10(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Const.bas')

	def test11(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Time.bas')

	def test12(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Book.bas')

	def test13(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/EPD.bas')

	def test14(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Hash.bas')

	def test15(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Search.bas')

	def test16(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/Debug.bas')

	def test17(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/HashMap.cls')

	def test18(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/ChessBrainVB.bas')

	def test19(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/RZulu54/Development/Modules/IO.bas')


if __name__ == '__main__':
	unittest.main()
