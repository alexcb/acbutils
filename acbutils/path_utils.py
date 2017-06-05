import os
import errno
from contextlib import contextmanager


@contextmanager
def chdir(path):
    old = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old)

def get_cthulhu_path():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '/'.join(['..']*6)))

def get_host_cthulhu_path():
    host_path = os.getenv('cthulhu')
    if host_path:
        return host_path
    return get_cthulhu_path()

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
