FROM python:3.8.7-slim-buster AS build-python
COPY ./requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.8.7-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
COPY --from=build-python /wheels /wheels
COPY --from=build-python requirements.txt .
RUN pip install --no-cache /wheels/*
WORKDIR /app
COPY . .
RUN python manage.py collectstatic --noinput
RUN adduser myuser
USER myuser
CMD gunicorn discussion_forum.wsgi:application