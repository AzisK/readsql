import app
from tests.timing import timing


@timing
def test_read_file():
    app.read_file()


@timing
def test_read_python_file():
    app.read_python_file()
