#!/usr/bin/python

"""
A mortgage repayment calculator. Used in the presentation at VanPy 2005 and PyCon 2005.

Subsequently borrowed for the presentation at OSDC 2005 
"""
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2005/12/13 11:13:22 $"

from PythonCard import dialog, model
import pyfi

class MyBackground(model.Background)

    def on_initialize(self, event):
        # if you have any initialization
        # including sizer setup, do it here
        self.on_Calculate_mouseClick(None)

    def on_Calculate_mouseClick(self, event):
        comp = self.components
        try:
            principal = float(comp.Principal.text)
            interestRate = float(comp.InterestRate.text)
            if interestRate > 1:
                interestRate = interestRate / 100.0
            payment15 = pyfi.amortization(principal, interestRate, 12, 15 * 12)
            payment30 = pyfi.amortization(principal, interestRate, 12, 30 * 12)
            comp.Result.text = "15 year monthly payment: %.2f\n30 year monthly payment: %.2f" % (payment15, payment30)
        except ValueError:
            dialog.alertDialog(self, 'Please enter valid values', 'Input Value(s) Error')

if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
