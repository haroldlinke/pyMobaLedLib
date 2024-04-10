#!/usr/bin/python
# RPN.py - an HP11 calulator clone (sorta)

# TO DO 
# make sure stack has at least 4 values after every operation



"""
__version__ = "$Revision: 1.10 $"
__date__ = "$Date: 2005/12/13 11:13:24 $"
"""

from PythonCard import dialog, model

class STACK:
    ''' Manages the stack (X,Y,Z, and T registers) and
        the 10 memory registers (0-9) '''
    
    def __init__(self):
        ''' Initialize stack and registers '''
        # init stack T, Z, Y, X , top of stack is at the right side
        self._emptyStack = [0.0, 0.0, 0.0, 0.0]
        self._stackData = self._emptyStack
        # new_data_flag is set when the first new character is entered for a value
        self.clr_flag()  
        # create a list for all 10 Storage Registers, initialize to 0
        self._mem = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
    def display(self):
        ''' display stack and memory data '''
        print "\nStack: ", self._stackData
        print "Mem:   ", self._mem, "\n"

    def stackSize(self):
        ''' make sure stack has at least 4 elements '''
        while len(self._stackData) < 5:
            self.display()
            self._stackData.insert(0,0.0)

    # Stack functions
    def rotate(self): 
        ''' rotate top 4 elements of stack '''
        self.stackSize()
        # remove top 4 elements, then add back to stack in reverse order
        self._X = self._stackData.pop()
        self._Y = self._stackData.pop()
        self._Z = self._stackData.pop()
        self._T = self._stackData.pop()
        self._stackData.append(self._X)
        self._stackData.append(self._T)
        self._stackData.append(self._Z)
        self._stackData.append(self._Y)

    def push(self, value):
        ''' add value to top of stack '''
        self._stackData.append(float(value))

    def pop(self):
        ''' remove and return top of stack - X '''
        self.stackSize()
        return self._stackData.pop()
    
    def readX(self):
        ''' return the top of stack, X, no change to stack '''
        return self._stackData[-1:][0]

    def swap(self):
        ''' swap X and Y '''
        self.stackSize()
        self._X = self._stackData.pop()
        self._Y = self._stackData.pop()
        self._stackData.append(self._X)
        self._stackData.append(self._Y)

    def add(self):
        ''' X = X + Y '''
        self.stackSize()
        self._stackData.append(self._stackData.pop() + self._stackData.pop())

    def subtract(self):
        ''' X = Y - X '''
        self.stackSize()
        self._stackData.append( - (self._stackData.pop()) + self._stackData.pop())

    def multiply(self):
        ''' X = X * Y '''
        self.stackSize()
        self._stackData.append(self._stackData.pop() * self._stackData.pop())
    
    def divide(self):
        ''' X = Y / X '''
        self.stackSize()
        self._X = self._stackData.pop()
        self._Y = self._stackData.pop()
        if self._X != 0.0:
            self._X = self._Y / self._X
        else:
            self._X = None
        self._stackData.append(self._X)

    # memory operations
    def SetReg(self, reg, value):
        ''' write value into memory register reg'''
        if (reg == int(reg) and (reg >= 0) and (reg <=9)):  
            self._mem[int(reg)] = value
        else:
            print "Error - invalid register"

    def GetReg(self, reg):
        ''' read memory register reg '''
        if (reg == int(reg) and (reg >= 0) and (reg <=9)):
            return self._mem[int(reg)] 
        else:
            print "Error - invalid register"  
            return None

    # These functions operate on the new_data_flag
    # Ehe flag is set when new data is entered into the 
    # text entry box, before the 'Enter' key is pressed
    def set_flag(self): self.new_data_flag = 1
    def clr_flag(self): 
        self.new_data_flag = 0
    def get_flag(self): return self.new_data_flag

