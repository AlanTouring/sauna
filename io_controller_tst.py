"""This module is an example of unittests, and use of suites."""
import inspect
import unittest

# pylint: disable=E0401 # impossible import
import io_port
import testframe.test_util
# pylint: enable=E0401
from io_controller import IO_Controller
from testframe.test_util import do_nothing
from testframe.test_util import unreachable_code_2


class IOControllerTestCase(unittest.TestCase):
    """This class test the IO_Controller module."""

    def setUp(self):
        pass

    def test_add_port(self):
        """This is a test of a add function."""
        control = IO_Controller()
        port = io_port.DigitalPort(2, port_type=io_port.PORT_IS_WRITEABLE)
        light_switch = "Light Switch"

        control.addPort(port, light_switch)
        value = control.getPortValue(light_switch)
        self.assertEqual(value, 0, msg='incorrect getter')
        control.setPortValue(light_switch)
        value = control.getPortValue(light_switch)
        self.assertEqual(value, 1, msg='incorrect getter')

    def test_create_port_1(self):
        """This is a test of a create function."""
        control = IO_Controller()
        port_type = io_port.PORT_IS_WRITEABLE
        port_num = 2
        pi_name = 'pi222'
        light_switch = "Light Switch"
        control.createPort(port_num, port_type, light_switch, pi_name)
        value = control.getPortValue(light_switch)
        self.assertEqual(value, 0)
        control.setPortValue(light_switch)
        value = control.getPortValue(light_switch)
        self.assertEqual(value, 1)

    def test_create_port_2(self):
        """This is a test of a create function."""
        control = IO_Controller()
        port_rw = io_port.PORT_IS_WRITEABLE
        port_r = io_port.PORT_IS_READ_ONLY
        pi_name = 'pi222'
        control.createPort(2, port_rw, "1", pi_name)
        control.createPort(3, port_rw, "2", pi_name)
        control.createPort(4, port_rw, "3", pi_name)
        control.createPort(7, port_rw, "4", pi_name)
        control.createPort(8, port_r, "5", pi_name)
        control.createPort(9, port_rw, "6", pi_name)

        self.assertEqual(control.getPortValue("1"), 0)
        control.setPortValue("1")
        control.setPortValue("4")
        control.setPortValue("6")
        self.assertEqual(control.getPortValue("1"), 1)
        self.assertEqual(control.getPortValue("4"), 1)
        self.assertEqual(control.getPortValue("6"), 1)
        control.resetPortValue("4")
        self.assertEqual(control.getPortValue("4"), 0)
        control.setPortValue("4")
        self.assertEqual(control.getPortValue("4"), 1)
        try:
            control.setPortValue("5")
            unreachable_code_2(str(inspect.stack()[0].function))
        except ValueError:
            do_nothing()

    def test_create_port_3(self):
        """This is a test of a create function."""
        control = IO_Controller()
        port_rw = io_port.PORT_IS_WRITEABLE
        port_r = io_port.PORT_IS_READ_ONLY
        pi_name = 'pi222'
        control.createPort(2, port_rw, "1", pi_name)
        control.createPort(3, port_rw, "2", pi_name)
        control.createPort(4, port_r, "3", pi_name)

        control.setPortValue("1")
        control.resetPortValue("2")

        control.togglePortValue("1")
        control.togglePortValue("2")
        self.assertEqual(control.getPortValue("1"), 1)
        self.assertEqual(control.getPortValue("2"), 0)

        try:
            control.togglePortValue("3")
            unreachable_code_2(str(inspect.stack()[0].function))
        except ValueError:
            do_nothing()

    def test_create_port_4(self):
        """This is a test of a create function."""
        control = IO_Controller()
        port_type = io_port.PORT_IS_ANALOG_READ_ONLY
        pi_name = 'pi222'

        control.createPort(4, port_type, "3", pi_name)
        self.assertGreaterEqual(control.getPortValue("3"), -10.0)
        self.assertLessEqual(control.getPortValue("3"), 100.0)

    def tearDown(self):
        pass


def create_test_suite() -> unittest.TestSuite:
    """This is a convenience function to collect all tests of this module."""
    suite = unittest.TestSuite()
    suite.addTest(IOControllerTestCase('test_add_port'))
    suite.addTest(IOControllerTestCase('test_create_port_1'))
    suite.addTest(IOControllerTestCase('test_create_port_2'))
    suite.addTest(IOControllerTestCase('test_create_port_3'))
    suite.addTest(IOControllerTestCase('test_create_port_4'))
    # TODO more tests for Analog Ports
    # TODO are callbacks required
    return suite


def main():
    """This is the main, which sets up and runs all tests of this module."""
    suites_list = testframe.test_util.get_empty_suites_list()
    suites_list.append(create_test_suite())

    testframe.test_util.run_unit_test_suites(suites_list)


if __name__ == '__main__':
    main()
