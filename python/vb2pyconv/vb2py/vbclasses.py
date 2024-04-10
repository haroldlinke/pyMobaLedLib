# -*- coding: utf -*-

"""
Classes which mimic the behaviour of VB classes

- Collection
"""

from . import vbfunctions
import threading
import time
import os
import sys
from operator import itemgetter


# noinspection PyPep8Naming
class Collection(dict):
    """A Collection Class

    An implementation of Visual Basic Collections.
    This implementation assumes that indexing by integers is rare and
    that memory is a less scarce resource than CPU time.

    Based on original code submitted by Jacob Hallén.

    """

    def __init__(self):
        dict.__init__(self)
        # self.insertOrder is used as the relative index when the collection
        # is treated as an array.
        # It is also used as the dictionary key for entries that have no
        # assigned key. This always works because VB keys can only be strings. 
        self.insertOrder = 1

    def __setitem__(self, Key, Item):
        if isinstance(Key, int):
            raise TypeError("Index must be a non-numeric string")
        if Key is None:
            Key = self.insertOrder
        dict.__setitem__(self, Key, (Item, self.insertOrder, Key))
        self.insertOrder += 1

    def __getitem__(self, Key):
        try:
            Key = int(Key)
            if Key < 1:
                raise IndexError
            lst = list(self.values())
            lst.sort(key=itemgetter(1))
            return lst[Key - 1][0]
        except ValueError:
            return dict.__getitem__(self, Key)[0]

    def __delitem__(self, Key):
        try:
            Key = int(Key)
            lst = list(self.values())
            lst.sort(key=itemgetter(1))
            _, _, key = lst[Key - 1]
        except ValueError:
            pass
        dict.__delitem__(self, Key)

    def __call__(self, Key):
        return self.Item(Key)

    def __iter__(self):
        lst = list(self.values())
        lst.sort(key=itemgetter(1))
        return iter([val[0] for val in lst])

    def _getElement(self, Key):
        if isinstance(Key, int):
            lst = list(self.values())
            lst.sort(key=itemgetter(1))
            return lst[Key - 1]
        else:
            return dict.__getitem__(self, Key)

    def Add(self, Item, Key=None, Before=None, After=None):
        """
        Add's an item with an optional key. The item can also be added
        before or after an existing item. The before/after parameters
        can either be integer indices or keys.
        **kw can contain
        - key
        - before
        - after
        before and after exclude each other
        """
        if Before is None and After is None:
            self[Key] = Item

        elif Before is not None and After is None:
            _, order, _ = self._getElement(Before)
            for k, entry in self.items():
                if entry[1] >= order:
                    dict.__setitem__(self, k, (entry[0], entry[1] + 1, k))
            if not isinstance(Key, str):
                Key = self.insertOrder
            dict.__setitem__(self, Key, (Item, order, Key))
            self.insertOrder += 1

        elif After is not None and Before is None:
            _, order, _ = self._getElement(After)
            for k, entry in self.items():
                if entry[1] > order:
                    dict.__setitem__(self, k, (entry[0], entry[1] + 1, k))
            if not isinstance(Key, str):
                Key = self.insertOrder
            dict.__setitem__(self, Key, (Item, order + 1, Key))
            self.insertOrder += 1

        else:
            raise vbfunctions.VB2PYCodeError("Can't specify both 'before' and 'after' parameters to Collection.Add")

    def Count(self):
        """Return the length of the collection"""
        return len(self)

    def Remove(self, Key):
        """Remove an item from the collection"""
        self.__delitem__(Key)

    def Item(self, Key):
        """Get an item from the collection"""
        return self.__getitem__(Key)
    # -- end -- << Collection Methods >>    


if __name__ == '__main__':
    # Tests
    c = Collection()
    c['a'] = 'va'
    c['b'] = 'vb'
    print(c['a'])
    print(c[2])
    del c[1]
    print(c[1])


class _DebugClass:
    """Intercept calls to Debug.Print"""

    _logger = None

    def Print(self, *args):
        """Print debugging output"""
        if self._logger:
            self._logger.debug("\t".join([str(arg) for arg in args]))


Debug = _DebugClass()


