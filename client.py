import socket

HOST = '127.0.0.1'
PORT = 666


def main():
    while True:
        request = input('Input request: ')
        if request != 'exit':
            sock = socket.socket()
            sock.connect((HOST, PORT))
            sock.send(request.encode())
            response = sock.recv(4096)
            print(response.decode())
            sock.close()


if __name__ == '__main__':
    main()
