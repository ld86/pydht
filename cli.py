if __name__ == "__main__":
    bootstrap = [("ts", 6881), ("192.168.1.100", 6881)]
    node = Node("0.0.0.0", 6881, bootstrap)
    node.start()
    while True:
        sleep(60)

