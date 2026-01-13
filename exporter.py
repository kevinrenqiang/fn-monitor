#!/usr/bin/env python3
"""
骨架：前台 HTTP 已就位，/metrics 先返回空，
后续把任何脚本逻辑写在 collect() 里即可。
"""
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import time
import threading

# -------------------- 1. 注册指标（需要几个就加几行） --------------------
g = Gauge('demo_metric', 'demo 说明', labelnames=['label1'])

# -------------------- 2. 采集函数（以后全写这里） ------------------------
def collect():
    """
    这里随便写脚本/命令/聚合逻辑，
    最后把结果 set 到 Gauge/Counter/Histogram 里即可。
    """
    # 示例：检测 /tmp/1.txt 是否存在
    exists = os.path.exists('/tmp/1.txt')
    g.labels(label1='exist').set(0 if exists else 1)

# -------------------- 3. 定时调度（每 10 秒跑一次） ---------------------
def scheduler():
    while True:
        collect()
        time.sleep(10)
threading.Thread(target=scheduler, daemon=True).start()

# -------------------- 4. HTTP 处理器（完全照抄即可） ---------------------
class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            # 实时把内存里的指标序列化成文本
            payload = generate_latest()
            self.send_response(200)
            self.send_header('Content-Type', CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

# -------------------- 5. 启动前台 HTTP （阻塞） --------------------------
if __name__ == '__main__':
    addr = ('0.0.0.0', 7733)
    print(f'Starting exporter on {addr}/metrics')
    HTTPServer(addr, MetricsHandler).serve_forever()