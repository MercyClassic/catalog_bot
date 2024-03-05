FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTEDECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt
COPY ./docker/entrypoint.sh /app/entrypoint.sh

RUN apt update \
    && apt install -y libmagic1 \
    && useradd -U app \
    && chown -R app:app /app \
    && pip install -r /app/requirements.txt

COPY --chown=app:app . /app

WORKDIR /app/src

USER app

CMD [ "sh", "/app/entrypoint.sh" ]
