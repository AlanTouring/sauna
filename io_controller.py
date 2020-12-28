"""This module is a generic io_controller for raspberry ports."""
import pigpio

import io_port
from io_port import DigitalPort, AnalogPort
from testframe.test_util import print_stderr, do_nothing


class IO_Controller:
    """This class is a generic io_controller for raspberry port
    it makes use of the the package pi gpio.
    Make sure that the raspberry is accessible in the network and
    that the pigpio daemon is running:

    sudo pigpiod                # start deamon
    ps aux |grep pigpiod        # check proess is running
    sudo killall pigpiod        # stop daemon

    For details to set up an use the package see:
    http://abyz.me.uk/rpi/pigpio/index.html."""

    def __init__(self):
        self.ports = dict()
        self.pies = dict()

    def addPort(self, port, port_name):
        self.ports[port_name] = port

    def __addPi(self, pi_name):
        pi = pigpio.pi(pi_name, show_errors=True)
        self.pies[pi_name] = pi
        assert pi.connected

    def getUpperLimit(self, port_name) -> int:
        port = self.ports[port_name]
        if not isinstance(port, AnalogPort):
            raise ValueError
        return port.upper_limit

    def increaseLimit(self, port_name):
        port = self.ports[port_name]
        if not isinstance(port, AnalogPort):
            raise ValueError
        port.increase()

    def getPortValue(self, port_name) -> int:
        port = self.ports[port_name]
        if not (isinstance(port, DigitalPort) or isinstance(port, AnalogPort)):
            raise ValueError

        if port.port_type == io_port.PORT_IS_READ_ONLY or \
                port.port_type == io_port.PORT_IS_WRITEABLE:
            assert isinstance(port, DigitalPort)
            if port.is_high():
                return 1
            return 0
        elif port.port_type == io_port.PORT_IS_ANALOG_READ_ONLY:
            assert isinstance(port, AnalogPort)
            value = port.get_value()
            # TODO alter code:= return str(value)
            return value
        else:
            raise ValueError

    def __hasPI(self, pi_name) -> bool:
        try:
            pi = self.pies[pi_name]
        except KeyError:
            return False

        assert isinstance(pi, pigpio.pi)
        if pi.connected:
            return True
        return False

    def __getPI(self, pi_name) -> pigpio.pi:
        pi = self.pies[pi_name]
        return pi

    def setPortValue(self, port_name):
        port = self.ports[port_name]
        assert isinstance(port, DigitalPort)
        port.set_high()

    def resetPortValue(self, port_name):
        port = self.ports[port_name]
        assert isinstance(port, DigitalPort)
        port.set_low()

    def createPort(self, port_num, pt, port_name, pi_name):
        if self.__hasPI(pi_name):
            do_nothing()
        else:
            self.__addPi(pi_name)

        pi = self.__getPI(pi_name)
        if pt == io_port.PORT_IS_READ_ONLY or pt == io_port.PORT_IS_WRITEABLE:
            port = DigitalPort(port_num, port_type=pt, pi_para=pi)
            self.addPort(port, port_name)
        elif pt == io_port.PORT_IS_ANALOG_READ_ONLY:
            port = AnalogPort(port_num, port_type=pt, pi_para=pi)
            self.addPort(port, port_name)
            pass
        else:
            raise ValueError

    def togglePortValue(self, port_name):
        port = self.ports[port_name]
        assert isinstance(port, DigitalPort)
        port.toggle()


if __name__ == '__main__':
    io_controller = IO_Controller()
    RESULT = io_controller.pies
    LABEL = '>> The value is :='
    print(LABEL, RESULT, "<<", sep=" ", end='')
