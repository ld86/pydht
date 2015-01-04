from bencode import bencode, bdecode
from logger import log

encode = bencode
decode = bdecode


class Protocol:

    def __init__(self, node):
        self.node = node

    def handle_request(self, request, address):
        request = decode(request)

        log("got request {0}".format(request))

        if request['y'] == 'q' and request['q'] in ['find_node']:
            getattr(self, 'handle_' + request['q'])(request, address)

    def handle_find_node(self, request, address):
        mid = self.node.nid         # my id
        hid = request['a']['id']    # his id

        if hid == mid:
            log("drop find_node request from myself")
            return

        self.node.table.add(hid)
        msg = dict(
            y='r',
            q='find_node',
            a=dict(nodes=self.node.table.get(hid)))
        self.send(msg, address)

    def send_find_node(self, address, nid):
        msg = dict(
            y="q",
            q="find_node",
            a=dict(id=self.node.nid, target=nid))
        self.send(msg, address)

    def send(self, message, address):
        self.node.send(encode(message), address)

    def bootstrap(self, nodes):
        for address in nodes:
            self.send_find_node(address, self.node.nid)
