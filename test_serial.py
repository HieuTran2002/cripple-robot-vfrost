from serial_utils import uart

uart = uart()
RobotMode = [0] * 5
b = 0
n = 0
while n < 5 and b != 255:
    b = uart.get()
    if b != 255:
        RobotMode[n] = b
    n += 1
    print("RobotMode: ", RobotMode)
