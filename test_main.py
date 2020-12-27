"""This module contains the top level function for all unit tests."""
import io_controller_tst
import io_port_tst
import sauna_tst
from testexamples import example_tst
from testframe import circle_tst
from testframe.test_util import get_empty_suites_list, check_test_case_number, run_unit_test_suites


def execute_main():
    """This is the main function, which sets up and runs all tests of ALL modules."""
    suites_list = get_empty_suites_list()

    # pylint: disable=W0511 # This following comment is not an error
    # TODO -- create and append your new test suite here
    # pylint: enable=W0511
    # these 2 test suites are simple examples
    suites_list.append(check_test_case_number(circle_tst.create_test_suite()))
    suites_list.append(check_test_case_number(example_tst.create_test_suite()))
    suites_list.append(check_test_case_number(io_port_tst.create_test_suite()))
    #suites_list.append(check_test_case_number(sauna_tst.create_test_suite()))
    #TODO wahrscheinlich kann man nur zu eimal zu einem pi connecten
    # fixme implementierung ändern
    suites_list.append(check_test_case_number(io_controller_tst.create_test_suite()))

    run_unit_test_suites(suites_list)


if __name__ == '__main__':
    execute_main()
