import socket

def connect(server_addr : tuple[str, int]) -> None:
    try:
        with socket.create_connection(server_addr) as tcp_service:
            while True:
                user_input = input('To quit, type QUIT\n')
                if user_input == 'QUIT':
                    break

                # add stuff here

                tcp_service.send(user_input.encode())
                response = tcp_service.recv(1024)
                print('Server echoed: {}'.format(response.decode()))

    except KeyboardInterrupt:
        print('Shutting down.')

