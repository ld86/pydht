import sys
sys.path.append('contrib')

import socket

from threading import Thread
from bencode import bencode, bdecode
from hashlib import sha1
from random import randint
from time import sleep


def entropy(length):
    return ''.join(chr(randint(0, 255)) for _ in xrange(length))


def random_id():
    hash = sha1()
    hash.update(entropy(20))
    return hash.digest()


class Node(Thread):

    def __init__(self, ip, port, bootstrap):
        Thread.__init__(self)
        self.daemon = True

        self.bind_ip = ip
        self.bind_port = port
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind((self.bind_ip, self.bind_port))

        self.nid = random_id()

        self.nodes = set([self.nid])
        self.bootstrap_nodes = bootstrap

    def run(self):
        self.bootstrap()
        while True:
            (data, address) = self.ufd.recvfrom(65536)
            self.handle_request(bdecode(data))

    def send_krpc(self, message, address):
        try:
            self.ufd.sendto(bencode(message), address)
        except Exception:
            pass

    def handle_request(self, request):
        if request['y'] == 'q' and request['q'] in ['find_node']:
            getattr(self, 'handle_' + request['q'])(request)

    def handle_find_node(self, request):
        if request['a']['id'] == self.nid:
            return

    def send_find_node(self, address, nid):
        msg = dict(
            y="q",
            q="find_node",
            a=dict(id=self.nid, target=nid))
        self.send_krpc(msg, address)

    def bootstrap(self):
        for address in self.bootstrap_nodes:
            self.send_find_node(address, self.nid)

if __name__ == "__main__":
    bootstrap = [("ts", 6881), ("192.168.1.100", 6881)]
    node = Node("0.0.0.0", 6881, bootstrap)
    node.start()
    while True:
        sleep(60)
