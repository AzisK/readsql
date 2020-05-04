import os
import sys

import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog='readsql', description='Convert SQL to most human readable format'
    )
    parser.add_argument('path', type=str, help='Path to the file to be converted')
    parser.add_argument('-s', '--string', action='store_true', help='Read a string')

    args = parser.parse_args()

    return args


def validate(args):
    path = args.path
    if not os.path.isfile(path):
        print('The file path specified does not exist')
        sys.exit()
