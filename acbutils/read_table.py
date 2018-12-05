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

def get_col_pos(lines):
    blanks = []
    for l in lines:
        assert '\t' not in l
        if len(l) > len(blanks):
            n = len(l) - len(blanks)
            blanks = blanks + [True]*n
        for i, c in enumerate(l):
            if c != ' ':
                blanks[i] = False

    pos = []
    looking = True
    for i, c in enumerate(blanks):
        if looking:
            if c == False:
                pos.append(i)
                looking = False
            continue
        else:
            if c == True:
                looking = True

    headers = get_words_at_pos(lines[0], pos)


    pos2 = []
    for s, i in zip(headers, pos):
        if s:
            pos2.append(i)

    return pos2

def get_words_at_pos(s, pos):
    start = pos
    end = [x-1 for x in pos[1:]]
    end.append(None)
    return [s[i:j].strip() for i, j in zip(start,end)]

def read_table(s, col_parsers={}):
    lines = s.split('\n')
    lines = [x for x in lines if x.strip()]
    col_pos = get_col_pos(lines)
    headers = get_words_at_pos(lines[0], col_pos)
    lines = lines[1:]

    rows = []
    for l in lines:
        rows.append(dict(list(zip(headers, get_words_at_pos(l, col_pos)))))

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
    
    print((read_table(x)))
