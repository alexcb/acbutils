def grouper(n, iterable):
    '''grouper(3, "abcd") -> [['a', 'b', 'c'], ['d']]'''
    i = iter(iterable)
    running = True
    while running:
        args = []
        for _ in range(n):
            try:
                args.append(next(i))
            except StopIteration:
                running = False
        if args:
            yield args

if __name__ == '__main__':
    def test_grouper():
        for x in grouper(3, list(range(10))):
            print(x)
        for x in grouper(3, "abc"):
            print(x)
    test_grouper()
