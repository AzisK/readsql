import readsql.__main__ as rsql
from tests.timing import timing
import os


DIR = os.path.dirname(__file__)


def test_read_file_wrap():
    @timing
    def test_read_file():
        return rsql.read_file(inplace=False)

    example = test_read_file()
    with open(DIR + '/sql_example_correct.sql', 'r') as inp:
        assert inp.read() == example


def test_read_python_file_wrap():
    @timing
    def test_read_python_file():
        return rsql.read_python_file(inplace=False)

    example = test_read_python_file()
    with open(DIR + '/sql_in_python_example_correct.py', 'r') as inp:
        assert inp.read() == example
