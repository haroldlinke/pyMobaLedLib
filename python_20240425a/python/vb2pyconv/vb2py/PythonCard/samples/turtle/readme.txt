turtle provides a fairly complete turtle library, numerous sample turtle
scripts (in the scripts directory). The shell can be used to move the
turtle(s) around interactively.

For example, the simple example below shows controlling the turtle from
the shell.

>>> t.st()
>>> t.color('blue')
>>> t.fd(100)
>>> for i in range(5):
... 	t.fd(50)
... 	t.rt(72)


See the turtle docs directory for more information.

2002-07-17 Update:
All of the samples will draw dramatically faster if Auto Refresh is unchecked in the Commands menu. If you have a fast machine and especially if you have a fast video card such as a nVidia GeForce2 or better, then a lot of the turtle samples will draw reasonably fast, except where points are plotted; the full window blit after each drawing operation will make even those sample scripts slow. If you have on-board video or a slow machine you will definitely want to uncheck Auto Refresh! This applies to Mac OS X as well which seems quite slow if Auto Refresh is checked.
