import serial
import socket
import threading
import signal
import time
import sys

class MySerialPort:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        if not self.ser or not self.ser.isOpen():
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        else:
            print("Port is already open.")

    def close(self):
        if self.ser and self.ser.isOpen():
            self.ser.close()
        else:
            print("Port is not open.")

    def send_string(self, data):
        if self.ser and self.ser.isOpen():
            self.ser.write(data.encode())
        else:
            print("Port is not open.")

    def read_data(self):
        if self.ser and self.ser.isOpen():
            return self.ser.readline().decode().strip()
        else:
            print("Port is not open.")
            return ""

def signal_handler(sig, frame):
    global server_socket, serial_port
    server_socket.close()
    serial_port.close()
    sys.exit(0)

def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_message = data.decode()
        received_message = received_message.replace('(', '<')
        received_message = received_message.replace(')', '>')
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
    server_socket.bind(('0.0.0.0', 12341))
    server_socket.listen(5)

    server_thread = threading.Thread(target=server_loop)
    server_thread.start()

    try:
        while True:
            serial_port.send_string("<Q00000001:0000>")
            time.sleep(1)
            if serial_port.read_data() != "":
                print("data arrived")
    except KeyboardInterrupt:
        pass
    finally:
        serial_port.close()

if __name__ == "__main__":
    main()
