import threading
import socket

import client
import server

if __name__ == '__main__':

    server_thread = threading.Thread(
            target=server.start,
            daemon=True,
            name='simple-python-server'
    )

    try:
        server_thread.start()
        print('Started background server.')
        client.connect(socket.gethostname(), 8081)

    except KeyboardInterrupt:
        print('Stopping daemon server.')
