Release History

Revision: $Revision: 1.1 $
Date:     $Date: 2001/08/06 21:15:05 $

2001-08-03
Converted to run as a PythonCard application. The shell can be used to move the turtle around the screen interactively.

2001-06-## - first public release. This is an alpha-release in order to get feedback from potential users. It is likely that the underlying turtle classes will be rewritten, but there should be minimal impact (other than a change to the module names used) on any scripts written to use the turtle modules. However, a major overhaul of the design is not out of the question, so don't build anything big on top of the module at this point without at least contacting me.


Overview
A turtle library alternative to turtle.py included in the Python Standard Library.

The current focus is on a turtle library for wxPython, but I'm trying to create the turtle modules in such a way that the various modules are subclassed from an abstract turtle class in order to isolate features that are specific to a given graphics library such as tk or wxPython. Hopefully, this will also simplify having a module that doesn't draw directly on the screen such as a PostScript module for printing or a module that controls a robot like those you can build with Lego Mindstorms. In all cases, a turtle script that doesn't make use of module specific features should run without changes using a different module. It should also be possible to do a Jython version, that uses Java classes for the actual drawing, but I'm not going to investigate that until later.

With that in mind, I created a tWrapper.py module with the sole purpose of hiding which underlying module is being used, so that turtle scripts can refer to the tWrapper class as their base class.

This is not Logo
My goal is not to create a simulated logo environment in Python. I wanted to make it very simple to translate existing Logo turtle graphic programs to my Python turtle scripts by supporting the same commands, but I didn't want to try and simulate the Logo data structures or program flow control such as for loops. If there are gotchas to look out for when converting from Logo, I'll try and identify that in the documentation and examples.

I would like the ability to do turtle graphics from the Python interpreter by creating a window and then typing simple commands such as "forward" and "right" in the interpreter to interactively control one or more turtles. The current version has turtle scripts that still look like Python, so assuming you have a turtle object t, you use:
    t.forward(100)
    t.right(90)

rather than the Logo style
    FORWARD 100
    RIGHT 90

Case is still significant, but there are abbreviated versions of methods, so t.forward(100) can be abbreviated to t.fd(100). You can have multiple turtle objects, but it would be possible to create a wrapper class that only allowed one global turtle and allowed you to type:
   fd(100)
   rt(90)
because somewhere in the class or script there was a
   fd = t.fd
   rt = t.rt
or something like that.

Scripts
   The scripts currently have a .txt extension. They must meet the same requirements as a normal Python file (.py), but since the scripts can't be run on their own I thought it best not to use the .py extension. wxTurtleApp.py is currently required in order to run the scripts since it handles setting up the drawing environment and execing the scripts. You can edit the scripts using PythonWin or any other editor; PythonWin treats the .txt files as Python code, if you're using Emacs or another editor you might be better off naming the scripts with a .py extension.

There are a number of scripts which show off chaotic behavior or do plotting and drawing that isn't strictly turtle graphics. However, the framework of providing a canvas to draw in and some simple tools for maintaining a pen, calculating distances, etc. show how the library can be used to visualize many different types of ideas quickly and easily.


Kevin Altis
altis@semi-retired.com
2001-06-08