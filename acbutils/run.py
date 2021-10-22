#!/bin/env python3
import os
import subprocess
import pwd
import grp

def get_sudo_user():
    if os.geteuid() != 0:
        return None
    try:
        sudo_user = os.environ['SUDO_USER']
    except KeyError:
        return None
    return sudo_user

def run(cmd, user=None, cwd=None, background=False):
    kwargs = {
        'shell': True,
            }
    if cwd:
        kwargs['cwd'] = cwd
    env = {}
    if user:
        pw = pwd.getpwnam(user)
        groups = [g.gr_gid for g in grp.getgrall() if user in g.gr_mem]
        def demote():
            os.setgid(pw.pw_gid)
            os.setgroups(groups)
            os.setuid(pw.pw_uid)
        kwargs['preexec_fn'] = demote
    else:
        pw = pwd.getpwuid(0)
    env['HOME'] = pw.pw_dir

    print(f'running `{cmd}` as {pw.pw_name} under {cwd} with {env}')
    kwargs['env'] = env

    if not background:
        return subprocess.check_call(cmd, **kwargs)

    proc = subprocess.Popen(cmd, **kwargs)
    def waitfunc():
        returncode = proc.wait()
        if returncode != 0:
            raise subprocess.CalledProcessError(cmd=cmd, returncode=returncode)
    def killfunc():
        proc.kill()

    return waitfunc, killfunc


if __name__ == '__main__':
    import sys

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)


    def main():
        sudo_user = get_sudo_user()
        if not sudo_user:
            eprint('must be with sudo (including SUDO_USER)')
            sys.exit(1)

        print('-- as root --')
        run(f'whoami')

        print('-- as sudo user --')
        run(f'whoami', user=sudo_user)

        print('-- assuming docker is installed, make sure we are still part of the docker group --')
        run(f'docker ps -a', user=sudo_user)

    main()
