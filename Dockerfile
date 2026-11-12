FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir boto3

RUN useradd --create-home appuser

COPY --chown=appuser:appuser hello.py .

USER appuser

ENTRYPOINT ["python", "hello.py"]
