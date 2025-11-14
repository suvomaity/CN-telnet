import socket
import os

ENCODING = 'utf-8'
CHUNK_SIZE = 4096

def main():
    host = input("Enter server IP: ")
    port = int(input("Enter port: "))
    sock = establish_connection(host, port)

    while True:
        command = input(f"{host}:{port}> ")

        if command == 'quit':
            sock.send(b'quit')
            print(sock.recv(CHUNK_SIZE).decode(ENCODING))
            sock.close()
            break

        elif command.startswith("exec"):
            sock.send(command.encode(ENCODING))

            # Receive until no more data
            sock.settimeout(1)
            data_out = b""
            while True:
                try:
                    part = sock.recv(CHUNK_SIZE)
                    if not part:
                        break
                    data_out += part
                except:
                    break

            print(data_out.decode(ENCODING))


        elif command.startswith("upload"):
            filename = command.split()[1]
            sock.send(f"upload {filename}".encode(ENCODING))
            send_file(sock, filename)
            print(sock.recv(CHUNK_SIZE).decode(ENCODING))

        elif command.startswith("download"):
            filename = command.split()[1]
            sock.send(f"download {filename}".encode(ENCODING))
            recv_file(sock, filename)
            print(f"Downloaded {filename}")

        else:
            sock.send(command.encode(ENCODING))
            print(sock.recv(CHUNK_SIZE).decode(ENCODING))

def establish_connection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("[CLIENT] Connected.")
    return sock

def send_file(sock, filename):
    size = os.path.getsize(filename)
    sock.send(str(size).encode(ENCODING))
    sock.recv(1)
    with open(filename, 'rb') as f:
        sock.sendall(f.read())

def recv_file(sock, filename):
    size = int(sock.recv(CHUNK_SIZE).decode(ENCODING))
    sock.send(b"1")
    with open(filename, 'wb') as f:
        remaining = size
        while remaining > 0:
            data = sock.recv(min(CHUNK_SIZE, remaining))
            f.write(data)
            remaining -= len(data)

if __name__ == "__main__":
    main()