"""A simple server to convert files from VB to Python"""

from . import vbparser
from . import parserclasses
from . import projectconverter as converter
from . import config
from docutils.core import publish_string
import base64
import io
import zipfile
import subprocess
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
            return vbparser.convertVBtoPython(text, container, returnpartial=returnpartial, dialect=dialect)
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
    start_time = time.time()
    #
    # Failure information
    parsing_failed = False
    parsing_stopped_vb = None
    parsing_stopped_py = None
    #
    conversion_style = 'unknown'
    extra = ''
    failure_mode = ''
    lines = []
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
        options = json.loads(request.values.get('options', '[]').strip())
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
        # Remove form stuff if it is there
        stripped_text = removeFormCruft(text)
        #
        try:
            try:
                if failure_mode == 'fail-safe':
                    utils.BASE_GRAMMAR_SETTINGS['mode'] = 'safe'
                result = ConversionHandler.convertSingleFile(stripped_text, module_type, conversion_style,
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
                match = re.match(r'.*?UNTRANSLATED VB LINE \[(.*?)\].*', result, re.DOTALL)
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
    app.logger.info('%s[%s] Completed %d lines %s %s (%s) with status %s. Time took %5.2fs%s%s' % (
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
            app.logger.debug('Failed: ||%s%s%s||' % (
                utils.TextColours.FAIL,
                lines[line_num],
                utils.TextColours.ENDC,
            ))
    #
    result = json.dumps({
        'status': status,
        'result': result,
        'parsing_failed': parsing_failed,
        'parsing_stopped_vb': parsing_stopped_vb,
        'parsing_stopped_py': parsing_stopped_py,
        'language': language,
        'version': version,
    })

    return result


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


def detectLanguage(text):
    """Try to detect the underlying VB dialect"""
    flags = re.DOTALL + re.MULTILINE
    dot_net_signals = [
        re.compile('.*End Class.*', flags),
        re.compile('.*End Module.*', flags),
    ]
    for signal in dot_net_signals:
        if signal.match(text):
            return 'VB.NET'
    else:
        return 'VB6'


def getErrorLinesBySafeMode(vbtext, pytext):
    """Return all the failing lines using the safe mode approach"""
    untranslated = re.compile(r'.*?UNTRANSLATED VB LINE \[(.*?)\].*', re.DOTALL + re.MULTILINE)
    py_lines = []
    vb_lines = []
    start_pos = 0
    vbtext = '\n'.join(l.strip() for l in vbtext.splitlines())
    while True:
        m = untranslated.match(pytext, start_pos)
        if m:
            py_line = len(pytext[:m.regs[1][0]].splitlines())
            py_lines.append(py_line - 1)
            vb_pos = vbtext.find(m.group(1))
            vb_line = len(vbtext[:vb_pos].splitlines())
            vb_lines.append(vb_line)
            start_pos = m.regs[1][1]
        else:
            break
    return vb_lines, py_lines
