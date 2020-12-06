# readsql

Convert SQL to most human readable format

It can convert SQL code and even SQL strings in other languages (only Python at the moment)

# Installation

`pip install readsql`

# Usage

1. Format SQL code provided in command line
    - `readsql <SQL_STRING> -s`
2. Format an SQL file
    - `readsql <FILE_PATH>`

# Usage examples

1. `readsql <SQL_STRING> -s`
    - `readsql 'select sushi from tokyo' -s`
    - returns `SELECT sushi FROM tokyo`
2. `readsql <FILE_PATH>`
    1. `readsql sql_example.sql`
    2. given a Python file (ends with `.py`), it looks for variables `query` and formats their insides
        - variable to represent SQL code can be changed with `-py` option
        - `readsql sql_in_python_variable_example.py -py sql`
        - given a Python file with this code
```python
def get_query():
    limit = 6
    sql = f"SELEct speed from world where animal='dolphin' limit {limit}"
    return sql
```
converts it to
```python
def get_query():
    limit = 6
    sql = f"SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}"
    return sql
```

# Add a pre-commit hook
How to add a [pre-commit](https://pre-commit.com/) hook of readsql?
```yaml
repos:
-   repo: https://github.com/AzisK/readsql
    rev: 0.0.3-alpha
    hooks:
    -   id: readsql
```

# Development
Having the repo cloned

- `python readsql tests/sql_example.sql` converts example SQL code to easier readable format
- `python readsql tests/sql_in_python_example.py` converts example SQL code in Python (it looks for variables `query`)
- we can change the SQL variable with `-py` option `python readsql tests/sql_in_python_variable_example.py -py sql`
- `python readsql "select sushi from tokyo" -s` takes the `"select sushi from tokyo"` string as input and outputs it formatted

# Testing

Have `pytest` installed and run `pytest -v` (-v stands for verbose)
