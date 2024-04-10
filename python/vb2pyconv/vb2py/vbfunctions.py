"""
Functions to mimic VB intrinsic functions or things
"""

from .vbclasses import *
from . import utils
from . import config

import math
import sys
import fnmatch  # For Like
import glob  # For Dir
import os
import shutil  # For FileCopy
import random  # For Rnd, Randomize
import time  # For timing
import inspect
from decimal import Decimal
from types import MethodType as instancemethod

try:
    from vb2py.PythonCard.graphic import Bitmap
except:
    Bitmap = None

try:
    import win32com.client
except ImportError:
    win32com = None


class VB2PYCodeError(Exception):
    """An error occurred executing a vb2py function"""


class VB2PYNotSupported(VB2PYCodeError):
    """The requested function is not supported"""


class VB2PYFileError(VB2PYCodeError):
    """Some kind of file error"""


class VB2PYEndOfFile(VB2PYFileError):
    """Reached the end of file"""


# -- end -- << Error classes >>

def Array(*args):
    """Create an array from our arguments"""
    array = VBArray(len(args) - 1, Variant)
    for idx in range(len(args)):
        array[idx] = args[idx]
    return array


def CBool(num):
    """Return the boolean version of a number"""
    n = float(num)
    if n:
        return 1
    else:
        return 0


def Choose(index, *args):
    """Choose from a list of options

    If the index is out of range then we return None. The list is
    indexed from 1.

    """
    if index <= 0:
        return None
    try:
        return args[index - 1]
    except IndexError:
        return None


def CreateObject(classname, ipaddress=None):
    """Try to create an OLE object

    This only works on windows!

    """
    if not win32com:
        raise ImportError('Not on Windows - cannot create COM object')
    if ipaddress:
        raise VB2PYNotSupported("DCOM not supported")
    return win32com.client.Dispatch(classname)


_last_files = []


def Dir(path=None):
    """Recursively return the contents of a path matching a certain pattern

    The complicating part here is that when you first call Dir it return the
    first file. Subsequent calls to Dir with no parameters return the other
    files. When all the files are exhausted, we return an empty string.

    Since we need to remember the original path we have to use a global variable
    which is a bit ugly.

    """
    global _last_files
    if path:
        _last_files = glob.glob(path)
    if _last_files:
        return os.path.split(_last_files.pop(0))[1]  # VB just returns the filename, not full path
    else:
        return ""


def Environ(envstring):
    """Return the String associated with an operating system environment variable

    envstring Optional. String expression containing the name of an environment variable. 
    number Optional. Numeric expression corresponding to the numeric order of the 
    environment string in the environment-string table. The number argument can be any 
    numeric expression, but is rounded to a whole number before it is evaluated. 


    Remarks

    If envstring can't be found in the environment-string table, a zero-length string ("") 
    is returned. Otherwise, Environ returns the text assigned to the specified envstring; 
    that is, the text following the equal sign (=) in the environment-string table for that environment variable.

    """
    try:
        envint = int(envstring)
    except ValueError:
        return os.environ.get(envstring, "")
    # Is an integer - need to get the envint'th value
    try:
        return "%s=%s" % (list(os.environ.keys())[envint], list(os.environ.values())[envint])
    except IndexError:
        return ""


def Erase(*args):
    """Erase the contents of fixed size arrays and return them to their initialized form"""
    for array in args:
        array.erase()


def EOF(channel):
    """Determine if we reached the end of file for the particular channel"""
    return VBFiles.EOF(channel)


def FileLen(filename):
    """Return the length of a given file"""
    return os.stat(str(filename))[6]


def Filter(sourcesarray, match, include=1):
    """Returns a zero-based array containing subset of a string array based on a specified filter criteria"""
    if include:
        return Array(*[item for item in sourcesarray if item.find(match) > -1])
    else:
        return Array(*[item for item in sourcesarray if item.find(match) == -1])


def FreeFile():
    """Return the next available channel number"""
    existing = VBFiles.getOpenChannels()
    if existing:
        return max(existing) + 1
    else:
        return 1


def Hex(num):
    """Return the hex of a value"""
    return hex(CInt(num))[2:].upper()


