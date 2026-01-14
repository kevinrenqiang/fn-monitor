import os

class CheckFileTask:
    """示例：探测 /tmp/1.txt 是否存在"""
    def run(self) -> int:
        return 0 if os.path.exists('/tmp/1.txt') else 1