"""This module is main controller for the sauna telegram bot."""
import io_port
from io_controller import IO_Controller
from io_port import AnalogPort


class Sauna:
    """This class forward the telegram bot commands to the raspberry ports and
    forwards the raspberry ports status data to the telegram bot."""
    temperature_status: AnalogPort

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

        self.main_power_status = io_port.DigitalPort(2, io_port.PORT_IS_READ_ONLY)
        self.power = io_port.DigitalPort(3)
        self.power_status = io_port.DigitalPort(11, io_port.PORT_IS_READ_ONLY)
        self.heat = io_port.DigitalPort(7)
        self.heat_status = io_port.DigitalPort(8, io_port.PORT_IS_READ_ONLY)
        self.light = io_port.DigitalPort(9)
        self.light_status = io_port.DigitalPort(10, io_port.PORT_IS_READ_ONLY)
        self.temperature_status = io_port.AnalogPort(4, "Temperature")
        self.temperature_status.set_lower_limit = 70
        self.temperature_status.set_upper_limit = 75

    def get_sensor_value(self, port_name) -> str:
        """method getting the sensor value"""
        return str(self.control.getPortValue(port_name))

    def get_main_port_status(self) -> str:
        """method controlling the electrical power"""
        return str(self.main_power_status.is_high())

    def get_power_port_status(self) -> str:
        """method controlling the electrical power"""
        return str(self.power_status.is_high())

    def set_power_on(self):
        """method controlling the electrical power"""
        self.power.set_high()

    def set_power_off(self):
        """method controlling the electrical power"""
        self.power.set_low()

    def get_temp(self) -> str:
        """method controlling the temperature"""
        return str(self.temperature_status.get_value()) + " Grad"

    def get_temp_val(self) -> int:
        """method controlling the temperature"""
        return self.temperature_status.get_value()

    def set_temp(self, temp_val: int) -> None:
        """method controlling the temperature"""
        self.temperature_status.increase()

    def set_heat_on(self) -> None:
        """method controlling the sauna oven"""
        if self.temperature_status.need_heating():
            self.heat.set_high()
        else:
            self.heat.set_low()

    def set_heat_off(self) -> None:
        """method controlling the sauna oven"""
        self.heat.set_low()

    def get_light_port_status(self) -> str:
        """method controlling the light"""
        return str(self.light_status.is_high())

    def set_light_on(self):
        """method controlling the light"""
        if self.light_status.set_low():
            self.light.set_high()

    def set_light_off(self):
        """method controlling the light"""
        self.light.set_low()


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
