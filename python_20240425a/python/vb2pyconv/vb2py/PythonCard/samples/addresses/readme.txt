addresses is the first test of converting the layout and data of an existing
HyperCard stack to the PythonCard format. All the code used to do the
conversion, limitations of the conversion, and the steps of the conversion
are documented. addresses can import Outlook contacts. Comma separated
values (CSV) import will be added in the future. addresses also implements
transparent loading and saving of the contact data to a separate text file.
The textIndexer sample and addresses thus provide the start of a generic
transparent data storage model for PythonCard that will eventually be
available to all PythonCard apps that want to use it.

This sample is an experiment in converting a HyperCard stack to a PythonCard program. I used the Addresses stack that comes with HyperCard as the test case.

The layout and rough functionality of the port is supposed to mirror the original, so if you don't like the interface, choice of fields, etc. then blame the original stack, I'm just the porter ;-)

The original stack actually has much more functionality than the port, but this is a simple test and it is too early in the development of PythonCard to try and duplicate everything.

I added the 'Import Outlook' menu item as yet another test. First of all, I'm not exactly sure what happens when the necessary modules can't be found, say on a *nix machine or a Windows box without the Python win32 extensions or Outlook isn't installed.

This is not meant to be an application that someone would use every day, it is only a test.

2001-11-24
I renamed the old addresses and its resource file to addresses052.py and addresses052.rsrc.py since they are from prototype release 0.5.2. If you're interested in the conversion from HyperCard, you should look at those files.