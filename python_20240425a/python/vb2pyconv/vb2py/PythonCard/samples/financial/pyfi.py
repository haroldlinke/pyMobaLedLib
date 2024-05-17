#!/usr/bin/python

"""A finance library for Python.

All interest rates are to be expressed in decimal notation
(i.e. 0.0825 instead of 8.25)

This library has been placed in the public domain.

Version history:

1.0 - 2001-01 - Initial program - Rupert Scammell <rupe@yak.net>

2.0 - 2001-03 - Additions and revisions by Louis Luangkesorn
                <lluang@northwestern.edu>
                (compound interest present value,
                 equivalent value of an annuity)
                
2.1 - 2004-01 - Readability changes by Matthew Scott <spud@goldenspud.com>
"""


import sys
import math


def simpleInterest(p, r, t):
    """Simple interest

    Returns: interest value

    Input values:
    See 'Simple interest future value' below
    """
    i = p * r * t
    return i


def simpleInterestFutureValue(p, r, t):
    """Simple interest future value
    
    Returns:  future value
    
    Input values:
    p : principal
    r : Interest rate (decimal)
    t : Investment periods
    """
    fv = p * (1 + r * t)
    return fv


def compoundedInterest(fv, p):
    """Compounded interest
    
    Returns: Interest value
    
    Input values:
    fv : Future value
    p  : Principal
    """
    i = fv - p
    return i


def compoundInterestFutureValue(p, r, c, n):
    """Compound interest future value
    
    Returns: future value
    
    Input values:
    p : principal
    r : interest rate
    c  : number of compounding periods in a year
    n  : (c * t) , total number of compounding periods
    """
    fv = (p * (1 + (r / c))) ** n
    return fv


def annualYield(r, c):
    """Annual yield
    
    Returns: Simple interest rate necessary to yield the same amount
    of dollars yielded by the annual rate r compounded c times for one
    year
    
    Input values:
    r : interest rate
    c : number of compounding periods in a year
    """
    y = ((1 + (r / c)) ** c) - 1
    return y


def ordinaryAnnuity(pymt, p, r, c, n):
    """Ordinary annuity formula
    
    Returns: future value
    
    Input values:
    pymt : payment made during compounding period
    p : principal
    r : annual interest rate
    c  : number of compounding periods in a year
    n  : total number of payments
    """
    block1 = ((1 + (r / c)) ** n) - 1
    block2 = r / c
    fv = pymt * (block1 / block2)
    return fv


def presentValueAnnuity(pymt, r, c, n):
    """Present value of an annuity

    Returns: Lump sum that can be deposited at the beginning of the
    annuity's term, at the same interest rate and with the same
    compounding period, that would yield the same amount as the
    annuity.
   
    Input values:
    See 'Ordinary annuity formula' above."""
    ipp = r / c
    pval = pymt * ((1 - ((1 + ipp) ** (-n))) / ipp)
    return pval


def equivalentAnnualCost(pval, r, c, n):
    """Equivalent value of an annuity

    Returns: Coupon amount for an annuity given the present value

    Input values:
    pval : present value of annuity
    r : annual interest rate
    c  : number of compounding periods in a year
    n  : total number of payments

    See 'Ordinary annuity formula' above.
    """
    ipp = r / c
    pymt = pval / ((1 - ((1 + ipp) ** (-n))) / ipp)
    return pymt

def amortization(loan, r, c, n):
    """Amortization

    Returns: The amount of money that needs to be paid at the end of
    each period to get rid of the total loan.

    Input values:
    loan : Total loan amount
    r : annual interest rate
    c : number of compounding periods a year
    n : total number of compounding periods
    """
    ipp = r / c
    amt = (loan * ipp) / (1 - ((1 + ipp) ** (-n)))
    return amt


def compoundInterestPresentValue(p, r, c, n):
    """Compound interest present value

    Returns: present value

    Input values:
    p : principal
    r : interest rate
    c  : number of compounding periods in a year
    n  : (c * t), total number of compounding periods
    """
    pv = (p / ((1 + (r / c)) ** n))
    return pv
