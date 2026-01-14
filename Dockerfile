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

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.11/site-packages:$PYTHONPATH

# 拷贝全部项目文件
COPY . .

EXPOSE 7733
ENTRYPOINT ["python", "/app/exporter.py"]