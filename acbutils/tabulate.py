def calc_width(x):
    n = 0
    for l in x.split('\n'):
        n = max(n, len(l))
    return n

def calc_height(x):
    return len(x.split('\n'))

def to_str(x):
    if x is None:
        return ''
    if isinstance(x, float):
        return '%.3f' % x
    return str(x)

def get_line(s, n):
    try:
        return s.split('\n')[n]
    except IndexError:
        return ''

def ensure_same_col_types(rows):
    for y, row in enumerate(rows):
        if y == 0:
            t = [type(x) for x in row]
        for x, col in enumerate(row):
            thetype = type(col)
            if thetype != t[x]:
                raise TypeError('row %d col %d type \"%s\" doesnt match type \"%s\" in row 0 col %d' % (y, x, str(thetype.__name__), str(t[x].__name__), x))

def format_rows_strings(rows):
    return [
        [to_str(x) for x in row]
        for row in rows
        ]

# rows[group][row][col]
def tabulate(*args, **kwargs):

    csep_pad = ' '
    style = kwargs.get('style', 'pipe')
    if style == 'pipe':
        rsep = '-'
        csep = '|'
    elif style == 'min':
        rsep = ''
        csep = ''
    elif style == 'section':
        rsep = '-'
        csep = ''
    else:
        raise ValueError(style)


    def join_line(l):
        buf = []
        buf.append(csep)
        for s in l:
            buf.append(csep_pad)
            buf.append(s)
            buf.append(csep_pad)
            buf.append(csep)
        return ''.join(buf)

    for rows in args:
        ensure_same_col_types(rows)

    first_row = args[0][0]
    expected_len = len(first_row)
    for rows in args:
        for row in rows:
            assert(len(row) == expected_len)

    justify = kwargs.get('justify')
    if justify is None:
        #import pdb; pdb.set_trace()
        justify = ['l'] * len(args[0][0])
        for rows in args:
            for row in rows:
                for i, col in enumerate(row):
                    if isinstance(col, float):
                        print 'changing justify type'
                        print justify, i
                        justify[i] = 'r'
    else:
        if len(justify) != expected_len:
            raise ValueError("justify string incorrect length")
        justify = list(justify)

    rows_groups = []
    for rows in args:
        for row in rows:
            if justify is None:
                justify = ['l'] * len(row)
            for i, col in enumerate(row):
                if isinstance(col, float):
                    justify[i] = 'r'
        rows = format_rows_strings(rows)
        rows_groups.append(rows)

    col_widths = None
    row_heights = []
    for rows in rows_groups:
        for row in rows:
            if col_widths is None:
                col_widths = [0] * len(row)
            else:
                if len(row) != len(col_widths):
                    raise ValueError('not all rows have equal numbers of columns')
            for i, col in enumerate(row):
                n = calc_width(col)
                if n > col_widths[i]:
                    col_widths[i] = n
            row_heights.append(max(calc_height(x) for x in row))

    ljust = lambda s, pad: s.ljust(pad)
    rjust = lambda s, pad: s.rjust(pad)

    buf = []

    total_width = len(join_line([' ' * x for x in col_widths]))

    y = 0
    for rows in rows_groups:
        buf.append(rsep * total_width)
        for row in rows:
            for i in range(row_heights[y]):
                line = []
                for col, w, j in zip(row, col_widths, justify):
                    s = get_line(col, i)
                    if j == 'l':
                        s = ljust(s, w)
                    else:
                        s = rjust(s, w)
                    line.append(s)
                buf.append(join_line(line))
            y += 1
    buf.append(rsep * total_width)

    return '\n'.join(buf)


if __name__ == '__main__':
    headers = [
        ('a', 'b', 'c'),
        ]
    data = [
        ('1',   2.0, '3'),
        ('11', 22.00, '33\nthirtythree'),
        ('11', 22.12, '33'),
        ]
    footer = [
        ('one', 'two', 'three'),
        ]
    print tabulate(headers, data, footer, style='section')
