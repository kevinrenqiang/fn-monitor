import subprocess

class KubectlVersionTask:
    """调用宿主机 kubectl version，只要命令本身能跑通就返回 0"""
    def run(self) -> int:
        try:
            r = subprocess.run(
                ['/host/usr/bin/kubectl', 'version', '--client=true', '--request-timeout=3s'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return 0 if r.returncode == 0 else 1
        except Exception:
            return 1