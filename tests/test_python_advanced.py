import textwrap
from pathlib import Path
import readsql.__main__ as rsql

def test_typed_assignment(tmp_path):
    content = textwrap.dedent("""
        def get_data():
            query: str = "select * from users"
            return query
    """)
    file = tmp_path / "test_typed.py"
    file.write_text(content, encoding="utf-8")
    
    formatted = rsql.read_python_file(file)
    assert 'SELECT * FROM users' in formatted

def test_f_string_preservation(tmp_path):
    content = textwrap.dedent("""
        def get_data(table_name):
            limit = 10
            query = f"select * from {table_name} where id < {limit}"
            return query
    """)
    file = tmp_path / "test_fstring.py"
    file.write_text(content, encoding="utf-8")
    
    formatted = rsql.read_python_file(file)
    expected = 'SELECT * FROM {table_name} WHERE id < {limit}'
    assert expected in formatted
    # Ensure f-string structure remains
    assert 'query = f"' in formatted

def test_nested_scope(tmp_path):
    content = textwrap.dedent("""
        class Repository:
            def get_query(self):
                def internal():
                    query = "select id from items"
                    return query
                return internal()
    """)
    file = tmp_path / "test_scope.py"
    file.write_text(content, encoding="utf-8")
    
    formatted = rsql.read_python_file(file)
    assert 'SELECT id FROM items' in formatted

def test_ignore_docstrings(tmp_path):
    """Docstrings should NOT be formatted even if they contain SQL-like text."""
    content = textwrap.dedent("""
        def func():
            \"\"\"
            select * from ignored
            \"\"\"
            query = "select * from formatted"
            return query
    """)
    file = tmp_path / "test_docstrings.py"
    file.write_text(content, encoding="utf-8")
    
    formatted = rsql.read_python_file(file)
    assert 'select * from ignored' in formatted  # Should NOT change
    assert 'SELECT * FROM formatted' in formatted # Should change

def test_multiple_targets(tmp_path):
    content = textwrap.dedent("""
        def func():
            q1 = q2 = "select x from y"
            return q1
    """)
    file = tmp_path / "test_multi.py"
    # We only look for default var "query", so let's check custom vars
    file.write_text(content, encoding="utf-8")
    
    formatted = rsql.read_python_file(file, variables=['q1', 'q2'])
    assert 'SELECT x FROM y' in formatted
