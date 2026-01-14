import subprocess

class KubectlVersionTask:
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