try:
    import vb2py.extensions as extensions
except ImportError:
    import extensions

class ReplaceCellsWithCellsDict(extensions.RenderHookPlugin, extensions.SystemPlugin):
    """Plugin to replace Cells with CellsDict in objects"""

    hooked_class_name = "VBObject"

    def addMarkup(self, indent, text):
        """Add markup to the rendered text"""
        return text.replace("Cells[", "CellDict[")
