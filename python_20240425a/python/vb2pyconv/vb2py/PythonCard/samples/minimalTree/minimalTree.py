#!/usr/bin/python

"""
__version__ = "$Revision: 1.6 $"
__date__ = "$Date: 2004/05/05 16:53:27 $"
"""

from PythonCard import model

# events
# itemActivated, itemExpanding, itemExpanded, 
# selectionChanging, selectionChanged

class Minimal(model.Background):

    def on_initialize(self, event):
        tree = self.components.tree
        root = tree.addRoot("1")
        tree.setItemHasChildren(root, 1)
        tree.selectItem(root)

    def on_tree_itemExpanding(self, event):
        tree = self.components.tree
        item=event.item
        # This event can happen twice in the self.Expand call
        if tree.isExpanded(item):
            return
        obj = int(tree.getItemText(item))
        if tree.getChildrenCount(item, 0) == 0:
            lst = [obj * 2, (obj *2) + 1]
            for o in lst:
                new_item = tree.appendItem(item, str(o))
                tree.setItemHasChildren(new_item, 1)
        event.skip()


if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
