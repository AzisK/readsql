import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        prog='readsql', description='Convert SQL to most human readable format'
    )
    parser.add_argument('path', nargs='+', help='Path to the file to be converted')
    parser.add_argument('-s', '--string', action='store_true', help='Read a string')
    parser.add_argument(
        '-n', '--nothing', action='store_true', help='Do nothing to the file'
    )
    parser.add_argument(
        '-py',
        '--python_var',
        nargs='+',
        default=['query'],
        help='Look for certain variables in a Python file (default variable is query)',
    )

    args = parser.parse_args()

    return args


def validate(paths):
    for path in paths:
        if not os.path.isfile(path) and not os.path.isdir(path):
            print('The specified path does not exist')
            sys.exit()