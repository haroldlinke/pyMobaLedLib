"""Main parsing and conversion routines for translating VB to Python code"""

#
# Configuration options
from . import config
Config = config.VB2PYConfig()

from pprint import pprint as pp
from simpleparse.common import chartypes
from simpleparse.parser import Parser
import sys
import os
import re
from . import utils

GRAMMAR_FILE = utils.relativePath("grammars", "vbgrammar.mako")


from . import logger
log = logger.getLogger("VBParser")


class VBParserError(Exception):
    """An error occurred during parsing"""


class UnhandledStructureError(VBParserError): 
    """A structure was parsed but could not be handled by class"""


class InvalidOption(VBParserError):
    """An invalid config option was detected"""


class NestingError(VBParserError):
    """An error occurred while handling a nested structure"""


class UnresolvableName(VBParserError):
    """We were asked to resolve a name but couldn't because we don't know it"""


class SystemPluginFailure(VBParserError): 
    """A system level plugin failed"""


class DirectiveError(VBParserError): 
    """An unknown directive was found"""


def convertToElements(details, txt, text_offset, line_offset):
    """Convert a parse tree to elements"""
    ret = []
    if details:
        for item in details:
            ret.append(VBElement(item, txt, text_offset, line_offset))
    return ret


def buildParseTree(vbtext, starttoken="line", verbose=0, returnpartial=0, returnast=0, dialect=None, grammar=None):
    """Parse some VB
    :param dialect:
    """
    #
    # Select the right grammar file
    if not grammar:
        grammar = utils.loadGrammarFrom(GRAMMAR_FILE, data={'dialect': dialect})
    parser = Parser(grammar, starttoken)

    txt = applyPlugins("preProcessVBText", vbtext)  + '\n\n'

    txt = original_txt = makeSafeFromUnicode(txt)

    nodes = []
    text_offset = 0
    line_offset = 0
    while 1:
        success, tree, next = parser.parse(txt)
        if not success:
            if txt.strip():
                # << Handle failure >>
                msg = "Parsing error: %d, '%s'" % (next, txt.split("\n")[0])
                if returnpartial:
                    log.error(msg)
                    nodes.append(VBFailedElement('parser_failure', msg))
                    break
                else:
                    raise VBParserError(msg)
                # -- end -- << Handle failure >>
            break
        if verbose:
            print(success, next)
            pp(tree)
            print(".")
        if not returnast:
            nodes.extend(convertToElements(tree, txt, text_offset, line_offset))
        else:
            new_entry = ParseTree(tree)
            new_entry.original_text = txt[:next]
            nodes.append(new_entry)
        #
        line_offset += utils.countNewlines(txt[:next])
        text_offset += next
        txt = txt[next:]

    return nodes


def makeSafeFromUnicode(text):
    """Return a safe version of the text without unicode characters

    We do some ugly hacks here to handle unicode since the SimpleParse library
    doesn't have an easy way to deal with it.

    """
    result = []
    letters = list(map(ord, text))
    marker1 = [ord('x'), ord('X')]
    marker2 = [ord('X'), ord('x')]    
    #
    # Replace all non asc characters with a marker
    for letter in letters:
        if letter < 128:
            result.append(letter)
        else:
            result.extend(marker1)
            result.extend(list(map(ord, str(letter))))
            result.extend(marker2)
    #
    return "".join(map(chr, result))


def makeUnicodeFromSafe(text):
    """Recover the unicode text from a safe version of the text

    We do some ugly hacks here to handle unicode since the SimpleParse library
    doesn't have an easy way to deal with it.

    """
    def replacer(match):
        """Replace the safe unicode thingumy"""
        text = match.groups()[1]
        code = int(text)
        try:
            return chr(code)
        except ValueError:
            raise

    proper_text = re.sub('(xX)(\d+)(Xx)', replacer, text)

    return proper_text


class ParseTree(list):
    """Markup in a parse tree to store original text"""

    original_text = ''


