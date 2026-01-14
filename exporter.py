#!/usr/bin/env python3
"""
通用多任务 exporter
新增任务只需写类 + 改 yaml，不动这里
"""
import time, threading, signal, sys
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from http.server import HTTPServer, BaseHTTPRequestHandler
from libs.loader import load_tasks

# 读取配置
INTERVAL, TASKS = load_tasks('config.yaml')

# 为每个任务注册一个 Gauge
gauges = {
    name: Gauge(f'task_{name}', f'Result of task {name}', labelnames=['task'])
    for name in TASKS
}

def collect():
    """轮询所有任务"""
    for name, task in TASKS.items():
        try:
            code = task.run()
            gauges[name].labels(task=name).set(code)
        except Exception as e:
            gauges[name].labels(task=name).set(-1)   # 异常时 -1
            print(f'[ERROR] {name}: {e}')

def scheduler():
    while True:
        collect()
        time.sleep(INTERVAL)

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

# 优雅退出
def shutdown(signum, frame):
    print('Shutting down...')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # 后台轮询
    threading.Thread(target=scheduler, daemon=True).start()

    # 前台 HTTP
    addr = ('0.0.0.0', 7733)
    print(f'Starting exporter on {addr}/metrics')
    HTTPServer(addr, MetricsHandler).serve_forever()