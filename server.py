import socket
import threading
import random
import string
import base64
from hashlib import new
from cryptography.fernet import Fernet

PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


users = {
    "karolwojtyla": "1232137",
    "barrackobama": "obamacare",
    "lechwalesa": "motorowka12"
}
def decrypt_with_key(challenge, password):
    passhash = new("md5", password.encode(FORMAT)).hexdigest()
    key = base64.urlsafe_b64encode(passhash.encode(FORMAT))
    f = Fernet(key)
    token = f.decrypt(challenge)
    return token

def handle_client(conn, addr):
    print(f"New connection from{addr}")
    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        challenge = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
        user = msg
        conn.send(challenge.encode(FORMAT))
        challenge_resp = conn.recv(HEADER)
        try:
             decrypt_with_key(challenge_resp, users[user])
        except:
            conn.send(DISCONNECT_MSG.encode(FORMAT))
            connected = False

        if decrypt_with_key(challenge_resp, users[user]) == challenge.encode(FORMAT):
            msg = f'super secret data for {user}'
            conn.send(msg.encode(FORMAT))
    
    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(ADDR)
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()