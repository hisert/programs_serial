import serial
import threading
import time

class MySerialPort:
    
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.buffer = bytearray()  # Veriyi tutmak için bir buffer
        self.gelen = "" # Veriyi tutmak için bir buffer
    
    def open(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
    
    def read_data(self):
        if self.ser:
            while True:
                byte = self.ser.read(1)
                if byte:
                    if byte == b'<':
                        self.buffer.clear()
                    self.buffer.extend(byte)
                    if byte == b'>':
                        data = self.buffer.decode().strip()
                        self.gelen = data
                        self.buffer.clear()  # Bufferi temizle
                        return self.gelen
                else:
                    return ""
        else:
            return ""
            
    def send_string(self, data):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode())
            
    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

def send_data(serial_port):
    while True:
        serial_port.send_string("<Q00000001:0000>")
        time.sleep(1)

def main():
    port = "/dev/ttyS1"  # Seri port adı
    baudrate = 9600  # Aktarılan bit hızı
    timeout = 1  # Okuma zaman aşımı

    serial_port = MySerialPort(port, baudrate, timeout)
    serial_port.open()

    send_thread = threading.Thread(target=send_data, args=(serial_port,))
    send_thread.start()

    try:
        while True:
            data = serial_port.read_data()
            if data:
                print("Received:", data)
    except KeyboardInterrupt:
        serial_port.close()

if __name__ == "__main__":
    main()
