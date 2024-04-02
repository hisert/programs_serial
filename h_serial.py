import serial
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
                        return gelen
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

# Seri port nesnesini oluştur
serial_port = MySerialPort("COM1", 9600, 1)

# Seri portu aç
serial_port.open()

# Ana program döngüsü
while True:
    # Belirli bir veriyi seri porta gönder
    serial_port.send_string("<Q00000001:0000>")
    
    # 1 saniye bekle
    time.sleep(1)
