#!/usr/bin/env python3
"""
多任务、各自独立周期的 Prometheus exporter
"""
import os
import signal
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from libs.loader import load_tasks

# 注册指标表
gauges: dict[str, Gauge] = {}

# 加载任务 → [(name, task_obj, interval), ...]
TASKS = load_tasks('config.yaml')
for name, _, _ in TASKS:
    gauges[name] = Gauge(f'task_{name}', f'Result of task {name}', labelnames=['task'])

def worker(name: str, task, interval: int):
    """单个任务线程"""
    while True:
        try:
            code = task.run()
            gauges[name].labels(task=name).set(code)
        except Exception as e:
            gauges[name].labels(task=name).set(-1)
            print(f'[ERROR] {name}: {e}')
        time.sleep(interval)

# 为每个任务单独启线程
for name, task, interval in TASKS:
    threading.Thread(target=worker, args=(name, task, interval), daemon=True).start()

# HTTP 处理器
class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            payload = generate_latest()
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

def shutdown(sig, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    addr = ('0.0.0.0', 7733)
    print(f'Starting exporter on {addr}/metrics')
    HTTPServer(addr, MetricsHandler).serve_forever()