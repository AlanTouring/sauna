"""This module is contains helper functions for unit testing."""
import inspect
import io
import unittest
import sys


def check_test_case_number(suite: unittest.suite) -> unittest.suite:
    """This is a test helper function."""
    # pylint: disable=C0122 # comparison should be reveresed
    # but this is more defensive code
    if 0 == suite.countTestCases():
        raise AttributeError
        # pylint: enable=C0122

    return suite


def unreachable_code():
    """This is a test helper function."""
    print_stderr("unreachable code was executed. Error in -->>", end="")
    print_stderr(inspect.stack()[1].function, end="")
    print_stderr("<<")
    raise RuntimeError()


def unreachable_code_2(f_name=""):
    """This is a test helper function."""
    print_stderr(" ERROR in-->>" + f_name + "<<")
    raise RuntimeError()


def do_nothing():
    """This is a test helper function."""


def TBD():
    """This is a test helper function."""


def print_stderr(*args, **kwargs):
    """This is a test helper function."""
    print(*args, file=sys.stderr, **kwargs)


def run_unit_test_suites(suites_list):
    """This is a test helper function."""
    stringio = io.StringIO()
    runner = unittest.TextTestRunner(descriptions=False, stream=stringio, verbosity=0)
    big_suite = unittest.TestSuite(suites_list)
    result = runner.run(big_suite)
    if result.wasSuccessful():
        output = "Number of Tests executed:= "
        output += str(big_suite.countTestCases())
        output += " -- Unit Testing was SUCCESSFUL --"
        print_stderr(output, end='')
    else:
        print_stderr(stringio.getvalue(), end='')


def get_empty_suites_list():
    """This is a test helper function."""
    suites_list = []
    return suites_list
