import socket
import time

time.sleep(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 5000))
if result == 0:
    print("[OK] Port 5000 is open - Flask server is running")
    
    # Send simple HTTP GET request
    request = b"GET / HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nConnection: close\r\n\r\n"
    sock.sendall(request)
    
    # Receive response
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    
    response_str = response.decode('utf-8', errors='ignore')
    
    if "200 OK" in response_str:
        print("[OK] Homepage returned HTTP 200")
    
    if "Enter Your Details" in response_str:
        print("[OK] Form HTML found in response")
    else:
        print("[ERROR] Form HTML not found")
        print("Response preview:", response_str[:500])
    
    sock.close()
else:
    print("[ERROR] Port 5000 is closed - Flask server is not responding")
