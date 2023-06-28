# 使用官方的python镜像作为基础
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录 
COPY . . 
 
# 安装构建所需依赖项
RUN pip install requests httpx fastapi uvicorn jinja2 ujson redis python-dotenv uvicorn[standard]

# 设置环境变量
ENV REDIS_HOST="192.168.2.101"
ENV REDIS_PORT="6379"
ENV REDIS_DB="0"
ENV REDIS_PASS=""
ENV AISET="192.168.2.101:8096"
ENV AISET2="192.168.2.101:8096"
ENV AISET3="192.168.2.101:8096"
ENV AISET4="192.168.2.101:8096"

# 暴露端口
EXPOSE 20235

# 运行主文件
CMD ["python", "main.py"]
