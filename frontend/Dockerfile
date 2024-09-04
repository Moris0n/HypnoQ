# frontend/Dockerfile
FROM python:3.12-slim
WORKDIR /app

COPY ./src/ /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

CMD ["sh", "entrypoint.sh"]