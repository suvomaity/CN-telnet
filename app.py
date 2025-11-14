from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from web_client import connect, send_message, upload_file, scan_ports, disconnect, exec_command, download_file
import bcrypt
import os
from werkzeug.utils import secure_filename
import time
from io import BytesIO  # For download blob

app = Flask(__name__)
app.secret_key = 'your_lab_secret_key_change_me'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

socketio = SocketIO(app, cors_allowed_origins="*")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {
    'student': bcrypt.hashpw('labpass'.encode(), bcrypt.gensalt()).decode()
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(username):
    if username in users:
        return User(username)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode()
        if username in users and bcrypt.checkpw(password, users[username].encode()):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
@login_required
def api_connect():
    host = request.json['host']
    port = request.json['port']
    print(f"[Flask] Connect: {host}:{port}")
    result = connect(host, port)
    print(f"[Flask] Connect result: {result}")
    return jsonify(result)

@app.route('/disconnect', methods=['POST'])
@login_required
def api_disconnect():
    result = disconnect()
    return jsonify(result)

@app.route('/send', methods=['POST'])
@login_required
def api_send():
    msg = request.json['message']
    print(f"[Flask] Send: {msg}")
    result = send_message(msg)
    print(f"[Flask] Send result: {result}")
    return jsonify(result)

@app.route('/upload', methods=['POST'])
@login_required
def api_upload():
    if 'file' not in request.files:
        return jsonify({"status": "Error", "error": "No file"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "Error", "error": "No file selected"})
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    print(f"[Flask] Upload: {filename}")
    result = upload_file(file_path)
    os.remove(file_path)
    print(f"[Flask] Upload result: {result}")
    return jsonify(result)

@app.route('/scan', methods=['POST'])
@login_required
def api_scan():
    host = request.json['host']
    start_str = request.json.get('start', '1')
    end_str = request.json.get('end', '100')
    try:
        start = int(start_str)
        end = int(end_str)
        if start < 1 or end > 65535 or start > end:
            return jsonify({"status": "Error", "error": "Invalid port range (1-65535)"})
        print(f"[Flask] Scan: {host} {start}-{end}")
        # UPGRADE: Pass socketio for emits
        result = scan_ports(host, start, end, socketio)
        print(f"[Flask] Scan result: {result['open_count']} open")
        socketio.emit('scan_complete', result)  # Final emit
        return jsonify(result)
    except ValueError as ve:
        return jsonify({"status": "Error", "error": str(ve)})
    except Exception as e:
        return jsonify({"status": "Error", "error": str(e)})

# NEW: Exec Route
@app.route('/exec', methods=['POST'])
@login_required
def api_exec():
    cmd = request.json['command']
    print(f"[Flask] Exec: {cmd}")
    result = exec_command(cmd)
    print(f"[Flask] Exec result: {result}")
    return jsonify(result)

# NEW: Download Route
@app.route('/download', methods=['POST'])
@login_required
def api_download():
    filename = request.json['filename']
    print(f"[Flask] Download: {filename}")
    result = download_file(filename)
    if result['status'] == 'Downloaded':
        # Send file as response for client Blob
        file_path = result['path']
        return send_file(file_path, as_attachment=True, download_name=filename)
    return jsonify(result)

@socketio.on('join_chat')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{username} has joined {room}'}, room=room)

@socketio.on('leave_chat')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{username} has left {room}'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    emit('message', data, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)