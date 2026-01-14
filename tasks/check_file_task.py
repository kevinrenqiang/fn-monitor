import os

class CheckFileTask:
    def run(self) -> int:
        return 0 if os.path.exists('/tmp/1.txt') else 1