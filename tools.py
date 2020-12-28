import inspect
import platform
import subprocess

import pigpio

from testframe.test_util import print_stderr


def is_os_mac():
    if platform.system() == "Darwin":
        return True
    return False


def is_os_linux():
    if platform.system() == "Linux":
        return True
    return False


def is_os_windows():
    if platform.system() == "Windows":
        return True
    return False


def is_hardware_raspberry():
    if is_os_linux():
        out = subprocess.Popen(['cat', '/sys/firmware/devicetree/base/model'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        data_str = stdout.decode("utf-8")
        if "Raspberry" not in data_str:
            return False

        return True


def get_raspberry_model() -> int:
    if is_os_linux():
        out = subprocess.Popen(['cat', '/sys/firmware/devicetree/base/model'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        stdout, stderr = out.communicate()
        data_str = stdout.decode("utf-8")
        if "Raspberry Pi 2" not in data_str:
            return 2
        if "Raspberry Pi 3" not in data_str:
            return 3
        if "Raspberry Pi 4" not in data_str:
            return 4
        return 0


def determine_hardware_and_os_environment():
    if is_os_linux() and is_hardware_raspberry():
        model = str(get_raspberry_model())
        print_stderr("hardware is:= Raspberry Pi " + model + " --- ", end="")
    if is_os_mac():
        print_stderr("os:= mac os --- ", end="")


init_was_executed = False
pi_gpio_daemon_is_running = False
skipped_tests = []
raspi_name = "pi222"


def is_pi_gpio_d_available() -> bool:
    global pi_gpio_daemon_is_running
    return pi_gpio_daemon_is_running


def init_pi_gpio_d():
    global pi_gpio_daemon_is_running
    global raspi_name
    global init_was_executed
    if not init_was_executed:
        init_was_executed = True
        pi = pigpio.pi(raspi_name, show_errors=True)
        if pi.connected:
            pi_gpio_daemon_is_running = True


def close_pi_gpio_d_check():
    global skipped_tests
    if len(skipped_tests) > 0:
        print_stderr("")
        for skipped_test in skipped_tests:
            print_stderr("test skipped --- ", end="")
            print_stderr(skipped_test)


def add_test_to_skip_list():
    global skipped_tests
    func_name = inspect.stack()[1].function
    skipped_tests.append(func_name)