import re


class ShortcutsSet:

    def __init__(self):

        self.shortcuts = {}

    def applyTo(self, text):

        for shortcut in self.shortcuts.keys():
            text = re.sub('(?<!\\\)"' + shortcut + '"', self.shortcuts[shortcut], text)
            
        text = text.replace('\\"', '"')
            
        return text

    def addShortcut(self, name, data):
        """Add's a single shortcut to the shortcuts list."""
        self.shortcuts[name] = data

    def delShortcut(self, name):
        """Delete's a shortcut from the list."""
        del self.shortcuts[name]

    def loadShortcutsFile(self, filename):
        """Load's in a set of shortcuts from a shortcuts file."""

        try:
            shortcutsFile = open(filename, "r")
        except IOError, e:
            # we don't want to print messages about non found shortcut files because many users
            # won't have them anyway
            return

        data = shortcutsFile.read().split("\n")
        shortcutsFile.close()
        
        for i in range(0,len(data),2):
            if i+1 < len(data):
                self.addShortcut(data[i], data[i+1])

    def saveShortcutsFile(self, filename):
        """Save's a set of shortcuts."""

        try:
            shortcutsFile = open(filename, "w")
        except IOError, e:
            # we don't want to print messages about non found shortcut files because many users
            # won't have them anyway
            return

        for k in self.shortcuts.keys():
            shortcutsFile.write(k + "\n")
            shortcutsFile.write(self.shortcuts[k] + "\n")

        shortcutsFile.close()

    def printShortcuts(self):
        """Prints out all of the shortcuts."""
        for key in self.shortcuts.keys():
            print key + " = " + self.shortcuts[key]
