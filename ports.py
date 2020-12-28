import pigpio

import pi_util


def all_port_status(pi_address_p, one_wire_path_p):
    pi = pigpio.pi(pi_address_p, show_errors=True)
    assert pi.connected

    print(pi_util.pi1_single_use_ports)

    port_status = []
    for port in pi_util.pi2_single_use_ports:
        port_status.append("Pi:=")
        port_status.append(pi_address_p)
        port_status.append("\t Port :=")
        port_status.append(str(port))
        port_status.append("\t Mode:=")
        port_status.append(str(pi.get_mode(port)))
        port_status.append("\t Value:=")
        port_status.append(str(pi.read(port)))
        port_status.append("\n")

    print("".join(port_status))


def main():
    pi_address = "pi224"
    one_wire_path = "/sys/bus/w1/devices/28-012033d01895/w1_slave"
    print(pi_address, one_wire_path)
    all_port_status(pi_address, one_wire_path)


if __name__ == '__main__':
    main()