class _TimeClass(str):
    """Represent the current time"""

    def __repr__(self):
        return time.ctime()

    __str__ = __repr__


Time = _TimeClass()


class VBString(str):
    @property
    def Length(self):
        return len(self)


class Integer(int):
    """Python version of VB's integer"""


class Single(float):
    """Python version of VB's Single"""


class Double(float):
    """Python version of VB's Double"""


class Long(int):
    """Python version of VB's Long"""


class Boolean(int):
    """Python version of VB's Boolean"""


class Byte(int):
    """Python version of VB's Byte"""


class Object(object):
    """Python version of VB's Object"""


class Variant(float):
    """Python version of VB's Variant"""


class FixedString(str):
    """Python version of VB's fixed length string"""

    def __new__(cls, length):
        """Initialize the string"""
        return " " * length


def IsMissing(argument):
    """Check if an argument was omitted from a function call

    Missing arguments default to the VBMissingArgument class so
    we just check if the argument is an instance of this type and
    return true if this is the case.

    """
    try:
        return argument._missing
    except AttributeError:
        return 0


class VBArray(list):
    """Represents an array in VB

    This is basically a list but we use the __call__ syntax to
    access indexes of the array

    """

    def __init__(self, size, init_type=None):
        """Initialize with a size or a low and upper bound"""
        super().__init__()
        if not isinstance(size, tuple) == 1:
            size = (0, size)
        self._min, self._max = size
        if init_type:
            for i in range(size[0], size[1] + 1):
                self.append(init_type())
            self.init_type = init_type
        else:
            self.init_type = Variant

    def __call__(self, *args):
        """Index the array"""
        return self.__getitem__(args)

    def __setitem__(self, index, value):
        """Set an item in the array"""
        if isinstance(index, tuple):
            if len(index) == 1:
                myindex, rest = index[0], ()
            else:
                myindex, rest = index[0], index[1:]
        else:
            myindex, rest = index, ()
        if rest:
            list.__getitem__(self, myindex - self._min).__setitem__(rest, value)
        else:
            list.__setitem__(self, myindex - self._min, value)

    def __getitem__(self, args):
        """Get an item from the array"""
        if isinstance(args, tuple):
            if len(args) == 1:
                myindex, rest = args[0], ()
            else:
                myindex, rest = args[0], args[1:]
        else:
            myindex, rest = args, ()
        if self._min <= myindex <= self._max:
            if rest:
                return list.__getitem__(self, myindex - self._min).__getitem__(rest)
            else:
                return list.__getitem__(self, myindex - self._min)
        else:
            raise IndexError("Index '%d' is out of range (%d, %d)" % (myindex, self._min, self._max))

    def __ubound__(self, dimension=1):
        """Return the upper bound"""
        if dimension <= 0:
            raise ValueError("Invalid dimension for UBound: %s" % dimension)
        elif dimension == 1:
            return self._max
        else:
            return self[self._min].__ubound__(dimension - 1)

    def __lbound__(self, dimension=1):
        """Return the lower bound"""
        if dimension <= 0:
            raise ValueError("Invalid dimension for LBound: %s" % dimension)
        elif dimension == 1:
            return self._min
        else:
            return self[self._min].__lbound__(dimension - 1)

    def __contents__(self, pre=()):
        """Iterate over the contents of the array"""
        idx = 0
        ret = []
        for item in self:
            if isinstance(item, VBArray):
                ret.extend(item.__contents__(pre + (idx,)))
            else:
                ret.append((pre + (idx,), item))
            idx += 1
        return ret

    def __copyto__(self, other):
        """Copy our values to another array"""
        for index, value in self.__contents__():
            try:
                other.__setitem__(index, value)
            except IndexError:
                pass  # Throw away values which aren't in the new range

    def createFromData(cls, data):
        """Create an array from some data"""
        arr = cls(len(data))
        arr.extend(data)
        return arr

    createFromData = classmethod(createFromData)

    def erase(self):
        """Return this array to its initial form"""
        for element in self:
            try:
                element.erase()
            except AttributeError:
                self.clear()
                self.__init__((self._min, self._max), self.init_type)



