from threading import Thread, Lock
from time import sleep, time, ctime
from math import log
from collections import deque
import heapq


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
                bucket.lock.acquire()
                for node in bucket[:1]:
                    self.node.protocol.send_ping((node.ip, node.port))
                bucket.lock.release()


class Deque(deque):

    def __init__(self):
        super(Deque, self).__init__()
        self.lock = Lock()


class Table:

    def __init__(self, node):
        self.node = node
        self.buckets = [Deque() for i in range(160)]

    def distance(self, nid):
        a = int(self.node.nid.encode('hex'), 16)
        b = int(nid.encode('hex'), 16)
        return a ^ b

    def bucket(self, nid):
        return int(log(self.distance(nid), 2))

    def update(self, node):
        if node.nid != self.node.nid:
            bucket = self.buckets[self.bucket(node.nid)]
            bucket.lock.acquire()
            try:
                bucket.remove(node)
            except ValueError:
                pass
            bucket.append(node)
            bucket.lock.release()

    def zigzag(self, b):
        n = len(self.buckets)

        yield b
        for i in range(1, n):
            if b - i >= 0:
                yield b - i
            if b + i < n:
                yield b + i

    def get(self, nid, k=20):
        nodes = []
        for b in self.zigzag(self.bucket(nid)):
            if len(nodes) > k:
                break
            for node in self.buckets[b]:
                heapq.heappush(nodes, (self.distance(node.nid), node))

        nodes = map(lambda distance_and_node: distance_and_node[1], heapq.nsmallest(k, nodes))
        return map(lambda node: node.address(), list(nodes))
