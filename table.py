class NodeAddress:

    def __init__(self, ip, port, nid):
        self.ip = ip
        self.port = port
        self.nid = nid


class NodePinger:

    def __init__(self, socket, table):
        pass


class Table:

    def __init__(self, node):
        self.node = node
        self.nodes = set()

    def add(self, node):
        self.nodes.add(node)

    def get(self, nid, k=None):
        return list(self.nodes)
