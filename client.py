import socket
import random
import time
import threading

HOST = '127.0.0.1'
PORT = 666


def client_thread():
    time.sleep(random.randint(0, 20))   # Случайная задержка
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send('Hello!'.encode())
    response = sock.recv(4096)
    print(response.decode())
    sock.close()


def main():
    thread_list = []
    for i in range(1000):
        thread_list.append(threading.Thread(target=client_thread))
    for thread in thread_list:
        thread.start()


if __name__ == '__main__':
    main()
