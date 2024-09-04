# chatbot_api/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install necessary build tools
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./src/ /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 8000
CMD ["sh", "entrypoint.sh"]

