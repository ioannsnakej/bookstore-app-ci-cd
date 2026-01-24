FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl iproute2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /bookstore
COPY . .
RUN pip install --no-cache-dir -r app/requirements.txt
ENTRYPOINT ["python", "./app/app.py"]
