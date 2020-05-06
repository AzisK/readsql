# readsql

Convert SQL to most human readable format

# Installation 

`pip install readsql`

# Usage

- Format SQL code provided in command line
    - `readsql <SQL_STRING> -s`
    - e.g., `readsql 'select sushi from tokyo' -s`
    - prints out `SELECT sushi FROM tokyo`
- Format an SQL file 
    - `readsql <FILE_PATH>` 
    - e.g., `readsql sql_example.sql`
    - given a Python file (ends with `.py`), it looks for variables `query` and formats their insides
    - variable to represent SQL code can be change with `-py` option
    - e.g., `readsql sql_in_python_variable_example.py -py sql`
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

# Development
Having the repo cloned

- `python readsql tests/sql_example.sql` converts example SQL code to easier readable format
- `python readsql tests/sql_in_python_example.py` converts example SQL code in Python (it looks for variables `query`)
- we can change the SQL variable with `-py` option `python readsql tests/sql_in_python_variable_example.py -py sql` 
- `python readsql "select gold from mine" -s` takes the `"select gold from mine"` string as input and outputs it formatted

# Testing

Have `pytest` installed and run `pytest -v` (-v stands for verbose)
