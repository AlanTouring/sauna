import platform
import subprocess


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
