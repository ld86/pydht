from threading import Thread
from time import sleep, time, ctime
from math import log
from collections import deque


class NodeAddress:

    def __init__(self, nid, ip, port):
        self.nid = nid
        self.ip = ip
        self.port = port
        self.ts = time()
        self.cts = ctime(self.ts)

    def __hash__(self):
        return self.nid.__hash__()

    def __eq__(self, other):
        return self.nid == other.nid

    def __repr__(self):
        return "{} {} {}".format(self.nid.__hash__(), self.ip, self.port)

    def address(self):
        return (self.nid, self.ip, self.port)


class NodePinger(Thread):

    def __init__(self, node):
        super(NodePinger, self).__init__()
        self.daemon = True
        self.node = node
        self.start()

    def run(self):
        while sleep(30) is None:
            for bucket in self.node.table.buckets:
                for node in bucket:
                    self.node.protocol.send_ping((node.ip, node.port))


class Table:

    def __init__(self, node):
        self.node = node
        self.buckets = [deque() for i in range(160)]

    def bucket(self, nid):
        a = int(self.node.nid.encode('hex'), 16)
        b = int(nid.encode('hex'), 16)
        return int(log(a ^ b, 2))

    def update(self, node):
        if node.nid != self.node.nid:
            bucket = self.buckets[self.bucket(node.nid)]
            try:
                bucket.remove(node)
            except ValueError:
                pass
            bucket.append(node)

    def get(self, nid, k=20):
        nodes = []
        for bucket in self.buckets:
            nodes.extend(bucket)
            if len(nodes) > k:
                break
        nodes = nodes[:k]
        return map(lambda node: node.address(), list(nodes))
