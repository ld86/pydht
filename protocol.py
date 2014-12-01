class Protocol:
            self.ufd.sendto(bencode(message), address)
    def __init__(

    def handle_request(self, request):
        if request['y'] == 'q' and request['q'] in ['find_node']:
            getattr(self, 'handle_' + request['q'])(request)

    def handle_find_node(self, request):
        if request['a']['id'] == self.nid:
            return

    def send_find_node(self, address, nid):
        msg = dict(
            y="q",
            q="find_node",
            a=dict(id=self.nid, target=nid))
        self.send_krpc(msg, address)

    def bootstrap(self):
        for address in self.bootstrap_nodes:
            self.send_find_node(address, self.nid)

