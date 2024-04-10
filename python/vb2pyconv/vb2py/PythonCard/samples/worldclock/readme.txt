worldclock downloads an image off the www.time.gov server. Worldclock doesn't use a menubar.

2001-08-23
Andy Todd converted the JavaScript code to a Python script
xearth.py, so JavaScript is no longer required to run this
sample. We left the old JavaScript calls and xearth.js with
the sample in case people want to compare the old and new.

The original readme below has not been updated to reflect
the code change.

ka
---

This is a very simple example that currently only uses two
StaticText widgets and an ImageButton widget. It runs an
external JavaScript program via a popen (pipe) call to
calculate the appropriate image which it then downloads 
from the www.time.gov server and displays
via the ImageButton. The clock is updated every minute
and the image is updated every five minutes by default.

I'm using an __init__ method and some wxPython code
(wxTimer and EVT_IDLE) directly because that functionality
isn't in PythonCard yet. As the PythonCard prototype
expands in functionality, the wxPython calls will be
replaced.

This code has been tested on Windows 98 and Windows 2000. I've been
told that if you are running Win98 and Norton Anti-virus, that the
popen call in Python won't work, so beware. Running the script on
*nix requires a number of changes described below.

in xearth.js you must change the line:
  var QueryTimeZone = -7;
to match the offset of your own time zone. The USA West coast is -7
the East coast is -4, Sydney, Australia is 10, other time zones
are left as an exercise for the reader ;-)

Eventually xearth.js will go away and be replaced by the
equivalent code in Python, but part of the fun of this
convoluted example is that it calls another program to
do its work.

If you want to run this on *nix you'll have to change the line
  jScript = "cscript //nologo xearth.js"
in worldclock.py to the equivalent for running a standalone
JavaScript (ECMAScript) program in your version of *nix. You'll
also need to change the line in xearth.js
  WScript.echo(updatexearthImage());
to the equivalent print statement for the JavaScript interpreter
on your *nix box.

Change worldclock_standalone.pyw to worldclock_standalone.py if
you want to see the output, say for debugging purposes.

ka
---
ps. The original HTML file timezone.html is included so you can see
the scary HTML someone had to write to get a page that looks like
http://www.time.gov/timezone.cgi?Pacific/d/-8/java
Luckily, I was able to steal the good parts for my own desktop app.
