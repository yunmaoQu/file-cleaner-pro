# 基于官方 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装依赖
RUN apt-get update && \
    apt-get install -y python3-tk libgl1-mesa-glx libmagic1 && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# 复制项目代码
COPY . .

# 设置中文环境变量
ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

# 暴露端口（如有Web服务可用）
# EXPOSE 8080

# 启动命令（如需GUI，需VNC或X11转发，默认命令如下）
CMD ["python", "main.py"] 