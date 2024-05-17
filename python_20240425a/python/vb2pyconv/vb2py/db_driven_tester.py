"""Database driven testing"""

import argparse
import sys
import os
import sqlite3
import glob
import re
import time
import datetime
import io
import signal
import clipboard

signal.signal(signal.SIGINT, signal.default_int_handler)
sys.path.append('..')
from vb2py import utils
from vb2py.test_at_scale import file_tester
from vb2py import conversionserver

C = utils.TextColours
WIDTH = 90


#
# Allow use of datetimes
def adapt_datetime(ts):
    return time.mktime(ts.timetuple())


sqlite3.register_adapter(datetime.datetime, adapt_datetime)


def get_connection(filename):
    """Get a connection to the database"""
    c = sqlite3.connect(filename)
    c.create_function("REVERSE", 1, lambda s: s[::-1])
    return c


def np(filename):
    """Return a shortened version of a filename"""
    return filename[len(file_tester.BASE_FOLDER):]


def create_database(filename):
    """Create the database"""
    print('Creating new database as {} ...'.format(filename), end='')
    #
    # Remove old if needed
    if os.path.exists(filename):
        os.remove(filename)
    #
    conn = get_connection(filename)
    #
    conn.execute('''
        CREATE TABLE tests
        (id integer primary key, path text, filename text, active bool, lines int, annotation text)
    ''')
    #
    conn.execute('''
        CREATE TABLE runs
        (id integer primary key, date text, name text unique, total integer, failed integer, duration float)
    ''')
    #
    conn.execute('''
        CREATE TABLE groups
        (id integer primary key, name text unique)
    ''')
    #
    conn.execute('''
        CREATE TABLE group_entries
        (group_id integer not null, test_id integer not null,
            FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
            FOREIGN KEY (test_id) REFERENCES tests (id) ON DELETE CASCADE,
            UNIQUE (group_id, test_id)
        )
    ''')
    #
    conn.execute('''
        CREATE TABLE results
        (test_id integer not null, run_id integer not null, result bool, duration float, output text,
            FOREIGN KEY (test_id) REFERENCES tests (id) ON DELETE CASCADE,
            FOREIGN KEY (run_id) REFERENCES runs (id) ON DELETE CASCADE
        )
    ''')
    conn.close()
    print('{} DONE{}\n'.format(C.OKGREEN, C.ENDC))


def create_tests(conn):
    """Create the initial tests"""
    print('Creating tests')
    #
    # Remove old
    conn.execute('DELETE FROM tests')
    #
    # Go through all files
    files = glob.glob(utils.relativePath('test_at_scale', 'test*.py'))
    total_count = 0
    for file in files:
        count = create_test(conn, file)
        total_count += count
        print('{} DONE [{} tests]{}'.format(C.OKGREEN, count, C.ENDC))
    #
    print('\nCompleted {} tests\n'.format(total_count))


def create_test(conn, file):
    """Create a single file"""
    count = 0
    print('Adding {} '.format(np(file)).ljust(WIDTH, '.'), end='')
    with open(file, 'r') as f:
        file_text = f.read()
        for test_file in re.findall("_testFile\('(.*?)'", file_text):
            if os.path.isfile(test_file):
                with open(test_file, 'rb') as t:
                    line_count = len(t.read().splitlines())
                folder, filename = os.path.split(test_file)
                count += 1
                conn.execute('''
                INSERT INTO tests ('path', 'filename', 'active', 'lines', 'annotation') 
                VALUES (?, ?, 1, ?, ?)
                ''', (folder, filename, line_count, ''))
    return count


