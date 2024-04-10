noresource is a short example of a PythonCard application that has no resource file. Normally apps should use a resource file to simplify editing layout and localization, but there might be times when you don't want an external resource file, so this shows how it can be done.

There is still a resource dictionary, but it is defined as part of the source file. The one used in this sample was copied from the minimal sample, so the names haven't been changed. I did delete the menubar to shorten the example code and removed the menu handler from the background class.

To make it a little more interesting, I also delayed creating 'field1' until the openBackground handler in order to show an example of creating components at runtime. Note that the name of the component must match in the assignment (self.components['field1']) and the dictionary ('name':'field1').
