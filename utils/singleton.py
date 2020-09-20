"""
class Singleton(object):
    def __init__(self):
        self._run_count = 0

    def foo(self):
        pass


mysington = Singleton()

"""

import os
import sys
import time
import logging
logger = logging


class Singleton:
    def __init__(self):
        pass

    def get_lock_file(self):
        py_file_path = os.getcwd() # os.path.abspath(__file__)
        basepath = py_file_path # os.path.dirname(py_file_path)
        return os.path.normpath(basepath + '/' + 'singleton.lock')

    def detect_instance(self):
        py_file_path = os.getcwd() # os.path.abspath(__file__)
        basepath = py_file_path # os.path.dirname(py_file_path)
        self.lockfile = os.path.normpath(basepath + '/' + os.path.basename(__file__) + '.lock')
        self.lockfile = self.get_lock_file()
        if sys.platform == 'win32':
            try:
                # file already exists, we try to remove (in case previous execution was interrupted)
                if os.path.exists(self.lockfile):
                    os.unlink(self.lockfile)
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                return True
            except OSError as e:
                if e.errno == 13:
                    return False
                raise e
        else:
            # non Windows
            import fcntl
            self.fp = open(self.lockfile, 'w')
            try:
                fcntl.lockf(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except IOError:
                return False

    def delete_lok_file(self):
        file = self.get_lock_file()
        # windows
        os.close(self.fd)
        if os.path.exists(file):
            os.remove(file)
