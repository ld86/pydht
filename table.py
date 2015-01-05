from threading import Thread
from time import sleep


class NodeAddress:

    def __init__(self, ip, port, nid):
        self.ip = ip
        self.port = port
        self.nid = nid

    def __hash__(self):
        return self.nid.__hash__()

    def __eq__(self, other):
        return self.nid == other.nid

    def __repr__(self):
        return "{} {} {}".format(self.nid.__hash__(), self.ip, self.port)


class NodePinger(Thread):

    def __init__(self, node):
        super(NodePinger, self).__init__()
        self.daemon = True
        self.node = node

    def run(self):
        while sleep(5) is None:
            for node in self.node.table.nodes:
                self.node.protocol.send_ping((node.ip, node.port))


class Table:

    def __init__(self, node):
        self.node = node
        self.nodes = set()

    def update(self, node):
        self.nodes.add(node)

    def get(self, nid, k=None):
        return map(lambda node: (node.nid, node.ip, node.port), list(self.nodes))
