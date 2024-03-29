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

        server_addr = (socket.gethostname(), 8081)
        client.connect(server_addr)

    except KeyboardInterrupt:
        print('Stopping daemon server.')