def IIf(cond, truepart, falsepart):
    """Conditional operator"""
    if cond:
        return truepart
    else:
        return falsepart


def Input(length, channelid):
    """Return the given number of characters from the given channel"""
    return VBFiles.getChars(channelid, length)


def InStr(*args):
    """Return the location of one string in another"""
    if len(args) == 2:
        text, subtext = args
        return text.find(subtext) + 1
    else:
        start, text, subtext = args
        pos = text[start - 1:].find(subtext)
        if pos == -1:
            return 0
        else:
            return pos + start


def InStrRev(text, subtext, start=None, compare=None):
    """Return the location of one string in another starting from the end"""
    assert compare is None, "Compare modes not allowed for InStrRev"
    if start is None:
        start = len(text)
    if subtext == "":
        return len(text)
    elif start > len(text):
        return 0
    else:
        return text[:start].rfind(subtext) + 1


def Int(value):
    """Return the int of a value"""
    n = float(value)
    if -32767 <= n <= 32767:
        return int(n)
    else:
        raise ValueError("Out of range in Int (%s)" % n)


def CByte(num):
    """Return the closest byte of a value"""
    n = round(float(num))
    if 0 <= n <= 255:
        return int(n)
    else:
        raise ValueError("Out of range in CByte (%s)" % n)


def CInt(num):
    """Return the closest int of a value"""
    n = round(float(num))
    if -32767 <= n <= 32767:
        return int(n)
    else:
        raise ValueError("Out of range in Int (%s)" % n)


def CLng(num):
    """Return the closest long of a value"""
    return int(round(float(num)))


def IsArray(obj):
    """Determine if an object is an array"""
    return isinstance(obj, (list, tuple))


def IsNumeric(text):
    """Return true if the string contains a valid number"""
    try:
        _ = float(text)
    except ValueError:
        return 0
    else:
        return 1


def Join(sourcearray, delimeter=" "):
    """Join a list of strings"""
    s_list = list(map(str, sourcearray))
    return delimeter.join(s_list)


def LCase(text):
    """Return the lower case version of a string"""
    return text.lower()


def UCase(text):
    """Return the lower case version of a string"""
    return text.upper()


def Left(text, number):
    """Return the left most characters in the text"""
    return text[:number]


def Like(text, pattern):
    """Return true if the text matches the pattern

    The pattern is a string containing wildcards
        * = any string of characters
        ? = any one character

    Fortunately, the fnmatch library module does this for us!

    """
    return fnmatch.fnmatch(text, pattern)


def Imp(x, y):
    """Return True if X implies Y

    Performs a bitwise comparison of identically positioned bits
    and sets corresponding bit in the output.

    This amounts to the following truth table:

        X       Y       Output
        F       F       T
        T       F       F
        F       T       T
        T       T       T

    https://docs.microsoft.com/en-us/office/vba/language/reference/user-interface-help/imp-operator

    """
    ix, iy = int(x), int(y)
    if not (ix or iy):
        result = 1
    else:
        result = 0
        while ix or iy:
            # Shift result by one bit
            result = result << 1
            #
            # Get the bits for comparison
            x_bit1 = ix & 1
            y_bit1 = iy & 1
            if not (x_bit1 and not y_bit1):
                result = result | 1
            #
            ix = ix >> 1
            iy = iy >> 1
    #
    if isinstance(x, bool) and isinstance(y, bool):
        return bool(result)
    else:
        return result


def LoadPicture(filename):
    """Load an image as a bitmap for display in a BitmapImage control"""
    return Bitmap(filename)


def Lof(channel):
    """Return the length of an open"""
    return FileLen(VBFiles.getFile(channel).name)


def Log(num):
    """Return the log of a value"""
    return math.log(float(num))


def Exp(num):
    """Return the log of a value"""
    return math.exp(float(num))


