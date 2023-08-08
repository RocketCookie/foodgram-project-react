FROM python:3.11-slim
WORKDIR /app
COPY requirements-docker.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements-docker.txt --no-cache-dir
COPY . .
RUN apt update && apt install -y make
CMD ["make", "run"]