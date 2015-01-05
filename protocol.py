from bencode import bencode, bdecode
from logger import log
from table import NodeAddress

encode = bencode
decode = bdecode


class Protocol:

    def __init__(self, node):
        self.node = node

    def handle_request(self, request, address):
        request = decode(request)

        log("got request {0}".format(request))
        if not self.prehandle(request, address):
            return

        if request['y'] == 'q' and request['q'] in ['find_node']:
            getattr(self, 'handle_' + request['q'])(request, address)

    def prehandle(self, request, address):
        hid = request['a']['id']    # his id
        if hid == self.node.address.nid:
            log("drop request from myself")
            return False

        ip, port = address
        node = NodeAddress(ip, port, hid)
        self.node.table.update(node)
        return True

    def handle_find_node(self, request, address):
        hid = request['a']['id']    # his id
        msg = dict(
            y='r',
            q='find_node',
            a=dict(id=self.node.address.nid, nodes=self.node.table.get(hid)))
        self.send(msg, address)

    def send_find_node(self, address, nid):
        msg = dict(
            y="q",
            q="find_node",
            a=dict(id=self.node.address.nid, target=nid))
        self.send(msg, address)

    def send(self, message, address):
        self.node.send(encode(message), address)

    def bootstrap(self, nodes):
        for address in nodes:
            self.send_find_node(address, self.node.address.nid)
