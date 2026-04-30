import socket
def encode(msg):
    return f"{len(msg):03d}{msg}".encode()
def decode(conn):
    l = conn.recv(3)
    if not l: return None
    return conn.recv(int(l)).decode()
if __name__ == '__main__':
    c = socket.socket()
    c.connect(('127.0.0.1', 55555))
    print("Connected")
    c.close()