The companies sample is a work in progress to explore the use of Python pickles for storage of data and to stress the find and sort capabilities of the underlying flatfileDatabase classes.

Before you can use it you must run the parse_companies.py file which will download the companies.xml file, parse it and save it as a list/dictionary in text and pickle format for use by the sample.

Note that the companies.xml data file is approximately 1.5MB and so can take a long time to download on a slow modem. Messages are printed to the console to indicate the progress of the download and parsing. Here is an example output from my machine:

C:\python\PythonCard\samples\companies>parse_companies.py
Downloading XML...
Saving XML...
Loading XML...
Parsing XML...
Number of entries: 6635
Parsing time: 24 seconds
Saving list...
Saving pickle...
Total Processing time: 24 seconds

The parsing time will take longer on slower machines. The parsing is not bullet-proof yet, so some fields and records contain garbage HTML data.

Since both the flatfileDatabase and companies sample use the flatfileDatabase.py module, it has been moved into the framework. The name and its location in the framework will likely change in the next release.

The findDialog is common as well and so a common dialogs/background sub-package will probably be added to the framework in release 0.7.

---
__version__ = "$Revision: 1.3 $"
__date__ = "$Date: 2004/04/08 21:07:35 $"
