import argparse
import os

import readsql.__main__ as rsql
from tests.timing import timing

DIR = os.path.dirname(__file__)


def test_read_file_wrap():
    @timing
    def test_read_file():
        return rsql.read_file(file_name=DIR + '/sql_example.sql', inplace=False)

    example = test_read_file()
    with open(DIR + '/sql_example_correct.sql', 'r') as inp:
        assert inp.read() == example


def test_read_python_file_wrap():
    @timing
    def test_read_python_file():
        return rsql.read_python_file(
            file_name=DIR + '/sql_in_python_example.py', inplace=False
        )

    example = test_read_python_file()
    with open(DIR + '/sql_in_python_example_correct.py', 'r') as inp:
        assert inp.read() == example


def test_read_python_file_variable_wrap():
    @timing
    def test_read_python_file(variable):
        return rsql.read_python_file(
            file_name=DIR + '/sql_in_python_variable_example.py',
            variables=variable,
            inplace=False,
        )

    example = test_read_python_file(variable=['sql'])
    with open(DIR + '/sql_in_python_variable_example_correct.py', 'r') as inp:
        assert inp.read() == example


def test_read_python_file_variables_wrap():
    @timing
    def test_read_python_file(variable):
        return rsql.read_python_file(
            file_name=DIR + '/sql_in_python_variables_example.py',
            variables=variable,
            inplace=False,
        )

    example = test_read_python_file(variable=['sql', 'query_template', 'query'])
    with open(DIR + '/sql_in_python_variables_example_correct.py', 'r') as inp:
        assert inp.read() == example


def test_read_python_multifile_wrap():
    args = argparse.Namespace(
        nothing=True,
        path=[
            DIR + '/sql_in_python_multifile1_example.py',
            DIR + '/sql_in_python_multifile2_example.py',
        ],
        python_var=['query'],
        string=False,
    )

    @timing
    def test_read_python_multifile():
        return rsql.command_line_file(args)

    example = test_read_python_multifile()
    corrects = [
        DIR + '/sql_in_python_multifile1_example_correct.py',
        DIR + '/sql_in_python_multifile2_example_correct.py',
    ]
    aggregate = []
    for file in corrects:
        with open(file, 'r') as inp:
            aggregate.append(inp.read())
    assert str(aggregate) == str(example)
