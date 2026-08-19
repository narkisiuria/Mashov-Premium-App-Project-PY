import subprocess
import sys

python_exe = sys.executable

server_process = subprocess.Popen([python_exe, "server.py"])
main_process = subprocess.Popen([python_exe, "main.py"])

print("Both server.py and main.py are now running...")

try:
    server_process.wait()
    main_process.wait()
    
except KeyboardInterrupt:
    print("\nStopping both scripts...")

    server_process.terminate()
    main_process.terminate()