def LSet(var, value):
    """Do a VB LSet

    Left aligns a string within a string variable, or copies a variable of one 
    user-defined type to another variable of a different user-defined type.

    LSet stringvar = string

    LSet replaces any leftover characters in stringvar with spaces.

    If string is longer than stringvar, LSet places only the leftmost characters, 
    up to the length of the stringvar, in stringvar.

    Warning   Using LSet to copy a variable of one user-defined type into a 
    variable of a different user-defined type is not recommended. Copying data 
    of one data type into space reserved for a different data type can cause unpredictable results.

    When you copy a variable from one user-defined type to another, the binary data 
    from one variable is copied into the memory space of the other, without regard 
    for the data types specified for the elements.

    """
    return value[:len(var)] + " " * (len(var) - len(value))


def MakeDate(*args):
    """Return a date from the given string"""
    raise NotImplementedError("MakeDate has not been written yet. Passsed: %s" % (args, ))


def Mid(text, start, num=None):
    """Return some characters from the text"""
    if num is None:
        return text[start - 1:]
    else:
        return text[(start - 1):(start + num - 1)]


def Oct(num):
    """Return the oct of a value"""
    n = CInt(num)
    if n == 0:
        return "0"
    else:
        return oct(n)[2:]


def RGB(r, g, b):
    """Return a Long whole number representing an RGB color value

    The value for any argument to RGB that exceeds 255 is assumed to be 255.
    If any argument is less than zero then this results in a ValueError.

    """
    rm = min(255, Int(r))
    gm = min(255, Int(g))
    bm = min(255, Int(b))
    #
    if rm < 0 or gm < 0 or bm < 0:
        raise ValueError("RGB values must be >= 0, were (%s, %s, %s)" % (r, g, b))
    #
    return ((bm * 256) + gm) * 256 + rm


def Replace(expression, find, replace, start=1, count=-1):
    """Returns a string in which a specified substring has been replaced with another
    substring a specified number of times

    The return value of the Replace function is a string, with substitutions made, 
    that begins at the position specified by start and and concludes at the end of 
    the expression string. It is not a copy of the original string from start to finish.

    """
    if find:
        return expression[:start - 1] + expression[start - 1:].replace(find, replace, count)
    else:
        return expression


def Right(text, number):
    """Return the right most characters in the text"""
    return text[-number:]


_last_rnd_number = random.random()


def Rnd(value=1):
    """Return a random numer and optionally seed the current state"""
    global _last_rnd_number
    if value == 0:
        return _last_rnd_number
    elif value < 0:
        random.seed(value)
    r = random.random()
    _last_rnd_number = r
    return r


def Randomize(seed=None):
    """Seed the RNG

    In VB this doesn't return a consistent sequence so we basically ignore the seed.

    """
    random.seed()


def RSet(var, value):
    """Do a VB RSet

    Right aligns a string within a string variable.

    RSet stringvar = string

    If stringvar is longer than string, RSet replaces any leftover characters 
    in stringvar with spaces, back to its beginning.

    """
    return " " * (len(var) - len(value)) + value[:len(var)]


def Seek(channel):
    """Return the current 'cursor' position in the specified channel"""
    return VBFiles.getFile(Int(channel)).tell() + 1  # VB starts at 1


class _OptionsDB(config.VB2PYConfigObject):
    """A special config parser class to handle central VB options"""

    def __init__(self, appname):
        """Initialize the parser"""
        config.VB2PYConfigObject.__init__(self, filename=utils.relativePath("settings.ini"))
        self.appname = appname

    def __getitem__(self, key):
        """Get an item"""
        section, name = key
        section = self._getSettingName(section)
        return config.VB2PYConfigObject.__getitem__(self, (section, name))

    def __setitem__(self, key, value):
        """Set an item"""
        section, name = key
        section = self._getSettingName(section)
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, name, value)
        self.save()

    def save(self):
        """Store the options"""
        f = open(utils.relativePath("settings.ini"), "w")
        self._config.write(f)
        f.close()

    def _getSettingName(self, section):
        """Return the name for a section"""
        return "%s.%s" % (self.appname, section)

    def getAll(self, section):
        """Return all the items in a sections"""
        thissection = self._getSettingName(section)
        options = self._config.options(thissection)
        ret = vbObjectInitialize(size=(len(options) - 1, 1), objtype=str)
        for idx in range(len(options)):
            ret[idx, 0] = options[idx]
            ret[idx, 1] = self[section, options[idx]]
        return ret

    def delete(self, section, name):
        """Delete a setting from the settings file"""
        section = self._getSettingName(section)
        self._config.remove_option(section, name)
        self.save()


