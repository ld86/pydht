from node import Node

if __name__ == "__main__":
    node = Node()
    node.protocol.send_find_node(("127.0.0.1", 6881), node.nid)
    print(node.recv())
