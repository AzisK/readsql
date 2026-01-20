import argparse
import os

import readsql.__main__ as rsql

DIR = os.path.dirname(__file__)


def check1():
    n1 = DIR + '/sql_example.sql'
    r1 = rsql.read_sql_file(n1)
    with open(n1, 'w') as f:
        f.write(r1)

    n2 = DIR + '/sql_in_python_example.py'
    r2 = rsql.read_python_file(n2)
    with open(n2, 'w') as f:
        f.write(r2)


def check2():
    args = argparse.Namespace(
        nothing=False,
        path=[DIR],
        python_var=['query'],
        string=False,
    )
    rsql.command_line_file(args)


if __name__ == '__main__':
    check1()
    check2()
