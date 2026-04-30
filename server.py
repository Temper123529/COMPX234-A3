import threading
import socket
class TupleSpace:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
    def put(self, k, v):
        with self.lock:
            if k not in self.data:
                self.data[k] = v
                return True
            return False
    def get(self, k):
        with self.lock:
            return self.data.pop(k, None)
    def read(self, k):
        with self.lock:
            return self.data.get(k, None)
def encode(msg):
    return f"{len(msg):03d}{msg}".encode()
def decode(conn):
    l = conn.recv(3)
    if not l: return None
    return conn.recv(int(l)).decode()
def handle(conn, ts):
    while True:
        msg = decode(conn)
        if not msg: break
        conn.sendall(encode("OK"))
    conn.close()
if __name__ == '__main__':
    ts = TupleSpace()
    s = socket.socket()
    s.bind(('0.0.0.0', 55555))
    s.listen(5)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle, args=(conn, ts)).start()