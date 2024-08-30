FROM python:3.12-slim

WORKDIR /app

COPY ./src/ /app/src

COPY ./pyproject.toml /app/pyproject.toml

COPY ./data/ /app/data

RUN pip install /app/pyproject.toml

CMD ["sh", "entrypoint.sh"]
