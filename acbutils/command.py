import argparse

class MyParser(object):
    def __init__(self, parser=None):
        self._parser = parser or argparse.ArgumentParser()
        self._subparsers = None

    def add_argument(self, *args, **kwargs):
        self._parser.add_argument(*args, **kwargs)

    def add_command(self, command):
        if self._subparsers is None:
            self._subparsers = self._parser.add_subparsers()
        parser = self._subparsers.add_parser(command.name(), help=command.__doc__)
        command.add_arguments(MyParser(parser))
        parser.set_defaults(func=command.run)

    def parse_args(self, *args, **kwargs):
        return self._parser.parse_args(*args, **kwargs)

    def print_help(self, *args, **kwargs):
        return self._parser.print_help(*args, **kwargs)


class Command(object):
    def run(self):
        parser = MyParser()
        self.add_arguments(parser)
        args = parser.parse_args()
        if hasattr(args, 'func'):
            return args.func(args)
        parser.print_help()

    def name(self):
        return self.__class__.__name__

    def add_arguments(self, parser):
        pass


if __name__ == '__main__':
    class LeafCommand(Command):
        def __init__(self):
            pass
    
        def add_arguments(self, parser):
            parser.add_argument('--last-option', default='a', type=str, help='cluster config', choices=('a', 'b', 'd'))
    
        def run(self, args):
            print('leaf was run')
    
    class OtherLeafCommand(Command):
        def __init__(self):
            pass
    
        def add_arguments(self, parser):
            parser.add_argument('--other-last-option', default='a', type=str, help='cluster config', choices=('a', 'b', 'd'))
            parser.add_argument('-c', '--cluster', default='a', type=str, help='cluster config', choices=('a', 'b', 'd'))
    
        def run(self, args):
            print(('other was run, %s' % args.cluster))
    
    class MiddleCommand(Command):
        def __init__(self):
            pass
    
        def add_arguments(self, parser):
            parser.add_argument('--middle-option', default='a', type=str, help='cluster config', choices=('a', 'b', 'd'))
            parser.add_command(LeafCommand())
    
        def run(self, args):
            assert 0
    
    class RootCommand(Command):
        def __init__(self):
            pass
    
        def add_arguments(self, parser):
            parser.add_argument('-c', '--cluster', default='a', type=str, help='cluster config', choices=('a', 'b', 'd'))
            parser.add_command(MiddleCommand())
            parser.add_command(OtherLeafCommand())
  
    cmd = RootCommand()
    cmd.run()

