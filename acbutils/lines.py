class MultipleLineEndingsError(ValueError):
    pass

def index_or_none(s, sub):
    try:
        return s.index(sub)
    except ValueError:
        return None

def lines(s):
    ''' iterate over lines terminated by "\n" or "\r\n" or a mix'''

    while s:
        unix = index_or_none(s, '\n')
        dos = index_or_none(s, '\r\n')
        mac = index_or_none(s, '\r')
        if mac is not None:
            if unix is not None:
                if mac < unix:
                    if dos == mac:
                        yield s[:dos], '\r\n'
                        s = s[dos+2:]
                    else:
                        yield s[:mac], '\r'
                        s = s[mac+1:]
                    continue
            else:
                yield s[:mac], '\r'
                s = s[mac+1:]
                continue

        if unix is not None:
            yield s[:unix], '\n'
            s = s[unix+1:]
            continue

        assert '\n' not in s
        assert '\r' not in s
        yield s, ''
        break

def _test_lines():
     assert list(lines('')) == []

     assert list(lines('abc')) == [ ('abc', '') ]
     assert list(lines('a\nb\nc')) == [ ('a', '\n'), ('b', '\n'), ('c', '') ]
     assert list(lines('a\nb\nc\n')) == [ ('a', '\n'), ('b', '\n'), ('c', '\n') ]
     assert list(lines('alpha\nbravo\ncharlie\n')) == [ ('alpha', '\n'), ('bravo', '\n'), ('charlie', '\n') ]
     assert list(lines('alpha\n\ncharlie\n')) == [ ('alpha', '\n'), ('', '\n'), ('charlie', '\n') ]
     assert list(lines('\n\n\n')) == [ ('', '\n'), ('', '\n'), ('', '\n') ]
     assert list(lines('\n')) == [ ('', '\n') ]

     assert list(lines('\r\r\r')) == [ ('', '\r'), ('', '\r'), ('', '\r') ]
     assert list(lines('a\rb\rc')) == [ ('a', '\r'), ('b', '\r'), ('c', '') ]
     assert list(lines('alpha\r\rcharlie')) == [ ('alpha', '\r'), ('', '\r'), ('charlie', '') ]
     assert list(lines('alpha\r\rcharlie\n\n')) == [ ('alpha', '\r'), ('', '\r'), ('charlie', '\n'), ('', '\n') ]
     assert list(lines('\r')) == [ ('', '\r') ]

     assert list(lines('\r\n')) == [ ('', '\r\n') ]
     assert list(lines('\r\n\r\n')) == [ ('', '\r\n'), ('', '\r\n') ]

     assert list(lines('one\ntwo\r\nthree\rfour')) == [ ('one', '\n'), ('two', '\r\n'), ('three', '\r'), ('four', '') ]
     assert list(lines('one\rtwo\r\nthree\nfour')) == [ ('one', '\r'), ('two', '\r\n'), ('three', '\n'), ('four', '') ]
     assert list(lines('one\rtwo\r\nthree\nfour\r\n')) == [ ('one', '\r'), ('two', '\r\n'), ('three', '\n'), ('four', '\r\n') ]

     assert list(lines('one\rtwo\n\rthree')) == [ ('one', '\r'), ('two', '\n'), ('', '\r'), ('three', '') ]

def ending(s):
    if not s:
        return ''
    l = list(lines(s))
    if len(l) != 1:
        raise MultipleLineEndingsError
    return l[0][1]

def _test_ending():
    assert ending('') == ''
    assert ending('\n') == '\n'
    assert ending('\r') == '\r'
    assert ending('\r\n') == '\r\n'

    assert ending('hello\n') == '\n'
    assert ending('hello\r') == '\r'
    assert ending('hello\r\n') == '\r\n'

    good = False
    try:
        ending('\rbad\n')
    except MultipleLineEndingsError:
        good = True
    assert good




if __name__ == '__main__':
    _test_lines()
    _test_ending()
