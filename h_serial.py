import serial
class MySerialPort:
    
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.buffer = bytearray()
        self.gelen = ""

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
                    self.gelen = data
                    self.buffer.clear() 
                    return self.gelen
            return ""
            
    def send_string(self, data):
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode())
            
    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            
import socket
import threading
import signal

def parse_data(data):
    try:
        data = data[data.index('(') + 1:data.index(')')]
        data = s.replace('(', '<')
        data = s.replace(')', '>')
        return data
    except Exception as e:
        print("Veri ayrıştırma hatası:", e)
        return None

def signal_handler(sig, frame):
    global server_socket
    server_socket.close()
    sys.exit(0)

def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_message = data.decode()
        serial_port.send_string(received_message) 
        print(received_message)
    client_socket.close()

def server_loop():
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

serial_port = MySerialPort(port='/dev/ttyS1', baudrate=9600, timeout=1)

def main():
    serial_port.open()
    global server_socket
    signal.signal(signal.SIGINT, signal_handler)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12347))
    server_socket.listen(5)

    server_thread = threading.Thread(target=server_loop)
    server_thread.start()

    try:
        while True:
            if serial_port.read_data() != "":
                print("data arrived")
    except KeyboardInterrupt:
        pass
    finally:
        serial_port.close()

if __name__ == "__main__":
    main()
