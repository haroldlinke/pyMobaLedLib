"""A simple server to convert files from VB to Python"""

from . import vbparser
from . import parserclasses
from . import projectconverter as converter
from . import config
from docutils.core import publish_string
import base64
import fnmatch
import io
import zipfile
import random
import logging
import json
import re
import os
import datetime
import tempfile
from . import utils
from flask import Flask, request
from flask_cors import CORS
import time
from logging.config import dictConfig


class ConversionError(Exception):
    """There was an error converting a line of text"""


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask('VB2PY')
CORS(app)
Config = config.VB2PYConfig()

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
app.logger.info('Starting conversion server (%s)' % converter.__version__)


class ConversionHandler(object):
    """A server to convert files"""

    @staticmethod
    def convertSingleFile(text, container=None, style='vb', returnpartial=True, dialect='VB6', options=None):
        """Convert a single file of text"""
        if container is None:
            container = parserclasses.VBModule()
        ConversionHandler.setPythonic(style)
        if options:
            ConversionHandler.setOptions(options)
        ConversionHandler.clearHistory()
        try:
            return vbparser.convertVBtoPythonAndGetModule(text, container, returnpartial=returnpartial, dialect=dialect)
        except vbparser.VBParserError as err:
            raise ConversionError('Error converting VB. %s' % err)

    @staticmethod
    def setOptions(options):
        """Set some user defined options"""
        for section, name, value in options:
            Config.setLocalOveride(section, name, value)

    @staticmethod
    def setPythonic(style):
        """Set a pythonic configuration"""
        if style == 'vb':
            Config.setLocalOveride("General", "RespectPrivateStatus", "Yes")
            Config.setLocalOveride("Functions", "PreInitializeReturnVariable", "Yes")
            Config.setLocalOveride("Functions", "ReturnVariableName", "_ret")
            Config.setLocalOveride("Select", "SelectVariablePrefix", "_select")
            Config.setLocalOveride("With", "WithVariablePrefix", "_with")
        else:
            Config.setLocalOveride("General", "RespectPrivateStatus", "No")
            Config.setLocalOveride("Functions", "PreInitializeReturnVariable", "No")
            Config.setLocalOveride("Functions", "ReturnVariableName", "fn_return_value")
            Config.setLocalOveride("Select", "SelectVariablePrefix", "select_variable_")
            Config.setLocalOveride("With", "WithVariablePrefix", "with_variable")

    @staticmethod
    def clearHistory():
        """Reset any history in the parser

        The parser stores counters for things like select and with unique values
        and so this clears them out to ensure that each call gets a unique context.

        """
        parserclasses.VBSelect._select_variable_index = 0
        parserclasses.VBFor._for_variable_index = 0
        parserclasses.VBWith._with_variable_index = 0


@app.route('/test', methods=['GET', 'POST'])
def testResult():
    return json.dumps({'status': 'OK'})


@app.route('/single_code_module', methods=['POST'])
def singleCodeModule():
    """Return a code module converted"""
    return singleModule(parserclasses.VBModule(), parserclasses.VBDotNetModule())


@app.route('/single_class_module', methods=['POST'])
def singleClassModule():
    """Return a class module converted"""
    return singleModule(parserclasses.VBClassModule(), parserclasses.VBDotNetModule())


@app.route('/single_form_module', methods=['POST'])
def singleFormModule():
    """Return a form module converted"""
    return singleModule(parserclasses.VBFormModule(), parserclasses.VBDotNetModule())


@app.route('/submit_file', methods=['POST'])
def submitFile():
    """Submit a file as a test"""
    return storeSubmittedFile()


@app.route('/server_log', methods=['GET'])
def serverLog():
    """Write a log to the server"""
    app.logger.info('%s[%s] Client logging: %s%s%s' % (
        utils.TextColours.OKBLUE,
        request.remote_addr,
        utils.TextColours.FAIL,
        request.values['text'],
        utils.TextColours.ENDC,
    ))
    return json.dumps({
        'status': 'OK',
    })


@app.route('/request_status', methods=['GET'])
def getCurrentStatus():
    """Return the status of our currently processing"""
    return json.dumps({
        'status': 'OK',
        'stage': vbparser.VBElement.current_action,
        'line_number': vbparser.VBElement.max_line,
    })


