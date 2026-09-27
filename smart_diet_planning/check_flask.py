import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 5000))
if result == 0:
    print("✓ Port 5000 is open - Flask server is running")
    sock.close()
    sys.exit(0)
else:
    print("✗ Port 5000 is closed - Flask server is not running")
    sock.close()
    sys.exit(1)
