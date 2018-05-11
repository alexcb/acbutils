def get_word_pos(s):
    pos = []
    last = None
    start = None
    for i, c in enumerate(s):
        if c == ' ':
            if start is not None:
                word = s[start:i]
                pos.append((word, start))
                start = None
        else:
            if start is None:
                start = i
    if start is not None:
        word = s[start:]
        pos.append((word, start))

    return pos

def get_words_at_pos(s, pos):
    start = pos
    end = [x-1 for x in pos[1:]]
    end.append(None)
    return [s[i:j].strip() for i, j in zip(start,end)]


def read_table(s, col_parsers={}):
    lines = s.split('\n')
    lines = [x for x in lines if x.strip()]
    headers = get_word_pos(lines[0])
    lines = lines[1:]

    colnames = [x[0] for x in headers]
    colpos =   [x[1] for x in headers]

    rows = []
    for l in lines:
        rows.append(dict(zip(colnames, get_words_at_pos(l, colpos))))

    for r in rows:
        for k in r:
            if k in col_parsers:
                r[k] = col_parsers[k](r[k])

    return rows


if __name__ == '__main__':
    x = '''
    aaa       bbb      ccc
    1          2         3
    one       two      three
              22
    un
    '''
    
    print(read_table(x))
