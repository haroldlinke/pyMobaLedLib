Last updated: 2006-01-09

This represents the beginnings of a GUI resource (layout) editor for PythonCard.

The layoutEditor is an experimental version that is intended to replace the existing resourceEditor and allows various operations to be performed on multiple selected components (eg. move, align, distribute, etc.)

You can view the attributes for all components and menus by selecting the Resource... menu item in the View menu prior to doing a Save or Save As... under the File menu to output a new file.

Known Bugs and Issues:
There are no constraints applied when the shift key is held down, but there is a grid for the widgets to "snap to".

Sizers and anchors are not supported. It is likely anchors will be supported before sizers.

Some of the components don't move or resize correctly all the time, you should report problems to the mailing list. The Choice component seems prone to this movement problem. If a component is difficult to select or move, you can always select it via the Property Editor and then change its position attribute via the Property Editor rather than trying to drag the control itself; the sizing handles should also work.

When editing a dialog or other window that doesn't have a menubar, you'll probably need to increase the vertical size of the window by 20 or 30 pixels to compensate for the resourceEditor menubar. Once your layout looks the way you want it you can subtract the pixel padding you added earlier. On Microsoft Windows, the menubar may wrap if the width of the window is not wide enough, in which case you'll need to add even more padding.

Some future revision of the resourceEditor will use a separate window for doing layout so that the size of a window is always accurate and shows the menubar of the app you're editing.
