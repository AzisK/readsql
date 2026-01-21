import argparse
import functools
import os
import re
import sys

DIR = os.path.dirname(__file__)


def main():
    args = parse_args()
    if args.string:
        print('\n'.join(read_replace(p) for p in args.path))
    else:
        run_on_files(args.path, args.python_var, dry_run=args.nothing)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='readsql', description='Convert SQL to most human readable format'
    )
    parser.add_argument('path', nargs='+', help='Path to the file to be converted')
    parser.add_argument('-s', '--string', action='store_true', help='Read a string')
    parser.add_argument(
        '-n', '--nothing', action='store_true', help='Dry run (do not modify files)'
    )
    parser.add_argument(
        '-py',
        '--python_var',
        nargs='+',
        default=['query'],
        help='Variables to search in Python files (default: query)',
    )
    return parser.parse_args()


def run_on_files(paths, variables, dry_run=False):
    results = []
    for path in collect_files(paths):
        lines = read_file(path, variables)
        if lines is None:
            continue
        if not dry_run:
            with open(path, 'w') as f:
                f.write(lines)
        else:
            results.append(lines)
        action = 'would be reformatted' if dry_run else 'reformatted'
        print(f'{path} {action}:\n{lines}')
    return results if dry_run else None


def collect_files(paths):
    for path in paths:
        if os.path.basename(path).startswith('.'):
            continue
        if os.path.isdir(path):
            yield from collect_files(os.path.join(path, f) for f in os.listdir(path))
        elif os.path.isfile(path):
            yield path
        else:
            print(f'Path does not exist: {path}', file=sys.stderr)
            sys.exit(1)


def read_file(path, variables):
    if path.endswith('.py'):
        return read_python_file(path, variables)
    elif path.endswith('.sql'):
        return read_sql_file(path)
    else:
        print(f'{path} is not an SQL or Python file')
        return


def read_sql_file(path):
    with open(path) as f:
        return read_replace(f.read())


def read_python_file(path, variables=None):
    variables = variables or ['query']
    pattern = '|'.join(re.escape(v) for v in variables)

    with open(path) as f:
        content = f.read()

    # Match a variable assignment (e.g. query = ...), optional f-string,
    # and the string content within matching quotes (single or triple, ' or ").
    regex = re.compile(
        r'(?:\s*(?:'
        + pattern
        + r')\s*=\s*\(?\s*f?)(?P<quote>"{3}|"{1}|\'{3}|\'{1})(?P<content>.*?)(?P=quote)',
        flags=re.DOTALL,
    )

    matches = list(regex.finditer(content))
    # Process matches in reverse order so that replacing content (which might change length)
    # does not invalidate the indices of earlier matches.
    for m in reversed(matches):
        query = m.group('content')
        replaced = read_replace(query)
        content = content[: m.start('content')] + replaced + content[m.end('content') :]

    return content


def read_replace(string):
    for sub in get_regexes():
        string = apply_rule(string, sub)
    return string


def apply_rule(text, rule):
    def replacer(m):
        prefix = text[m.start() : m.start(rule['group'])]
        suffix = text[m.end(rule['group']) : m.end()]
        return prefix + rule['substitute'] + suffix

    return re.sub(rule['regex'], replacer, text, flags=re.IGNORECASE)


@functools.lru_cache(maxsize=1)
def get_regexes():
    rules = []
    with open(f'{DIR}/regexes.txt') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('__')
            rules.append(
                {
                    'substitute': parts[0],
                    'regex': parts[1],
                    'group': int(parts[2]),
                }
            )
    return rules


def command_line_file(args):
    return run_on_files(args.path, args.python_var, dry_run=args.nothing)


if __name__ == '__main__':
    main()
