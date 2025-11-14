import socket
import subprocess
import threading
import os

ENCODING = 'utf-8'
CHUNK_SIZE = 4096

def main():
    port = int(input("Enter port to start server on (ex: 23): "))
    server_mode(port)

def server_mode(port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen()
        print(f"[SERVER] Telnet server running on port {port}")

        while True:
            connection, info = server_socket.accept()
            print(f"[+] Client {info[0]}:{info[1]} Connected.")
            threading.Thread(target=client_handler, args=(connection,)).start()

    except Exception as exc:
        print(f"Server Error: {exc}")

def client_handler(conn):
    while True:
        try:
            data = conn.recv(CHUNK_SIZE).decode(ENCODING)

            if not data:
                break

            if data.startswith('exec'):
                command = data.replace('exec ', '')
                output = exec_command(command)
                conn.sendall(output.encode(ENCODING))


            elif data.startswith('upload'):
                filename = data.replace('upload ', '').strip()
                recv_file(conn, filename)
                conn.send(b"[Server] File received successfully.\n")

            elif data.startswith('download'):
                filename = data.replace('download ', '').strip()
                send_file(conn, filename)

            elif data == 'quit':
                conn.send(b"[Server] Closing connection.\n")
                conn.close()
                break

            else:  
                conn.send(f"[Server] Received: {data}\n".encode(ENCODING))

        except:
            conn.close()
            break

def exec_command(cmd):
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode(ENCODING) + result.stderr.decode(ENCODING)

def send_file(conn, path):
    size = os.path.getsize(path)
    conn.send(str(size).encode(ENCODING))
    conn.recv(1)
    with open(path, 'rb') as f:
        conn.sendall(f.read())

def recv_file(conn, filename):
    size = int(conn.recv(CHUNK_SIZE).decode(ENCODING))
    conn.send(b"1")
    with open(filename, 'wb') as f:
        remaining = size
        while remaining > 0:
            data = conn.recv(min(CHUNK_SIZE, remaining))
            f.write(data)
            remaining -= len(data)

if __name__ == "__main__":
    main()
