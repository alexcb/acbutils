from .lines import lines

def diffparse(s):
    return diffparse_(enumerate(lines(s)))

def diffparse_(lines_itr, expect_end=None, line_start=0):
    sections = []
    section = []
    for line_num, (line, line_ending) in lines_itr:
        splits = line.split()
        if splits:
            prefix = splits[0]
            if prefix == '<<<<<<<':
                if section:
                    sections.append({
                        'type': 'text',
                        'text': section,
                        })
                    section = []
                a = diffparse_(lines_itr, '=')
                b = diffparse_(lines_itr, '>')
                sections.append({
                    'type': 'diff',
                    'a': a,
                    'b': b,
                    })
                continue
            elif prefix == '=======':
                assert expect_end == '='
                if section:
                    sections.append({
                        'type': 'text',
                        'text': section,
                        })
                return sections
            elif prefix == '>>>>>>>':
                assert expect_end == '>'
                if section:
                    sections.append({
                        'type': 'text',
                        'text': section,
                        })
                return sections
        section.append((line_num+1, line + line_ending))
    if section:
        sections.append({
            'type': 'text',
            'text': section,
            })
    return sections

def _test_diffparse():
    from textwrap import dedent
    s = dedent('''
    start
    line
    <<<<<<< HEAD
    alpha
    =======
    bravo
    charlie
    >>>>>>> remotes/earthly/earthly-main
    finish
    line
    ''').lstrip()
    actual = diffparse(s)
    want = [
        {
            'type': 'text',
            'text': [
                (1, 'start\n'),
                (2, 'line\n'),
                ],
            },
        {
            'type': 'diff',
            'a': [
                {'type': 'text',
                    'text': [
                        (4, 'alpha\n'),
                        ],
                }
                ],
            'b': [
                {'type': 'text',
                    'text': [
                        (6, 'bravo\n'),
                        (7, 'charlie\n'),
                        ],
                }
                ],
            },
        {
            'type': 'text',
            'text': [
                (9, 'finish\n'),
                (10,'line\n'),
                ],
            },
        ]
    assert actual == want

def _test_diffparse_empty():
    from textwrap import dedent
    s = dedent('''
    <<<<<<< HEAD
    =======
    >>>>>>> remotes/earthly/earthly-main
    ''').lstrip()
    actual = diffparse(s)
    want = [
        {
            'type': 'diff',
            'a': [],
            'b': [],
            },
        ]
    assert actual == want

def _test_diffparse_nested():
    from textwrap import dedent
    s = dedent('''
    hello
    <<<<<<< HEAD
    <<<<<<< HEAD:vendor/go.opentelemetry.io/contrib/instrumentation/net/http/httptrace/otelhttptrace/LICENSE
       Copyright [yyyy] [name of copyright owner]
    =======
       Copyright {yyyy} {name of copyright owner}
    >>>>>>> remotes/earthly/earthly-main:vendor/gopkg.in/yaml.v2/LICENSE
    =======
       Copyright [yyyy] [name of copyright owner]
    >>>>>>> remotes/earthly/earthly-main
    ''').lstrip()
    actual = diffparse(s)
    want = [
        {
            'type': 'text',
            'text': [(1, 'hello\n')],
            },
        {
            'type': 'diff',
            'a': [
                {'type': 'diff',
                    'a': [
                        {'type': 'text',
                            'text': [(4, '   Copyright [yyyy] [name of copyright owner]\n')],
                            }],
                    'b': [
                        {'type': 'text',
                            'text': [(6, '   Copyright {yyyy} {name of copyright owner}\n')],
                            }],
                    }
                ],
            'b': [
                {'type': 'text',
                    'text': [(9, '   Copyright [yyyy] [name of copyright owner]\n')],
                }
                ],
            },
        ]
    assert actual == want


if __name__ == '__main__':
    _test_diffparse()
    _test_diffparse_empty()
    _test_diffparse_nested()