def GetSetting(appname, section, key, default=None):
    """Get a setting from the central setting file"""
    settings = _OptionsDB(appname)
    try:
        return settings[section, key]
    except config.configparser.Error:
        if default is not None:
            return default
        raise


def GetAllSettings(appname, section):
    """Get all settings from the central setting file"""
    settings = _OptionsDB(appname)
    return settings.getAll(section)


def SaveSetting(appname, section, key, value):
    """Set a setting in the central setting file"""
    settings = _OptionsDB(appname)
    settings[section, key] = str(value)


def DeleteSetting(appname, section, key):
    """Delete a setting in the central setting file"""
    settings = _OptionsDB(appname)
    settings.delete(section, key)


def Sgn(num):
    """Return the sign of a number"""
    n = float(num)
    if n < 0:
        return -1
    elif n == 0:
        return 0
    else:
        return 1


def String(num=None, text=None, value=None):
    """Return a repeated number of string items"""
    if value:
        return VBString(value)
    elif num is None and text is None:
        return VBString()
    else:
        return VBString(text[:1] * CInt(num))


def Space(num):
    """Return a repeated number of spaces"""
    return String(num, " ")


Spc = Space


def Split(text, delimiter=" ", limit=-1, compare=None):
    """Split a string using the delimiter

    If the optional limit is present then this defines the number
    of items returned. The compare is used for different string comparison
    types in VB, but this is not implemented at the moment

    """
    if compare is not None:
        raise VB2PYNotSupported("Compare options for Split are not currently supported")
    #
    if limit == 0:
        return VBArray(0)
    elif limit > 0:
        return Array(*str(text).split(delimiter, limit - 1))
    else:
        return Array(*str(text).split(delimiter))


def Sqr(num):
    """Return the square root of a value"""
    return math.sqrt(float(num))


def Sin(num):
    """Return the sin of a value"""
    return math.sin(float(num))


def Cos(num):
    """Return the cosine of a value"""
    return math.cos(float(num))


def Tan(num):
    """Return the tangent of a value"""
    return math.tan(float(num))


def Atn(num):
    """Return the arc-tangent of a value"""
    return math.atan(float(num))


def StrReverse(s):
    """Reverse a string"""
    lst = list(str(s))
    lst.reverse()
    return "".join(lst)


def Switch(*args):
    """Choose from a list of expression each with its own condition

    The arguments are presented as a sequence of condition, expression pairs
    and the first condition that returns a true causes its expression to be
    returned. If no conditions are true then the function returns None

    """
    arg_list = list(args)
    arg_list.reverse()
    #
    while arg_list:
        cond, expr = arg_list.pop(), arg_list.pop()
        if cond:
            return expr
    return None


def Timer():
    """Returns a Single representing the number of seconds elapsed since midnight"""
    ltime = time.localtime()
    h, m, s = ltime[3:6]
    return h * 3600.0 + m * 60.0 + s


def Trim(text):
    """Strip spaces from the text"""
    return str(text).strip()


def LTrim(text):
    """Strip spaces from the left of the text"""
    return str(text).lstrip()


def RTrim(text):
    """Strip spaces from the right of the text"""
    return str(text).rstrip()


def UBound(obj, dimension=1):
    """Return the upper bound for the index"""
    try:
        return obj.__ubound__(dimension)
    except AttributeError:
        #
        # Might have been called for a list so give this a try
        if dimension == 1:
            try:
                return len(obj)
            except TypeError:
                pass
        raise ValueError("UBound called for invalid object")


def LBound(obj, dimension=1):
    """Return the lower bound for the index"""
    try:
        return obj.__lbound__(dimension)
    except AttributeError:
        raise ValueError("LBound called for invalid object")


