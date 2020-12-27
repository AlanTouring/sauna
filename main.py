"""This module is the root script for my Python projects."""
from test_main import execute_main
from testframe.test_util import print_stderr


def print_hi(name: object):
    """This function just print a greeting."""

    print_stderr(f'Hi, {name} --- ', end='')


if __name__ == '__main__':
    print_hi('Py charms')
    execute_main()
    # pylint: disable=W0511 # This following comment is not an error
    # TODO -- create and append new function calls here
    # pylint: enable=W0511
