import socket

def start(ip : str=socket.gethostname(), port : int=8081) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip, port))
        server_socket.listen() 
        print('Started accepting connections at {} {}'.format(ip, port))

        try:
            while True:
                client, addr = server_socket.accept()
                print('Accepted connection from {}'.format(addr))
                _serve(client, addr)

        except KeyboardInterrupt:
            print('Shutting down.')


def _serve(client : socket.socket, addr : tuple[str, int]) -> None:
    # client here is a socket object used for connecting to the client
    # addr is the ip address and the port number
    try:
        while client:
            data = client.recv(1024)
            if not data:
                print('Client at {} disconnected.'.format(addr))
                break

            print('Client@{}: {}'.format(addr[0], data.decode()))
            client.send(data)

    except ConnectionResetError as client_disconnect:
        print('Client at {} disconnected.'.format(addr))

    except Exception as unhandled:
        print(unhandled)

    finally:
        client.close()

