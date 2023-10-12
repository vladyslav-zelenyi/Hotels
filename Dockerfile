# syntax=docker/dockerfile:1
FROM python:3.11-alpine

WORKDIR /code

COPY . .

RUN pip install poetry
RUN pip install python-dotenv
RUN poetry config virtualenvs.create false && poetry install
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
