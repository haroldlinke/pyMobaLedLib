import glob
import os
import sys
import re
import time
import vb2py.utils
import subprocess


bcolors = vb2py.utils.TextColours


ok = re.compile(r".*Ran\s(\d+).*", re.DOTALL+re.MULTILINE)
fail = re.compile(r".*Ran\s(\d+).*\w+=(\d+)", re.DOTALL+re.MULTILINE)

show_errors = 0
if len(sys.argv) == 2:
    if sys.argv[1] == "-v":
        show_errors = 1



def preferentialSort(original, preferred_items):
    """Move the preferred items to the start of the original list

    Used to put the failing tests first so that we can quickly see them.

    """
    for item in preferred_items:
        try:
            idx = original.index(item)
        except ValueError:
            pass
        else:
            original.pop(idx)
            original.insert(0, item)


if __name__ == "__main__":
    print("\nStarting testall at %s\n" % time.ctime())
    #
    files = glob.glob(r"test/test*.py")
    files.sort()
    preferentialSort(files, [
        'test/testdotnet.py', 'test/testdotnet_execution.py', 'test/testfailures.py',
        'test/testdirectives.py', 'test/testlanguagedetection.py',
    ])
    #
    total_run = 0
    total_failed = 0
    start = time.time()
    try:
        for file in files:
            if file not in (r"test/testall.py", r"test/testframework.py",
                            r"test/testparser.py",):
                fname = os.path.join((r"python %s" % vb2py.utils.rootPath()), file)
                print(((bcolors.ENDC + "Running '%s' " % file) + bcolors.OKGREEN).ljust(55, '.'), end=' ')
                #
                start_time = time.time()
                p = subprocess.Popen(fname, shell=True, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    close_fds=True)
                pi, po, pe = (p.stdin, p.stdout, p.stderr)
                result = pe.read()
                duration = time.time() - start_time
                #
                print('[%5.1fs]' % duration, end=' ')
                #
                if result.find(b"FAILED ") > -1:
                    try:
                        num = int(fail.match(str(result)).groups()[0])
                        num_fail = int(fail.match(str(result)).groups()[1])
                    except:
                        num, num_fail = 0, 0
                    total_run += num
                    total_failed += num_fail
                    if show_errors:
                        print(bcolors.OKBLUE + "\n%s" % result)
                    else:
                        print(bcolors.FAIL + bcolors.BOLD + "*** %s errors out of %s" % (num_fail, num))
                else:
                    try:
                        num = int(ok.match(str(result)).groups()[0])
                    except:
                        print(bcolors.FAIL + bcolors.BOLD + "Failed completely: %s" % result)
                    else:
                        print(bcolors.OKBLUE + "Passed %s tests" % num)
                        total_run += num
                pi.close()
                po.close()
                pe.close()
    except KeyboardInterrupt:
        pass
    print((bcolors.ENDC + "\nRan %d tests\n" + bcolors.BOLD + bcolors.FAIL + "Failed %d\n" + bcolors.ENDC + "Took %d seconds") % (
        total_run, total_failed, time.time()-start))
