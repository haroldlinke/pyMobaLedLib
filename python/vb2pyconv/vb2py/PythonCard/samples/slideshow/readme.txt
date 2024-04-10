slideshow is a PythonCard application that allows you to display a series of images and HTML in a selected directory or in a list of files.

You can provide a directory name on the command-line like this example on my own machine:

slideshow.py "c:\digital_images\2001-03-14"

to have it automatically start the slideshow in that directory. 
You can also provide a filename instead like this:

slideshow.py filelist.txt

The text file must contain a list of files for the slideshow like this:
c:\digital_images\2001-03-14\DSC00393.JPG
c:\digital_images\2001-03-14\DSC00388.JPG
c:\digital_images\2001-03-14\DSC00390.JPG

This allows you more flexibility than the directory approach to controlling both the files to be displayed and the order in which they will be shown.

Of course, since this is a PythonCard application, there is a graphical interface for accomplishing these tasks as well. You can just launch slideshow.py in the usual way and then select the directory you want to use for this slide show by choosing the appropriate option from the Slildeshow menu. (For this version, at least, you cannot select a file containing a text list of images to display from a menu in the PythonCard application.)

The remaining menu choices on the Slideshow menu are self-explanatory. Regardless of how you start the slide show - from the command line or from inside the application - You can use the navigation keys or menu options to move around inside the slide show. You can also change the interval between slides on the fly from the menu as well.

It is legal to use navigation techniques whether or not the slideshow is in progress.  If you use manual navigation at any time the show is in process, the interval timer will be restarted. If you then select "Continue," the slideshow will start from the current slide and advance automatically.

Navigations Keys:
First Slide:    Home, Up arrow
Previous Slide: Left arrow
Next Slide:     Right arrow
Last Slide:     End, Down arrow
