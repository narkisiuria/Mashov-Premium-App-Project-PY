# pythonMashovAppProject

### Latest Updates (July 21, 2026)
- Completely redesigned the app with new colors and visual aesthetics

This README describes a multi-threaded Python school management system built on a client-server architecture. 

**Features:**
* **Client:** Tkinter/TTK GUI, real-time class chat, timetable/homework reminders, and a dynamic grades/GPA calculator.
* **Server:** TLS/SSL encryption over TCP, multi-threaded user handling, automated IP/account blocking after 4 failed login attempts, and a thread-safe JSON database.

**Structure & Requirements:**
Includes `main.py`, `server.py`, helper modules, a custom stress-test tool, JSON data files, and local SSL certificates. Requires only Python 3.x and standard libraries (`socket`, `ssl`, `tkinter`, `threading`, `json`, `os`).

**How to Run:**
1. Start the server first (`python server.py`).
2. Launch the client in a new terminal (`python main.py`).
Ensure SSL certificates are correctly placed in the `keys/` directory before execution.