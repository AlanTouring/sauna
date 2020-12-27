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
        print("hardware is:= Raspberry Pi " + model)
    if is_os_mac():
        print("os:= mac os.")


init_was_executed = False
raspberry_pi_has_pigpio_daemon_running_and_connected = False
skipped_tests = []
raspi_name = "pi222"


def is_pi_available() -> bool:
    global raspberry_pi_has_pigpio_daemon_running_and_connected
    global skipped_tests
    if not raspberry_pi_has_pigpio_daemon_running_and_connected:
        skipped_tests.append(str(inspect.stack()[1].function))
    return raspberry_pi_has_pigpio_daemon_running_and_connected


def init_pi_check():
    global raspberry_pi_has_pigpio_daemon_running_and_connected
    global raspi_name
    global init_was_executed
    if not init_was_executed:
        init_was_executed = True
        pi = pigpio.pi(raspi_name, show_errors=True)
        if pi.connected:
            raspberry_pi_has_pigpio_daemon_running_and_connected = True


def close_pi_check():
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