"""This module is main controller for the sauna telegram bot."""
import io_port
from io_controller import IO_Controller


class Sauna:
    """This class forward the telegram bot commands to the raspberry ports and
    forwards the raspberry ports status data to the telegram bot."""

    def __init__(self):
        self.control = IO_Controller()
        port_rw = io_port.PORT_IS_WRITEABLE
        port_ro = io_port.PORT_IS_READ_ONLY
        port_aro = io_port.PORT_IS_ANALOG_READ_ONLY
        pi_name = 'pi222'
        self.control.createPort(2, port_ro, "Mains Sensor", pi_name)
        self.control.createPort(3, port_ro, "Power Sensor", pi_name)
        self.control.createPort(7, port_rw, "Power Switch", pi_name)
        self.control.createPort(8, port_ro, "Light Sensor", pi_name)
        self.control.createPort(9, port_rw, "Light Switch", pi_name)
        self.control.createPort(10, port_ro, "Oven Sensor", pi_name)
        self.control.createPort(11, port_rw, "Oven Switch", pi_name)
        self.control.createPort(4, port_ro, "Temperature Sensor", pi_name)
        self.control.createPort(14, port_aro, "Temperature Sensor 2", pi_name)

    def get_sensor_value(self, port_name) -> str:
        """method getting the sensor value"""
        return str(self.control.getPortValue(port_name))


class Login:
    """This class is handles the login of the telegram user,
    who wants to control the sauna bot."""
    password: str

    def __init__(self):
        self.user_is_logged_in = False
        self.password = "1234"

    def is_user_logged_in(self) -> bool:
        """method controlling a simple login in the telegram chat"""
        return self.user_is_logged_in

    def login_user(self, pwd: str):
        """method controlling a simple login in the telegram chat"""
        if pwd == self.password:
            self.user_is_logged_in = True

    def logout_user(self):
        """method controlling a simple login in the telegram chat"""
        self.user_is_logged_in = False

    def get_log_status_text(self) -> str:
        """method controlling a simple login in the telegram chat"""
        res: str
        if self.user_is_logged_in:
            res = "You are logged in. Welcome."
        else:
            res = "You are not logged in."
        return res
