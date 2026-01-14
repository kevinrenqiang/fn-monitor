# ---- 构建阶段 ----
FROM registry.cn-chengdu.aliyuncs.com/zrqpublic/fn-monitor:python-3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt \
    -i http://mirrors.aliyun.com/pypi/simple \
    --trusted-host mirrors.aliyun.com

# ---- 运行阶段 ----
FROM registry.cn-chengdu.aliyuncs.com/zrqpublic/fn-monitor:python-3.11-slim
WORKDIR /app

# 1. 拷贝已安装的库
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.11/site-packages:$PYTHONPATH

# 2. 拷贝 exporter 代码
COPY exporter.py .

# 3. 容器里同样监听 7733
EXPOSE 7733
ENTRYPOINT ["python", "/app/exporter.py"]