def matching_tests(conn, args):
    """Return a list of matching tests"""
    #
    # Get files based on tests
    if args.continuation:
        with open('.continuation.txt', 'r') as f:
            files = eval(f.read())
    elif args.last_test or args.last_failed or args.last_passed or args.previous_run:
        if args.previous_run:
            cur = conn.execute('SELECT id, date, name FROM runs WHERE name like ?', [args.previous_run])
        else:
            cur = conn.execute('SELECT id, date, name FROM runs ORDER BY date desc')
        matches = cur.fetchone()
        if not matches:
            print('{}No matching tests{}\n'.format(C.FAIL, C.ENDC))
            return []
        #
        run_id, timestamp, name = matches
        #
        # A clause to filter the tests down
        if args.last_failed:
            success_clause = 'AND results.result = 0'
        elif args.last_passed:
            success_clause = 'AND results.result = 1'
        else:
            success_clause = ''
        #
        print('Selecting test {}"{}"{} run at {}{}{}'.format(
            C.OKBLUE,
            name,
            C.ENDC,
            C.OKBLUE,
            datetime.datetime.fromtimestamp(int(float(timestamp))),
            C.ENDC
        ))
        cur = conn.execute('''SELECT tests.id, tests.path, tests.filename, tests.lines, tests.annotation FROM tests 
            INNER JOIN results ON tests.id = results.test_id
            WHERE results.run_id = ?
            AND path LIKE ?
            AND filename LIKE ?
            AND tests.annotation LIKE ?
            AND tests.active
            {}
        '''.format(success_clause), [run_id, args.folder, args.filename, args.with_annotation])
        files = cur.fetchall()
    elif args.group:
        if args.never_run:
            except_clause = '''
            EXCEPT SELECT tests.id, path, filename FROM tests INNER JOIN results r ON tests.id = r.test_id
            '''
        else:
            except_clause = ''
        #
        cur = conn.execute('''
            SELECT t.id, t.path, t.filename, t.lines, t.annotation FROM group_entries 
            INNER JOIN groups g on group_entries.group_id = g.id
            INNER JOIN tests t on group_entries.test_id = t.id
            WHERE g.name LIKE ?
            AND t.active
            AND t.annotation LIKE ?
            {}
        '''.format(except_clause), [args.group, args.with_annotation])
        files = cur.fetchall()
    elif args.never_run:
        cursor = conn.execute('''
            select id, path, filename, lines, annotation from tests
            WHERE path like ?
            AND filename like ?
            AND active
            AND annotation like ?
            EXCEPT 
            SELECT tests.id, path, filename, lines, annotation FROM tests INNER JOIN results r ON tests.id = r.test_id      
        ''', [args.folder, args.filename, args.with_annotation])
        files = cursor.fetchall()
    else:
        #
        # Get files based on folders and files
        active_clause = 'AND active' if not args.enable else ''
        cursor = conn.execute('''
        SELECT id, path, filename, lines, annotation FROM tests 
        WHERE path LIKE ?
        AND filename LIKE ? 
        AND annotation LIKE ?
        ''' + active_clause, [args.folder, args.filename, args.with_annotation])
        files = cursor.fetchall()
    #
    if args.failed_last_time:
        files = [item for item in files if get_last_result(conn, item[0]) == 0]
    #
    if args.broken:
        files = [item for item in files if get_last_result(conn, item[0], 1) and not get_last_result(conn, item[0])]
    #
    return files


def get_last_result(conn, test_id, number_from_last=0):
    """Return the last test result"""
    cur = conn.execute('''select result from results
        inner join runs r on results.run_id = r.id
        where test_id = ?
        order by date desc 
    ''', [test_id])
    result = cur.fetchall()
    if not result:
        return None
    else:
        return result[number_from_last][0]


