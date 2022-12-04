from hashlib import new
from cryptography.fernet import Fernet
import socket
import base64

PORT = 8080
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)
HEADER = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def encrypt_with_key(challenge, password):
    passhash = new("md5", password.encode(FORMAT)).hexdigest()
    key = base64.urlsafe_b64encode(passhash.encode(FORMAT))
    f = Fernet(key)
    token = f.encrypt(challenge)
    return token

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"connected")

    connected = True
    while connected:
        msg = input("username: ")
        client.send(msg.encode(FORMAT))
        challenge = client.recv(HEADER)
        password = input("password: ")
        resp = encrypt_with_key(challenge, password)
        client.send(resp)
        resp = client.recv(HEADER).decode(FORMAT)
        print(resp)
        client.send(DISCONNECT_MSG.encode(FORMAT))
        connected = False

if __name__ == "__main__":
    main()