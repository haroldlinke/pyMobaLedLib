#
# Turn off logging in extensions (too loud!)
import vb2py.extensions
import unittest
vb2py.extensions.disableLogging()
import vb2py.vbparser
vb2py.vbparser.log.setLevel(0) # Don't print all logging stuff


from vb2py.plugins.attributenames import TranslateAttributes



if __name__ == "__main__":
    unittest.main()
