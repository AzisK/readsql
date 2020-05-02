import re


SELECT_SUBSTITUTION = {
    'regex': r'(?:^|\s|\()(select)(?:\s)',
    'group': 1,
    'substitute': 'SELECT',
}
FROM_SUBSTITUTION = {'regex': r'(?:\s)(from)(?:\s)', 'group': 1, 'substitute': 'FROM'}
WHERE_SUBSTITUTION = {
    'regex': r'(?:\s)(where)(?:\s)',
    'group': 1,
    'substitute': 'WHERE',
}
AS_SUBSTITUTION = {'regex': r'(?:\s)(as)(?:\s)', 'group': 1, 'substitute': 'AS'}
IS_SUBSTITUTION = {'regex': r'(?:\s)(is)(?:\s)', 'group': 1, 'substitute': 'IS'}
NOT_SUBSTITUTION = {'regex': r'(?:\s)(not)(?:\s)', 'group': 1, 'substitute': 'NOT'}
NULL_SUBSTITUTION = {
    'regex': r'(?:\s)(null)(?:\s|;|\))',
    'group': 1,
    'substitute': 'NULL',
}
SUM_SUBSTITUTION = {'regex': r'(?:\s)(sum)(?:\()', 'group': 1, 'substitute': 'SUM'}
COUNT_SUBSTITUTION = {
    'regex': r'(?:\s)(count)(?:\()',
    'group': 1,
    'substitute': 'COUNT',
}
DISTINCT_SUBSTITUTION = {
    'regex': r'(?:\s)(distinct)(?:\s)',
    'group': 1,
    'substitute': 'DISTINCT',
}
GROUP_SUBSTITUTION = {
    'regex': r'(?:\s)(group)(?:\s)',
    'group': 1,
    'substitute': 'GROUP',
}
BY_SUBSTITUTION = {'regex': r'(?:\s)(by)(?:\s)', 'group': 1, 'substitute': 'BY'}
CREATE_SUBSTITUTION = {
    'regex': r'(?:^|\s|\()(create)(?:\s)',
    'group': 1,
    'substitute': 'CREATE',
}
TABLE_SUBSTITUTION = {
    'regex': r'(?:\s)(table)(?:\s)',
    'group': 1,
    'substitute': 'TABLE',
}
IF_SUBSTITUTION = {'regex': r'(?:\s)(if)(?:\s)', 'group': 1, 'substitute': 'IF'}
EXISTS_SUBSTITUTION = {
    'regex': r'(?:\s)(exists)(?:\s)',
    'group': 1,
    'substitute': 'EXISTS',
}


file_name = 'sql_example.sql'


def replace(lines, substitution):
    regex = [m for m in re.finditer(substitution['regex'], lines, re.IGNORECASE)]
    if regex:
        for g in regex:
            start = g.start(substitution['group'])
            lines = (
                lines[:start]
                + substitution['substitute']
                + lines[start + len(substitution['substitute']) :]
            )
    return lines


def read(file_name):
    with open(file_name, 'r') as inp:
        lines = inp.read()

        for sub in [
            SELECT_SUBSTITUTION,
            FROM_SUBSTITUTION,
            WHERE_SUBSTITUTION,
            AS_SUBSTITUTION,
            IS_SUBSTITUTION,
            NOT_SUBSTITUTION,
            NULL_SUBSTITUTION,
            SUM_SUBSTITUTION,
            COUNT_SUBSTITUTION,
            DISTINCT_SUBSTITUTION,
            GROUP_SUBSTITUTION,
            BY_SUBSTITUTION,
            CREATE_SUBSTITUTION,
            TABLE_SUBSTITUTION,
            IF_SUBSTITUTION,
            EXISTS_SUBSTITUTION,
        ]:
            lines = replace(lines, sub)

        with open(file_name, 'w') as out:
            out.write(lines)


if __name__ == "__main__":
    read(file_name)
