import threading
import subprocess
import time
from select import select
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read


def _readerthread(running, fh, buffer):
    while running[0]:
        inputs = [fh.fileno()]
        rlist, _, xlist = select(inputs, [], inputs, 0.1)
        if not rlist and not xlist:
            continue

        try:
            x = read(fh.fileno(), 1024)
        except OSError as e:
            if e.errno == 11:
                pass
            else:
                raise
        else:
            if x:
                buffer.append(x)
            else:
                break
    fh.close()

def _setnonblocking(fh):
    flags = fcntl(fh, F_GETFL)
    fcntl(fh, F_SETFL, flags | O_NONBLOCK)

def run(cmd, shell=False, timeout=10):
    p = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    _setnonblocking(p.stdout)
    _setnonblocking(p.stderr)

    stdout = []
    stderr = []

    running = [True]

    t1 = threading.Thread(target=_readerthread, args=(running, p.stdout, stdout))
    t1.start()
    t2 = threading.Thread(target=_readerthread, args=(running, p.stderr, stderr))
    t2.start()

    while timeout > 0:
        res = p.poll()
        if res is not None:
            break
        x = 0.1
        if timeout < x:
            x = timeout
        time.sleep(x)
        timeout -= x

    running[0] = False

    t1.join()
    t2.join()

    stdout = b''.join(stdout)
    stderr = b''.join(stderr)

    return res, stdout, stderr
