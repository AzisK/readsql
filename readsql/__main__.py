import os
import re

from readsql.parse_args import validate, parse_args

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


def read_file(file_name, inplace=True):
    with open(file_name, 'r') as inp:
        lines = inp.read()

        for sub in read_regexes():
            lines = replace(lines, sub)

        if not inplace:
            return lines

        with open(file_name, 'w') as out:
            out.write(lines)


def read_python_file(file_name='tests/sql_in_python_example.py', inplace=True):

    with open(file_name, 'r') as inp:
        lines = inp.read()
        subs = []

        regex = [
            m
            for m in re.finditer(
                r'(?:\s*query\s*=\s*f?)(?:"{1,3}|\'{1,3})([^"]*)(:?"|\')', lines
            )
        ]
        if regex:
            subs = read_regexes()
        for g in regex:
            query = lines[g.start(1) : g.end(1)]

            for sub in subs:
                query = replace(query, sub)

            lines = replace_part_of_string(lines, query, g.start(1))

        if not inplace:
            return lines

        with open(file_name, 'w') as out:
            out.write(lines)


def read(string):
    for sub in read_regexes():
        string = replace(string, sub)

    return string


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
    lines = read_file(args.path, inplace=False)

    print(f'{args.path} has been reformatted to:\n', lines)

    with open(args.path, 'w') as out:
        out.write(lines)


def command_line():
    args = parse_args()
    if args.string:
        print(read(args.path))
    else:
        command_line_file(args)


if __name__ == '__main__':
    command_line()
