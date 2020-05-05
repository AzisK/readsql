import os

import readsql.__main__ as rsql

DIR = os.path.dirname(__file__)


def check():
    rsql.read_file(file_name=DIR + '/sql_example.sql')
    rsql.read_python_file(file_name=DIR + '/sql_in_python_example.py')


if __name__ == '__main__':
    check()
