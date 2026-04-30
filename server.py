import threading
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
if __name__ == '__main__':
    print("TupleSpace Loaded")