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
        self.server_thread = None
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.backlog)

        self.running = True
        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.start()

    def stop(self):
        if self.server_socket:
            self.server_socket.close()
            self.running = False

    def server_loop(self):
        while self.running:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            received_message = data.decode()
            received_message = received_message.replace('(', '<')
            received_message = received_message.replace(')', '>')
            # Burada seriale gönderim işlemini ekleyebilirsiniz, ancak seri port nesnesine erişim sağlanmalı
            # Bu örnekte seri port nesnesi kullanılmadığı için doğrudan print ediliyor.
            print(received_message)
        client_socket.close()

def signal_handler(sig, frame):
    global server
    server.stop()
    sys.exit(0)

def main():

    global server
    server = MyServer('0.0.0.0', 12341, 5)
    signal.signal(signal.SIGINT, signal_handler)
    server.start()

    while True:
        print("working")
        time.sleep(1)

if __name__ == "__main__":
    main()
