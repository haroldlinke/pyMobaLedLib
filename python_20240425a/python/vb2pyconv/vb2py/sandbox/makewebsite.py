"""Make the website"""

import mako.template
import mako.lookup
import glob
import os
import re
from vb2py import utils
from vb2py.utils import TextColours as C
from vb2py.doc import examples

#
# Key paths
ROOT_PATH = utils.relativePath('..', 'website')
MAKO_PATH = os.path.join(ROOT_PATH, 'mako')

news = [
    ('one', 'some text'),
    ('two', 'some more text'),
    ('three', 'some additional text'),
    ('four', 'some final text'),
]


def getChanges():
    with open(utils.relativePath('doc', 'whatsnew.txt')) as f:
        text = f.read()
    items = []
    new_item = None
    for line in text.splitlines():
        if line.startswith('**'):
            if new_item:
                items.append(new_item)
            new_item = [line.strip()[2:-2], []]
        elif line.startswith('- '):
            new_item[1].append(line[2:])
    #
    return items


def getNews():
    with open(utils.relativePath('doc', 'news.txt')) as f:
        text = f.read()
    items = []
    new_item = None
    for line in text.splitlines():
        if line.startswith('**'):
            if new_item:
                items.append(new_item)
            new_item = [line.strip()[3:-3], '']
        elif line.strip():
            new_item[1] = new_item[1] + line.strip().lstrip() + ' '
    #
    return items


if __name__ == '__main__':
    print('Creating website ...')
    mako_files = glob.glob(os.path.join(MAKO_PATH, '*.mako'))
    lookup = mako.lookup.TemplateLookup(directories=[MAKO_PATH])
    for file in mako_files:
        base_name = os.path.splitext(os.path.split(file)[1])[0]
        print('Processing {} ... '.format(base_name), end='')
        template = lookup.get_template('{}.mako'.format(base_name))
        result = template.render(attributes={
            'news': getNews(),
            'changes': getChanges(),
            'examples': examples.code_samples,
        })
        with open(os.path.join(ROOT_PATH, '{}.html'.format(base_name)), 'w') as f:
            f.write(result)
        print('{}DONE{}'.format(C.OKBLUE, C.ENDC))