class RPN(model.Background):
    ''' RPN Calculator '''
    def on_initialize(self, event):
        # can't use a variable named self.stack
        # because that would conflict with self.stack defined in the Background class
        self._stack = STACK()
                        
    # menu functions    
    def on_menuHelpAbout_select(self,  event):
        try:
            self.readme = open('RPN.about.txt').read()
        except IOError:
            self.readme = 'RPN.about.txt not found'
        dlg = dialog.ScrolledMessageDialog(self, self.readme, 'About RPN Calc ...')

    def on_menuHelpContents_select(self, event):
        try:
            self.readme = open('RPN.help.txt').read()
        except IOError:
            self.readme = 'RPN.help.txt not found'
        dlg = dialog.ScrolledMessageDialog(self, self.readme, 'RPN Calc Help ...')

    # operation buttons
    def on_EnterBtn_mouseClick(self, event):
        try:
            self._stack.push(self.components.result.text)
            # update display to float
            self.components.result.text = str(self._stack.readX())
        except ValueError:
            print "ERROR - invalid number"
            self.components.result.text = "ERROR"
        self._stack.clr_flag()
        self._stack.display()

    def on_InvertBtn_mouseClick(self, event): 
        self.storeX()
        # don't divide by zero
        if self._stack.readX != 0:
            self._stack.push( 1 / self._stack.pop() )
        else:
            self.stack.pop()
            self._stack.push(None)
        self.components.result.text = str(self._stack.readX())
        self._stack.display()

    def on_ROTBtn_mouseClick(self, event):
        self.storeX()
        self._stack.rotate()
        # put X back into the result box
        self.components.result.text = str(self._stack.readX())
        self._stack.display()


    def on_SwapBtn_mouseClick(self, event):    
        self.storeX()
        self._stack.swap()
        # put X back into the result box
        self.components.result.text = str(self._stack.readX())
        self._stack.display()


    def on_BackBtn_mouseClick(self, event):    
        if self._stack.get_flag() == 1:
            # remove the last entry and stuff back into result
            self.components.result.text = self.components.result.text[:-1]
            # self.components.result.text = str(self._stack.X)
            
    def on_PlusBtn_mouseClick(self, event):    
        self.storeX()   
        self._stack.add()
        # put X back into the result box
        self.components.result.text = str(self._stack.readX())
        self._stack.display()
   
    def on_MinusBtn_mouseClick(self, event):    
        self.storeX()
        self._stack.subtract()
        # put X back into the result box
        self.components.result.text = str(self._stack.readX())
        self._stack.display()


    def on_MultiplyBtn_mouseClick(self, event):    
        self.storeX()
        self._stack.multiply()
        # put X back into the result box
        self.components.result.text = str(self._stack.readX())
        self._stack.display()

    
    def on_DivideBtn_mouseClick(self, event):    
        self.storeX()
        self._stack.divide()
        # read the X register to see if operation OK
        self._result = self._stack.readX() 
        if  self._result is not None:   
            self.components.result.text = str(self._result)
        else:
            self.components.result.text = "Divide by Zero Error"
        self._stack.display()


    def on_CHSBtn_mouseClick(self, event):
        # make sure that X has most recent data
        if self._stack.get_flag() == 1:
            self._stack.push (float( self.components.result.text ))
        self._stack.push( -1.0 * self._stack.pop() )
        self.components.result.text = str(self._stack.readX())
        self._stack.display()
        
    # storage register operations
    def on_STOBtn_mouseClick(self, event):
        self.storeX()    
        # pop the X and Y values for the register and the value to write
        self._mem = self._stack.pop()
        self._value = self._stack.pop()
        # is the register a valid  integer value?
        if (self._mem == int(self._mem) and (self._mem >= 0) and (self._mem <=9 )):
            # write value to register
            self._stack.SetReg(self._mem, self._value)
        else:
            # register is a non-integer
            print "ERROR - Non-integer value given for register"
        self._stack.display()

        
    def on_RCLBtn_mouseClick(self, event):
        self.storeX()
        self._stack.clr_flag()
        self._mem = self._stack.pop()
        if(self._mem == int(self._mem) and (self._mem >= 0) and (self._mem <=9 )):
            self._stack.push(self._stack.GetReg(self._mem))
            self.components.result.text = str(self._stack.readX())
        else:
            print "ERROR - Non-integer value given for register"
            return
        self._stack.display()

    # misc
    def add_digit(self, new_value):
        ''' add a new digit to the result window '''
        # start at 0 after an operation (+-*/ or Enter)
        if self._stack.get_flag() == 1:
            self.components.result.text = self.components.result.text + new_value
        elif self._stack.get_flag() == 0:
            self.components.result.text = new_value
        self._stack.set_flag()

    def storeX(self):
        ''' If new number has been entered, push it onto the stack '''
        # if necessary, push data onto stack
        if self._stack.get_flag() == 1:
            self._stack.push(self.components.result.text)
        self._stack.clr_flag()
        
    # calculator digit buttons (and the decimal '.')
    def on_0Btn_mouseClick(self, event): self.add_digit('0') 
    def on_1Btn_mouseClick(self, event): self.add_digit('1')
    def on_2Btn_mouseClick(self, event): self.add_digit('2')
    def on_3Btn_mouseClick(self, event): self.add_digit('3')
    def on_4Btn_mouseClick(self, event): self.add_digit('4')
    def on_5Btn_mouseClick(self, event): self.add_digit('5')
    def on_6Btn_mouseClick(self, event): self.add_digit('6')    
    def on_7Btn_mouseClick(self, event): self.add_digit('7')
    def on_8Btn_mouseClick(self, event): self.add_digit('8')    
    def on_9Btn_mouseClick(self, event): self.add_digit('9')   
    def on_DecimalBtn_mouseClick(self, event): self.add_digit('.')

if __name__ == '__main__':
    app = model.Application(RPN)
    app.MainLoop()