def run_file(conn, list_of_tests, name, show_output):
    """Perform a single test on a file"""
    tester = file_tester.FileTester()
    success = failure = 0
    beginning_time = time.time()
    #
    # Create a new test run
    cur = conn.execute("INSERT INTO runs ('date', 'name') VALUES(?, ?)", [datetime.datetime.now(), name])
    run_id = cur.lastrowid
    idx = 0
    #
    try:
        for idx, item in enumerate(list_of_tests):
            test_id, folder, filename, lines, annotation = item
            print('{:3.0f}% {} '.format(
                float(idx + 1) / len(list_of_tests) * 100.0,
                np(os.path.join(folder, filename))).ljust(WIDTH - 10, '.') +
                get_last_tests(conn, test_id), end='')
            start_time = time.time()
            with Suppress() as capture:
                try:
                    tester._testFile(os.path.join(folder, filename))
                except Exception as err:
                    report = ' {}FAILED [{:.1f}s] {}'.format(C.FAIL, time.time() - start_time, C.ENDC)
                    failure += 1
                    result = 0
                else:
                    report = ' {}DONE [{:.1f}s] {}'.format(C.OKGREEN, time.time() - start_time, C.ENDC)
                    success += 1
                    result = 1
                #
                output_text = capture.get_output()
                #
                if show_output and not success:
                    report = '{}\n\n{}'.format(report, output_text)
                conn.execute('''
                    INSERT INTO results 
                    (test_id, run_id, result, duration, output)
                    VALUES (?, ?, ?, ?, ?)
                    ''', [test_id, run_id, result, time.time() - start_time, output_text])
            #
            print(report)
    except KeyboardInterrupt:
        print('\n\nCTR-C Pressed - exiting now\n')
        store_continue_files(conn, list_of_tests[idx:])
    #
    cur = conn.execute('UPDATE runs SET total=?, failed=?, duration=? WHERE id=?', (
        success + failure, failure, time.time() - beginning_time, run_id))
    #
    if not failure:
        print('\n{}Completed {} test{}'.format(C.OKGREEN, success, C.ENDC))
    else:
        print('\n{}Completed {} test with {} failures{}'.format(C.FAIL, success + failure, failure, C.ENDC))


def store_continue_files(conn, list_of_files):
    """Store a list of tests to run in case we continue"""
    with open('.continuation.txt', 'w') as f:
        f.write(repr(list_of_files))


def set_active(conn, list_of_tests, active):
    """Set whether tests are active or not"""
    for item in list_of_tests:
        test_id, folder, filename, lines, annotation = item
        print('Setting {} to {}{}{}'.format(
            np(os.path.join(folder, filename)), C.OKBLUE, active, C.ENDC))
        conn.execute('UPDATE tests SET active = ? WHERE id = ?', (active, test_id))
    #
    print('\nComplete')


def get_last_tests(conn, test_id):
    """Return the last tests run on this"""
    cur = conn.execute('''
        SELECT result FROM results INNER JOIN runs ON results.run_id = runs.id
        WHERE test_id = ?
        ORDER BY runs.date desc LIMIT 10
        ''', [test_id])
    results = [' '] * 10
    for item in reversed(cur.fetchall()):
        if item[0]:
            results.append('{}*{}'.format(C.OKGREEN, C.ENDC))
        else:
            results.append('{}!{}'.format(C.FAIL, C.ENDC))
    return ''.join(results[-10:])


def show_matching(conn, list_of_tests, show_output, show_results, history=1):
    """Show which files match
    :param show_results:
    """
    for item in list_of_tests:
        test_id, folder, filename, lines, annotation = item
        if show_results:
            c = conn.execute('''
                select result, results.duration, r.date
                from results join tests t on results.test_id = t.id
                join runs r on results.run_id = r.id
                where t.id = ?
                order by path, filename, r.date
            ''', [test_id])
            print('{}{}{} [{:5d} lines] [{}]'.format(
                C.HEADER, np(os.path.join(folder, filename)).ljust(WIDTH, '.'), C.ENDC,
                lines, annotation,
            ))
            for result, duration, timestamp in c.fetchall():
                if result:
                    result_text = '{}{}{}'.format(C.OKGREEN, 'OK', C.ENDC)
                else:
                    result_text = '{}{}{}'.format(C.FAIL, 'FAILED', C.ENDC)
                print('{} - [{:5.1f}s] - {}'.format(
                    datetime.datetime.fromtimestamp(int(float(timestamp))),
                    duration,
                    result_text,
                ))
            print()
        else:
            last_tests = get_last_tests(conn, test_id)
            print('{} [{:5d} lines] {} [{}]'.format(
                np(os.path.join(folder, filename)).ljust(WIDTH, '.'),
                lines,
                last_tests,
                annotation,
            ))
        if show_output:
            c = conn.execute('''
                select output from results
                inner join tests t on results.test_id = t.id
                where t.id = ?
                order by run_id desc
                limit  ?           
            ''', [test_id, history])
            for report in c.fetchall():
                print('\n{}\n'.format(report[0]))

    #
    print('\nTotal {} tests\n'.format(len(list_of_tests)))


