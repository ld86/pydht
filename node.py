import sys
sys.path.append('contrib')

import socket
from table import Table, NodePinger, NodeAddress
from random import randint
from utils import random_id
from protocol import Protocol
from logger import log


class Node:
    bootstrap_nodes = [("ts", 6881), ("192.168.1.100", 6881)]

    def __init__(self, ip=None, port=None, nid=None):
        ip, port = address = (ip if ip is not None else "0.0.0.0", port if port is not None else randint(40000, 50000))
        nid = nid if nid is not None else random_id()
        self.address = NodeAddress(nid, ip, port)

        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind(address)

        self.table = Table(self.address)
        self.pinger = NodePinger(self)
        self.protocol = Protocol(self)

    def send(self, message, address):
        try:
            self.ufd.sendto(message, address)
        except Exception as e:
            log("%s %s", address, e)

    def recv(self):
        return self.ufd.recvfrom(65536)

    def recv_and_handle(self):
        (message, address) = self.recv()
        self.protocol.handle_request(message, address)

    def serve(self):
        self.protocol.bootstrap(Node.bootstrap_nodes)
        while True:
            self.recv_and_handle()
