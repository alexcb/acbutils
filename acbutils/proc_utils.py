import subprocess
import threading
import time
from Queue import Queue, Empty
from __future__ import print_function

def _readerthread(fh, piperef, q):
    if fh:
        l = fh.readline()
        while l:
            q.put((piperef, l.strip('\n')))
            l = fh.readline()
        fh.close()
    q.put((piperef, None))

def communicate_stream(p, input=None):
    q = Queue()
    stdout_thread = threading.Thread(target=_readerthread,
                                     args=(p.stdout, 1, q))
    stdout_thread.setDaemon(True)
    stdout_thread.start()

    stderr_thread = threading.Thread(target=_readerthread,
                                     args=(p.stderr, 2, q))
    stderr_thread.setDaemon(True)
    stderr_thread.start()

    if input:
        try:
            p.stdin.write(input)
        except BrokenPipeError:
            pass  # communicate() must ignore broken pipe errors.
        except OSError as exc:
            if exc.errno == errno.EINVAL:
                # bpo-19612, bpo-30418: On Windows, stdin.write() fails
                # with EINVAL if the child process exited or if the child
                # process is still running but closed the pipe.
                pass
            else:
                raise

    try:
        p.stdin.close()
    except BrokenPipeError:
        pass  # communicate() must ignore broken pipe errors.
    except OSError as exc:
        if exc.errno == errno.EINVAL:
            pass
        else:
            raise

    num_none = 0
    while 1:
        piperef, line = q.get()
        if line is None:
            num_none += 1
            if num_none >= 2:
                break
        else:
            yield piperef, line

    stdout_thread.join()
    stderr_thread.join()


if __name__ == '__main__':
    cmd = ['ls']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    for piperef, line in communicate_stream(p):
        print(piperef, line)
