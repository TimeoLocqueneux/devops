FROM python:3.11-alpine

LABEL maintainer="devops-team@example.com" version="1.0.0"

RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser \
    && mkdir -p /app && chown appuser:appuser /app

WORKDIR /app
COPY --chown=appuser:appuser worker.py .

ENV PYTHONUNBUFFERED=1
USER appuser

CMD ["python", "-u", "worker.py"]
