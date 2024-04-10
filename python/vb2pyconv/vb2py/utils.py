import os
import re
import mako.template
import mako.lookup


class TextColours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


BASE_GRAMMAR_SETTINGS = {
    'dialect': 'VB6',
    'mode': 'rigorous',
}


def rootPath():
    """Return the root path"""
    return os.path.split(os.path.abspath(__file__))[0]


def relativePath(*paths):
    """Return the path to a file"""
    return os.path.join(rootPath(), *paths)


def loadGrammarFrom(filename, data=None):
    """Return the text of a grammar file loaded from the disk"""
    with open(filename, 'r') as f:
        text = f.read()
    lookup = mako.lookup.TemplateLookup(directories=[relativePath('grammars')])
    template = mako.template.Template(text, lookup=lookup)
    #
    base_data = {}
    base_data.update(BASE_GRAMMAR_SETTINGS)
    #
    if data:
        for k, v in data.items():
            if v is not None:
                base_data[k] = v
    #
    return str(template.render(**base_data))


def countNewlines(text):
    """Return the number of newlines in some text"""
    return len(re.findall('\n', text))
