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
import sys
import time

def parse_data(data):
    try:
        data = data[data.index('(') + 1:data.index(')')]
        parts = data.split(',')
        temp_a = parts[0]
        return temp_a
    except Exception as e:
        print("Veri ayrıştırma hatası:", e)
        return None

def signal_handler(sig, frame):
    server_socket.close()  
    for thread in threading.enumerate():
        if thread != threading.main_thread():  # Ana threadi kapatma
            thread.join()
    sys.exit(0)

def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_message = data.decode()
        serial_port.send_string(temp_a.decode()) 
        print(temp_a)
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
    server_socket.bind(('0.0.0.0', 12346))
    server_socket.listen(5)

    server_thread = threading.Thread(target=server_loop)
    server_thread.start()

    while True:
        if read_data != "":
            print("data arrived")

if __name__ == "__main__":
    main()