def create_group(conn, list_of_tests, new_group_name):
    """Create a new group"""
    try:
        cur = conn.execute('INSERT INTO groups (name) VALUES(?)', [new_group_name])
    except sqlite3.IntegrityError:
        print('\n{}Group "{}" already exists{}\n'.format(C.FAIL, new_group_name, C.ENDC))
        return
    #
    group_id = cur.lastrowid
    print('\nCreated group {}"{}"{}'.format(C.OKBLUE, new_group_name, C.ENDC))
    #
    for item in list_of_tests:
        test_id, folder, filename, lines, annotation = item
        conn.execute('INSERT INTO group_entries (group_id, test_id) VALUES(?, ?)', [group_id, test_id])
        print('Added {} to group'.format(np(os.path.join(folder, filename))))
    #
    print('\nAdded {} tests'.format(len(list_of_tests)))


def add_to_group(conn, list_of_tests, group_name):
    """Add to an existing group"""
    cur = conn.execute('SELECT id FROM groups WHERE name = ?', [group_name])
    result = cur.fetchone()
    if not result:
        print('\n{}Group "{}" does not exist{}\n'.format(C.FAIL, group_name, C.ENDC))
        return
    #
    group_id = result[0]
    print('\nAdding to group {}"{}"{}'.format(C.OKBLUE, group_name, C.ENDC))
    #
    count = 0
    for item in list_of_tests:
        test_id, folder, filename, lines, annotation = item
        try:
            conn.execute('INSERT INTO group_entries (group_id, test_id) VALUES(?, ?)', [group_id, test_id])
        except sqlite3.IntegrityError:
            print('{}{} already in group{}'.format(C.FAIL, np(os.path.join(folder, filename)), C.ENDC))
        else:
            print('Added {} to group'.format(np(os.path.join(folder, filename))))
            count += 1
    #
    print('\nAdded {} tests'.format(count))


def delete_group(conn, list_of_tests, group_name):
    """Delete an existing group"""
    cur = conn.execute('SELECT id FROM groups WHERE name = ?', [group_name])
    result = cur.fetchone()
    if not result:
        print('\n{}Group "{}" does not exist{}\n'.format(C.FAIL, group_name, C.ENDC))
        return
    group_id = result[0]
    conn.execute('DELETE FROM groups WHERE name = ?', [group_name])
    conn.execute('DELETE FROM group_entries WHERE group_id = ?', [group_id])
    print('\nGroup {}"{}"{} deleted'.format(C.OKBLUE, group_name, C.ENDC))


def delete_all_groups(conn):
    """Delete an existing group"""
    cur = conn.execute('SELECT id, name FROM groups')
    all_groups = cur.fetchall()
    for result in all_groups:
        group_id, group_name = result
        conn.execute('DELETE FROM groups WHERE name = ?', [group_name])
        conn.execute('DELETE FROM group_entries WHERE group_id = ?', [group_id])
        print('Group {}"{}"{} deleted'.format(C.OKBLUE, group_name, C.ENDC))
    #
    print('\nDeleted {} groups'.format(len(all_groups)))


def clear_group(conn, group_name):
    """Clear an existing group"""
    cur = conn.execute('SELECT id, name FROM groups where name like ?', [group_name])
    all_groups = cur.fetchall()
    for result in all_groups:
        group_id, group_name = result
        conn.execute('DELETE FROM group_entries WHERE group_id = ?', [group_id])
        print('Group {}"{}"{} cleared'.format(C.OKBLUE, group_name, C.ENDC))
    #
    print('\nCleared {} groups'.format(len(all_groups)))


