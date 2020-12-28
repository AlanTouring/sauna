# User GPIO 2-4, 7-11, 14-15, 17-18, 22-25, 27-31.
# for Pi Type 2 Model B Rev 2


pi1_ports = [2, 3, 4, 17, 27, 22, 10, 9, 11, 14, 15, 18, 23, 24, 25, 8, 7]
pi1_ports_extra = [5, 6, 13, 19, 26, 12, 16, 20, 21]
pi1_ports.sort()


pi1_uart_ports = [14, 15]
pi1_w1_ports = [4]
pi1_i2c_ports = [2, 3]
pi1_spi_ports = [7, 8, 9, 10, 11]

pi1_double_use_ports = pi1_spi_ports + pi1_i2c_ports + pi1_w1_ports + pi1_uart_ports
pi1_single_use_ports = list(set(pi1_ports) - set(pi1_double_use_ports))


pi2_ports = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]
pi2_ports.sort()

pi2_w1_ports = [4]
pi2_i2c_ports = [2, 3]
pi2_spi_1_ports = [7, 8, 9, 10, 11]
pi2_spi_2_ports = [16, 19, 20, 21]
pi2_double_use_ports = pi2_spi_2_ports + pi2_spi_1_ports + pi2_i2c_ports + pi2_w1_ports
pi2_single_use_ports = list(set(pi2_ports) - set(pi2_double_use_ports))


