import time
import pigpio
import io_port


def do_nothing(port_num, port_status, tick):
    pass


def port_example(pi_address_p, one_wire_path_p):
    pi = pigpio.pi(pi_address_p, show_errors=True)
    assert pi.connected

    # Pi 1 Model B1 remaining ports
    # [ 4, 17, 18, 22, 23, 24, 25, 27]
    # [ 1, --,  L,  B,  L,  L,  L, --]

    dps = []
    led_ports = [18, 23, 24, 25]
    for port_num in led_ports:
        port = io_port.DigitalPort(port_num, pi_obj=pi)
        dps.append(port)

    print("Blinking")
    for i in range(0, 5):
        for dp in dps:
            dp.set_high()

        time.sleep(0.15)

        for dp in dps:
            dp.set_low()

        time.sleep(0.15)

    print("Toggle")
    for i in range(0, 3):
        for dp in dps:
            dp.toggle()

        time.sleep(0.2)

    one_wire = io_port.AnalogPort(4, port_type=io_port.PORT_IS_READ_ONLY,
                                  path_to_1wire=one_wire_path_p, pi_obj=pi)
    print("Temp Reading: ", end="")
    for i in range(0, 3):
        temp = one_wire.get_value()
        print(str(temp) + " ", end="")
        time.sleep(0.2)
    print("")

    button = io_port.DigitalPort(22, port_type=io_port.PORT_IS_READ_ONLY,
                                 pi_obj=pi, callback=do_nothing(1, 1, 1))
    print("Waiting for button press:")
    try:
        last_state = 0
        for i in range(0, 30):
            if button.is_high() and last_state == 0:
                print("Press ", end="")
                last_state = 1

            if button.is_low() and last_state == 1:
                print("Release ", end="")
                last_state = 0

            time.sleep(0.1)
        print("")

    except KeyboardInterrupt:
        print("\nTidying up")


def main():
    pi_address = "pi224"
    one_wire_path = "/sys/bus/w1/devices/28-012033d01895/w1_slave"
    print(pi_address, one_wire_path)

    port_example(pi_address, one_wire_path)


if __name__ == '__main__':
    main()
