import socket
from select import select

tasks = []      # Список задач(генераторов), которые готовы к выполнению

to_read = {}
to_write = {}

HOST = 'localhost'
PORT = 666


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    while True:
        yield 'read', server_socket
        client_socket, addr = server_socket.accept()
        print('Connection from', addr)
        tasks.append(client(client_socket))     # Добавляем задачу(генератор)


def client(client_socket):
    while True:

        yield 'read', client_socket
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = request.decode().upper().encode()
            yield 'write', client_socket
            client_socket.send(response)

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:

            # Мониторим сокеты, готовые к операциям
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            # Наполняем список задачами(генераторами), которые готовы к выполнению
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            # Извлекаем и выполняем задачу(генератор), которая возвращает сокет
            task = tasks.pop(0)
            reason, sock = next(task)

            # Наполняем список сокетов для мониторинга
            if reason == 'read':
                to_read[sock] = task
            if reason == 'write':
                to_write[sock] = task

        except StopIteration:
            print('Done!')


tasks.append(server())      # Добавляем задачу(генератор)
event_loop()
