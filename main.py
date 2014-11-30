import sys
sys.path.append('contrib')

import socket

from threading import Thread
from bencode import bencode, bdecode


class DHT(Thread):

    def __init__(self, ip, port, bootstrap):
        Thread.__init__(self)
        self.bind_ip = ip
        self.bind_port = port
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.ufd.bind((self.bind_ip, self.bind_port))

    def run(self):
        pass

if __name__ == "__main__":
    bootstrap = [("router.bittorrent.com", 6881), ("dht.transmissionbt.com", 6881), ("router.utorrent.com", 6881)]
    node = DHT("0.0.0.0", 6881, bootstrap)
    node.start()
