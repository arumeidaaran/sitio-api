FROM python:3.14-slim

ARG SITIO_API_VERSION

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        --no-install-recommends \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN python -m pip install \
        --no-cache-dir \
        --group prd \
    && python -m pip check

COPY . .

RUN mkdir -p /app/config

RUN test -n "${SITIO_API_VERSION}" \
    && test \
        "$(python -c 'from __version__ import __version__; print(__version__)')" \
        = "${SITIO_API_VERSION}"

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:5000/api/v1/health/', timeout=3).close()"]

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