@app.route('/server_stats', methods=['POST', 'GET'])
def getServerStats():
    """Return stats from the server"""
    app.logger.info('%s[%s] Server stats check%s' % (
        utils.TextColours.OKBLUE,
        request.remote_addr,
        utils.TextColours.ENDC
    ))
    #
    # Get last modification
    info = os.stat(utils.relativePath('doc', 'whatsnew.txt'))
    date = datetime.datetime.fromtimestamp(info.st_atime)
    #
    # Get what's new text
    with open(utils.relativePath('doc', 'whatsnew.txt'), 'r') as f:
        whats_new_text = f.read()
    #
    return json.dumps({
        'status': 'OK',
        'version': converter.__version__,
        'date': date.strftime('%Y-%m-%d'),
        'whats-new': publish_string(whats_new_text, writer_name='html').decode(),
    })


@app.route('/get_runtime_zip', methods=['POST'])
def getRunTimeZip():
    """Return a zip of the code and the runtime files"""
    app.logger.info('%sCreating Zip file for download%s'% (
        utils.TextColours.OKBLUE,
        utils.TextColours.ENDC,
    ))
    try:
        python = request.values['code']
    except KeyError:
        status = 'FAILED'
        result = 'No code present'
        zipdata = ''
    else:
        f = io.BytesIO()
        z = zipfile.ZipFile(f, mode='w')
        z.writestr('converted_code.py', python)
        z.writestr(os.path.join('vb2py', 'vbfunctions.py'), open(utils.relativePath('vbfunctions.py'), 'r').read())
        z.writestr(os.path.join('vb2py', 'vbdebug.py'), open(utils.relativePath('vbdebug.py'), 'r').read())
        z.writestr(os.path.join('vb2py', '__init__.py'), '# vb2py run time package\n')
        z.close()
        #
        f.seek(0)
        zipdata = base64.b64encode(f.read())
        status = 'OK'
        result = 'Zipfile created'
    #
    return json.dumps({
        'status': status,
        'result': result,
        'zipdata': zipdata.decode(),
    })


