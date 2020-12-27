"""This module is an example of unittests, and use of suites."""
import unittest
# pylint: disable=E0401 # impossible import
import testexamples.example
import testframe.test_util
# pylint: enable=E0401


class ExampleTestCase(unittest.TestCase):
    """This class gives examples of test cases."""

    def setUp(self):
        self.example = testexamples.example.Example()

    def test_get_value(self):
        """This is a test of a getter function."""
        self.assertAlmostEqual(self.example.get_value(), 4, places=2, msg='incorrect getter')
        # pylint: disable=W1503 # redundant code
        self.assertTrue(True)
        # pylint: enable=W1503

    def tearDown(self):
        pass


def create_test_suite() -> unittest.TestSuite:
    """This is a convenience function to collect all tests of this module."""
    suite = unittest.TestSuite()
    # If you copy this example, you should add her all testcases of this module
    suite.addTest(ExampleTestCase('test_get_value'))
    return suite


def main():
    """This is the main, which sets up and runs all tests of this module."""
    suites_list = testframe.test_util.get_empty_suites_list()
    suites_list.append(create_test_suite())

    testframe.test_util.run_unit_test_suites(suites_list)


if __name__ == '__main__':
    main()
