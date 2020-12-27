"""This module contains the handling of raspberry pi gpio ports."""
import time
from typing import List

import pigpio
from pigpio import pi

from testframe.test_util import print_stderr

PORT_IS_READ_ONLY: int = 0
PORT_IS_WRITEABLE: int = 1
PORT_IS_ANALOG_READ_ONLY: int = 3
PORT_STATE_LOW: int = 0
PORT_STATE_HIGH: int = 1


# pylint: disable=W0511 # many todos in code and that is ok
# TODO finish implementation

def print_GPIO_Status(port_num, port_status, tick):
    print("Port={} Status in now={}".format(port_num, port_status))


def do_nothing(port_num, port_status, tick):
    print("callback")


class Port:
    def __init__(self, pt=PORT_IS_READ_ONLY):
        self.super_port_type = pt


class AnalogPort():
    upper_limit: int

    def __init__(self, address: int, port_type=PORT_IS_ANALOG_READ_ONLY,
                 callback=do_nothing, pi_para=None):
        self.callback = callback
        self.error_text = "Measured value is not plausible."
        self.upper_limit = 80
        self.lower_limit = 75
        self.__ADDRESS = address
        self.port_type = port_type
        if pi_para is None:
            self.pi = pigpio.pi('pi222', show_errors=True)
        else:
            self.pi = pi_para
        assert self.pi.connected

    @staticmethod
    def is_value_plausible(temps) -> bool:
        if len(temps) == 0:
            return False
        if len(temps) == 1:
            return True
        if (max(temps) - min(temps)) > 10:
            return False

        return True

    def is_below_limit(self) -> bool:
        temps = self.get_values()
        if not self.is_value_plausible(temps):
            print_stderr(self.error_text)

        average = sum(temps) / len(temps)
        return self.lower_limit > average

    def is_above_limit(self) -> bool:
        temps = self.get_values()
        if not self.is_value_plausible(temps):
            print_stderr(self.error_text)

        average = sum(temps) / len(temps)
        return self.upper_limit < average

    def get_value(self) -> float:
        temps = self.get_values()
        if not self.is_value_plausible(temps):
            return 75

        average = sum(temps) / len(temps)
        return average

    def get_values(self) -> List[float]:
        """
        This uses the file interface to access the remote file system.

        In this case it is used to access the sysfs 1-wire bus interface
        to read any connected DS18B20 temperature sensors.

        The remote file /opt/pigpio/access is used to grant access to
        the remote file system.

        For this example the file must contain the following line which
        grants read access to DS18B20 device files.

        /sys/bus/w1/devices/28*/w1_slave r

        Get list of connected sensors, handle error rather than the
        default of raising exception if none found.
        """
        pigpio.exceptions = False
        number, files = self.pi.file_list("/sys/bus/w1/devices/28-00*/w1_slave")
        pigpio.exceptions = True
        temperatures: List[float] = []

        self.scan_one_wire_files(files, number, temperatures)

        return temperatures

    def get_values_2(self, path_to_one_wire_files) -> List[float]:
        temperatures: List[float] = []
        pigpio.exceptions = False
        number, files = self.pi.file_list(path_to_one_wire_files)
        pigpio.exceptions = True
        if number > 0:
            file_list = files.decode("utf-8")
            self.scan_one_wire_files(file_list, number, temperatures)
        return temperatures

    def scan_one_wire_files(self, files, number, temperatures):
        if number >= 0:
            for sensor in files[:-1].split("\n"):
                """
                Typical file name
                /sys/bus/w1/devices/28-000005d34cd2/w1_slave
                """
                device_id = sensor.split("/")[5]  # Fifth field is the device Id.
                handle = self.pi.file_open(sensor, pigpio.FILE_READ)
                number, data = self.pi.file_read(handle, 1000)  # 1000 is plenty to read full file.
                if handle >= 0:
                    self.pi.file_close(handle)

                """
                Typical file contents
                73 01 4b 46 7f ff 0d 10 41 : crc=41 YES
                73 01 4b 46 7f ff 0d 10 41 t=23187
                """
                data_str = data.decode("utf-8")
                if "YES" in data_str:
                    (discard, separator, temperature_str) = data_str.partition(' t=')
                    temperature = float(temperature_str) / 1000.0
                    print("{} {:.1f}".format(device_id, temperature))
                    temperatures.append(temperature)
                else:
                    print("999.9")

    def cancel_callback(self):
        self.callback = do_nothing

    def increase(self):
        if self.upper_limit <= 91:
            self.upper_limit += 5
            self.lower_limit = self.upper_limit - 5
        else:
            self.upper_limit = 65
            self.lower_limit = 60

    def need_heating(self) -> bool:
        return self.lower_limit > self.get_value() and \
               self.upper_limit > self.get_value

    def set_default_temp(self):
        self.upper_limit = 75
        self.lower_limit = 70


class DigitalPort:
    """This class handles a raspberry pi port with these functions:
    set low, set high, etc.."""
    pi: pigpio.pi

    def __init__(self, address: int, port_type=PORT_IS_WRITEABLE,
                 callback=do_nothing, pi_para=None):
        # pylint: disable=C0103 # The following identifiers are written as private constants
        self.__ADDRESS = address
        self.port_type = port_type
        self.pt = port_type
        # pylint: enable=C0103
        self.state = PORT_STATE_LOW
        if self.__ADDRESS < 1000:
            if pi_para is None:
                self.pi = pigpio.pi('pi222', show_errors=True)
            else:
                self.pi = pi_para

            assert self.pi.connected

            if PORT_IS_WRITEABLE:
                self.pi.set_mode(self.__ADDRESS, pigpio.OUTPUT)
                self.pi.write(self.__ADDRESS, 0)
            else:
                self.pi.set_mode(self.__ADDRESS, pigpio.INPUT)
                set.pi.set_glitch_filter(self.__ADDRESS, 50000)
                self.callback = self.pi.callback(self.__ADDRESS,
                                                 pigpio.EITHER_EDGE,
                                                 callback)

    def __del__(self):
        if PORT_IS_READ_ONLY and self.__ADDRESS < 1000:
            self.callback.cancel()

    def set_high(self):
        """Set output port to high."""
        if self.port_type != PORT_IS_WRITEABLE:
            raise ValueError()

        if self.__ADDRESS < 1000:
            self.pi.write(self.__ADDRESS, 1)

        self.state = PORT_STATE_HIGH

    def set_low(self):
        """Set output port to low."""
        if self.port_type != PORT_IS_WRITEABLE:
            raise ValueError()

        if self.__ADDRESS < 1000:
            self.pi.write(self.__ADDRESS, 0)

        self.state = PORT_STATE_LOW

    def is_high(self) -> bool:
        """Check if input port is high."""
        if self.__ADDRESS < 1000:
            self.state = self.pi.read(self.__ADDRESS)

        return bool(self.state == PORT_STATE_HIGH)

    def is_low(self) -> bool:
        """Check if input port is low."""
        if self.__ADDRESS < 1000:
            self.state = self.pi.read(self.__ADDRESS)

        return bool(self.state == PORT_STATE_LOW)

    def toggle(self):
        """Toggle output port from either
        from low -> high/low or from high to low/high."""
        if self.port_type != PORT_IS_WRITEABLE:
            raise ValueError()
        if self.__ADDRESS >= 1000:
            return

        if self.is_high():
            self.set_low()
            time.sleep(0.1)
            self.set_high()
            self.state = PORT_STATE_HIGH

        else:
            self.set_high()
            time.sleep(0.1)
            self.set_low()
            self.state = PORT_STATE_LOW
