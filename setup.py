# -*- coding: utf-8 -*-
import pathlib

from setuptools import setup

packages = ['readsql']

package_data = {'': ['*']}

install_requires = ['argparse>=1.4.0,<2.0.0']

entry_points = {'console_scripts': ['readsql = readsql.__main__:command_line']}

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup_kwargs = {
    'name': 'readsql',
    # 'version': 'version is specified in poetry.toml',
    'description': 'Convert SQL to most human readable format',
    'long_description': 'README',
    'long_description_content_type': "text/markdown",
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
