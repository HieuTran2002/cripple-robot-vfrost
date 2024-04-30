import serial 

usbUART_id = 0
ser = serial.Serial()


class uart:
    ser = None
    port = None

    def __init__(self, port="/dev/ttyS0"):
        self.port = port
        try:
            if self.ser is None:
                try: 
                    self.ser = serial.Serial(port, baudrate = 115200, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 1)
                except Exception as e:
                    print(e)

            self.ser = serial.Serial(port, baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
        except Exception as e:
            print("Init ", e)
    
    def get(self):
        try:
            if self.ser is None:
                try: 
                    self.ser = serial.Serial(self.port, baudrate = 115200, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 1)
                except Exception as e:
                    print("UART ERROR: ", e)
                    self.ser = None
                    return 0
            return int.from_bytes(self.ser.read(), 'little')
        except Exception as e:
            self.ser = None
            print("UART read eror", e)

        return 0

    def put(self, data):
        try:
            buffer = bytearray([data[0], data[1], data[2], data[3], 0, 0, 0, 13])
            self.ser.write(buffer)
        except Exception as e:
            self.ser = None
            self.ser = serial.Serial(self.port, baudrate = 115200, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 1)
            # self.ser.open()
            print("UART write eror:", e)