def parseVB(vbtext, container=None, starttoken="line", verbose=0, returnpartial=None, grammar=None, dialect=None):
    """Parse some VB"""

    if returnpartial is None:
        returnpartial = Config["General", "ReportPartialConversion"] == "Yes"

    nodes = buildParseTree(vbtext, starttoken, verbose, returnpartial, grammar=grammar, dialect=dialect)

    if container is None:
        m = VBModule()
    else:
        m = container

    for idx, node in zip(range(sys.maxsize), nodes):
        if verbose:
            print(idx, end=' ')
        try:
            m.processElement(node)
        except UnhandledStructureError:
            log.warn("Unhandled: %s\n%s" % (node.structure_name, node.text))

    m.structure = nodes
    return m


def getAST(vbtext, starttoken="line", returnpartial=None, grammar=None, dialect='VB6'):
    """Parse some VB to produce an AST"""

    if returnpartial is None:
        returnpartial = Config["General", "ReportPartialConversion"] == "Yes"

    nodes = buildParseTree(vbtext, starttoken, 0, returnpartial, returnast=1, grammar=grammar, dialect=dialect)

    return nodes


def renderCodeStructure(structure):
    """Render a code structure as Python

    We have this as a separate function so that we can apply the plugins

    """
    return applyPlugins("postProcessPythonText", structure.renderAsCode())


def convertVBtoPythonAndGetModule(vbtext, *args, **kw):
    """Convert some VB text to Python"""
    VBElement.setCurrentAction('Parsing')
    m = parseVB(vbtext, *args, **kw)
    VBElement.setCurrentAction('Generating Python')
    python_code = m.renderAsCode()
    if Config['General', 'ReturnLineNumbers'].lower() == 'yes':
        result = decodeLineNumbers(python_code)
        python_code, line_lookup = result
        m.line_lookup = line_lookup
    python = applyPlugins("postProcessPythonText", python_code)
    VBElement.setCurrentAction('Finishing')
    return python, m


def convertVBtoPython(vbtext, *args, **kw):
    """Convert some VB text to Python"""
    return convertVBtoPythonAndGetModule(vbtext, *args, **kw)[0]


def decodeLineNumbers(python_code):
    """Return the cleaned python code and a line_number lookup"""
    get_line = re.compile(r'!\$VB2PY-(\d+)\$!.*')
    clean_lines = []
    lookup = {}
    for pyline, line in enumerate(python_code.splitlines()):
        match = get_line.match(line)
        if match:
            lookup[pyline] = int(match.group(1))
            line = re.subn('!\$VB2PY-(\d+)\$!', '', line)[0]
        clean_lines.append(line)
    #
    clean_code = '\n'.join(clean_lines)
    return clean_code, lookup


def applyPlugins(methodname, txt):
    """Apply the method of all active plugins to this text"""
    use_user_plugins = Config["General", "LoadUserPlugins"] == "Yes"
    for plugin in plugins:
        if plugin.isEnabled() and plugin.system_plugin or use_user_plugins:
            try:
                txt = getattr(plugin, methodname)(txt)	
            except Exception as err:
                if plugin.system_plugin:
                    raise SystemPluginFailure(
                        "System plugin '%s' had an exception (%s) while doing %s. Unable to continue" % (
                            plugin.name, err, methodname))
                else:                        
                    log.warn("Plugin '%s' had an exception (%s) while doing %s and will be disabled" % (
                            plugin.name, err, methodname))
                    plugin.disable()
    return txt


def parseVBFile(filename, text=None, parent=None, **kw):
    """Parse some VB from a file"""
    if not text:
        # << Get text >>
        f = open(filename, "r")
        try:
            text = f.read()
        finally:
            f.close()
        # -- end -- << Get text >>
    # << Choose appropriate container >>
    # Type of container to use for each extension type
    container_lookup = {
            ".bas" : VBCodeModule,
            ".cls" : VBClassModule,
            ".frm" : VBFormModule,
    }

    extension = os.path.splitext(filename)[1]
    try:
        container = container_lookup[extension.lower()]
    except KeyError:
        log.warn("File extension '%s' not recognized, using default container", extension)
        container = VBCodeModule
    # -- end -- << Choose appropriate container >>
    new_container=container()
    if parent:
        new_container.parent = parent
    code_structure = parseVB(text, container=new_container, **kw)
    return code_structure


# The following imports must go at the end to avoid import errors 
# caused by poor structuring of the package. This needs to be refactored!

# Plug-ins
from . import extensions
plugins = extensions.loadAllPlugins()

from .parserclasses import *

if __name__ == "__main__":	
    from .testparse import txt
    m = parseVB(txt)
