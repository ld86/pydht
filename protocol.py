from contrib.bencode import bencode, bdecode
from logger import log
from table import NodeAddress

encode = bencode
decode = bdecode


class Protocol:

    def __init__(self, node):
        self.node = node
        self.q = ['find_node', 'ping']

    def handle_request(self, request, address):
        request = decode(request)

        log("got request {0}".format(request))
        if not self.prehandle(request, address):
            return

        if request['y'] == 'q' and request['q'] in self.q:
            getattr(self, 'handle_' + request['q'])(request, address)

        if request['y'] == 'r' and request['q'] in self.q:
            getattr(self, 'handle_' + request['q'] + '_response')(request, address)

    def prehandle(self, request, address):
        hid = request['a']['id']    # his id
        if hid == self.node.address.nid:
            log("drop request from myself")
            return False

        ip, port = address
        node = NodeAddress(hid, ip, port)
        self.node.table.update(node)
        return True

    def handle_find_node(self, request, address):
        target = request['a']['target']
        tail = request['a']['tail']
        origin = address if not request['a']['origin'] else request['a']['origin']

        nodes = self.node.table.get(target)
        msg = dict(
            y='r',
            q='find_node',
            a=dict(id=self.node.address.nid, nodes=nodes))
        self.send(msg, origin)

        new_tail = tail[:]
        new_tail.extend([node[0] for node in nodes])

        for node in nodes:
            if node[0] not in tail:
                self.send_find_node(tuple(node[1:]), target, origin, new_tail)

    def handle_find_node_response(self, request, address):
        for node in request['a']['nodes']:
            self.node.table.update(NodeAddress(node[0], node[1], node[2]))

    def send_find_node(self, address, nid, origin=None, tail=None):
        origin = False if origin is None else origin
        tail = [self.node.address.nid] if tail is None else tail
        msg = dict(
            y="q",
            q="find_node",
            a=dict(id=self.node.address.nid,
                   target=nid,
                   origin=origin,  # origin address
                   tail=tail))  # tail, who send me something
        self.send(msg, address)

    def handle_ping(self, request, address):
        msg = dict(
            y="r",
            q="ping",
            a=dict(id=self.node.address.nid))
        self.send(msg, address)

    def handle_ping_response(self, request, address):
        pass

    def send_ping(self, address):
        msg = dict(
            y="q",
            q="ping",
            a=dict(id=self.node.address.nid))
        self.send(msg, address)

    def send(self, message, address):
        self.node.send(encode(message), address)

    def bootstrap(self, nodes):
        for address in nodes:
            self.send_find_node(address, self.node.address.nid)
