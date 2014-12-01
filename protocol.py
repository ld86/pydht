import logging
import sys
from bencode import bencode, bdecode

encode = bencode
decode = bdecode


def logger(name):
    root = logging.getLogger(name)
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    return root


class Protocol:

    def __init__(self, node):
        self.node = node
        self.log = logger(self.__class__.__name__).info

    def handle_request(self, request, address):
        request = decode(request)

        self.log("got request {0}".format(request))

        if request['y'] == 'q' and request['q'] in ['find_node']:
            getattr(self, 'handle_' + request['q'])(request, address)

    def handle_find_node(self, request, address):
        if request['a']['id'] == self.node.nid:
            self.log("drop find_node request from myself")
            return
        self.node.table.add(request['a']['id'])
        msg = dict(
            y='r',
            q='find_node',
            a=dict(nodes=self.node.table.get()))
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
