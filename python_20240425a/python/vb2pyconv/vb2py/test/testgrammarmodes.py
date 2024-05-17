"""Test of the different grammar modes and settings"""

import re
import unittest
import vb2py.utils
import vb2py.vbparser
import vb2py.parserclasses


class TestGrammarModes(unittest.TestCase):

    def tearDown(self):
        """Tear down the tests"""
        self._setVB6()

    def assertParserFails(self, text, num_blocks):
        """Check that parsing fails for some text"""
        result = vb2py.vbparser.parseVB(text)
        self.assertEqual(len(result.blocks), num_blocks)
        self.assertIsInstance(result.blocks[num_blocks - 1], vb2py.parserclasses.VBParserFailure)

    def assertParsesAndContains(self, text, expected, num_failures=1):
        """Check that parsing succeeds and a bit of text is included"""
        result = vb2py.vbparser.parseVB(text)
        result_text = result.renderAsCode()
        self.assertIn(expected, result_text)
        self.assertEqual(num_failures, len(re.findall('UNTRANSLATED', result_text)))
        return result_text

    def assertParses(self, text):
        """Check that parsing succeeds"""
        result = vb2py.vbparser.parseVB(text)
        result_text = result.renderAsCode()
        self.assertEqual(0, len(re.findall('UNTRANSLATED', result_text)))
        self.assertEqual(0, len(re.findall('ParserError', result_text)))
        return result_text

    def _setDotNet(self):
        """Set .net mode on"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['dialect'] = 'vb.net'

    def _setVB6(self):
        """Set VB6 mode on"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['dialect'] = 'VB6'

    def _setSafe(self):
        """Set safe mode on"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'

    def _setUnsafe(self):
        """Set safe mode off"""
        vb2py.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'rigorous'


class TestSafeMode(TestGrammarModes):
    """Test of the SafeMode class"""

    def setUp(self):
        """Set up the tests"""

    def testSingleLine(self):
        """testSingleLine: single line works in safe mode"""
        text = 'a ='
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[a =]', 1)

    def testLineInBlock(self):
        """testLineInBlock: line a block works"""
        self._setDotNet()
        text = 'a = 1\nb =\nc = 2\nd ='
        self._setUnsafe()
        self.assertParserFails(text, 2)
        self._setSafe()
        self.assertParsesAndContains(text, 'a = Integer(1)', 2)
        self.assertParsesAndContains(text, '[b =]', 2)
        self.assertParsesAndContains(text, 'c = Integer(2)', 2)
        self.assertParsesAndContains(text, '[d =]', 2)

    def testForStart(self):
        """testForStart: works with a failure during the first line of a for"""
        text = 'For i error = 1 To 20\nB = B + 1\nNext i\n'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[For i error = 1 To 20]', 2)
        self.assertParsesAndContains(text, '[Next i]', 2)

    def testForEnd(self):
        """testForEnd: works with a failure during the last line of a for"""
        text = 'For i = 1 To 20\nB = B + 1\n'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[For i = 1 To 20]')

    def testSubWithInnerError(self):
        """testSubWithInnerError: should be able to do a sub with inner error"""
        text = 'Sub DoIt()\na =\nEnd Sub'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[a =]')

    def testSubWithInnerBlockError(self):
        """testSubWithInnerBlockError: should be able to do a sub with inner block error"""
        text = 'Sub DoIt()\nFor i  = 1 To 10\na =\nNext i\nEnd Sub'
        self._setUnsafe()
        self.assertParserFails(text, 1)
        self._setSafe()
        self.assertParsesAndContains(text, '[a =]', 1)

    def testSafeInlineIf(self):
        """testSafeInlineIf: should be able to work with inline if"""
        self._setUnsafe()
        self.assertParses('If X Then DoIt')
        self._setSafe()
        self.assertParses('If X Then DoIt')

    def testIfAndElseIf(self):
        """testIfAndElseIf: should handle ElseIf"""
        text = """
            If A = 10 Then
                    DoSomething()
            ElseIf  B = 20 Then
                    DoSomethingElse()
            Else
                    OtherCase()
                    If B = 20 Then C = 0 Else C = 1
            End If        
        """
        self._setSafe()
        self.assertParses(text)

    def testIfWithOneBlock(self):
        """testIfWithOneBlock: should handle a single block if"""
        text = """
            If A = 10 Then
                b = b -
            End If
        """
        self._setSafe()
        self.assertParsesAndContains(text, "[b = b -]", 1)

    def testWhile(self):
        """testWhile: while should work"""
        text = """
            While A
            Wend   
            
            Do Until A
            Loop    
            
            Do
            Loop Until a
        """
        self._setSafe()
        self.assertParses(text)

    def testSelect(self):
        """testSelect: should zoom in on a select clause"""
        text = """
                Select Case A
                    Case 1
                        B = B + X
                    Case 2
                        B = B - 
                    Case Else
                        B = 0
                    End Select
        """
        self._setSafe()
        self.assertParsesAndContains(text, "[B = B -]", 1)

    def testImplicitCall(self):
        """testImplicitCall: implicit call should work"""
        text = 'DoIt'
        self._setUnsafe()
        self.assertParsesAndContains(text, 'DoIt()', 0)
        self._setSafe()
        self.assertParsesAndContains(text, 'DoIt()', 0)

    def testImplicitCallParameters(self):
        """testImplicitCallParameters: implicit call with parameters should work"""
        text = 'DoIt 10'
        self._setUnsafe()
        self.assertParsesAndContains(text, 'DoIt(10)', 0)
        self._setSafe()
        self.assertParsesAndContains(text, 'DoIt(10)', 0)
        self._setDotNet()
        self._setUnsafe()
        self.assertParsesAndContains(text, 'DoIt(Integer(10))', 0)
        self._setSafe()
        self.assertParsesAndContains(text, 'DoIt(Integer(10))', 0)
        #
        self.assertParsesAndContains('DoIt AddressOf x', 'DoIt(AddressOf(x))', 0)

    def testExplicitCall(self):
        """testExplicitCall: explicit call should work"""
        text = 'CType(Me.NewSizeUpDown, System.ComponentModel.ISupportInitialize).BeginInit()'
        self._setDotNet()
        self._setUnsafe()
        self.assertParsesAndContains(text, 'BeginInit()', 0)
        self._setSafe()
        self.assertParsesAndContains(text, 'BeginInit()', 0)

    def testDoubleElseIf(self):
        """testDoubleElseIf: safe mode with double elseif should work"""
        text = '''
            If A Then
            ElseIf B Then
            ElseIf C Then
            End If        
        '''
        self._setUnsafe()
        self.assertParses(text)
        self._setSafe()
        self.assertParses(text)

    def testForWithLabel(self):
        """testForWithLabel: empty for loop with a label"""
        text = '''
            For i = 1 To 10
            Label:
            Next
        '''
        self._setUnsafe()
        self.assertParses(text)
        self._setSafe()
        self.assertParses(text)

    def testDoWithLabel(self):
        """testDoWithLabel: do loop with a label"""
        text = '''
            Do While a <10
                doi = 1
112         Loop 
        '''
        self._setUnsafe()
        self.assertParses(text)
        self._setSafe()
        self.assertParses(text)

    def testBadlyFormedWith(self):
        """testBadlyFormedWith: badly formed with should work"""
        text = '''
            With ThisThing
            End With
            .Value = 1
        '''
        self._setSafe()
        self.assertParsesAndContains(text, 'With variable outside of block', 0)

    def testIfBlockWithLabels(self):
        """testIfBlockWithLabels: if block with labels should work"""
        text = '''
            102     If vTask Is Nothing And vItem Is Nothing Then
            104         Set vItem = LstTasks.SelectedItem
            106         Set vTask = ListItemToTask(vItem)
            108     ElseIf vTask Is Nothing Then
            110         Set vTask = ListItemToTask(vItem)
            112     Else 
            114         Set vItem = TaskToTaskListItem(vTask)
                    End If        
        '''
        self._setSafe()
        self.assertParses(text)

    def testSelectBlockWithLabels(self):
        """testSelectBlockWithLabels: select block with labels should work"""
        text = '''
            100 Select Case X
            110 Case 10
            120 Case 20
            130 End Select
        '''
        self._setSafe()
        self.assertParses(text)

    def testDirectiveWithEndComment(self):
        """testDirectiveWithEndComment: a directive with end comment"""
        text = '''
        #If DEBUG_MODE Then  

          If RootDepth > 5 Then
      '      SendCommand "D:" & RootDepth & ">>> Search A:" & RootAlpha & ", B:" & RootBeta & " => SC: " & FinalScore
          End If
        #End If        '
        '''
        self._setSafe()
        self.assertParses(text)

    def testDirectiveWithStartComment(self):
        """testDirectiveWithStartComment: a directive with start comment"""
        text = '''
            #If 0 Then  ' In Visual Basic? No way!
             a = 1
            #End If
        '''
        self._setSafe()
        self.assertParses(text)

class TestDotNet(TestGrammarModes):
    """Test of the .net conversion dialect"""

    def testDotNetFunctionReturns(self):
        """testDotNetFunctionReturns: return should be simplified in .net"""
        text = """
        Function A()
            Return 10
        End Function
        """
        self._setDotNet()
        r = self.assertParses(text)
        self.assertIn('return Integer(10)', r)

    def testClassAsKeyword(self):
        """testClassAsKeyword: class as keyword should be OK in VB6"""
        text = 'Class = 1'
        self._setVB6()
        self.assertParses(text)
        self._setDotNet()
        self.assertParserFails(text, 1)

    def testDotNetRegions(self):
        """testDotNetRegions: test that regions work"""
        text = '''
        #Region "the first"
        Public Sub DoIt()
        End Sub
        #End Region
        '''
        self._setVB6()
        self.assertParserFails(text, 1)
        self._setDotNet()
        self.assertParses(text)
        self._setSafe()
        self.assertParses(text)


if __name__ == '__main__':
    unittest.main()