"""
Created: 2001/08/03
Purpose: When a new release is made, a tag will be created in the cvs tree
         and the VERSION below will be updated to match the tag
         and .zip release file posted.
         For example:
             tag: release_0_8_1
             release file on SourceForge: PythonCard-0.8.1.zip

__version__ = "$Revision: 1.39 $"
__date__ = "$Date: 2004/10/19 22:19:14 $"

"""

VERSION = (0, 8, 2)
VERSION_STRING = ".".join([str(digit) for digit in VERSION])
