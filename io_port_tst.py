"""This module contains unit tests."""
import inspect
import unittest

import pigpio

import io_port
import tools
from testframe.test_util import do_nothing
from testframe.test_util import get_empty_suites_list
from testframe.test_util import run_unit_test_suites
from testframe.test_util import unreachable_code
from testframe.test_util import unreachable_code_2
from tools import determine_hardware_and_os_environment, is_pi_available, init_pi_check, close_pi_check, \
    add_test_to_skip_list


class IPPortTestCase(unittest.TestCase):
    """This class contains test cases for:

    - DigitalPort"""

    def assert_low(self, port: io_port.DigitalPort):
        """This is a helper function in this test case."""
        self.assertTrue(port.is_low())

    def assert_high(self, port: io_port.DigitalPort):
        """This is a helper function in this test case."""
        self.assertTrue(port.is_high())

    def test_digital_port_test_1(self):
        """This is a test case.

        default -> low -> high -> low"""
        port = io_port.DigitalPort(1017)
        self.assert_low(port)
        port.set_low()
        self.assert_low(port)
        port.set_high()
        self.assert_high(port)
        port.set_low()
        self.assert_low(port)

    def test_digital_port_test_2(self):
        """This is a test case.

        high -> low/high -> low -> high/low"""
        port = io_port.DigitalPort(1017)
        port.set_high()
        self.assert_high(port)
        port.toggle()
        self.assert_high(port)
        port.set_low()
        self.assert_low(port)
        port.toggle()
        self.assert_low(port)

    def test_digital_port_test_3(self):
        """This is a test case to test exceptions."""
        port = io_port.DigitalPort(1017, io_port.PORT_IS_READ_ONLY)
        self.assert_low(port)
        try:
            port.set_low()
            unreachable_code()
            unreachable_code_2(str(inspect.stack()[0].function))

        except ValueError:
            do_nothing()

        self.assert_low(port)

        try:
            port.set_high()
            unreachable_code()
            unreachable_code_2(str(inspect.stack()[0].function))
        except ValueError:
            do_nothing()

        self.assert_low(port)

        # trick: modify internal variable in order to test special state
        port.state = io_port.PORT_STATE_HIGH
        self.assert_high(port)
        try:
            port.set_low()
            unreachable_code()
            unreachable_code_2(str(inspect.stack()[0].function))
        except ValueError:
            do_nothing()

        self.assert_high(port)

    def test_digital_port_test_4(self):
        """This is a test case to test exceptions."""
        port = io_port.DigitalPort(1017, io_port.PORT_IS_READ_ONLY)
        try:
            port.toggle()
            unreachable_code()
            unreachable_code_2(str(inspect.stack()[0].function))
        except ValueError:
            do_nothing()

    def test_digital_port_test_5(self):
        """This is a test case to test exceptions."""
        port = io_port.DigitalPort(1017, io_port.PORT_IS_READ_ONLY)

        try:
            # trick: modify internal variable in order to test special state
            # trick the class to test a toggle from high to low/high
            port.state = io_port.PORT_STATE_HIGH

            port.toggle()
            unreachable_code()
            unreachable_code_2(str(inspect.stack()[0].function))
        except ValueError:
            do_nothing()

    def test_pig_pio_test_0(self):
        """This is a test case to test the actual io interface."""
        if not is_pi_available():
            add_test_to_skip_list()
            return

        pi = pigpio.pi('pi222', show_errors=True)
        self.assertTrue(pi.connected)

        # User GPIO 2-4, 7-11, 14-15, 17-18, 22-25, 27-31.
        # for Pi Type 2 Model B Rev 2
        # I split the port into a arbitrary number
        ports_w = [2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 17]
        ports_r = [18, 22, 23, 24, 25, 27, 28, 29, 30, 31]

        for port in ports_w:
            pi.set_mode(port, pigpio.OUTPUT)

        for port in ports_w:
            if pi.get_mode(gpio=port) == pigpio.OUTPUT:
                pi.write(port, 0)
                self.assertEqual(0, pi.read(port))
                pi.write(port, 1)
                self.assertEqual(1, pi.read(port))
                pi.write(port, 0)
                self.assertEqual(0, pi.read(port))

        for port in ports_r:
            pi.set_mode(port, pigpio.INPUT)

        for port in ports_r:
            if pi.get_mode(gpio=port) == pigpio.INPUT:
                result = pi.read(port)
                do_nothing()  # to test read value of a readonly port you new a hw trigger

    def test_pig_pio_test_1(self):
        """This is a test case.

        default -> low -> high -> low"""
        if not is_pi_available():
            add_test_to_skip_list()
            return

        port = io_port.DigitalPort(2)
        self.assert_low(port)
        port.set_low()
        self.assert_low(port)
        port.set_high()
        self.assert_high(port)
        port.set_low()
        self.assert_low(port)
        port30 = io_port.DigitalPort(30)
        port30.set_low()
        port30.set_high()
        port30.set_low()

    def test_pig_pio_test_2(self):
        """This is a test case.

        high -> low/high -> low -> high/low"""
        if not is_pi_available():
            add_test_to_skip_list()
            return
        port = io_port.DigitalPort(4)
        port.set_high()
        self.assert_high(port)
        port.toggle()
        self.assert_high(port)
        port.set_low()
        self.assert_low(port)
        port.toggle()
        self.assert_low(port)
        port30 = io_port.DigitalPort(30)
        port30.set_low()
        port30.set_high()
        port30.set_low()

    def test_pig_pio_test_3(self):
        """This is a test case to test exceptions."""
        if not is_pi_available():
            add_test_to_skip_list()
            return

        port = io_port.DigitalPort(9, io_port.PORT_IS_READ_ONLY)
        self.assert_low(port)
        try:
            port.set_low()
            unreachable_code()

        except ValueError:
            do_nothing()

        self.assert_low(port)

        try:
            port.set_high()
            unreachable_code()
        except ValueError:
            do_nothing()

        self.assert_low(port)

    def test_analog_gpio_test_1(self):
        """This is a test case for an analog senor using 1 wire protocol."""
        if not is_pi_available():
            add_test_to_skip_list()
            return

        my_pi = pigpio.pi('pi222', show_errors=True)
        port = io_port.AnalogPort(2, "Temperature Port", io_port.do_nothing, my_pi)
        port.upper_limit = 75
        port.lower_limit = 70
        self.assertGreater(port.get_value(), -20)
        self.assertLess(port.get_value(), 100)
        self.assertFalse(port.need_heating())


    def test_analog_gpio_test_2(self):
        """This is a test case for an analog senor using 1 wire protocol."""
        if not is_pi_available():
            add_test_to_skip_list()
            return

        my_pi = pigpio.pi('pi222', show_errors=True)
        port = io_port.AnalogPort(2, "Temperature Port", io_port.do_nothing, my_pi)
        # a valid file sensor data file must be in that directory
        sensor_data_file_path = "/home/pi/sauna/w1_slave/*.txt"
        values = port.get_values_2(sensor_data_file_path)
        print("temp values are:=" + str(values))

    def test_analog_gpio_test_3(self):
        pass


