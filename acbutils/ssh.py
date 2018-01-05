import StringIO
import multiprocessing.dummy
import os
import subprocess
import textwrap
import zipfile
import sys
import functools
import time
import random
import threading
import curses

from .proc_utils import communicate_stream

from .tabulate import tabulate


# Example usage
#
# import acbutils.ssh
# ips = ['1.2.3.4', '5.4.3.6', 'localhost']
# scripts = {}
# for ip in ips:
#   scripts[ip] = acbutils.ssh.build_remote_script(textwrap.dedent('''
#     import socket
#     print socket.gethostname()
#     '''))
#
# ssh_opts = [
#     '-o', 'ConnectTimeout=5',
#     '-o', 'StrictHostKeyChecking no',
#     ]
# print acbutils.ssh.tabulate_results(acbutils.ssh.run_scripts_over_ssh_parallel(scripts, ssh_opts=ssh_opts, status=True))


def build_remote_script(script, vars={}, remotelib=None):
    buf = StringIO.StringIO()

    zf = zipfile.ZipFile(buf, "a", zipfile.ZIP_DEFLATED, False)
    zf.writestr("__main__.py", script)

    if remotelib:
        for root, dir, files in os.walk(remotelib):
            for f in files:
                zf.writestr(f, open(os.path.join(root, f)).read())
    zf.close()

    data = repr(buf.getvalue().encode('base64'))

    return textwrap.dedent('''
        import tempfile
        import runpy
        
        vars = %s
        data = %s
        
        with tempfile.NamedTemporaryFile(suffix='.zip') as f:
            f.write(data.decode('base64'))
            f.flush()
            runpy.run_path(f.name, init_globals=vars)
    ''' % (repr(vars), data))

def _get_ssh_cmd(host, sudo=False, ssh_opts=[]):
    sudo_cmd = ['sudo'] if sudo else []
    cmd = ['ssh'] + ssh_opts + [host] + sudo_cmd + ['python', '-']
    return cmd

def run_script_over_ssh(host, script, sudo=False, ssh_opts=[]):
    cmd = _get_ssh_cmd(host, sudo, ssh_opts)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.communicate(input=script)[0]
    return p.returncode, out.decode()

def run_scripts_over_ssh_parallel(scripts, sudo=False, ssh_opts=[], max_conn=4, rand_wait=5, status=False):

    host_status = {x:('waiting', 0) for x in scripts}

    if status:
        screen = curses.initscr()
        running = [True]
        def display_status():
            while running[0]:
                screen.clear()
                active = sorted([(k, v[1]) for k,v in host_status.iteritems() if v[0] == 'running'], key=lambda x: x[1])
                num_done = len([1 for k,v in host_status.iteritems() if v[0] == 'done'])
                num_total = len(host_status)
                screen.addstr(1, 0, '%d / %d done' % (num_done, num_total))
                y = 2
                if active:
                    screen.addstr(y, 0, 'currently running:')
                    rows = []
                    for h, started in active:
                        ago = int(time.time() - started)
                        rows.append([h, '%d second(s)' % ago])
                    for l in tabulate([['hostname', 'session age']], rows).split('\n'):
                        screen.addstr(y, 0, l)
                        y += 1
                else:
                    screen.addstr(y, 0, 'no active sessions')
                screen.refresh()
                time.sleep(1)

    def helper(args):
        host, script = args
        now = time.time()
        host_status[host] = ('running', now)
        time.sleep(random.uniform(0, rand_wait))
        result = run_script_over_ssh(host, script, sudo=sudo, ssh_opts=ssh_opts)
        host_status[host] = ('done', time.time() - now)
        return (host, result)

    if status:
        stdscr = curses.initscr()

        t = threading.Thread(target=display_status)
        t.start()

    p = multiprocessing.dummy.Pool(max_conn)
    results = dict(p.map(helper, scripts.items()))

    if status:
        running[0] = False
        t.join()
        curses.endwin()


    return results

def stream_script_over_ssh(host, script, stream_callback, sudo=False, ssh_opts=[]):
    cmd = _get_ssh_cmd(host, sudo, ssh_opts)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    for linetype, line in communicate_stream(p, script):
        stream_callback(linetype, line)
    return p.poll()

def stream_scripts_over_ssh_parallel(scripts, stream_callback, sudo=False, ssh_opts=[], max_conn=4, rand_wait=5):
    def helper(args):
        time.sleep(random.uniform(0, rand_wait))
        host, script = args
        return (host, stream_script_over_ssh(host, script, functools.partial(stream_callback, host), sudo=sudo, ssh_opts=ssh_opts))
    p = multiprocessing.dummy.Pool(max_conn)
    return dict(p.map(helper, scripts.items()))

def tabulate_results(results):
    rows = []
    for k, v in sorted(results.tems()):
        code, output = v
        rows.append([k, code, output.strip()])
    return tabulate([['Hostname', 'Exit code', 'Output']], rows)
