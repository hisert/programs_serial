import socket
import threading
import signal
import time
import sys

class MyServer:
  
    def __init__(self, host, port, backlog):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.server_socket = None
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.backlog)

        self.running = True
        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.start()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.server_thread:
            self.server_thread.join()

    def server_loop(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except KeyboardInterrupt:
                self.stop()
                break

    def handle_client(self, client_socket, client_address):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            received_message = data.decode()
            received_message = received_message.replace('(', '<')
            received_message = received_message.replace(')', '>')
            print(received_message)
        client_socket.close()

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # Ctrl+C sinyalini varsayılan işlemi gerçekleştirmesi için ayarla
    server = MyServer('0.0.0.0', 12341, 5)
    server.start()

if __name__ == "__main__":
    main()
