"""A simple module intended to aid interactive testing of the parser

We just import a lot of useful things with short names so they are easy to type!

"""


import sys
sys.path.append('..')

from vb2py.vbparser import convertVBtoPython, parseVB as p, parseVBFile as f, getAST as t, ParseTree as PT
import vb2py.vbparser
import vb2py.logger
b = vb2py.vbparser.utils.TextColours
vb2py.vbparser.log.setLevel(0)

def dologging():
    import vb2py.parserclasses
    vb2py.parserclasses.log = vb2py.logger.getLogger('CommandLine')
    vb2py.parserclasses.log.handlers[0].allowed.append('CommandLine')
    vb2py.parserclasses.log.setLevel(-100)


def pp(ast, text, indent=0):
    """Print out a pretified version of the ast"""
    if not ast:
        print()
        return None
    cleaned_ast = []
    for entry in ast:
        if isinstance(entry, PT):
            text = entry.original_text
        if isinstance(entry, vb2py.vbparser.VBFailedElement):
            print((' ' * indent), entry)
        elif len(entry) == 4 and isinstance(entry[0], str):
            production, start, end, contents = entry
            print(' ' * indent + nice_text(text, production, start, end))
            cleaned_ast.append((indent, nice_text(text, production, start, end), pp(contents, text, indent + 1)))
        elif isinstance(entry, str):
            print(' ' * indent + entry)
            cleaned_ast.append((indent, entry))
        else:
            cleaned_ast.append(pp(entry, text, indent + 1))
    return cleaned_ast


def nn(text, *args, **kw):
    m = p(text, *args, **kw)
    pp_t(m)


def pp_t(container):
    for item in container.structure:
        pp_t_item(item, indent=0)


def pp_t_item(item, indent):
    conjoined = item.text.replace('\n', ' $ ')
    print('{:04d} {:04d} | {}{} [{}]'.format(
        item.line_offset, item.start_on_line,
        ' ' * indent,
        b.UNDERLINE + b.BOLD + item.name + b.ENDC,
        b.OKBLUE + conjoined + b.ENDC
    ))
    for sub_item in item.elements:
        pp_t_item(sub_item, indent + 1)


def n(text, *args, **kw):
    ast = t(text, *args, **kw)
    pp(ast, text)
    try:
        print(c(text, *args, **kw))
    except:
        print('Cannot convert text')


def nice_text(text, name, start, finish):
    subset = text[start:finish]
    conjoined = subset.replace('\n', ' $ ')
    return '%s [%s]' % (
        b.UNDERLINE + b.BOLD + name + b.ENDC,
        b.OKBLUE + conjoined + b.ENDC
    )


def safe():
    vb2py.vbparser.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'

def unsafe():
    vb2py.vbparser.utils.BASE_GRAMMAR_SETTINGS['mode'] = 'rigorous'


if __name__ == "__main__":
    def c(*args, **kw):
        print(convertVBtoPython(*args, **kw))