def Val(text):
    """Return the value of a string

    This function finds the longest leftmost number in the string and
    returns it. If there are no valid numbers then it returns 0.

    The method chosen here is very poor - we just keep trying to convert the 
    string to a float and just use the last successful as we increase
    the size of the string. A Regular expression approach is probably 
    quicker.

    """
    best = 0
    for idx in range(len(text)):
        try:
            best = float(text[:idx + 1])
        except ValueError:
            pass
    return best


def vbForRange(start, stop, step=1):
    """Mimic the range in a for statement

    VB's range is inclusive and can include non-integer elements so
    we use an generator. 

    """
    num_repeats = (stop - start) / step
    if num_repeats < 0:
        return
    current = start
    while num_repeats >= 0:
        yield current
        current += step
        num_repeats -= 1


def vbGetEventArgs(names, arguments):
    """Return arguments passed in an event

    VB Control events have parameters passed in the call, eg MouseMove(Button, Shift, X, Y).
    In vb2py.PythonCard the event parameters are all passed as a single event object. We
    can easily unpack the attributes back to the values in the Event Handler but
    we also have to account for the fact that someone might call the Handler
    directly and therefore assume that they can pass parameters individually.

    This function tries to unpack the params from an event object and, if
    successful, returns them as a tuple. If this fails then it tries to 
    assume that they were already in a tuple and return them that way.

    This can still fail if there are keyword arguments ... TODO!

    """
    # arguments is the *args tuple
    #
    # Is there only one parameter
    if len(arguments) == 1:
        # Try to unpack names from this argument
        try:
            ret = []
            for name in names:
                if name.endswith("()"):
                    ret.append(getattr(arguments[0], name[:-2])())
                else:
                    ret.append(getattr(arguments[0], name))
            return ret
        except AttributeError:
            pass
    # If we have as many arguments as we need then just return them
    if len(names) == len(arguments):
        return arguments
    # Couldn't unpack the event and didn't have the right number of args so we are dead
    raise VB2PYCodeError("EventHandler couldn't unpack arguments")


class VBMissingArgument:
    """A generic class to represent an argument omitted from a call"""

    _missing = 1


def VBGetMissingArgument(fn, argument_index):
    """Return the default value for a particular argument of a function"""
    try:
        args, varargs, varkw, defaults = inspect.getargspec(fn)
    except Exception as err:
        raise VB2PYCodeError("Unable to determine default argument for arg %d of %s: %s" % (
            argument_index, fn, err))
    #
    # Find correct argument default
    offset = argument_index - len(args)
    #
    # If this is an instancemethod then we must skip the 'self' argument
    if isinstance(fn, instancemethod):
        offset += 1
    try:
        return defaults[offset]
    except IndexError:
        raise VB2PYCodeError("Default argument for arg %d of %s doesn't seem to exist" % (
            argument_index, fn))


def vbObjectInitialize(size=None, objtype=None, preserve=None):
    """Return a new object with the given size and type"""
    if size is None:
        size = [0]

    #
    # Create the object
    def getObj():
        if len(size) == 1:
            return objtype()
        else:
            return vbObjectInitialize(size[1:], objtype)

    ret = VBArray(size[0], getObj)
    #
    # Preserve the old values if needed
    if preserve is not None:
        preserve.__copyto__(ret)
    return ret


def VB2PY_ERROR(text):
    """Used to flag a conversion error of some kind that should fail when executed"""
    raise Exception('VB2PY conversion error: %s' % text)


def AddressOf(obj):
    """Return the AddressOf a variable

    This does not work in Python and likely the code using it is going to need significant
    work so we just throw an error here.

    """
    raise NotImplementedError('AddressOf does not work in Python and code will likely need refactoring')


Abs = abs
Asc = AscB = AscW = ord
Chr = ChrB = ChrW = chr
Fix = Int
CStr = Str = str
CSng = CDbl = float
Len = len
Round = round


def StrComp(a, b):
    return (a > b) - (a < b)


#
# Command line parameters are retrieved as a whole
Command = " ".join(sys.argv[1:])

#
# File stuff
Kill = os.remove
RmDir = os.rmdir
MkDir = os.mkdir
ChDir = os.chdir
FileCopy = shutil.copyfile
# -- end -- << VBFunctions >>
