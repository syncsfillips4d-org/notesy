FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN pip install \
    "fastapi>=0.115" \
    "uvicorn[standard]>=0.32" \
    "jinja2>=3.1" \
    "python-multipart>=0.0.12" \
    "strawberry-graphql[fastapi]>=0.245" \
    "anthropic>=0.40" \
    "itsdangerous>=2.2"

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
