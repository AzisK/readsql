# -*- coding: utf-8 -*-
from setuptools import setup

packages = ['readsql']

package_data = {'': ['*']}

install_requires = ['argparse>=1.4.0,<2.0.0']

entry_points = {'console_scripts': ['readsql = readsql.__main__:command_line']}

setup_kwargs = {
    'name': 'readsql',
    'version': '0.1.0',
    'description': 'Convert SQL to most human readable format',
    'long_description': '# readsql\n\nConvert SQL to most human readable format\n\nIt can convert SQL code and even SQL strings in other languages (only Python at the moment)\n\n# Installation\n\n`pip install readsql`\n\n# Usage\n\n1. Format SQL code provided in command line\n    - `readsql <SQL_STRING> -s`\n2. Format an SQL file\n    - `readsql <FILE_PATH>`\n\n# Usage examples\n\n1. `readsql <SQL_STRING> -s`\n    - `readsql \'select sushi from tokyo\' -s`\n    - returns `SELECT sushi FROM tokyo`\n2. `readsql <FILE_PATH>`\n    1. `readsql sql_example.sql`\n    2. given a Python file (ends with `.py`), it looks for variables `query` and formats their insides\n        - variable to represent SQL code can be changed with `-py` option\n        - `readsql sql_in_python_variable_example.py -py sql`\n        - given a Python file with this code\n```python\ndef get_query():\n    limit = 6\n    sql = f"SELEct speed from world where animal=\'dolphin\' limit {limit}"\n    return sql\n```\nconverts it to\n```python\ndef get_query():\n    limit = 6\n    sql = f"SELECT speed FROM world WHERE animal=\'dolphin\' LIMIT {limit}"\n    return sql\n```\n\n# Development\nHaving the repo cloned\n\n- `python readsql tests/sql_example.sql` converts example SQL code to easier readable format\n- `python readsql tests/sql_in_python_example.py` converts example SQL code in Python (it looks for variables `query`)\n- we can change the SQL variable with `-py` option `python readsql tests/sql_in_python_variable_example.py -py sql`\n- `python readsql "select sushi from tokyo" -s` takes the `"select sushi from tokyo"` string as input and outputs it formatted\n\n# Testing\n\nHave `pytest` installed and run `pytest -v` (-v stands for verbose)\n',
    'author': 'Azis',
    'author_email': 'azuolas.krusna@yahoo.com',
    'maintainer': 'Azis',
    'maintainer_email': 'azuolas.krusna@yahoo.com',
    'url': 'https://github.com/AzisK/readsql/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