def singleModule(module_type, dot_net_module_type):
    """Convert a single module"""
    correlation_id = random.randint(0, 10000)
    vbparser.VBElement.resetLineCounter()
    correlation_string = '%s%06d%s' % (
        utils.TextColours.OKBLUE,
        correlation_id,
        utils.TextColours.ENDC,
    )
    app.logger.info('%s | Starting request' % correlation_string)
    start_time = time.time()
    #
    # Failure information
    parsing_failed = False
    parsing_stopped_vb = None
    parsing_stopped_py = None
    #
    conversion_style = 'unknown'
    return_structure = 'no'
    return_line_numbers = 0
    extra = ''
    failure_mode = ''
    lines = []
    structure = []
    line_lookup = {}
    line_count = -1
    language = 'UNKNOWN'
    version = converter.__version__
    logging_colour = utils.TextColours.OKGREEN
    #
    try:
        conversion_style = request.values['style']
        text = request.values['text']
        class_name = request.values.get('class_name', 'MyClass')
        failure_mode = request.values.get('failure-mode', 'line-by-line')
        requested_dialect = request.values.get('dialect', 'detect')
        return_structure = request.values.get('return-structure', 'no')
        options = json.loads(request.values.get('options', '[]').strip())
        return_line_numbers = int(request.values.get('return-line-numbers', '0'))
    except KeyError:
        result = 'No text or style parameter passed'
        status = 'FAILED'
    else:
        #
        language = requested_dialect if requested_dialect != 'detect' else detectLanguage(text)
        lines = text.splitlines()
        line_count = len(lines)
        if language != 'VB.NET':
            module_type.classname = class_name
            dialect = 'VB6'
        else:
            module_type = dot_net_module_type
            dialect = 'vb.net'
        module_type.classname = class_name
        #
        # Set line numbers option
        if return_line_numbers:
            Config.setLocalOveride('General', 'ReturnLineNumbers', 'Yes')
        #
        # Remove form stuff if it is there
        stripped_text = removeFormCruft(text)
        #
        try:
            try:
                if failure_mode == 'fail-safe':
                    utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'
                result, module = ConversionHandler.convertSingleFile(stripped_text, module_type, conversion_style,
                                                                     dialect=dialect, options=options)
            finally:
                utils.BASE_GRAMMAR_SETTINGS['mode'] = 'line-by-line'
            status = 'OK'
        except Exception as err:
            result = str(err)
            status = 'ERROR'
        else:
            #
            # Check for errors and store them
            if failure_mode == 'fail-safe':
                match = re.match(r'.*?UNTRANSLATED VB LINE #(\d+)\s+\[(.*?)\].*', result, re.DOTALL)
            else:
                match = re.match(r".*\(ParserError\).*?'(.*?)'", result, re.DOTALL)
            if match:
                logging_colour = utils.TextColours.FAIL
                parsing_failed = True
                if failure_mode == 'line-by-line':
                    parsing_stopped_vb = getLineMatch(match.groups()[0], text)
                    parsing_stopped_py = getLineMatch('(ParserError)', result)
                    parsing_stopped_vb += locateBadLine(text, parsing_stopped_vb)
                    extra = ' (parser failure after %5.2f%% of lines): [%s]' % (
                        100.0 * parsing_stopped_vb / line_count,
                        lines[parsing_stopped_vb]
                    )
                elif failure_mode == 'quick':
                    parsing_stopped_vb = 0
                    parsing_stopped_py = 0
                    extra = ' Quick fail mode'
                elif failure_mode == 'fail-safe':
                    parsing_stopped_vb, parsing_stopped_py = getErrorLinesBySafeMode(text, result)
                    extra = ' Fail safe mode. %s errors.' % len(parsing_stopped_vb)
            #
            if return_structure != 'no':
                structure = getStructure(module.structure, return_structure, stripped_text.splitlines() + ['', ''])
            if return_line_numbers:
                line_lookup = module.line_lookup
    #
    app.logger.info('%s | %s[%s] Completed %d lines %s %s (%s) with status %s. Time took %5.2fs%s%s' % (
        correlation_string,
        logging_colour,
        request.remote_addr,
        line_count, module_type.__class__.__name__, conversion_style,
        language,
        status, time.time() - start_time,
        extra,
        utils.TextColours.ENDC,
    ))
    if failure_mode == 'fail-safe' and parsing_stopped_vb:
        for line_num in parsing_stopped_vb:
            try:
                app.logger.info('Failed: ||%s%s%s||' % (
                    utils.TextColours.FAIL,
                    lines[line_num],
                    utils.TextColours.ENDC,
                ))
            except IndexError:
                app.logger.info('Failed and also out of bounds: %s, %s' % (line_num, len(lines)))
    #
    main_response = {
        'status': status,
        'result': result,
        'parsing_failed': parsing_failed,
        'parsing_stopped_vb': parsing_stopped_vb,
        'parsing_stopped_py': parsing_stopped_py,
        'language': language,
        'version': version,
    }
    if return_structure != 'no':
        main_response['structure'] = structure
    if return_line_numbers:
        main_response['line_number_lookup'] = line_lookup
    #
    return json.dumps(main_response)


def log_request(text):
    """Log the request

    A short term measure to debug server crashes.

    """
    handle, path = tempfile.mkstemp(prefix='vb2py_', suffix='.txt', dir='/tmp')
    f = os.fdopen(handle, 'w')
    f.write(text)
    f.close()
    return path


def getLineMatch(search, text):
    """Return the line partially matching the text"""
    for idx, line in enumerate(text.splitlines()):
        if search in line:
            return idx
    else:
        return 0


def storeSubmittedFile():
    """Store a file that was submitted"""
    vb = request.values['text']
    filename = time.strftime('%Y-%m-%d %H:%M:%S code.vb')
    full_path = os.path.join(utils.rootPath(), 'submitted_files', filename)
    app.logger.info('%sStoring file for testing as %s%s' % (
        utils.TextColours.OKBLUE,
        filename,
        utils.TextColours.ENDC
    ))
    with open(full_path, 'w') as f:
        f.write(vb)
    return json.dumps({
        'status': 'OK',
        'result': 'File stored for testing',
    })


