FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl iproute2
WORKDIR /bookstore
COPY . .
RUN pip install --no-cache-dir -r app/requirements.txt
ENTRYPOINT ["python", "./app/app.py"]
