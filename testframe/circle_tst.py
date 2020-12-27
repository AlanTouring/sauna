"""This module is an example of unittests, and use of suites."""
import unittest
# pylint: disable=E0401 # impossible import
from testframe.circle import Circle
import testframe.test_util
# pylint: enable=E0401


class CircleTestCase(unittest.TestCase):
    """This class gives examples of test cases."""
    def setUp(self):
        self.circle = Circle()

    def test_get_radius(self):
        """This is a test of a getter function."""
        self.assertAlmostEqual(self.circle.get_radius(), 1, places=2, msg='incorrect getter')

    def test_get_area(self):
        """This is a test of a getter function."""
        self.assertAlmostEqual((self.circle.get_area()), 3.14, places=2, msg='incorrect getter')

    def test_get_outline(self):
        """This is a test of a getter function."""
        self.assertAlmostEqual((self.circle.get_outline()), 2 * 3.14, places=2,
                               msg='incorrect getter')
        # pylint: disable=W1503 # redundant code
        self.assertTrue(True)
        # pylint: enable=W1503

    def tearDown(self):
        pass


def create_test_suite() -> unittest.TestSuite:
    """This is a convenience function to collect all tests of this module."""
    suite = unittest.TestSuite()
    suite.addTest(CircleTestCase('test_get_radius'))
    suite.addTest(CircleTestCase('test_get_area'))
    return suite


def create_2nd_suite() -> unittest.TestSuite:
    """This is a convenience function to collect all tests of this module.
    The idea is to group test cases within one module to improve structure."""
    suite = unittest.TestSuite()
    suite.addTest(CircleTestCase('test_get_area'))
    suite.addTest(CircleTestCase('test_get_outline'))
    return suite


def create_3rd_suite() -> unittest.TestSuite:
    """This is a convenience function to collect all tests of this module.
    The idea is to group test cases within one module to improve structure."""
    suite = unittest.TestSuite()
    suite.addTest(CircleTestCase('test_get_radius'))
    suite.addTest(CircleTestCase('test_get_area'))
    suite.addTest(CircleTestCase('test_get_outline'))
    return suite


def main():
    """This is the main, which sets up and runs all tests of this module."""
    suites_list = testframe.test_util.get_empty_suites_list()
    suites_list.append(create_test_suite())
    suites_list.append(create_2nd_suite())
    suites_list.append(create_3rd_suite())

    testframe.test_util.run_unit_test_suites(suites_list)


if __name__ == '__main__':
    main()
