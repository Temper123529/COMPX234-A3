import threading
import socket
import time
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
class Stats:
    def __init__(self):
        self.put=self.get=self.read=0
        self.lock=threading.Lock()
stats=Stats()
def encode(msg):
    return f"{len(msg):03d}{msg}".encode()
def decode(conn):
    l=conn.recv(3)
    if not l:return None
    return conn.recv(int(l)).decode()
def handle(conn,ts):
    while True:
        msg=decode(conn)
        if not msg:break
        parts=msg.split(maxsplit=2)
        if not parts:continue
        cmd=parts[0].upper()
        res="ERROR"
        if cmd=="PUT"and len(parts)==3:
            ts.put(parts[1],parts[2])
            with stats.lock:stats.put+=1
            res="PUT_OK"
        elif cmd=="GET"and len(parts)==2:
            val=ts.get(parts[1])
            with stats.lock:stats.get+=1
            res=val if val else "NULL"
        elif cmd=="READ"and len(parts)==2:
            val=ts.read(parts[1])
            with stats.lock:stats.read+=1
            res=val if val else "NULL"
        conn.sendall(encode(res))
    conn.close()
def show_stats():
    while True:
        time.sleep(10)
        with stats.lock:
            print(f"PUT:{stats.put} GET:{stats.get} READ:{stats.read}")
if __name__ == '__main__':
    ts=TupleSpace()
    threading.Thread(target=show_stats,daemon=True).start()
    s=socket.socket()
    s.bind(('0.0.0.0',55555))
    s.listen(10)
    while True:
        conn,_=s.accept()
        threading.Thread(target=handle,args=(conn,ts)).start()