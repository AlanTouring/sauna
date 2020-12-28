"""This module is main controller for the sauna telegram bot."""
import io_port
import pi_util
from io_controller import IO_Controller


class Sauna:
    """This class forward the telegram bot commands to the raspberry ports and
    forwards the raspberry ports status data to the telegram bot."""

    def __init__(self, pi_address="pi222"):
        self.pi_address = pi_address
        self.control = IO_Controller()
        port_rw = io_port.PORT_IS_WRITEABLE
        port_ro = io_port.PORT_IS_READ_ONLY
        port_aro = io_port.PORT_IS_ANALOG_READ_ONLY
        ports = pi_util.pi1_single_use_ports
        # Pi 1 Model B1 remaining ports
        #       0   1   2   3   4   5   6
        # [ 4, 17, 18, 22, 23, 24, 25, 27]
        # [ 1, --,  L,  B,  L,  L,  L, --]

        self.control.createPort(ports[0], port_ro, "Mains Sensor", pi_address)
        self.control.createPort(ports[1], port_ro, "Power Sensor", pi_address)
        self.control.createPort(ports[3], port_ro, "Light Sensor", pi_address)
        self.control.createPort(ports[2], port_ro, "Oven Sensor", pi_address)
        self.control.createPort(ports[4], port_rw, "Power Switch", pi_address)
        self.control.createPort(ports[5], port_rw, "Light Switch", pi_address)
        self.control.createPort(ports[6], port_rw, "Oven Switch", pi_address)
        self.control.createPort(4, port_aro, "Temperature Sensor", pi_address)

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
