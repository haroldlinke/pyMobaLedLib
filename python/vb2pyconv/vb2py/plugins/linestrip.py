try:
    import vb2py.extensions as extensions
except ImportError:
    import extensions

import re
commented_continuation = re.compile(r"(([^']*'[^']*')*[^']*'[^']*)(_)$")


class LineStrip(extensions.SystemPlugin):
    """Plugin to strip tailing text from lines"""

    order = 10 # We would like to happen quite early
    __is_plugin__ = 1

    def preProcessVBText(self, txt):
        """Convert continuation markers by joining adjacent lines"""

        stripped_lines = '\n'.join([lne.strip() for lne in txt.splitlines()])
        return stripped_lines
