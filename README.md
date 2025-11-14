Here is a **more elaborate, polished, and professional README.md**, formatted perfectly for GitHub.
You can **copy-paste directly into your repo**.

---

# 🌐 CN-Telnet-Web

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-Real--Time-black.svg)](https://socket.io/)

A **modern, web-based frontend** for the original **[CN-telnet](https://github.com/mies47/CN-telnet)** peer-to-peer telnet implementation.
This project transforms the classic CLI-based CN telnet lab into a **user-friendly, interactive platform** that is perfect for:

* Computer Networks practicals
* TCP socket experimentation
* Remote execution labs
* Real-time communication demos
* Complete mini “network toolkit” project for college

Built using **Flask**, **SocketIO**, **Bootstrap**, and **Chart.js**.

---

## 🚀 Why CN-Telnet-Web?

The traditional CN telnet programs run purely on CLI.
This project enhances it with:

* A modern Web UI
* Real-time communication
* Port scanning dashboard
* Remote command execution
* File upload/download
* Multi-user chat
* Device-to-device testing

This makes it perfect for **college submissions, lab demos, viva, and portfolio projects**.

---

## ✨ Features

### 🔐 Authentication

* Simple login system (default: `student` / `labpass`)
* Protects dashboard and telnet routes

### 🖥️ Telnet Core Operations

* Connect to P2P server
* Send/receive messages
* Execute remote commands (e.g., `ls`, `whoami`, `dir`)
* Upload files to remote server
* Download files from server

### 🔍 Port Scanner

* Fast TCP port scanning using Python sockets
* Displays real-time progress
* Beautiful **Chart.js** bar graph for open ports

### 💬 Real-Time Chat (SocketIO Rooms)

* Join rooms like `"lab_group"`
* Broadcast telnet results for group debugging
* Test multi-user chat across devices

### 📱 Responsive Web UI

* Built with Bootstrap 5 + custom dark theme
* Works on laptops, tablets, and phones

### 🌐 Cross-Network Support

* Works across LAN/Wi-Fi
* Tested on devices with different OS (Windows/Linux)

---

## 🖼️ Screenshots

| Dashboard                    | Port Scanner                      | Chat Room                      |
| ---------------------------- | --------------------------------- | ------------------------------ |
| ![](screenshots/main_ui.png) | ![](screenshots/scan_results.png) | ![](screenshots/chat_room.png) |

---

## 🌍 Live Demo

> **Hosted on Render** (free tier, may spin down after inactivity)
> 🔗 [https://cn-telnet-web.onrender.com](https://cn-telnet-web.onrender.com)

Refresh the page once if the server is waking from sleep.

---

# 📦 Installation

## 1️⃣ Prerequisites

* Python **3.8+**
* Git
* Optional: PostgreSQL (for history logging)

---

## 2️⃣ Clone This Repository

```bash
git clone https://github.com/suvomaity/CN-Telnet-Web.git
cd CN-Telnet-Web
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Download CN-Telnet Backend (Optional)

You may use:

* The **original CN-telnet repo**, or
* The **minimal server included in this project**

Original repo:

```
https://github.com/mies47/CN-telnet
```

---

# ▶️ Running the Project

## Terminal 1 — Start Telnet Server

```bash
python main.py server 8080
```

* Runs on `0.0.0.0:8080`
* Clients can connect using IP:8080

---

## Terminal 2 — Start Web Frontend

```bash
python app.py
```

Access the UI at:
👉 **[http://localhost:5000](http://localhost:5000)**

---

# 📘 Usage Guide

## 🔑 1. Login

Default credentials:

```
username: student
password: labpass
```

---

## 🔌 2. Connect to CN-Telnet Server

* Host: `127.0.0.1` (for local testing)
* Or: Server Machine IP (for LAN testing)
* Port: `8080`

---

## 🛠️ 3. Operations Available

### ✔ Send Message

Sends text to server → echoed back.

### ✔ Execute Command

Examples:

* `whoami`
* `ls`
* `dir`
* `ipconfig`
* `uname -a`

### ✔ Upload File

* Small files recommended (<1 MB)

### ✔ Download File

* Specify filename → auto-saved in `/downloads/`

### ✔ Scan Ports

* Enter host and port range
* Watch real-time logs
* View bar chart of open ports

### ✔ Real-Time Chat

* Create/join room (`lab`, `group1`, etc.)
* Multi-tab/device instant communication

---

# 🧪 Cross-Device / LAN Testing

### On server laptop:

```
python main.py server 8080
```

Check local IP:

```
ipconfig   # Windows
ifconfig   # Linux/Mac
```

### On client laptop:

Enter:

```
<server-ip>:8080
```

🔔 Important: Disable firewall or allow Python through.

---

# 🌍 Remote Demo Options

### ✔ ngrok (recommended)

```
./ngrok http 5000
```

Share public URL.

### ✔ GitHub Codespaces

* Open repo in Codespaces
* Flask auto-detects forwarded ports

---

# 🗃️ Database Support (Optional)

If you want logs/history in PostgreSQL:

1. Create DB:

```
createdb telnet_history
```

2. Update credentials in `main.py`
3. Uncomment DB code block

If not needed → keep disabled.

---

# 🛠️ Troubleshooting

| Issue                  | Fix                                            |
| ---------------------- | ---------------------------------------------- |
| **Connection Refused** | Server not running / wrong IP / firewall block |
| **No Exec Output**     | Use patched `main.py` with `.strip()` fix      |
| **Port Scan Slow**     | Reduce range (1–100 fast)                      |
| **Chat Not Syncing**   | Check SocketIO JavaScript loaded properly      |
| **Upload Fails**       | File too large / permission issue              |

---

# 🤝 Contributing

1. Fork this repository
2. Create feature branch:

   ```
   git checkout -b feature/my-update
   ```
3. Commit changes:

   ```
   git commit -m "Add new feature"
   ```
4. Push:

   ```
   git push origin feature/my-update
   ```
5. Create Pull Request
6. Tag: **@suvomaity**

Ideas for enhancement:

* End-to-end encryption
* Complete activity logs
* REST API endpoints
* User account system
* Built-in terminal console

---

# 📄 License

Distributed under the **MIT License**.
See `LICENSE` for details.

---

# 🙌 Acknowledgments

* Original CN-telnet project → [https://github.com/mies47/CN-telnet](https://github.com/mies47/CN-telnet)
* Flask Web Framework
* Bootstrap for UI
* Chart.js for port scan visualization
* SocketIO for real-time chat

---

# ⭐ If you like this project, give it a star on GitHub!

Let me know if you want:
✔ Better screenshots
✔ A project logo/banner
✔ A downloadable PDF version of README
✔ Auto-deployment GitHub Actions setup

Just tell me!
