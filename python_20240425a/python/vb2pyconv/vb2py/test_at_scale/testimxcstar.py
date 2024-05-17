
import unittest
from vb2py.test_at_scale import file_tester


class Test_imxcstar(file_tester.FileTester):

	def test0(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Cls/MiniblinkAPI.cls')

	def test1(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Cls/MiniblinkCallBack.cls')

	def test2(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Cls/MiniblinkTypeEnum.cls')

	def test3(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Cls/fastcallCallback.cls')

	def test4(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Cls/SBrowserCls.cls')

	def test5(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Cls/cUniversalDLLCalls.cls')

	def test6(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/使用例子/VB6/Form1.frm')

	def test7(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/使用例子/VB.Net/WindowsApp5/WindowsApp5/Form1.Designer.vb')

	def test8(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/使用例子/VB.Net/WindowsApp5/WindowsApp5/Form1.vb')

	def test9(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/使用例子/VB.Net/WindowsApp5/WindowsApp5/My Project/Application.Designer.vb')

	def test10(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/使用例子/VB.Net/WindowsApp5/WindowsApp5/My Project/Resources.Designer.vb')

	def test11(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/使用例子/VB.Net/WindowsApp5/WindowsApp5/My Project/Settings.Designer.vb')

	def test12(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/使用例子/VB.Net/WindowsApp5/WindowsApp5/My Project/AssemblyInfo.vb')

	def test13(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Bas/MiniblinkAPIConst.bas')

	def test14(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Bas/MyModule.bas')

	def test15(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Bas/SBrowserCallBack.bas')

	def test16(self):
		self._testFile('/Users/paul/Workspace/sandbox/vb2py-git-files/imxcstar/Bas/wke.bas')


if __name__ == '__main__':
	unittest.main()
