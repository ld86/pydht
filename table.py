class NodePinger:

    def __init__(self, table):
        pass


class Table:

    def __init__(self, node):
        self.nid = node.nid
        self.nodes = set()
        self.add(self.nid)

    def add(self, nid):
        self.nodes.add(nid)

    def get(self, nid, k=None):
        return list(self.nodes)
