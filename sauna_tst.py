"""This module is the test suite for the sauna and login class."""
import unittest
import io_port
import sauna
import testframe.test_util


class SaunaTestCase(unittest.TestCase):
    """This class contains the sauna test cases."""

    def setUp(self):
        self.sauna = sauna.Sauna("pi222")
        self.login = sauna.Login()

    def test_sauna_1(self):
        """This is a test of all digital sensors and digital switches."""
        self.assertEqual("0", self.sauna.get_sensor_value("Mains Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Power Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Light Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Oven Sensor"))
        self.assertEqual("75", self.sauna.get_sensor_value("Temperature Sensor"))

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
        """This is a test of a nominal sauna sequence. Without HW Feedback"""
        self.assertEqual("0", self.sauna.get_sensor_value("Mains Sensor"))
        # Power
        self.assertEqual("0", self.sauna.get_sensor_value("Power Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Power Switch"))
        self.sauna.control.togglePortValue("Power Switch")
        self.assertEqual("0", self.sauna.get_sensor_value("Power Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Power Switch"))
        # Light
        self.assertEqual("0", self.sauna.get_sensor_value("Light Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Light Switch"))
        self.sauna.control.togglePortValue("Light Switch")
        self.assertEqual("0", self.sauna.get_sensor_value("Light Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Light Switch"))
        # Oven
        self.assertEqual("0", self.sauna.get_sensor_value("Oven Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Oven Switch"))
        self.sauna.control.togglePortValue("Oven Switch")
        self.assertEqual("0", self.sauna.get_sensor_value("Oven Sensor"))
        self.assertEqual("0", self.sauna.get_sensor_value("Oven Switch"))

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
    suite.addTest(SaunaTestCase('test_sauna_1'))
    suite.addTest(SaunaTestCase('test_login'))
    suite.addTest(SaunaTestCase('test_sauna_sequence_1'))
    # TODO add test cases here
    return suite


def main():
    """This is the main, which sets up and runs all tests of this module."""
    suites_list = testframe.test_util.get_empty_suites_list()
    suites_list.append(create_test_suite())
    testframe.test_util.run_unit_test_suites(suites_list)


if __name__ == '__main__':
    main()
