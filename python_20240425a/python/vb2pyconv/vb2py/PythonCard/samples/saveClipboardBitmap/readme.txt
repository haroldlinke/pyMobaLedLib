This is a very simple, single purpose, sample. I wrote it to avoid having to paste screenshots into MS Paint, save them as BMP files and then convert to PNG format using a command-line tool.

If the clipboard contains a bitmap you can save that bitmap to disk in a variety of formats, by pressing Ctrl+S or selecting Save As... from the file menu. You can provide the extension (.jpg, .png, .bmp) to save the file in and the script will choose the format based on the extension. You can leave saveClipboardBitmap app open and then capture a different bitmap in the clipboard, switch back to saveClipboardBitmap and do another save. As a convenience, if the clipboard contains a valid bitmap when the app is started you will be prompted to do a Save As immediately without having to type Ctrl+S or select Save As...

Due to licensing issues, wxWindows does not contain code to save GIF images. PNG is generally preferred for screenshots, but if there is demand I could add Python Imaging Library (PIL) support, which I think can save in GIF format.

I'll probably add a clipboard preview to the script once I get a chance to play with it some more.

saveClipboardBitmap is another sample that has no resource file. See the noresource sample for more of an explanation.
