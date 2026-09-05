FROM python:3.14-slim

ARG SITIO_API_BRANCH=main

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        --no-install-recommends \
        ca-certificates \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone \
    --branch "${SITIO_API_BRANCH}" \
    --single-branch \
    https://github.com/arumeidaaran/sitio-api.git \
    .

RUN python -m pip install \
        --no-cache-dir \
        --group prd \
    && python -m pip check

COPY config/profile-config.json /app/config/profile-config.json

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:5000/api/v1/health/', timeout=3).close()"]

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
