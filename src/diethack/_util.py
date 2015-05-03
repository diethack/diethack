import subprocess
import logging

def call(cmdLine, workDir = '.'):
    logging.debug('Invoking command line: %s', cmdLine)
    try:
        return subprocess.check_output(cmdLine, shell=True,
                                       cwd=workDir, stderr=subprocess.STDOUT)
    except OSError as e:
        raise Exception('os error: %s, %s, %s' % (cmdLine, workDir, str(e)))
    except subprocess.CalledProcessError as e:
        raise Exception('proc error: %s, %s, %s' % (cmdLine, workDir, str(e.output)))

def roughlyLessEqual(a, b):
    return a <= b + 0.001

def roughlyGreaterEqual(a, b):
    return a >= b - 0.001

def readFile(fname):
    try:
        f = open(fname, 'r')
    except IOError:
        return None
    res = f.read()
    f.close()
    return res

def readFileLines(fname):
    try:
        f = open(fname, 'r')
    except IOError:
        return []
    res = f.readlines()
    f.close()
    return res

def writeFile(fname, data):
    with open(fname, 'w') as f:
        f.write(data)

def htmlEscape(s):
    t = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(t.get(c,c) for c in s)
