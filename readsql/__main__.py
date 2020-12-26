import os
import re
import functools

from readsql.parse_args import parse_args
from readsql.parse_args import validate

DIR = os.path.dirname(__file__)


def replace(lines, substitution):
    regex = [m for m in re.finditer(substitution['regex'], lines, re.IGNORECASE)]
    for g in regex:
        start = g.start(substitution['group'])
        lines = replace_part_of_string(lines, substitution['substitute'], start)
    return lines


def replace_part_of_string(string, part, start):
    string = string[:start] + part + string[start + len(part) :]
    return string


def write_file(file_name, lines):
    with open(file_name, 'w') as out:
        out.write(lines)


def read_file(file_name, inplace=True):
    with open(file_name, 'r') as inp:
        lines = inp.read()

    lines = read(lines)

    if not inplace:
        return lines

    write_file(file_name, lines)


def read_python_file(file_name, variables=None, inplace=True):
    variables = variables if variables else ['query']
    variables_regex = (
        f"(?:{'|'.join(variables)})" if len(variables) > 1 else variables[0]
    )

    with open(file_name, 'r') as inp:
        lines = inp.read()

    regex = [
        m
        for m in re.finditer(
            r'(?:\s*'
            + variables_regex
            + r'\s*=\s*\(?\s*f?)(?:"{1,3}|\'{1,3})([^"]*)(:?"|\')',
            lines,
        )
    ]

    for g in regex:
        query = lines[g.start(1) : g.end(1)]

        query = read(query)

        lines = replace_part_of_string(lines, query, g.start(1))

    if not inplace:
        return lines

    write_file(file_name, lines)


def read(string):
    for sub in read_regexes():
        string = replace(string, sub)

    return string


@functools.lru_cache(maxsize=1)
def read_regexes():
    file_name = f'{DIR}/regexes.txt'

    rules = []

    with open(file_name, 'r') as inp:
        for line in inp:
            if line.startswith('#') or not line.strip():
                continue

            regex_line = line.split('__')
            regex_dict = {
                'substitute': regex_line[0],
                'regex': regex_line[1],
                'group': int(regex_line[2]),
            }

            rules.append(regex_dict)

    return rules


def command_line_file(args):
    validate(args)
    aggregate = []

    for path in args.path:
        if path.endswith('.py'):
            lines = read_python_file(path, args.python_var, inplace=False)
        elif path.endswith('.sql'):
            lines = read_file(path, inplace=False)
        else:
            print('No SQL or Python files were provided')
            return

        if args.nothing:
            print(f'{path} would be reformatted to:\n', lines)
            aggregate.append(lines)
        else:
            print(f'{path} has been reformatted to:\n', lines)

            write_file(path, lines)

    if args.nothing:
        return aggregate


def command_line():
    args = parse_args()
    if args.string:
        print('\n'.join([read(p) + '\n' for p in args.path]))
    else:
        command_line_file(args)


if __name__ == '__main__':
    command_line()
