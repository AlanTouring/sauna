"""This module is the test suite for the sauna and login class."""
import unittest
import io_port
import sauna
import testframe.test_util


class SaunaTestCase(unittest.TestCase):
    """This class contains the sauna test cases."""

    def setUp(self):
        self.sauna = sauna.Sauna()
        self.login = sauna.Login()

    def test_sauna_1(self):
        """This is a test of all digital sensors and digital switches."""
        self.assertEqual("0", self.sauna.get_sensor_value("Mains Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Power Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Light Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Oven Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Temperature Sensor"))

        self.assertEqual("0", self.sauna.get_sensor_value("Power Switch"))
        self.assertEqual("0", self.sauna.get_sensor_value("Light Switch"))
        self.assertEqual("0", self.sauna.get_sensor_value("Oven Switch"))

        self.sauna.control.setPortValue("Power Switch")
        self.assertEqual("1", self.sauna.get_sensor_value("Power Switch"))
        self.sauna.control.setPortValue("Light Switch")
        self.assertEqual("1", self.sauna.get_sensor_value("Light Switch"))
        self.sauna.control.setPortValue("Oven Switch")
        self.assertEqual("1", self.sauna.get_sensor_value("Oven Switch"))

    def test_sauna_sequence_1(self):
        """This is a test of a nominal sauna sequence."""
        # main power
        self.assertFalse(self.sauna.main_power_status.is_high(), msg="main power is off. Should be on.")
        # Trick the class to create the test by modifying temporarily a __private attribute
        # In reality the main switch in the sauna must be pressed manually to main power = on
        self.sauna.main_power_status.state = io_port.PORT_STATE_HIGH
        self.assertTrue(self.sauna.main_power_status.state == io_port.PORT_STATE_HIGH)
        self.assertTrue(self.sauna.main_power_status.is_high())

        # remoter controlled 2nd power switch
        self.assertFalse(self.sauna.power.is_high(), msg="remote controlled power switch = off")
        self.sauna.power.set_high()
        self.assertTrue(self.sauna.power.is_high())

        # switch for actually putting electrical power to the heating coil
        self.assertFalse(self.sauna.heat.is_high(), msg="at beginning this should be of.")
        self.sauna.heat.set_high()
        self.assertTrue(self.sauna.heat.is_high())

        self.assertFalse(self.sauna.light.is_high(), msg="at beginning this should be of.")
        self.sauna.light.set_high()
        self.assertTrue(self.sauna.light.is_high())

    def test_sauna_sequence_2(self):
        # TODO not all sauna related functions are tested. need more tests.
        pass

    def test_get_temp(self):
        """This is a test of a getter function."""
        self.assertEqual(self.sauna.get_temp_val(), 0, msg='incorrect getter')
        self.sauna.set_temp(5)
        self.assertEqual(self.sauna.get_temp_val(), 5, msg='incorrect getter')

    def test_login(self):
        """This is a test of the login process.
        sequence: init -> logged out -> fail login -> login -> log out"""
        self.assertFalse(self.login.is_user_logged_in())
        self.login.login_user("2932")
        self.assertFalse(self.login.is_user_logged_in())
        self.login.login_user("1234")
        self.assertTrue(self.login.is_user_logged_in())
        self.login.logout_user()
        self.assertFalse(self.login.is_user_logged_in())

    def tearDown(self):
        pass


def create_test_suite() -> unittest.TestSuite:
    """This is a convenience function to collect all tests of this module."""
    suite = unittest.TestSuite()
    #suite.addTest(SaunaTestCase('test_get_temp'))
    suite.addTest(SaunaTestCase('test_login'))
    #suite.addTest(SaunaTestCase('test_sauna_sequence_1'))
    #suite.addTest(SaunaTestCase('test_sauna_sequence_2'))
    suite.addTest(SaunaTestCase('test_sauna_1'))
    # TODO add test cases here
    return suite


def main():
    """This is the main, which sets up and runs all tests of this module."""
    suites_list = testframe.test_util.get_empty_suites_list()
    suites_list.append(create_test_suite())
    testframe.test_util.run_unit_test_suites(suites_list)


if __name__ == '__main__':
    main()
