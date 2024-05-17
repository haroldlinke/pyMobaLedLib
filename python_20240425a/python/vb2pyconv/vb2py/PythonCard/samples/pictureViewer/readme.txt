pictureViewer is a sample for displaying images in a variety
of formats (surprise). It can can load and save images of type:

BMP, GIF, JPG/JPEG, PCX, PNG, PNM, TIF/TIFF, XBM, and XPM

Due to licensing restrictions, the wxWindows/wxPython library
is unable to save images of type GIF, so that limitation also
applies to PythonCard. I recommend that use same images in the
PNG format instead.

You can resize the image using the Image menu options. Dragging the
window frame doesn't work quite right yet.

You can Copy and Paste to the current window, so there is some
overlap with the saveClipboardBitmap and doodle samples.

A filename can be passed in as the first argument on the command-line
and pictureViewer will open that image when it starts up. This means
you can use pictureViewer from other applications or as the default
viewer for Windows.

Printing is not supported yet.
