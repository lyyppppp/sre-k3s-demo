FROM docker.m.daocloud.io/library/python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 60 --retries 10 -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
