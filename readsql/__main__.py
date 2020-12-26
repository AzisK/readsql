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


def read_file(file_name, variables):
    if file_name.endswith('.py'):
        return read_python_file(file_name, variables)
    elif file_name.endswith('.sql'):
        return read_sql_file(file_name)
    else:
        print(f'{file_name} is not an SQL or Python file')
        return


def read_sql_file(file_name):
    with open(file_name, 'r') as inp:
        lines = inp.read()

    return read_replace(lines)


def read_python_file(file_name, variables=None):
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
        query = read_replace(query)
        lines = replace_part_of_string(lines, query, g.start(1))

    return lines


def read_replace(string):
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


def get_message(path, replaces):
    if replaces:
        return f'{path} has been reformatted to:\n'
    return f'{path} would be reformatted to:\n'


def format_files(files, variables, replaces=True):
    lines_list = []

    for path in files:
        lines = read_file(path, variables)
        if not lines:
            continue

        if replaces:
            write_file(path, lines)
        else:
            lines_list.append(lines)

        message = get_message(path, replaces)
        print(message, lines)

    return lines_list


def read_all_files_into(paths, files_list):
    for path in paths:
        if path.startswith('.'):
            continue
        if os.path.isdir(path):
            dir_files = [os.path.join(path, file) for file in os.listdir(path)]
            read_all_files_into(dir_files, files_list)
        elif os.path.isfile(path):
            files_list.append(path)


def get_all_files(paths):
    files_list = []
    read_all_files_into(paths, files_list)
    return files_list


def command_line_file(args):
    paths = args.path
    validate(paths)
    files = get_all_files(paths)
    return format_files(files, args.python_var, not args.nothing)


def command_line():
    args = parse_args()
    if args.string:
        print('\n'.join([read_replace(p) + '\n' for p in args.path]))
    else:
        command_line_file(args)


if __name__ == '__main__':
    command_line()
