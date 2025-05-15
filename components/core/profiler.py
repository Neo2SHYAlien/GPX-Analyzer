import time

class Timer:
    def __init__(self):
        self.start = time.perf_counter()
    
    def log(self, label):
        now = time.perf_counter()
        print(f"[⏱️] {label}: {now - self.start:.3f} s")
        self.start = now
