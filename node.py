import sys
sys.path.append('contrib')

import socket
from hashlib import sha1
from random import randint
from table import Table


def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in xrange(length))


def random_id():
    hash = sha1()
    hash.update(entropy(40))
    return hash.digest()


class Node:

    def __init__(self, ip=None, port=None, nid=None):
        self.bind_ip = ip if ip is not None else "0.0.0.0"
        self.bind_port = port if port is not None else randint(40000, 50000)
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind((self.bind_ip, self.bind_port))

        self.nid = nid if nid is not None else random_id()
        self.nodes = Table(self.nid)

    def send(self, message, address):
        try:
            self.ufd.sendto(message, address)
        except Exception:
            pass

    def recv(self):
        return self.ufd.recvfrom(65536)
