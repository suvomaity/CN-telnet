import socket
import threading
import os
import time
import socketio  # For emit in scan (import in app.py too)

CHUNK_SIZE = 4096  # Match original

# Global session
current_sock = None
lock = threading.Lock()

def connect(host, port):
    global current_sock
    with lock:
        try:
            current_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            current_sock.settimeout(5.0)  # For recv responses
            current_sock.connect((host, int(port)))
            print(f"Connected to {host}:{port}")  # Debug
            return {"status": "Connected", "error": None}
        except Exception as e:
            print(f"Connect error: {e}")
            return {"status": "Error", "error": str(e)}

def disconnect():
    global current_sock
    with lock:
        if current_sock:
            current_sock.close()
            current_sock = None
            return {"status": "Disconnected"}
    return {"status": "Error", "error": "Not connected"}

def recv_full(sock):
    """Recv until timeout/empty, like original recv_message (no encrypt)"""
    full_text = b''
    while True:
        try:
            data = sock.recv(CHUNK_SIZE)
            if not data:
                break
            full_text += data
        except socket.timeout:
            break
        except Exception as e:
            print(f"Recv error: {e}")
            break
    return full_text.decode('utf-8', errors='ignore').strip()

def send_message(msg):
    global current_sock
    if not current_sock:
        return {"status": "Error", "error": "Not connected"}
    with lock:
        try:
            # Send padded command: 'send message ' + spaces to 4096
            command = "send message "
            padded_cmd = command + ' ' * (CHUNK_SIZE - len(command))
            current_sock.send(padded_cmd.encode('utf-8'))
            print(f"Sent command: {command}")  # Debug

            # Send body: msg + \r\n + padded spaces (simulate single-line multi-input)
            body = msg + '\r\n'
            padded_body = body + ' ' * (CHUNK_SIZE - len(body))
            current_sock.send(padded_body.encode('utf-8'))
            print(f"Sent body: {msg}")  # Debug

            # Recv response
            response = recv_full(current_sock)
            print(f"Response: {response}")  # Debug
            return {"status": "Sent", "response": response or "No response"}
        except Exception as e:
            print(f"Send error: {e}")
            return {"status": "Error", "error": str(e)}

def upload_file(file_path):
    global current_sock
    if not current_sock:
        return {"status": "Error", "error": "Not connected"}
    filename = os.path.basename(file_path)
    if not os.path.exists(file_path):
        return {"status": "Error", "error": "File not found"}
    with lock:
        try:
            # Send padded command: 'upload' + filename + spaces to 4096 (len('upload')=6)
            cmd_len = 6 + len(filename)
            padded_cmd = 'upload' + filename + ' ' * (CHUNK_SIZE - cmd_len)
            current_sock.send(padded_cmd.encode('utf-8'))
            print(f"Sent upload cmd for {filename}")  # Debug

            # Send padded size
            size = os.path.getsize(file_path)
            size_str = str(size)
            padded_size = size_str + ' ' * (CHUNK_SIZE - len(size_str))
            current_sock.send(padded_size.encode('utf-8'))
            print(f"Sent size: {size}")  # Debug

            # Send binary chunks
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(CHUNK_SIZE)
                    if not data:
                        break
                    current_sock.send(data)
            print(f"Uploaded {filename} ({size} bytes)")  # Debug

            # Recv response
            response = recv_full(current_sock)
            print(f"Upload response: {response}")  # Debug
            return {"status": "Uploaded", "response": response}
        except Exception as e:
            print(f"Upload error: {e}")
            return {"status": "Error", "error": str(e)}

# NEW: Exec Command
# ... (rest unchanged from last)

def exec_command(cmd):
    global current_sock
    if not current_sock:
        return {"status": "Error", "error": "Not connected"}
    with lock:
        try:
            full_cmd = f"exec {cmd}"
            padded_cmd = full_cmd + ' ' * (CHUNK_SIZE - len(full_cmd))
            current_sock.send(padded_cmd.encode('utf-8'))
            print(f"Sent exec: {cmd}")  # Debug

            # Recv with more buffer/time for multi-line response
            current_sock.settimeout(10.0)  # Increase for response
            full_text = b''
            start_time = time.time()
            while time.time() - start_time < 10:  # 10s total
                try:
                    data = current_sock.recv(CHUNK_SIZE)
                    if not data:
                        break
                    full_text += data
                except socket.timeout:
                    break
                except Exception as e:
                    print(f"Recv error: {e}")
                    break
            response = full_text.decode('utf-8', errors='ignore').strip()
            print(f"Raw response bytes len: {len(full_text)}")  # NEW DEBUG
            print(f"Decoded raw: {repr(response[:200])}")  # NEW DEBUG (truncate)
            current_sock.settimeout(5.0)  # Reset
            return {"status": "Executed", "response": response or "No output"}
        except Exception as e:
            print(f"Exec error: {e}")
            return {"status": "Error", "error": str(e)}
# NEW: Download File
def download_file(filename):
    global current_sock
    if not current_sock:
        return {"status": "Error", "error": "Not connected"}
    with lock:
        try:
            # Send padded command: 'download' + filename + spaces
            full_cmd = f"download {filename}"
            padded_cmd = full_cmd + ' ' * (CHUNK_SIZE - len(full_cmd))
            current_sock.send(padded_cmd.encode('utf-8'))
            print(f"Sent download: {filename}")  # Debug

            # Recv size (padded)
            size_str = recv_full(current_sock).strip()
            size = int(size_str)
            print(f"Recv size: {size}")  # Debug

            # Recv binary chunks
            downloaded_data = b''
            remaining = size
            while remaining > 0:
                chunk = current_sock.recv(min(CHUNK_SIZE, remaining))
                if not chunk:
                    break
                downloaded_data += chunk
                remaining -= len(chunk)

            # Save locally
            local_path = os.path.join('downloads', filename)  # Create dir if needed
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(downloaded_data)
            print(f"Downloaded {filename} ({len(downloaded_data)} bytes) to {local_path}")  # Debug
            return {"status": "Downloaded", "file": filename, "path": local_path, "size": len(downloaded_data)}
        except Exception as e:
            print(f"Download error: {e}")
            return {"status": "Error", "error": str(e)}

def scan_ports(host, start_port=1, end_port=100, sio=None):  # sio for emit
    try:
        socket.gethostbyname(host)  # Validate host
    except socket.gaierror:
        raise ValueError(f"Invalid host: {host} (unresolvable)")
    open_ports = []
    total = end_port - start_port + 1
    for i, port in enumerate(range(start_port, end_port + 1)):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass

        # UPGRADE: Emit progress every 10 ports
        if sio and (i + 1) % 10 == 0:
            progress = ((i + 1) / total) * 100
            sio.emit('scan_update', {'progress': progress, 'open_count': len(open_ports)}, namespace='/')

    return {
        "status": "Scanned",
        "open_ports": open_ports,
        "total_ports": total,
        "open_count": len(open_ports)
    }