def show_groups(conn):
    """Show all the groups"""
    cur = conn.execute('''
        select name, count(group_id) from groups
        left join group_entries ge on groups.id = ge.group_id
        group by name, group_id
    ''')
    print('\nList of groups\n')
    total_groups = cur.fetchall()
    total_passed = total_failed = total_duration = total_lines = 0
    #
    for item in total_groups:
        name, count = item
        results = get_group_summary(conn, name)
        passed = sum(1 for i in results if i[2])
        failed = sum(1 for i in results if not i[2])
        duration = sum(i[3] for i in results)
        lines = sum(i[4] for i in results)
        #
        total_passed += passed
        total_failed += failed
        total_duration += duration
        total_lines += lines
        #
        print(' - {}{:20}{} {}{:4} tests{} [{:6d} loc] [{:4.0f}s].{}{:4}{} pass, {}{:4}{} failed'.format(
            C.WARNING if not (passed + failed) else C.OKGREEN if not failed else C.FAIL,
            name, C.ENDC,
            C.OKBLUE,
            count, C.ENDC,
            lines,
            duration,
            C.OKGREEN, passed, C.ENDC,
            C.FAIL, failed, C.ENDC,
        ))
    print('\nNumber groups = {}\n{} tests ({} passed, {} failed)\nDuration = {:6.1f}s\n{} lines\n\n'.format(
        len(total_groups),
        total_passed + total_failed, total_passed, total_failed,
        total_duration,
        total_lines,
    ))


def get_group_summary(conn, group_name):
    """Return the summary of the group results"""
    cur = conn.execute('''
        select t.path, t.filename, 
            cast(substr(reverse(group_concat(cast(result as char))), 1, 1) as integer), 
            duration, t.lines from results
        inner join tests t on results.test_id = t.id
        inner join group_entries ge on t.id = ge.test_id
        inner join groups g on ge.group_id = g.id
        where g.name = ?
        and t.active
        group by t.id
        order by run_id
    ''', [group_name])
    return cur.fetchall()


def create_test_groups(conn):
    """Create groups for all the folders"""
    print('\nCreating all test groups\n')
    cur = conn.execute('select id, path from tests')
    folders = {}
    count = 0
    for item in cur.fetchall():
        test_id, path = item
        root_path = path[len(file_tester.BASE_FOLDER) + 1:].split('/')[0]
        if root_path not in folders:
            try:
                cur = conn.execute('INSERT INTO groups (name) VALUES(?)', [root_path])
            except sqlite3.IntegrityError:
                print('{}Group "{}" already exists {}'.format(C.FAIL, root_path, C.ENDC))
                folders[root_path] = None
            else:
                print('Created group {}"{}"{}'.format(C.OKBLUE, root_path, C.ENDC))
                folders[root_path] = cur.lastrowid
                count += 1
        #
        group_id = folders[root_path]
        if group_id is not None:
            conn.execute('INSERT INTO group_entries (group_id, test_id) VALUES (?, ?)',
                         [group_id, test_id])
    #
    print('\nCreated {} groups\n'.format(count))


def annotate_language(conn, list_of_tests):
    """Annotate the items by language"""
    for test_id, folder, filename, lines, annotation in list_of_tests:
        print('Annotating {} '.format(np(os.path.join(folder, filename))).ljust(WIDTH - 10, '.'), end='')
        #
        text = file_tester.FileTester.getFileText(os.path.join(folder, filename))
        language = conversionserver.detectLanguage(text)
        conn.execute('''
            UPDATE tests SET annotation = ?
            WHERE id = ?
        ''', [language, test_id])
        print(' {}{}{}'.format(C.OKBLUE, language, C.ENDC))


