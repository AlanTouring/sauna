#!/usr/bin/env python

# monitor_raspberry_ports.py
# monitor_raspberry_ports.py except port 16 because it seems to toggle
import sys
import time
import pigpio


def print_GPIO_Status(port_num, port_status, tick):
    print("Port={} Status in now={}".format(port_num, port_status))


def main():
    pi = pigpio.pi('pi222')
    if not pi.connected:
        exit()

    ports = create_port_list()

    callbacks = create_callbacks(pi, ports)

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nTidying up")
        for callback in callbacks:
            callback.cancel()

    pi.stop()


def create_port_list():
    if len(sys.argv) == 1:
        ports = range(0, 32)
    else:
        ports = []
        for a in sys.argv[1:]:
            ports.append(int(a))
    return ports


def create_callbacks(pi, ports):
    callbacks = []

    for port in ports:
        if port != 16:
            # port 16 seems to toggle all the time
            # therefore it is excluded
            callbacks.append(pi.callback(port, pigpio.EITHER_EDGE, print_GPIO_Status))

    return callbacks


main()