def create_test_suite() -> unittest.TestSuite:
    """This is a convenience function to collect all tests of this module."""
    suite = unittest.TestSuite()
    suite.addTest(IPPortTestCase('test_digital_port_test_1'))
    suite.addTest(IPPortTestCase('test_digital_port_test_2'))
    suite.addTest(IPPortTestCase('test_digital_port_test_3'))
    suite.addTest(IPPortTestCase('test_digital_port_test_4'))
    suite.addTest(IPPortTestCase('test_digital_port_test_5'))
    suite.addTest(IPPortTestCase('test_pig_pio_test_1'))
    suite.addTest(IPPortTestCase('test_pig_pio_test_2'))
    suite.addTest(IPPortTestCase('test_pig_pio_test_3'))
    # TODO
    suite.addTest(IPPortTestCase('test_pig_pio_test_0'))  # braucht was länger
    suite.addTest(IPPortTestCase('test_analog_gpio_test_1'))
    suite.addTest(IPPortTestCase('test_analog_gpio_test_2'))
    suite.addTest(IPPortTestCase('test_analog_gpio_test_3'))
    return suite


def main():
    """This is the main, which sets up and runs all tests of this module."""
    init_pi_check()

    suites_list = get_empty_suites_list()
    suites_list.append(create_test_suite())
    run_unit_test_suites(suites_list)

    close_pi_check()


if __name__ == '__main__':
    determine_hardware_and_os_environment()
    main()
