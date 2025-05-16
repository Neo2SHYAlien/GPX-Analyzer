import time

class Timer:
    def __init__(self, log_file="execution_log.txt"):
        self.start = time.perf_counter()
        self.log_file = log_file
        with open(self.log_file, "w") as f:
            f.write("---- GPX Analyzer Execution Log ----\n")

    def log(self, label):
        now = time.perf_counter()
        elapsed = now - self.start
        message = f"[⏱️] {label}: {elapsed:.3f} s"
        print(message)
        with open(self.log_file, "a") as f:
            f.write(message + "\n")
        self.start = now
