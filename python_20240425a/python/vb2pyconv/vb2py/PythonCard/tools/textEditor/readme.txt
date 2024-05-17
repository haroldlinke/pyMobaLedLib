simple text editor

If you use this sample as a real text editor then you should be careful to always work on backup copies of documents in case there are bugs that might corrupt your text.

You can set the default font which along with the last position and size of the window will be saved in a user.config.txt file.

This sample shows off the FindDialog in dialog.py, which is a custom dialog built directly in wxPython as well as the FindDialog class based on GenericDialog, which works more like a normal background. The resource definition for the class is in find.rsrc.py. You can use the FindDialog class as a template for how to do your own modal dialog classes. You must use the OK (5100) and Cancel (5101) ids for your default and cancel buttons or the dialog won't be dismissed properly.

The find dialog remembers the last find settings and so acts more like a Find Next.

The find algorithm is not able to do a "match whole words only" find.

The About dialog displays the current filename, character, word, and line count.

This is the only sample that uses a .pyw extension, so it doesn't show a console window when the sample is run. If any error messages are output due to a runtime error, you won't see them. You can change the extension back to .py if you want to experiment with the code.

Scriptlets
See the following message in the archive for more info.
http://aspn.activestate.com/ASPN/Mail/Message/PythonCard/1181106