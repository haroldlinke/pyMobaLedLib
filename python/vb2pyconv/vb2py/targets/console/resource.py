import vb2py
import os
import vb2py.projectconverter
import vb2py.vbparser

event_translator = {
        "Click" : "mouseClick",
}

possible_controls = {}


class Resource(vb2py.projectconverter.BaseResource):
    """Represents a resource object"""

    target_name = "Console"

    def __init__(self, *args, **kw):
        """Initialize the vb2py.PythonCard resource"""
        vb2py.projectconverter.BaseResource.__init__(self, *args, **kw)
        # self._rsc = eval(open("%s.txt" % self.basesourcefile, "r").read())
        # self._rsc["controls"] = []
        self._code = open("%s.py" % self.basesourcefile, "r").read()

    def writeToFile(self, basedir, write_code=0):
        """Write ourselves out to a directory"""
        fle = open(os.path.join(basedir, self.form.name) + ".py", "w")
        lines = []
        if write_code:
            added_code = vb2py.vbparser.renderCodeStructure(self.form.code_structure)
        else:
            added_code = ""

        text = self._code.replace("# CODE_GOES_HERE", added_code)
        text = text.replace("# CONTROLS GO HERE", self.form.form_data)

        fle.write(text)
        fle.close()


class VBUnknownControl:
    """Dummy to hold control properties"""

