import serial
import time

class MySerialPort:
    
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.buffer = bytearray()  # Veriyi tutmak için bir buffer
    
    def open(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
    
    def read_data(self):
        if self.ser:
            byte = self.ser.read(1)
            if byte:
                if byte == b'<':
                    self.buffer.clear()
                self.buffer.extend(byte)
                if byte == b'>':
                    data = self.buffer.decode().strip()
                    self.buffer.clear()  # Bufferi temizle
                    return data
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

def main():
    port = '/dev/ttyS1'  # Seri port adı
    baudrate = 9600  # Aktarılan bit hızı
    timeout = 1  # Okuma zaman aşımı

    serial_port = MySerialPort(port, baudrate, timeout)
    serial_port.open()

    last_send_time = time.time()

    try:
        while True:
            # Veri gönderme
            current_time = time.time()
            if current_time - last_send_time >= 1:
                serial_port.send_string("<Q00000001:0000>")
                last_send_time = current_time
            
            # Veri alma
            data = serial_port.read_data()
            if data:
                print("Received:", data)  # Gelen veriyi ekrana yazdır
    except KeyboardInterrupt:
        serial_port.close()

if __name__ == "__main__":
    main()
