FROM python:3.9-slim AS base

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY google_domain_ddns.py .

CMD [ "python", "google_domain_ddns.py" ]


FROM python:3.9-slim AS test

WORKDIR /usr/src/app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt -r requirements.txt

COPY google_domain_ddns.py .
COPY tests/ .

ENTRYPOINT [ "pytest" ]
