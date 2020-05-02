import re


SELECT_SUBTITUTION = {
    'regex': r'(?:^|\s|\()(select)',
    'group': 1,
    'substitute': 'SELECT',
}
FROM_SUBTITUTION = {'regex': r'(?:\s)(from)', 'group': 1, 'substitute': 'FROM'}
WHERE_SUBTITUTION = {'regex': r'(?:\s)(where)', 'group': 1, 'substitute': 'WHERE'}
AS_SUBTITUTION = {'regex': r'(?:\s)(as)(?:\s)', 'group': 1, 'substitute': 'AS'}
IS_SUBTITUTION = {'regex': r'(?:\s)(is)(?:\s)', 'group': 1, 'substitute': 'IS'}
NOT_SUBTITUTION = {'regex': r'(?:\s)(not)(?:\s)', 'group': 1, 'substitute': 'NOT'}
NULL_SUBTITUTION = {'regex': r'(?:\s)(null)(?:\s|;)', 'group': 1, 'substitute': 'NULL'}

file_name = 'sql_example.sql'


def replace(lines, substitution):
    regex = [m for m in re.finditer(substitution['regex'], lines, re.IGNORECASE)]
    if regex:
        for g in regex:
            lines = (
                lines[: g.start(substitution['group'])]
                + substitution['substitute']
                + lines[
                    g.start(substitution['group']) + len(substitution['substitute']) :
                ]
            )
    return lines


with open(file_name, 'r') as inp:
    lines = inp.read()

    for sub in [
        SELECT_SUBTITUTION,
        FROM_SUBTITUTION,
        WHERE_SUBTITUTION,
        AS_SUBTITUTION,
        IS_SUBTITUTION,
        NOT_SUBTITUTION,
        NULL_SUBTITUTION,
    ]:
        lines = replace(lines, sub)

    with open(file_name, 'w') as out:
        out.write(lines)
