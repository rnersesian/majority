from websocket_server import WebSocketServer


if __name__ == '__main__':
    server = WebSocketServer(host='0.0.0.0')
    server.start()

