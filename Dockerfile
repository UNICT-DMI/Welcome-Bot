FROM python:3-slim
WORKDIR /bot/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "/bot/src/main.py"]