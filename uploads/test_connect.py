import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('127.0.0.1', 8080))
    print("Connected OK!")
    s.close()
except Exception as e:
    print(f"Connect failed: {e}")