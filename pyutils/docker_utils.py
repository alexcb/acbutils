import subprocess
import json
import random
import string
from proc_utils import communicate_stream

def get_ip(network_name, container_name):
    x = subprocess.check_output('docker inspect --type container %s' % container_name, shell=True)
    x = json.loads(x)
    assert len(x) == 1
    x = x[0]
    ip = x['NetworkSettings']['Networks'][network_name]['IPAddress']
    return ip

def get_network_names():
    x = subprocess.check_output('docker network ls', shell=True)
    names = []
    for l in x.split('\n')[1:]:
        l = l.strip()
        if not l:
            continue
        # this will break if the network name has a space in it
        names.append(l.split()[1])
    return names

def create_random_network():
    while True:
        x = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        if x not in get_network_names():
            break
    subprocess.check_call('docker network create %s' % x, shell=True)
    return x

def interactive_wait(container_id):
    logs_proc = subprocess.Popen('docker logs -f %s' % container_id, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for log in communicate_stream(logs_proc):
        yield log, None
    logs_proc.wait()

    exit_code = subprocess.check_output('docker wait %s' % container_id, shell=True)
    yield None, int(exit_code)
