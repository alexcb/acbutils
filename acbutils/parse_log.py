# parselog parses lines like
#   time="2021-12-13T19:02:51Z" level=debug msg="<< unpark hello world"
def parselog(s):
    word = []
    escape=False
    key=None
    value=None
    quote=False
    items = []
    for c in s:
        if escape:
            word.append(c)
            escape=False
            continue
        if c == '\\':
            escape=True
            continue
        if quote:
            if c == '"':
                quote=False
                continue
            word.append(c)
            continue
        if c == '"':
            quote=True
            continue
        if key is None:
            if c == '=':
                key = ''.join(word)
                word = []
                continue
        else:
            if c == ' ':
                value = ''.join(word)
                word = []
                items.append((key.strip(), value.strip()))
                key = None
                continue
        word.append(c)
    if key:
        value = ''.join(word)
        items.append((key.strip(), value.strip()))
    return items
