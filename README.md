# Mashov System Project

A secure, multi-threaded school management system built in Python. This project utilizes a client-server architecture featuring an interactive Graphical User Interface (GUI) for users and a robust backend server powered by secure TLS socket communication.

---

## 🚀 Key Features

### Client-Side (GUI)
* **Interactive Dashboard:** Built using Tkinter and TTK, providing modern transitions and a streamlined user flow.
* **Timetable & Reminders:** Real-time school schedule tracker filtered by class and day, alongside homework and exam reminders.
* **Grades System:** Dynamic data viewing with built-in logic for grade management and GPA calculations.
* **Built-in Assistant:** An integrated help chatbot module to easily guide students and staff through the application.

### Server-Side (Backend)
* **Encrypted Communication:** Full TLS/SSL encryption over standard TCP sockets utilizing localized certificate chains.
* **Brute-Force Prevention:** Active tracking mechanism that automatically blocks suspicious IPs or accounts after exceeding the failed login attempt limit (`max = 4`).
* **Multi-Threaded Architecture:** Concurrently processes multiple incoming client requests without blocking operations.
* **Thread-Safe Database Locks:** Uses synchronization locks (`threading.Lock`) to ensure safe data read/write transactions into JSON files, preventing race conditions.

---

## 📂 Project Directory Structure

### Core Codebase

| File Name | Component | Description |
| :--- | :--- | :--- |
| `main.py` | Client | The entry point of the app. Manages the GUI screens (Login, Registration, Dashboard, Chatbot) and client-side TLS sockets. |
| `server.py` | Server | The core backend service. Controls user validation, multi-threaded request routing, log recording, and rate limiting. |
| `src.py` | Logic | Handles internal arithmetic calculations, grades analysis, and average computation tasks. |
| `getServersStrength.py` | Utility | A dedicated multi-threaded stress-testing tool used to measure server limits and strength. |
| `test.py` | Testing | A small utility script used for prototyping and generating random password strengths. |

### Data & Security Layer

| Asset Path | Format | Description |
| :--- | :--- | :--- |
| `data/users.json` | Database | Stores user metadata, access roles, and securely hashed credentials. |
| `data/schedule.json` | Database | Contains structured classroom timetables broken down by class names and week days. |
| `data/reminder.json` | Database | Holds assignment descriptions, dates, and student task logs. |
| `data/server_connection_logs.json` | Log | Automatically registers client IPs, timestamps, and login session statuses. |
| `keys/server.crt` & `keys/server.key` | Credentials | Local SSL/TLS certificate pairs ensuring a safe and fully encrypted network tunnel. |

---

## 🛠️ Getting Started

### Prerequisites
This project requires **Python 3.x** installed on your system. It relies heavily on standard native libraries, meaning no heavy external dependencies are required:
* `socket` & `ssl` (Secure Networking)
* `tkinter` & `ttk` (Graphical Desktop Interface)
* `threading` (Asynchronous Client Management)
* `json` & `os` (Local Data Operations)

### Installation & Execution

1. **Launch the Backend Server:**
   Start the centralized listening node before launching any client applications.
   ```bash
   python server.py