def removeFormCruft(text):
    """Remove form stuff if it is there"""
    match = re.match(r'.*?^Begin.*?^End\s*$(.*)', text, re.DOTALL + re.MULTILINE)
    if match:
        app.logger.debug('Removed form information')
        stripped = match.groups()[0]
        return stripped
    else:
        return text


def locateBadLine(vb, error_line):
    """Given some vb with a parsing error at the line number, try to zoom in and get more precise

    We do this by parsing each line starting at the error to see which one fails.

    """
    for idx, line in enumerate(vb.splitlines()[error_line:]):
        try:
            _ = vbparser.buildParseTree(line, 'isolated_single_line', returnpartial=False)
        except parserclasses.VBParserError:
            return idx
    else:
        return 0


flags = re.DOTALL + re.MULTILINE
LANGUAGE_SIGNALS = [
    ('C#', re.compile(r'.*^((using)|(#include))\s+.*', flags)),
    ('C#', re.compile(r'.*for\(int\s+i.*', flags)),
    ('C#', re.compile(r'.*return\s+\w+;.*', flags)),
    ('VB.NET', re.compile('.*End Class.*', flags)),
    ('VB.NET', re.compile('.*End Module.*', flags)),
    ('VB.NET', re.compile('.*End Namespace.*', flags)),
    ('VB.NET', re.compile('.*^Imports.*', flags)),
    ('VB.NET', re.compile('.*End Try.*', flags)),
    ('VB.NET', re.compile('.*#End\s+Region.*', flags)),
    ('VBP', re.compile('.*^Type=Exe$.*', flags)),
    ('VBA', re.compile(r'.*Active((Book)|(Sheet)|(Chart)).*', flags)),
    ('VBA', re.compile(r'.*Cells\(.*?\)\.Value.*', flags)),
    ('VBA', re.compile(r'.*Range\(.*?\)\.\w+.*', flags)),
    ('VBA', re.compile(r'.*Macro\w*\s+Macro.*', flags)),
]


def detectLanguage(text):
    """Try to detect the underlying VB dialect"""
    for language, signal in LANGUAGE_SIGNALS:
        if signal.match(text):
            return language
    else:
        return 'VB6'


def getErrorLinesBySafeMode(vbtext, pytext):
    """Return all the failing lines using the safe mode approach"""
    untranslated = re.compile(r'.*?UNTRANSLATED VB LINE \#(\d+)\s+\[(.*?)\].*', re.DOTALL + re.MULTILINE)
    py_lines = []
    vb_lines = []
    start_pos = 0
    vbtext = '\n'.join(l.strip() for l in vbtext.splitlines())
    while True:
        m = untranslated.match(pytext, start_pos)
        if m:
            py_line = len(pytext[:m.regs[1][0]].splitlines())
            py_lines.append(py_line - 1)
            vb_line = int(m.group(1))
            vb_lines.append(vb_line)
            start_pos = m.regs[1][1]
        else:
            break
    return vb_lines, py_lines


STRUCTURE_TYPES = {
    'all': ['*'],
    'methods': ['sub_definition', 'fn_definition']
}


def getStructure(structure, structure_type, text_lines):
    """Return a JSON suitable structure for the VB code"""
    result = []
    for item in structure:
        for pattern in STRUCTURE_TYPES[structure_type]:
            if fnmatch.fnmatch(item.name, pattern):
                children = getStructure(item.elements, structure_type, text_lines)
                definition_name = text_lines[item.line_offset].lstrip()
                #
                # Watch out in case there is a decorator
                if definition_name.startswith('<') and item.line_offset + 1 < len(text_lines):
                    definition_name = text_lines[item.line_offset + 1].lstrip()
                #
                result.append([
                    item.line_offset,
                    item.name,
                    removeScopes(definition_name),
                    item.start_on_line, item.length,
                    children])
                break
        else:
            result.extend(getStructure(item.elements, structure_type, text_lines))
    return result


def removeScopes(line):
    """Return a VB line with the scopes removed

    This helps in the structure explorer, where the scopes get in the way
    and make the line appear very long.

    """
    potentials = [
        "Sub ", "Function ", "Property ",
    ]
    for item in potentials:
        if item in line:
            return '{}{}'.format(item, line.split(item, 1)[1])
    else:
        return line
