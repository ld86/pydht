import sys
sys.path.append('contrib')

import socket

from threading import Thread
from bencode import bencode, bdecode
from hashlib import sha1
from random import randint


def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in xrange(length))


def random_id():
    hash = sha1()
    hash.update(entropy(20))
    return hash.digest()


class DHT(Thread):

    def __init__(self, ip, port, bootstrap):
        Thread.__init__(self)
        self.bind_ip = ip
        self.bind_port = port
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind((self.bind_ip, self.bind_port))

        self.nid = random_id()

        self.bootstrap_nodes = bootstrap

    def run(self):
        self.bootstrap()
        while True:
            (data, address) = self.ufd.recvfrom(65536)
            print(bdecode(data))

    def send_krpc(self, message, address):
        self.ufd.sendto(bencode(message), address)

    def send_find_node(self, address):
        tid = entropy(4)
        msg = dict(
            t=tid,
            y="q",
            q="find_node",
            a=dict(id=self.nid, target=random_id()))
        self.send_krpc(msg, address)

    def bootstrap(self):
        for address in self.bootstrap_nodes:
            self.send_find_node(address)

if __name__ == "__main__":
    bootstrap = [("router.bittorrent.com", 6881), ("dht.transmissionbt.com", 6881), ("router.utorrent.com", 6881)]
    node = DHT("0.0.0.0", 6881, bootstrap)
    node.start()
