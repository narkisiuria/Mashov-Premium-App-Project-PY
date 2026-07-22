# Mashov System Project

A multi-threaded school management system built entirely in Python. I developed this project using a client-server architecture to handle school schedules, grades, and real-time class communication securely.

## Features

**Client-Side**

* Clean GUI built natively with Tkinter and TTk.
* Real-time class chat room.
* Timetable and homework reminder system.
* Dynamic grades viewer and GPA calculator.

**Server-Side**

* Full TLS/SSL encryption over TCP sockets.
* Multi-threaded architecture to handle multiple users simultaneously.
* Bruteforce protection (automatically blocks accounts/IPs after 4 failed attempts).
* Thread-safe JSON database using `threading.Lock`.

## Project Structure

* `main.py` - The client application.
* `server.py` - The backend server node.
* `utils/` - Hashing algorithms and helper modules.
* `tools/strength.py` - A custom stress-testing tool to measure server limits.
* `data/` - JSON databases (users, schedules, tasks, and connection logs).
* `keys/` - Local SSL certificates (`server.crt`, `server.key`).

## Requirements

The project relies on standard native Python libraries. You only need **Python 3.x** installed. No heavy external dependencies are required.

Modules used: `socket`, `ssl`, `tkinter`, `threading`, `json`, `os`.

## How to Run

1. **Start the Server**
   The central server must be running before any client can connect.
   ```bash
   python server.py
   ```

2. **Start the Client**
   Open a new terminal window and run the main application.
   ```bash
   python main.py
   ```
   
Note: Ensure the SSL certificates are properly located inside the keys/ directory before starting the server.