from sys import argv
from protocol import Protocol
from random import randint
import socket


class Client:

    def __init__(self):
        ip, port = address = ("0.0.0.0", randint(40000, 50000))
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ufd.bind(address)

        self.protocol = Protocol(self)

    def get(key):
        pass

    def store(self, key, value):
        self.protocol.send_store(key, value)

if __name__ == "__main__":
    client = Client()

    if len(argv) == 1:
        print(client.get(argv[1]))
    elif len(argv) == 2:
        client.store(argv[1], argv[2])
