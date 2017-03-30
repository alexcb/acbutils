import subprocess
import threading
import time
from Queue import Queue, Empty

def _readerthread(fh, piperef, q):
    while True:
        x = fh.readline()
        if x == '':
            break
        q.put((piperef, x.strip('\n')))

    q.put((piperef, None))

def communicate_stream(p):
    q = Queue()
    stdout_thread = threading.Thread(target=_readerthread,
                                     args=(p.stdout, 1, q))
    stdout_thread.setDaemon(True)
    stdout_thread.start()

    stderr_thread = threading.Thread(target=_readerthread,
                                     args=(p.stderr, 2, q))
    stderr_thread.setDaemon(True)
    stderr_thread.start()

    num_none = 0
    while 1:
        piperef, line = q.get()
        if line is None:
            num_none += 1
            if num_none >= 2:
                break
        else:
            yield line

