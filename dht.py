from node import Node
from flask import Flask, render_template

port = 6881
node = Node(port=port)
status_app = Flask(__name__)


@status_app.route('/')
def status():
    return render_template("status.html", node=node)

if __name__ == '__main__':
    node.start()
    status_app.run(host=node.address.ip, port=port + 1)
