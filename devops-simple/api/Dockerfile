# Stage 1 : installation des dépendances
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2 : image finale légère
FROM python:3.11-slim

LABEL maintainer="devops-team@example.com" version="1.0.0"

RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser \
    && mkdir -p /app && chown appuser:appuser /app

WORKDIR /app

COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser app.py .

ENV PATH=/home/appuser/.local/bin:$PATH \
    PORT=5000 \
    APP_VERSION="1.0.0" \
    PYTHONUNBUFFERED=1

USER appuser
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
