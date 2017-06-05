# rows[group][row][col]
def tabulate(*rows, **kwargs):

    def to_str(x):
        if x is None:
            return ''
        if isinstance(x, float):
            return '%.3f' % x
        return str(x)

    rows = [[[to_str(c) for c in row] for row in group_of_rows] for group_of_rows in rows]

    assert len(set(len(y) for x in rows for y in x)) == 1, "not all rows have the same number of elements"
    lengths = [[len(str(xx)) for xx in y] for x in rows for y in x]
    padding = [max(x) for x in zip(*lengths)]
    width = sum(padding) + len(padding) * 3 + 1
    justify = kwargs.get('justify', 'l' * len(padding))
    assert len(justify) == len(padding), 'padding doesnt match length of columns'
    ljust = lambda s, pad: s.ljust(pad)
    rjust = lambda s, pad: s.rjust(pad)

    def f(s, j, n):
        if s is None:
            s = ''
        if isinstance(s, float):
            s = '%.3f' % s
        s = str(s)
        if j == 'l':
            return s.ljust(n)
        if j == 'r':
            return s.rjust(n)


    buf = []
    for i, rr in enumerate(rows):
        buf.append('-' * width)
        for r in rr:
            s = '|'.join(' %s ' % f(x, j, n) for x, j, n in zip(r, justify, padding))
            buf.append('|%s|' % s)
    buf.append('-' * width)
    return '\n'.join(buf)

if __name__ == '__main__':
    headers = [
        ('a', 'b', 'c'),
        ]
    data = [
        ('1', '2', '3'),
        ('11', '22', '33'),
        ]
    footer = [
        ('one', 'two', 'three'),
        ]
    print tabulate(headers, data, footer)