class _VBFiles:
    """A class to control all interfaces to the file system

    This is required since VB accesses files through channel numbers rather than
    file objects. Since a channel number might be an expression that is evaluated at
    runtime we can't do a static conversion.

    The solution used here is to have a global object which everyone interfaces to when
    doing reading and writing to files. This object maintains the list of open channels 
    and marshalls all read and write operations.

    """

    def __init__(self):
        """Initialize the file interface"""
        self._channels = {}
        self._lock = threading.Lock()

    def openFile(self, channelid, filename, mode):
        """Open a file

        If the channel is already one then close it. There are likely to be some
        race conditions here in multithreaded applications so we use a lock to make
        this entire process atomic.

        Watch out for path separators in the filename

        """
        filename = filename.replace('\\', os.path.sep)
        self._lock.acquire()
        try:
            try:
                old_file = self._channels[channelid]
            except KeyError:
                pass
            else:
                old_file.close()
            #
            self._channels[channelid] = open(filename, mode)
        finally:
            self._lock.release()

    def closeFile(self, channelid=None):
        """Close a file

        TODO - what should the error be if there is no file open?

        """
        if channelid is None:
            for channel in list(self._channels.keys()):
                self.closeFile(channel)
        else:
            self._channels[channelid].close()
            del (self._channels[channelid])

    def getInput(self, channelid, number, separators=None, evaloutput=1):
        """Get data from a file

        VB nicely parses the input from files into variables so we have to mimic this
        here. 

        For safety sake we go one character at a time here. TODO: find out how VB does this
        and what the implications of chunking would be in a multithreaded app.

        We use the lock to prevent multiple reads.

        """
        if separators is None:
            separators = ("\n", ",", "\t", "")
        #
        self._lock.acquire()
        try:
            vars = []
            f = self._channels[channelid]
            buffer = ""
            while len(vars) < number:
                char = f.read(1)
                if char != '\r':
                    if char in separators:
                        if evaloutput:
                            # Try to eval it - if we get a syntax error then assume it is a string
                            try:
                                vars.append(eval(buffer))
                            except SyntaxError:
                                vars.append(buffer)
                        else:
                            vars.append(buffer)
                        buffer = ""
                    else:
                        buffer += char
        finally:
            self._lock.release()
        #	
        if number == 1:
            return vars[0]
        else:
            return vars

    def getLineInput(self, channelid, number=1):
        """Get data from a file one line at a time with no parsing"""
        return self.getInput(channelid, number, separators=("\n", ""), evaloutput=0)

    def writeText(self, channelid, *args):
        """Write data to the file

        We write with tabs separating the variables that are given in the *args parameter. The 
        lock is used to protect this section in multi-threaded environments.

        If the channelid is None then this is a bare Print statement which we
        send using Python's normal 'print'. TODO: Is this really what VB does?

        """
        output = "".join([str(arg) for arg in args])
        if channelid is None:
            print(output)
        else:
            self._lock.acquire()
            try:
                if args:
                    self._channels[channelid].write(output)
                else:
                    self._channels[channelid].write("\n")
            finally:
                self._lock.release()

    def seekFile(self, channelid, position):
        """Move to the specified point in the given channel"""
        self._channels[channelid].seek(position - 1)  # VB starts at 1

    def getFile(self, channelid):
        """Return the underlying file link to a channel"""
        return self._channels[channelid]

    def getChars(self, channelid, length):
        """Return the specified number of characters from a file"""
        return self._channels[channelid].read(length)

    def getOpenChannels(self):
        """Return a list of currently open channels"""
        return list(self._channels.keys())

    def EOF(self, channelid):
        """Determine if the named channel is at the end of the file"""
        f = self.getFile(channelid)
        return f.tell() == vbfunctions.FileLen(f.name)
    # -- end -- << VBFiles methods >>


VBFiles = _VBFiles()


class VBExitTry(Exception):
    """A fake exception used to break out of Catch clauses

    This enables the "Exit Try" statement to work properly in Python.

    """


class _App:
    """Represents the App object in VB"""

    def __init__(self):
        """Initialize the App objects"""
        # Application path is the path of the file we exectuted to run this
        self.Path = os.path.split(os.path.abspath(sys.argv[0]))[0]


App = _App()
# -- end -- << VB Classes >>
