import sys
sys.path.append('contrib')

import socket
from table import Table
from random import randint
from utils import random_id
from protocol import Protocol


class Node:

    def __init__(self, ip=None, port=None, nid=None):
        address = (ip if ip is not None else "0.0.0.0", port if port is not None else randint(40000, 50000))
        self.address = address
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind(self.address)

        self.nid = nid if nid is not None else random_id()
        self.table = Table(self.nid)
        self.protocol = Protocol(self)

    def send(self, message, address):
        try:
            self.ufd.sendto(message, address)
        except Exception:
            pass

    def recv(self):
        return self.ufd.recvfrom(65536)

    def serve(self):
        while True:
            (message, address) = self.recv()
            self.protocol.handle_request(message, address)


if __name__ == "__main__":
    bootstrap_nodes = [("ts", 6881), ("192.168.1.100", 6881)]
    node = Node(port=6881)
    node.protocol.bootstrap(bootstrap_nodes)
    node.serve()
