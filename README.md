# Mashov Premium Mobile/Desktop App Project

An advanced, multi-threaded school management system built entirely in Python. **Mashov+ Premium** reimagines the original "Mashov" platform using a high-performance, secure client-server architecture capable of handling active student connections, real-time communication, and data distribution.

---

## 🚀 Key Features

### 🖥️ Premium Client-Side Experience
*   **Modern Desktop Interface:** A fast, native GUI engineered cleanly using Tkinter and TTK.
*   **Real-Time Class Chat:** Instant classroom messaging channels built directly over low-latency socket networking.
*   **Academic Planner:** Built-in homework reminder engine and automated school timetable management.
*   **Performance Metrics:** Dynamic school grade viewer paired with an instant GPA calculator.

### 🛡️ Enterprise-Grade Server Security
*   **End-to-End TLS/SSL:** Full cryptographic encryption layer protecting all data traveling over raw TCP sockets.
*   **High Concurrency:** Multi-threaded pooling architecture designed to manage dozens of simultaneous clients without dropping packets.
*   **Bruteforce Defense:** Automated security middleware that blocks malicious accounts or flood-heavy IPs after 4 consecutive failed authentications.
*   **Thread-Safe State Management:** Zero-dependency database reads and writes powered safely by `threading.Lock` to completely prevent race conditions or database corruption.

---

## 📂 Project Structure

```text
Mashov-Premium-App-Project-PY/
├── assets/                 # App icons, visual assets, and theme components
├── utils/                  # Core cryptographic modules and system helpers
│   ├── hashingAlg.py       # Custom password hashing algorithms
│   └── src.py              # Central utilities and shared runtime code
├── app_runner.py           # Global bootstrapper script
├── main.py                 # Core Client application launcher
├── flet_main.py            # Experimental alternative UI entrypoint
├── server.py               # Master Backend Server node
├── .gitignore              # Configured repository filter rules
└── README.md               # Project documentation
```

> **Note on Data Privacy:** Local database engines (`data/`), encryption keys (`keys/`), dependencies (`kivy_env/`), and compiler cache artifacts (`build/`, `__pycache__/`) are intentionally decoupled from the source tree to ensure local deployment isolation.

---

## 🛠️ Requirements & System Setup

The project relies entirely on Python's native ecosystem. There are **zero heavy external dependencies** to manage.

*   **Runtime Environment:** Python 3.10 or higher.
*   **Standard Library Footprint:** `socket`, `ssl`, `tkinter`, `threading`, `json`, `os`.

---

## 💻 How to Run the App Local Environment

To spin up the network architecture locally, run the components inside separate terminal windows inside your workspace:

### 1. Initialize Local Secrets
Before starting the backend infrastructure, make sure to generate or place your local TLS certificates inside a root folder named `keys/`. The server expects to bind using:
*   `keys/server.crt`
*   `keys/server.key`

### 2. Boot up the Backend Core
Just run the premade app runner and the frontend + backend will boot:
```bash
python app_runner.py
```

## 🌐 External Reference
For information regarding the original production system and reference specifications, check out the [Official Mashov Portal](https://mashov.info).