def clipboard_runs(conn, list_of_tests):
    """Run through all tests copying the text to clipboard"""
    print('Running through all tests\n')
    position = 0
    while position < len(list_of_tests):
        test_id, folder, filename, lines, annotation = list_of_tests[position]
        print('Copy {} to clipboard'.format(np(os.path.join(folder, filename))).ljust(WIDTH - 10, '.'), end='')
        #
        text = file_tester.FileTester.getFileText(os.path.join(folder, filename))
        clipboard.copy(text)
        #
        result = input(' n = next, p = prev, x = exit, t = test, d = disable: [n] ')
        if result == 'x':
            break
        elif result == 'd':
            conn.execute('''
                UPDATE tests SET active = ?
                WHERE id = ?
            ''', [0, test_id])
        elif result == 'p':
            position = max(0, position - 1)
        else:
            position += 1


class Suppress:
    def __init__(self, *, suppress_stdout=True, suppress_stderr=True):
        self.suppress_stdout = suppress_stdout
        self.suppress_stderr = suppress_stderr
        self.original_stdout = None
        self.original_stderr = None
        self.output = None

    def __enter__(self):
        import sys, os
        self.output = devnull = io.StringIO()
        sys.stdout.flush()

        # Suppress streams
        if self.suppress_stdout:
            self.original_stdout = sys.stdout
            sys.stdout = devnull

        if self.suppress_stderr:
            self.original_stderr = sys.stderr
            sys.stderr = devnull

        return self

    def __exit__(self, *args, **kwargs):
        import sys
        # Restore streams
        if self.suppress_stdout:
            sys.stdout = self.original_stdout

        if self.suppress_stderr:
            sys.stderr = self.original_stderr

    def get_output(self):
        """Return the output"""
        self.output.flush()
        self.output.seek(0)
        return self.output.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Database driven tester')
    #
    # The database itself
    parser.add_argument('--db-file', required=False, default='testing.db', type=str,
                        dest='db_file', action='store',
                        help='the database name to use')
    parser.add_argument('--db-path', required=False, default='test_at_scale', type=str,
                        dest='db_path', action='store',
                        help='the database path, relative to vb2py')
    #
    # Which tests to act on
    parser.add_argument('--filename', required=False, type=str,
                        dest='filename', action='store', default='%',
                        help='a filename to act on')
    parser.add_argument('--folder', required=False, type=str,
                        dest='folder', action='store', default='%',
                        help='a folder to act on')
    parser.add_argument('--last-test', required=False, default=False, action='store_true',
                        dest='last_test',
                        help='the last tests run')
    parser.add_argument('--last-failed', required=False, default=False, action='store_true',
                        dest='last_failed',
                        help='the last tests run that failed')
    parser.add_argument('--last-passed', required=False, default=False, action='store_true',
                        dest='last_passed',
                        help='the last tests run that passed')
    parser.add_argument('--previous-run', required=False, type=str,
                        dest='previous_run', action='store', default='',
                        help='a previous run to act on')
    parser.add_argument('--never-run', required=False, default=False, action='store_true',
                        dest='never_run',
                        help='a test that has never been run')
    parser.add_argument('--failed-last-time', required=False, default=False, action='store_true',
                        dest='failed_last_time',
                        help='a test that failed last time it was run')
    parser.add_argument('--broken', required=False, default=False, action='store_true',
                        dest='broken',
                        help='a test that used to work but is now broken')
    parser.add_argument('--group', required=False, type=str,
                        dest='group', action='store', default='',
                        help='a named group to act on')
    parser.add_argument('--continue', required=False, default=False, action='store_true',
                        dest='continuation',
                        help='continue with the last set of files we were doing')
    #
    # Parameters
    parser.add_argument('--run-name', required=False, type=str,
                        dest='run_name', action='store', default='Test {}'.format(
                            datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')),
                        help='a folder to act on')
    parser.add_argument('--show-output', required=False,
                        dest='show_output', action='store_true',
                        help='whether to show the output')
    parser.add_argument('--show-results', required=False,
                        dest='show_results', action='store_true',
                        help='whether to show all the results')
    parser.add_argument('--history', required=False, type=int,
                        dest='history', action='store', default=1,
                        help='the number of reports to show for a test')
    #
    # The commands to create the overall database
    parser.add_argument('--create', required=False, default=False, action='store_true',
                        help='create the database')
    parser.add_argument('--create-tests', required=False, default=False, action='store_true',
                        dest='create_tests',
                        help='create the test cases')
    parser.add_argument('--create-test', required=False, type=str,
                        dest='create_test', action='store', default='',
                        help='a single test file to create from')
    parser.add_argument('--create-test-groups', required=False, default=False, action='store_true',
                        dest='create_test_groups',
                        help='create the groups for the test cases')
    #
    # Annotating
    parser.add_argument('--annotate-language', required=False, default=False, action='store_true',
                        dest='annotate_language',
                        help='add annotation of the language')
    parser.add_argument('--with-annotation', required=False, type=str,
                        dest='with_annotation', action='store', default='%',
                        help='limit to only files with annotation')
    #
    # Marking and un-marking tests
    parser.add_argument('--disable', required=False, default=False, action='store_true',
                        help='disable the given tests')
    parser.add_argument('--enable', required=False, default=False, action='store_true',
                        help='enable the given tests')
    #
    # Groups
    parser.add_argument('--create-group', required=False, type=str,
                        dest='create_group', action='store', default='',
                        help='a group to create')
    parser.add_argument('--add-to-group', required=False, type=str,
                        dest='add_to_group', action='store', default='',
                        help='a group to add files to')
    parser.add_argument('--delete-group', required=False, type=str,
                        dest='delete_group', action='store', default='',
                        help='a group to delete')
    parser.add_argument('--clear-group', required=False, type=str,
                        dest='clear_group', action='store', default='',
                        help='a group to clear')
    parser.add_argument('--delete-all-groups', required=False, default=False, action='store_true',
                        help='delete all the groups')
    #
    # Doing things
    parser.add_argument('--run-file', required=False, default=False, action='store_true',
                        help='run a test on a file or file pattern')
    parser.add_argument('--show', required=False, default=False, action='store_true',
                        help='just show the matching tests')
    parser.add_argument('--show-groups', required=False, default=False, action='store_true',
                        help='show the groups')
    parser.add_argument('--clipboard', required=False, default=False, action='store_true',
                        help='run through each test copying to clipboard')

    args = parser.parse_args()
    print('\n{}{}Database testing application - {}\n{}'.format(
        C.HEADER, C.OKBLUE,
        datetime.datetime.now().strftime('%H:%M %d-%m-%Y'),
        C.ENDC
    ))
    #
    db_filename = utils.relativePath(args.db_path, args.db_file)
    #
    # Database population
    if args.create:
        create_database(db_filename)
    #
    # Manipulation
    with get_connection(db_filename) as connection:
        if args.create_tests:
            create_tests(connection)
        if args.create_test_groups:
            create_test_groups(connection)
        if args.create_test:
            create_test(connection, utils.relativePath('test_at_scale', args.create_test))
        #
        tests = matching_tests(connection, args)
        if args.run_file:
            run_file(connection, tests, args.run_name, args.show_output)
        if args.disable:
            set_active(connection, tests, False)
        if args.enable:
            set_active(connection, tests, True)
        if args.show:
            show_matching(connection, tests, args.show_output, args.show_results, args.history)
        #
        # Groups
        if args.create_group:
            create_group(connection, tests, args.create_group)
        if args.add_to_group:
            add_to_group(connection, tests, args.add_to_group)
        if args.delete_group:
            delete_group(connection, tests, args.delete_group)
        if args.delete_all_groups:
            delete_all_groups(connection)
        if args.clear_group:
            clear_group(connection, args.clear_group)
        if args.show_groups:
            show_groups(connection)
        #
        if args.annotate_language:
            annotate_language(connection, tests)
        if args.clipboard:
            clipboard_runs(connection, tests)
