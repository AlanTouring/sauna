"""This module contains unit tests."""
import unittest
import pigpio
import io_port
import pi_util
from testframe.test_util import do_nothing
from testframe.test_util import get_empty_suites_list
from testframe.test_util import run_unit_test_suites
from testframe.test_util import unreachable_code
from tools import determine_hardware_and_os_environment, \
    is_pi_gpio_d_available, \
    init_pi_gpio_d, close_pi_gpio_d_check, \
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
        # high port numbers do not use real pi
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
        # high port numbers do not use real pi
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
        # high port numbers do not use real pi
        port = io_port.DigitalPort(1017, io_port.PORT_IS_READ_ONLY)
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

        # trick: modify internal variable in order to test special state
        port.state = io_port.PORT_STATE_HIGH
        self.assert_high(port)
        try:
            port.set_low()
            unreachable_code()
        except ValueError:
            do_nothing()

        self.assert_high(port)

    def test_digital_port_test_4(self):
        """This is a test case to test exceptions."""
        # high port numbers do not use real pi
        port = io_port.DigitalPort(1017, io_port.PORT_IS_READ_ONLY)
        try:
            port.toggle()
            unreachable_code()
        except ValueError:
            do_nothing()

    def test_digital_port_test_5(self):
        """This is a test case to test exceptions."""
        # high port numbers do not use real pi
        port = io_port.DigitalPort(1017, io_port.PORT_IS_READ_ONLY)

        try:
            # trick: modify internal variable in order to test special state
            # trick the class to test a toggle from high to low/high
            port.state = io_port.PORT_STATE_HIGH

            port.toggle()
            unreachable_code()
        except ValueError:
            do_nothing()

    def test_pig_pio_test_0(self):
        """This is a test case to test the actual io interface."""
        if not is_pi_gpio_d_available():
            add_test_to_skip_list()
            return

        pi = pigpio.pi(test_pi_address[0], show_errors=True)
        self.assertTrue(pi.connected)

        # see pi_util for different pin outs on different raspberry
        ports = pi_util.pi1_single_use_ports

        for port in ports:
            pi.set_mode(port, pigpio.OUTPUT)

        for port in ports:
            if pi.get_mode(gpio=port) == pigpio.OUTPUT:
                pi.write(port, 0)
                self.assertEqual(0, pi.read(port))
                pi.write(port, 1)
                self.assertEqual(1, pi.read(port))
                pi.write(port, 0)
                self.assertEqual(0, pi.read(port))

        for port in ports:
            pi.set_mode(port, pigpio.INPUT)

        for port in ports:
            if pi.get_mode(gpio=port) == pigpio.INPUT:
                result = pi.read(port)
                # to test read value of a readonly port you new a hw trigger
                # therefore a change in the read value of readonly port is not sw testable
                do_nothing()

    def test_pig_pio_test_1(self):
        """This is a test case.

        default -> low -> high -> low"""
        if not is_pi_gpio_d_available():
            add_test_to_skip_list()
            return

        port = io_port.DigitalPort(2, pi_obj=test_pi[0])
        self.assert_low(port)
        port.set_low()
        self.assert_low(port)
        port.set_high()
        self.assert_high(port)
        port.set_low()
        self.assert_low(port)
        port30 = io_port.DigitalPort(30, pi_obj=test_pi[0])
        port30.set_low()
        port30.set_high()
        port30.set_low()

    def test_pig_pio_test_2(self):
        """This is a test case.

        high -> low/high -> low -> high/low"""
        if not is_pi_gpio_d_available():
            add_test_to_skip_list()
            return

        port = io_port.DigitalPort(4, pi_obj=test_pi[0])
        port.set_high()
        self.assert_high(port)
        port.toggle()
        self.assert_high(port)
        port.set_low()
        self.assert_low(port)
        port.toggle()
        self.assert_low(port)
        port30 = io_port.DigitalPort(30, pi_obj=test_pi[0])
        port30.set_low()
        port30.set_high()
        port30.set_low()

    def test_pig_pio_test_3(self):
        """This is a test case to test exceptions."""
        if not is_pi_gpio_d_available():
            add_test_to_skip_list()
            return

        port = io_port.DigitalPort(9, io_port.PORT_IS_READ_ONLY,
                                   pi_obj=test_pi[0])
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
        if not is_pi_gpio_d_available():
            add_test_to_skip_list()
            return

        port = io_port.AnalogPort(2, "Temperature Port", io_port.do_nothing, pi_obj=test_pi[0])
        port.upper_limit = 75
        port.lower_limit = 70
        self.assertGreater(port.get_value(), -20)
        self.assertLess(port.get_value(), 100)

    def test_analog_gpio_test_2(self):
        """This is a test case for an analog senor using 1 wire protocol."""
        if not is_pi_gpio_d_available():
            add_test_to_skip_list()
            return

        port = io_port.AnalogPort(2, "Temperature Port", io_port.do_nothing, pi_obj=test_pi[0])
        # a valid file sensor data file must be in that directory on the pi
        # access must be granted by in opt/pigpio/access
        # /home/pi/sauna/w1_slave/*.txt r
        # to have the 1wire file on the mac for testing is therefore not doable
        sensor_data_file_path = "/home/pi/sauna/w1_slave/*.txt"
        values = port.get_values_2(sensor_data_file_path)
        self.assertAlmostEqual(23.187, values[0], places=3)
        self.assertAlmostEqual(26.297, values[1], places=3)

    def test_analog_gpio_test_3(self):
        # TODO needs more test
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
    suite.addTest(IPPortTestCase('test_pig_pio_test_0'))
    suite.addTest(IPPortTestCase('test_analog_gpio_test_1'))
    suite.addTest(IPPortTestCase('test_analog_gpio_test_2'))
    suite.addTest(IPPortTestCase('test_analog_gpio_test_3'))
    return suite


def main():
    """This is the main, which sets up and runs all tests of this module."""
    init_pi_gpio_d()

    suites_list = get_empty_suites_list()
    suites_list.append(create_test_suite())
    run_unit_test_suites(suites_list)

    close_pi_gpio_d_check()


# pi222 no sensor
# pi224 with temp sensor
test_pi_address = ["pi222", "pi224"]
test_pi = []

if __name__ == '__main__':
    determine_hardware_and_os_environment()
    print(test_pi_address)
    test_pi.append(pigpio.pi(test_pi_address[0], show_errors=True))
    test_pi.append(pigpio.pi(test_pi_address[1], show_errors=True))
    main()
