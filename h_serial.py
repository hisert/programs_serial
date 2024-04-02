import socket
import threading
import signal
import time
import sys

class MyServer:
  
    def __init__(self, host, port, backlog, custom_function=None,, stop_function=None):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.server_socket = None
        self.running = False
        self.custom_function = custom_function
        self.stop_function = stop_function
        self.client_sockets = []  # Bağlı olan tüm client soketlerini saklamak için liste

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
                self.client_sockets.append(client_socket)  # Yeni client soketini listeye ekle
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except KeyboardInterrupt:
                if self.custom_function:
                self.stop_function()
                self.stop()
                break

    def handle_client(self, client_socket, client_address):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            if self.custom_function:
                self.custom_function(data.decode())

        client_socket.close()
        self.client_sockets.remove(client_socket)  # Client soketini listeden kaldır

    def send(self, message):
        for client_socket in self.client_sockets:
            try:
                client_socket.sendall(message.encode())
            except Exception as e:
                print("Error sending message to client:", e)
              


def data_arrived(data):
    global server
    received_message = data.replace('(', '<')
    received_message = received_message.replace(')', '>')
    print(received_message)
    server.send(received_message)
    
def stop_func():
    print("BY BY")
  
server = MyServer('0.0.0.0', 12349, 5, custom_function=data_arrived,, stop_function=stop_func)        
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    server.start()
    
    while True:
        print ("asker")
        time.sleep(1)

if __name__ == "__main__":
    main()
