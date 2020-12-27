# readsql

Convert SQL to most human readable format. For the time being it upper cases SQL keywords, it might prettify of even suggest improvements of SQL code in the future. It converts SQL code and even SQL-strings in programming languages (only Python at the moment).

So if we write

```sql
select sushi, avg(price) from tokyo where ocean = 'pacific' group by sushi
```

readsql will help us read it as

```sql
SELECT sushi, AVG(price) FROM tokyo WHERE ocean = 'pacific' GROUP BY sushi
```

# Installation

`pip install readsql`

# Usage

1. Format SQL code provided in command line
    - `readsql <SQL_STRING> -s`
2. Format an SQL file or folder
    - as in a folder, it will look for files ending with .sql or .py
    - `readsql <FILE_OR_FOLDER_PATH>`

It supports multiple strings and files or folders as well

1.
```bash
readsql <SQL_STRING1> <SQL_STRING2> -s
```

2. In Python files it looks for `query` strings and formats them
```bash
readsql <FILE_OR_FOLDER_PATH1> <FILE_OR_FOLDER_PATH2>
```

We can look for different strings in Python files with `-py` arguments
```bash
readsql <FILE_OR_FOLDER_PATH> -py <PY_VAR1> <PY_VAR2>
```

# Usage examples

1. `readsql 'select sushi from tokyo' -s` command returns
    - `SELECT sushi FROM tokyo`

2. a. `readsql sql_example.sql` command, while `sql_example.sql` is a SQL file with code as below,
```sql
select max(height), avg(mass), min(age) from jungle group by forest where animal=elephant;
```
replaces the file with this code
```sql
SELECT MAX(height), AVG(mass), MIN(age) FROM jungle GROUP BY forest WHERE animal=elephant;
```

2.c. `readsql sql_in_python_variable_example.py` command, while `sql_in_python_variable_example.py` is a Python file with code as below,
```python
def get_query():
    limit = 6
    sql = f"SELEct speed from world where animal='dolphin' limit {limit}"
    return sql
```
replaces the file with this code
```python
def get_query():
    limit = 6
    sql = f"SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}"
    return sql
```

2.c. `readsql sql_in_python_variable_example.py -py sql` command, while `sql_in_python_variable_example.py` is a Python file with code as below,
```python
def get_query():
    limit = 6
    sql = f"SELEct speed from world where animal='dolphin' limit {limit}"
    return sql
```
replaces the file with this code
```python
def get_query():
    limit = 6
    sql = f"SELECT speed FROM world WHERE animal='dolphin' LIMIT {limit}"
    return sql
```

2.d. `readsql tests -n` command outputs all of the formated SQL code in `tests` folder, files are not replaced by the formatted version (`-n` argument stand for not-replace)

# Add a pre-commit hook
How to add a [pre-commit](https://pre-commit.com/) hook of readsql?
```yaml
repos:
-   repo: https://github.com/AzisK/readsql
    rev: 0.1.1 # Replace by any tag/version: https://github.com/azisk/readsql/tags
    hooks:
    -   id: readsql
```

# Development
Having the repo cloned dig into

- `python -m readsql "select sushi from tokyo" -s` takes the `"select sushi from tokyo"` string as input and outputs it formatted
- `python -m readsql tests/sql_example.sql` converts example SQL code to easier readable format
- `python -m readsql tests/sql_in_python_example.py` converts example SQL code in Python (it looks for variables `query`)
- we can change the SQL variable with `-py` option `python -m readsql tests/sql_in_python_variable_example.py -py sql`
- `python -m readsql tests` formats all Python and SQL files in `tests` folder

# Testing

Have `pytest` installed and run `pytest -v` (-v stands for verbose)
