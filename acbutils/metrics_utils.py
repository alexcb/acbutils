import requests
import time

def parse_metrics(text):
    metrics = {}
    for l in text.split('\n'):
        l = l.strip()
        if l.startswith('#') or not l:
            continue
        name, value = l.split(' ')
        metrics[name] = float(value)
    return metrics

def get_prometheus_metric(url, metric_name, timeout=30, min_val=None, max_val=None):
    end = time.time() + timeout
    ee = None
    while time.time() < end:

        try:
            r = requests.get(url)
            m = parse_metrics(r.text)
            val = m[metric_name]
            if min_val is not None and val < min_val:
                raise ValueError(metric_name)
            if max_val is not None and val > max_val:
                raise ValueError(metric_name)
            return val
        except Exception as e:
            ee = e
            pass
        time.sleep(1)
