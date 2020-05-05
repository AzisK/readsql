# readsql

Convert SQL to most human readable format

# Usage

- `python readsql tests/sql_example.sql` converts example SQL code to easier readable format
- `python readsql "select gold from mine" -s` takes the `"select gold from mine"` string as input and outputs it formatted

# Testing

Have `pytest` installed and run `pytest -v` (-v stands for verbose)
