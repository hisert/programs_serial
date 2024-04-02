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
        self.gelen = bytearray()  # Veriyi tutmak için bir buffer
        self.thread = None
        self.running = False
        self.data_ready = False  # Veri hazır flag'i
    def open(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
    def read_data(self):
        if self.ser:
            while True:
                # Seri porttan bir byte oku
                byte = self.ser.read(1)
                if byte:
                    if byte == b'<':
                        self.buffer.clear()
                    self.buffer.extend(byte)
                    if byte == b'>':
                        data = self.buffer.decode().strip()
                        self.gelen = data
                        self.buffer.clear()  # Bufferi temizle
                        return data
                else:
                   return None
        else:
            return None
    def send_string(self, data):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode())
    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
    def start_serial_reading(self):
        if not self.running:
            self.thread = threading.Thread(target=self.serial_reader)
            self.running = True
            self.thread.start()

    def stop_serial_reading(self):
        if self.running:
            self.running = False
            self.thread.join()

    def serial_reader(self):
        while self.running:
            data = self.read_data()
            if data:
                self.data_ready = True  # Veri hazır flag'ini true yap
            time.sleep(0.1)
    
    def get_serial_data(self):
        if self.data_ready:
            self.data_ready = False
            return self.gelen
        else:
            return None
            
serial_port = MySerialPort(port='/dev/ttyS1', baudrate=9600, timeout=1)
serial_port.open()
received_data = b"<Q00000001:0000>"
serial_port.send_string(received_data)  
serial_port.close()
