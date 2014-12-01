class Table:

    def __init__(self, nid):
        self.nid = nid
        self.nodes = set()
        self.add(nid)

    def add(self, nid):
        self.nodes.add(nid)

    def get(self, nid, k=None):
        return list(self.nodes)
