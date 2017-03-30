def parse_metrics(text):
    metrics = {}
    for l in text.split('\n'):
        l = l.strip()
        if l.startswith('#') or not l:
            continue
        name, value = l.split(' ')
        metrics[name] = float(value)
    return metrics
