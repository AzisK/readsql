import os
from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        timing_string = f'func:{f.__name__}__var:({args, kw})__took: {te-ts:2.6f} sec'
        print(timing_string)

        is_function = False

        new_lines = []

        speed_file = os.path.dirname(__file__) + '/speed.txt'

        if os.path.isfile(speed_file):
            with open(speed_file, 'r') as inp:
                for line in inp:
                    if not line.strip():
                        continue
                    if line.startswith(f'func:{f.__name__}__var:({args, kw})__'):
                        is_function = True
                        new_lines.append(timing_string)
                    else:
                        new_lines.append(line)

        if not is_function:
            new_lines.append(timing_string)

        file_write_lines(speed_file, new_lines)

        return result

    return wrap


def file_write_lines(file_name, lines):
    with open(file_name, 'w') as out:
        for line in lines:
            out.write(f'{line}\n')
