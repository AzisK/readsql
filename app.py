import re


file_name = 'sql_example.sql'


def replace(lines, substitution):
    regex = [m for m in re.finditer(substitution['regex'], lines, re.IGNORECASE)]
    for g in regex:
        start = g.start(substitution['group'])
        lines = (
            lines[:start]
            + substitution['substitute']
            + lines[start + len(substitution['substitute']) :]
        )
    return lines


def read_file(file_name):
    with open(file_name, 'r') as inp:
        lines = inp.read()

        for sub in read_regexes():
            lines = replace(lines, sub)

        with open(file_name, 'w') as out:
            out.write(lines)

def read(string):
    for sub in read_regexes():
        string = replace(string, sub)
    return string

def read_regexes():
    file_name = 'regexes.txt'

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

if __name__ == '__main__':
    read_file(file_name)
