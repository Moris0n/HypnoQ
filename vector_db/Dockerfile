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

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

CMD ["sh", "/app/entrypoint.sh"]

