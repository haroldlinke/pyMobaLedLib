"""Base class for testing file translation"""

import unittest
import os
import json
import argparse
import sys
import subprocess
import re
import chardet


sys.path.append('../..')

import vb2py.parserclasses
import vb2py.conversionserver


#
# Private data hiding may obscure some of the testing so we turn it off
import vb2py.config
Config = vb2py.config.VB2PYConfig()
Config.setLocalOveride("General", "RespectPrivateStatus", "No")
Config.setLocalOveride("General", "ReportPartialConversion", "No")


BASE_FOLDER = '/Users/paul/Workspace/sandbox/vb2py-git-files'
FAILURES_FOLDER = '/Users/paul/Workspace/sandbox/vb2py-git-files/AAA-Failing-Files'


class FileTester(unittest.TestCase):
    """Base class for file testing"""

    @staticmethod
    def getFileText(filename):
        """Return the file text"""
        #
        # Get the text
        with open(filename, 'r') as f:
            try:
                vb_code = f.read()
            except:
                #
                # Get encoding
                with open(filename, 'rb') as bf:
                    binary_text = bf.read()
                    details = chardet.detect(binary_text)
                #
                # Get the text
                vb_code = binary_text.decode(details.get('encoding', 'utf-8'), 'replace')
        #
        return vb_code

    def _testFile(self, filename, store_failure=True):
        """Try to parse a file"""
        vb_code = self.getFileText(filename)
        #
        # Some strange preamble seen in some code
        preambles = ['\xef\xbb\xbf', '\ufeff']
        for preamble in preambles:
            vb_code = vb_code.replace(preamble, '')
        #
        # Get the container
        container_lookup = {
            ".vb": (vb2py.parserclasses.VBDotNetModule, 'class'),
            ".bas": (vb2py.parserclasses.VBCodeModule, 'code'),
            ".cls": (vb2py.parserclasses.VBClassModule, 'class'),
            ".frm": (vb2py.parserclasses.VBFormModule, 'form'),
        }
        extension = os.path.splitext(filename)[1]
        container_class, url_part = container_lookup[extension.lower()]
        container = container_class()
        #
        client = vb2py.conversionserver.app.test_client()
        result = client.post(
            ('/single_%s_module' % url_part),
            data={
                'text': vb_code, 'style': 'vb', 'failure-mode': 'line-by-line',
            }
        )

        def store_failed_file():
            """Copy file failure"""
            if store_failure:
                failed_name = os.path.split(filename)[1]
                with open(os.path.join(FAILURES_FOLDER, failed_name), 'w') as f:
                    f.write(vb_code)
        #
        data = json.loads(result.data)
        if data['parsing_failed']:
            store_failed_file()
            #
            # Now also see what happens in safe mode
            result_safe = client.post(
                ('/single_%s_module' % url_part),
                data={
                    'text': vb_code, 'style': 'vb', 'failure-mode': 'fail-safe',
                }
            )
            data_safe = json.loads(result_safe.data)
            msg = 'Parsing %s failed\nFailsafe result %s, lines %s\n\n%s' % (
                filename,
                data_safe['parsing_failed'],
                data_safe['parsing_stopped_vb'],
                vb_code.splitlines()[data['parsing_stopped_vb']]
            )
            #
            self.fail(msg)
        else:
            #
            # Also try in safe mode to see that we get the same success
            result_safe = client.post(
                ('/single_%s_module' % url_part),
                data={
                    'text': vb_code, 'style': 'vb', 'failure-mode': 'fail-safe',
                }
            )
            data_safe = json.loads(result_safe.data)
            if data_safe['parsing_failed']:
                msg = 'Safe mode parsing %s failed when rigorous didn\'t: %s' % (
                    filename,
                    '\n\n'.join([vb_code.splitlines()[idx] for idx in data_safe['parsing_stopped_vb']])
                )
                store_failed_file()
                self.fail(msg)

        if data['status'] == 'ERROR':
            self.fail('Server reported an error: %s' % data['result'])


def scanForFiles(folder_name, extensions=('.frm', '.bas', '.cls', '.vb')):
    """Return all suitable VB files in a folder and subfolders"""
    filenames = []
    for subdir, dirs, files in os.walk(folder_name):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            extn = os.path.splitext(filepath)[1]
            if extn.lower() in extensions:
                print('Creating tests for %s' % filepath)
                filenames.append(filepath)
    return filenames


if __name__ == '__main__':
    #
    # Arguments
    parser = argparse.ArgumentParser(description='Clone repo and create tests')
    parser.add_argument('repos', type=str, nargs='+',
                        help='repo to clone and create tests for')
    parser.add_argument('--no-git', required=False,
                        dest='no_git', action='store_true',
                        help='just use existing folder, do not checkout from git')
    args = parser.parse_args()
    #
    # Create a repo
    for repo in args.repos:
        if args.no_git:
            name = repo
        else:
            name_match = re.match('https://github.com/(.*?)/', repo)
            if not name_match:
                print('Repo format not recognized: %s' % repo)
                sys.exit(1)
            #
            name = name_match.groups()[0]
        #
        folder_name = os.path.join(BASE_FOLDER, name)
        #
        # Clone if it is not there
        if os.path.isdir(folder_name):
            print('Folder exists. Skipping clone')
        elif args.no_git:
            print('Folder not found. Quiting')
            sys.exit(1)
        else:
            print('Cloning repository %s as %s' % (repo, name))
            subprocess.call(['git', 'clone', repo, folder_name])
        #
        # Now try to find all the files
        filenames = scanForFiles(folder_name)
        #
        # Now create the test file
        file_start_text = '''
import unittest
from vb2py.test_at_scale import file_tester


class Test_%s(file_tester.FileTester):
'''
        test_fragment = '''
\tdef test%s(self):
\t\tself._testFile('%s')
'''
        file_end_text = '''

if __name__ == '__main__':
\tunittest.main()
'''
        file_text = '%s%s%s' % (
            (file_start_text % name),
            ''.join((test_fragment % (idx, filename)) for idx, filename in enumerate(filenames)),
            file_end_text,
        )
        #
        # Write the file
        test_file_name = 'test%s.py' % name
        with open(test_file_name, 'w') as f:
            f.write(file_text)
        #
        print('Complete\n')
