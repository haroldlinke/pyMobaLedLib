Last updated: 2002-04-13

This represents the beginnings of a GUI resource (layout) editor for PythonCard.

You can view the attributes for all components and menus by selecting the Resource... menu item in the View menu prior to doing a Save or Save As... under the File menu to output a new file.

Known Bugs and Issues:
There are no constraints applied when the shift key is held down, but there is there a grid for the widgets to "snap to".

You can only select one widget at a time.

Sizers and anchors are not supported. It is likely anchors will be supported before sizers.

Some of the components don't move or resize correctly all the time, you should report problems to the mailing list. The Choice component seems prone to this movement problem. If a component is difficult to select or move, you can always select it via the Property Editor and then change its position attribute via the Property Editor rather than trying to drag the control itself; the sizing handles should also work.

There is a bug that causes the top three sizing handles to appear incorrectly, usually when the widget y position is at -1. I am trying to determine if this is actually a problem with wxPython or some rare interaction in the resourceEditor code. [I think this is fixed as of release 0.6.2 -ka]

When editing a dialog or other window that doesn't have a menubar, you'll probably need to increase the vertical size of the window by 20 or 30 pixels to compensate for the resourceEditor menubar. Once your layout looks the way you want it you can subtract the pixel padding you added earlier. On Microsoft Windows, the menubar may wrap if the width of the window is not wide enough, in which case you'll need to add even more padding.

The next revision of the resourceEditor will use a separate window for doing layout so that the size of a window is always accurate and shows the menubar of the app you're editing.
