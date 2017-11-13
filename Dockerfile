FROM python:3.6.3-jessie

MAINTAINER Alex van der Wal

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y dos2unix

WORKDIR iframe/src
COPY . .
COPY ./src/docker-entrypoint.sh /src/docker-entrypoint.sh

RUN pip install -r requirements.txt
RUN chmod +x src/docker-entrypoint.sh
RUN dos2unix /src/docker-entrypoint.sh && apt-get --purge remove -y dos2unix

EXPOSE 8000

ENTRYPOINT ["/src/docker-entrypoint.sh"]


