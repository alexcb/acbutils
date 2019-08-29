import sys

flag_type = object()

class ArgumentParser(object):
    def __init__(self):
        self.short_flags = {}
        self.long_flags = {}
        self.values = {}
        self.default_values = {}

    def add_argument(self, *args, **kwargs):
        action = kwargs.get('action')
        arg_type = kwargs.get('type')
        default = kwargs.get('default')

        long_name = None
        short_name = None
        for flag in args:
            if flag.startswith('--'):
                if long_name:
                    raise ValueError('long name already defined')
                long_name = flag[2:]
            elif flag.startswith('-'):
                if short_name:
                    raise ValueError('short name already defined')
                short_name = flag[1:]
            else:
                raise ValueError(f'{flag} must start with - or --')

        if long_name is None and short_name is None:
            raise ValueError('no flags given')

        if short_name in self.short_flags:
            raise ValueError(f'-{short_name} already registered')

        if long_name in self.long_flags:
            raise ValueError(f'--{long_name} already registered')

        var_name = long_name or short_name

        if action:
            if arg_type:
                raise ValueError('"action" keyword can not be used with "type" keyword')
            if default:
                raise ValueError('"action" keyword can not be used with "default" keyword')

            if action != 'store_true':
                raise ValueError('store_true is the only supported action')

            if short_name:
                self.short_flags[short_name] = {
                        'var_name': var_name,
                        'type': flag_type,
                        }

            if long_name:
                self.long_flags[long_name] = {
                        'var_name': var_name,
                        'type': flag_type,
                        }
            self.default_values[var_name] = False
            return

        if arg_type is None:
            arg_type = str

        if short_name:
            self.short_flags[short_name] = {
                    'var_name': var_name,
                    'type': arg_type,
                    }

        if long_name:
            self.long_flags[long_name] = {
                    'var_name': var_name,
                    'type': arg_type,
                    }
        self.default_values[var_name] = default

    def handle_flag(self, flag_def):
        if flag_def['type'] is flag_type:
            return True, 1
        return 

    def parse_args(self, args=sys.argv[1:]):
        values = self.default_values.copy()
        non_flag_args = []

        i = 0
        while i < len(args):
            arg = args[i]

            if i+1 == len(args):
                next_arg = None
            else:
                next_arg = args[i+1]

            if arg == '--':
                i += 1
                break
            if arg.startswith('--'):
                long_name = arg[2:]
                if long_name not in self.long_flags:
                    raise ValueError(f'--{long_name} is not a valid option')
                flag_def = self.long_flags[long_name]
                if flag_def['type'] is flag_type:
                    values[flag_def['var_name']] = True
                    i += 1
                else:
                    if next_arg is None:
                        raise ValueError(f'missing value for --{long_name}')
                    values[flag_def['var_name']] = flag_def['type'](next_arg)
                    i += 2
            elif arg.startswith('-'):
                short_name = arg[1:]
                if short_name not in self.short_flags:
                    raise ValueError(f'-{short_name} is not a valid option')
                flag_def = self.short_flags[short_name]
                if flag_def['type'] is flag_type:
                    values[flag_def['var_name']] = True
                    i += 1
                else:
                    if next_arg is None:
                        raise ValueError(f'missing value for -{short_name}')
                    values[flag_def['var_name']] = flag_def['type'](next_arg)
                    i += 2
            else:
                non_flag_args.append(arg)
                i += 1


        return values, non_flag_args, args[i:]


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--flag', action='store_true')
    parser.add_argument('-i', '--int', type=int, default=10)
    parser.add_argument('-s', '--str')
    args = parser.parse_args()
    print(args)
