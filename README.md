# fn-monitor
# 1. 把上面两个文件放同一目录
ls
Dockerfile  exporter.py  requirements.txt

# 2. 构建镜像
docker build -t py-file-exporter:1.0 .

# 3. 启动（/tmp/1.txt 在宿主机，挂进去就能检测到）
docker run -d --restart=unless-stopped \
  -p 7733:7733 \
  -v /tmp:/tmp:ro \
  --name file-exporter \
  py-file-exporter:1.0

# 4. 验证
curl localhost:7733/metrics